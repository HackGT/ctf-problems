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
use error_chain::ChainedError;
use num::Integer;
use rocket::http::{Cookie, Cookies, Status};
use rocket::request::Form;
use rocket::response::Failure;
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
        next_val = next_val << (8 * (8 - tail));
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

    fn from_cookies(cookies: &Cookies) -> Result<State> {
        match cookies.get("state") {
            Some(c) => {
                let value = c.value();
                let dot_index = match value.find('.') {
                    Some(x) => x,
                    None => bail!("No dot"),
                };
                let (pay, dothash) = value.split_at(dot_index);
                let hash = &dothash[1..];
                let pay_bytes = base64::decode(&pay).chain_err(|| "base64::decode(pay)")?;
                let hash_bytes = base64::decode(&hash).chain_err(|| "base64::decode(hash)")?;
                let pay_hash = custom_hash(&pay_bytes);
                let hash_int = Cursor::new(&hash_bytes)
                    .read_u64::<BigEndian>()
                    .expect("read vec");
                let pay_int = Cursor::new(&pay_hash)
                    .read_u64::<BigEndian>()
                    .expect("read vec");
                if hash_int != pay_int {
                    bail!("Bad signature")
                }
                Ok(serde_json::from_slice(&pay_bytes).chain_err(|| "JSON decode")?)
            }
            None => Ok(State::new()),
        }
    }

    fn to_cookie(&self) -> Result<Cookie> {
        let ser = serde_json::to_string(self).chain_err(|| "Failed to dump state to JSON")?;
        let ser_bytes = ser.as_bytes();
        let hash = custom_hash(&ser_bytes);
        let value = format!("{}.{}", base64::encode(&ser_bytes), base64::encode(&hash));
        Ok(Cookie::new("state", value))
    }
}

fn load_state(cookies: &Cookies) -> std::result::Result<State, Failure> {
    match State::from_cookies(cookies) {
        Ok(state) => Ok(state),
        Err(err) => {
            println!("{}", err.display_chain().to_string());
            Err(Failure(Status::BadRequest))
        }
    }
}

#[get("/")]
fn index(cookies: Cookies) -> std::result::Result<State, Failure> {
    load_state(&cookies)
}

#[derive(FromForm, Debug)]
struct UpdateForm {
    notes: String,
}

#[post("/", data = "<data>")]
fn update_notes(
    mut cookies: Cookies,
    data: Form<UpdateForm>,
) -> std::result::Result<State, Failure> {
    let mut state = load_state(&cookies)?;
    state.notes = data.into_inner().notes;
    if let Ok(cookie) = state.to_cookie() {
        cookies.add(cookie.into_owned());
    }
    Ok(state)
}

fn main() {
    rocket::ignite()
        .mount("/", routes![index, update_notes])
        .launch();
}
