from flask import Flask, render_template, request, url_for, flash, redirect, make_response
from markupsafe import escape
import requests

api_url = "http://localhost:81/"

app = Flask("delilnica")

def prijavljen():
    avt = request.cookies.get("zeton")
    # print(avt)

    return avt != None

def vzd():
    return request.cookies.get("vzdevek")

# ref: domača stran (+ nalaganje fragmenta)
@app.route("/")
def hello():
    # print("auth:", request.authorization)
    # print("prijava:", prijavljen())
    return render_template("index.html", prijavljen=prijavljen(), vzd=vzd())

# ref: ogled fragmenta
@app.route("/fragment/<string:raw_fragment_id>")
def get_fragment(raw_fragment_id: str):
    o = escape(raw_fragment_id)
    headers = {}

    if prijavljen():
        print("poskušam avtorizacijo")
        # headers = {"Authorization": str(request.authorization)}
        headers = {"Authorization": request.cookies.get("zeton")}
        print(headers)

    print(f"Pridobivam oznako {o}...")

    r = requests.get(api_url + "fragment.php?o=" + o, headers=headers, timeout=5.0)

    fragment = r.json()
    response, status = fragment["response"], fragment["status"]
    success = (r.status_code == 200)

    if success:
        fragment = fragment["response"]
        return render_template("fragment.html",
                               success=success,
                               ime=fragment["ime"],
                               datum=fragment["datum"],
                               besedilo=fragment["besedilo"],
                               prijavljen=prijavljen(),
                               vzd=vzd()
                               )
    else:
        print(r.status_code, fragment)
        return render_template("fragment.html", success=success, response=response, status=status,
                               prijavljen=prijavljen(), vzd=vzd())

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html", status=1, prijavljen=prijavljen(), vzd=vzd());
