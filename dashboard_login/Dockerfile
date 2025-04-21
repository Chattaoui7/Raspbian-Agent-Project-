#build stage
FROM rust:latest as builder

RUN apt-get update && \
    apt-get install -y musl-tools && \
    rustup target add x86_64-unknown-linux-musl

WORKDIR /app
COPY . .

RUN cargo build --release --target x86_64-unknown-linux-musl
#runtime stage
FROM alpine:latest

RUN apk add --no-cache ca-certificates

WORKDIR /app
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/rocket-login .
COPY --from=builder /app/templates ./templates
COPY --from=builder /app/static ./static

ENV ROCKET_ADDRESS=0.0.0.0
ENV ROCKET_PORT=8000
EXPOSE 8000

CMD ["/app/rocket-login"]
