#![feature(plugin, custom_derive)]
#![plugin(rocket_codegen)]
#![recursion_limit = "1024"]

extern crate askama;
extern crate base64;
extern crate byteorder;
#[macro_use]
extern crate error_chain;
extern crate num;
extern crate rocket;
#[macro_use]
extern crate serde_derive;
extern crate serde_json;

use askama::Template;
use byteorder::{BigEndian, ReadBytesExt, WriteBytesExt};
use num::Integer;
use rocket::http::{Cookie, Cookies};
use rocket::request::Form;
use std::io::Cursor;

mod errors {
    error_chain!{}
}

use errors::*;

const BASE: u64 = 9223372036854775783;

fn custom_hash(data: &[u8]) -> Vec<u8> {
    let mut cur = Cursor::new(data);
    let mut state = 0;
    let (whole, tail) = data.len().div_rem(&8);
    for _ in 0..whole {
        let next_val = cur.read_u64::<BigEndian>().expect("read vec");
        state = (state + (next_val % BASE)) % BASE;
    }
    {
        let mut next_val = 0;
        for _ in 0..tail {
            next_val = (next_val << 8) + cur.read_u8().expect("read vec") as u64;
        }
        state = (state + (next_val % BASE)) % BASE;
    }
    let mut res = Vec::with_capacity(8);
    res.write_u64::<BigEndian>(state).expect("write into vec");
    res
}

#[derive(Template, Serialize, Deserialize, Debug)]
#[template(path = "index.html")]
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

    fn from_cookies_impl(cookies: &Cookies) -> Result<State> {
        match cookies.get("state") {
            Some(c) => Ok(serde_json::from_slice(
                &base64::decode(c.value()).chain_err(|| "base64::decode")?,
            ).chain_err(|| "JSON decode")?),
            None => bail!("No cookie!"),
        }
    }

    fn from_cookies(cookies: &Cookies) -> State {
        State::from_cookies_impl(cookies).unwrap_or_else(|_| State::new())
    }

    fn to_cookie(&self) -> Result<Cookie> {
        let ser = serde_json::to_string(self).chain_err(|| "Failed to dump state to JSON")?;
        //let hash = custom_hash(&ser);
        let value = base64::encode(&ser.as_bytes());
        Ok(Cookie::new("state", value))
    }
}

#[get("/")]
fn index(cookies: Cookies) -> State {
    State::from_cookies(&cookies)
}

#[derive(FromForm, Debug)]
struct UpdateForm {
    notes: String,
}

#[post("/", data = "<data>")]
fn update_notes(mut cookies: Cookies, data: Form<UpdateForm>) -> State {
    let mut state = State::from_cookies(&cookies);
    state.notes = data.into_inner().notes;
    if let Ok(cookie) = state.to_cookie() {
        cookies.add(cookie.into_owned());
    }
    state
}

fn main() {
    rocket::ignite()
        .mount("/", routes![index, update_notes])
        .launch();
}
