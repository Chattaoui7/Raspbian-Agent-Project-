#[macro_use] extern crate rocket;

use rocket::form::{Form, FromForm};
use rocket::response::Redirect;
use rocket::http::{Cookie, CookieJar};
use rocket_dyn_templates::Template;
use serde::Serialize;
use rocket::fs::{FileServer, relative};
#[derive(FromForm)]
struct LoginForm {
    username: String,
    password: String,
}

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
fn handle_login(form: Form<LoginForm>, cookies: &CookieJar<'_>) -> Result<Redirect, Template> {
    let valid_username = "user";
    let valid_password = "pass";

    if form.username == valid_username && form.password == valid_password {
        cookies.add_private(Cookie::new("authenticated", "true"));
        Ok(Redirect::to("/dashboard"))
    } else {
        Err(Template::render("login", &TemplateContext {
            error: Some("Invalid username or password".into())
        }))
    }
}

#[get("/dashboard")]
fn dashboard(cookies: &CookieJar<'_>) -> Result<&'static str, Redirect> {
    if cookies.get_private("authenticated").is_some() {
        Ok("Welcome to the dashboard!")
    } else {
        Err(Redirect::to("/login"))
    }
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![login, handle_login, dashboard])
        .mount("/static", FileServer::from(relative!("static")))
        .attach(Template::fairing())
}
