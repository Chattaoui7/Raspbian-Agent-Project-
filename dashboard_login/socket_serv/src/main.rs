use tokio::net::{TcpListener, TcpStream};
use tokio_tungstenite::{connect_async, accept_async, tungstenite::Message};
use futures_util::{StreamExt, SinkExt};
use std::sync::{Arc};
use tokio::sync::broadcast;
use url::Url;

#[tokio::main]
async fn main() {
    // Channel for broadcasting upstream messages to all downstream clients
    let (tx, _) = broadcast::channel::<String>(100);

    // Connect to upstream WebSocket server
    let upstream_url = Url::parse("ws://192.168.1.102:8765").unwrap();
    let (mut upstream_ws, _) = connect_async(upstream_url).await.expect("Failed to connect upstream");
    println!("[Upstream] Connected");

    // Spawn task to read from upstream and broadcast
    let tx_clone = tx.clone();
    tokio::spawn(async move {
        while let Some(Ok(msg)) = upstream_ws.next().await {
            if let Message::Text(txt) = msg {
                println!("[Upstream] Received: {}", txt);
                let _ = tx_clone.send(txt); // Ignore errors if no clients
            }
        }
    });

    // Start WebSocket server for downstream clients
    let listener = TcpListener::bind("0.0.0.0:8500").await.unwrap();
    println!("[Server] Listening on ws://0.0.0.0:8500");

    while let Ok((stream, _)) = listener.accept().await {
        let tx_subscriber = tx.subscribe();
        tokio::spawn(handle_client(stream, tx_subscriber));
    }
}

// Handle each downstream WebSocket client
async fn handle_client(stream: TcpStream, mut rx: broadcast::Receiver<String>) {
    let ws_stream = accept_async(stream).await.expect("Failed to accept");
    let (mut ws_sink, _) = ws_stream.split();
    println!("[Client] New connection");

    while let Ok(msg) = rx.recv().await {
        println!("[Client] Sending: {}", msg);
        if ws_sink.send(Message::Text(msg)).await.is_err() {
            break; // client disconnected
        }
    }

    println!("[Client] Disconnected");
}

