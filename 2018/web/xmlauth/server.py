from flask import Flask, request, Response

from test import verify_and_get_user, sign

app = Flask(__name__)

@app.route('/')
def index():
    return open('login.html').read()

@app.route('/register', methods=['GET', ])
def register_get():
    return open('register.html').read()

@app.route('/register', methods=['POST',])
def register_post():
    if request.form['name']:
        name = request.form['name']
        if name == 'admin':
            return open('error.html').read()
        signed = sign(name)
        if type(signed) == type('str') and signed:
            return Response(signed, mimetype='text')
        else:
            return open('error.html').read()


@app.route('/login', methods=['POST',])
def login():
    if request.form['xml']:
        xml = request.form['xml']
        parsed = verify_and_get_user(xml.strip())
        if parsed and type(parsed) == type("str"):
            if parsed == "admin":
                return open('flag.html').read()
            else:
                return open('login_ok.html').read()
    return open('error.html').read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
