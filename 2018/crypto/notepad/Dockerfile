FROM rust:latest as builder
WORKDIR /notepad

RUN rustup install nightly
RUN rustup target add --toolchain=nightly x86_64-unknown-linux-musl
RUN apt-get update && apt-get install -y musl-tools

COPY . /notepad

RUN echo -n "secret_key = " >>Rocket.toml
RUN openssl rand -base64 32 >>Rocket.toml
RUN cargo build --release --target=x86_64-unknown-linux-musl

FROM scratch
WORKDIR /
ENV ROCKET_ENV production
EXPOSE 8000

COPY --from=builder /notepad/Rocket.toml /notepad/target/x86_64-unknown-linux-musl/release/weak-cookie-sig /

ENTRYPOINT ["/weak-cookie-sig"]
