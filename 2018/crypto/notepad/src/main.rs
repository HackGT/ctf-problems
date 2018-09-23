#![feature(plugin)]
#![plugin(rocket_codegen)]

extern crate askama;
extern crate base64;
extern crate byteorder;
extern crate rocket;
#[macro_use]
extern crate serde_derive;
extern crate serde_json;

use askama::Template;
use byteorder::{BigEndian};
use rocket::{Cookie,Cookies,FromForm};
use std::io::Cursor;

const BASE: u64 = 9223372036854775783;

fn custom_hash(data: &[u8]) -> Vec[u8] {
    let cur = Cursor::new(data);
    let mut state: u64 = 0;
    let mut loc = 0;
    let whole, tail = data.length().div_rem(8);
    while loc < whole{
        let next_val = cur::read_u64<BigEndian>();
        state = (state + (next_val % BASE)) % BASE;
    }
    let mut res = Vec::with_capacity(8);
    let out_cur = Cursor::new(&res);
    out_cur.write_u64<BigEndian>(state);
    res
}

#[derive(Template, Serialize, Deserialize, Debug)]
#[template(path="index.html")]
struct State {
    found_flag: bool,
    notes: String,
}

impl State {
    fn new() -> State {
        State {
            found_flag: false,
            notes: String::new(),
        }
    }

    fn from_cookies(cookies: Cookies) -> State {
        match cookies.get("state").map(|c| c.value()) {
            Some(value) => {
            }
            None => State::new()
        }
    }

    fn to_cookie(&self: Self) -> Cookie {
        let ser = serde_json::to_string(self);
        let hash = custom_hash(&ser);
        let value = format!("{}.{}", base64::encode(ser), base64::encode(hash));
        Cookie::new("state", value)
    }
}

#[derive(FromForm, Debug)]
struct UpdateForm {
    notes: String,
}

#[get("/")]
fn index(cookies: Cookies) -> State {
    State::from_cookie(cookies.get("state"))
}

#[post("/")]
fn update_notes(cookies: Cookies, data: Form<UpdateForm>) -> State {
    let state = State::from_cookie(cookies.get("state"));
    state.notes = data.notes;
    cookies.add('state', state.to_cookie());
    state
}

fn main() {
    rocket::ignite().mount("/", routes![index]).launch();
}
