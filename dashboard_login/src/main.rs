#[macro_use] extern crate rocket;

use rocket::form::{Form, FromForm};
use rocket::response::Redirect;
use rocket::http::{Cookie, CookieJar};
use rocket_dyn_templates::Template;
use serde::Serialize;
use rocket::fs::FileServer;
use bcrypt::{verify};
use sqlx::postgres::{PgPool, PgPoolOptions};
use sqlx::Row;

#[derive(FromForm)]
struct LoginForm {
    username: String,
    password: String,
}

#[derive(Serialize)]
struct DashboardContext {}

#[derive(Serialize)]
struct TemplateContext {
    error: Option<String>,
}

#[get("/login?<error>")]
fn login(error: Option<String>) -> Template {
    let context = TemplateContext { error };
    Template::render("login", &context)
}

#[post("/login", data = "<form>")]
async fn handle_login(
    form: Form<LoginForm>,
    cookies: &CookieJar<'_>,
    pool: &rocket::State<PgPool>,
) -> Result<Redirect, Template> {
    let query_result = sqlx::query(
        "SELECT password_hash FROM users WHERE username = $1"
    )
    .bind(&form.username)
    .fetch_optional(pool.inner())
    .await;

    match query_result {
        Ok(Some(row)) => {
            let password_hash: String = row.get("password_hash");
            if verify(&form.password, &password_hash).unwrap_or(false) {
                cookies.add_private(Cookie::new("authenticated", "true"));
                Ok(Redirect::to("/dashboard"))
            } else {
                Err(Template::render("login", &TemplateContext {
                    error: Some("Invalid username or password".into()),
                }))
            }
        }
        Ok(None) => Err(Template::render("login", &TemplateContext {
            error: Some("User not found".into()),
        })),
        Err(_) => Err(Template::render("login", &TemplateContext {
            error: Some("An error occurred while processing your request.".into()),
        })),
    }
}

#[get("/dashboard")]
fn dashboard(cookies: &CookieJar<'_>) -> Result<Template, Redirect> {
    let context = DashboardContext{};
    if cookies.get_private("authenticated").is_some() {
        Ok(Template::render("dashboard", &context))
    } else {
        Err(Redirect::to("/login"))
    }
}
#[get("/detection")]
fn detection()-> Option<Template> {
    let context = DashboardContext{};
    Some(Template::render("detection", &context))
}
#[launch]
async fn rocket() -> _ {
    dotenvy::dotenv().ok();
    
    let database_url = std::env::var("DATABASE_URL")
        .expect("DATABASE_URL must be set");
    
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&database_url)
        .await
        .expect("Failed to create pool");

    sqlx::query("SELECT 1")
        .execute(&pool)
        .await
        .expect("Database connection failed");

    rocket::build()
        .manage(pool)
        .mount("/", routes![login, handle_login, dashboard, detection])
        .mount("/static", FileServer::from("static"))
        .attach(Template::fairing())
}
