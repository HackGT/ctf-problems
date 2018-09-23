#![feature(plugin)]
#![plugin(rocket_codegen)]

extern crate askama;
extern crate rocket;

use askama::Template;

#[derive(Template)]
#[template(path="index.html")]
struct IndexTemplate {
    found_flag: bool,
    notes: String,
}

#[get("/")]
fn index() -> IndexTemplate {
    IndexTemplate {
        found_flag: false,
        notes: String::new(),
    }
}

fn main() {
    rocket::ignite().mount("/", routes![index]).launch();
}
