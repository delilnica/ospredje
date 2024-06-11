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
                               vzd=vzd(),
                               datoteka=(api_url + "shramba/" + fragment["uri"] if fragment["did"] else False)
                               )
    else:
        print(r.status_code, fragment)
        return render_template("fragment.html", success=success, response=response, status=status,
                               prijavljen=prijavljen(), vzd=vzd())

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html", prijavljen=prijavljen(), vzd=vzd());

@app.route("/admin", methods=["GET"])
def admin():
    if not prijavljen():
        return redirect("/", code=302)

    headers = {"Authorization": request.cookies.get("zeton")}

    r = requests.get(api_url + "fragment.php", headers=headers, timeout=5.0)

    fragment1 = r.json()
    response1, status1 = fragment1["response"], fragment1["status"]
    success1 = (r.status_code == 200)
    if not success1:
        return redirect("/", code=302)

    r = requests.get(api_url + "admin.php", headers=headers, timeout=5.0)

    fragment2 = r.json()
    response2, status2 = fragment2["response"], fragment2["status"]
    success2 = (r.status_code == 200)
    if not success2:
        return redirect("/", code=302)

    return render_template("admin.html", vzd=vzd(), prijavljen=prijavljen(), fragmenti=response1, uporabniki=response2);
