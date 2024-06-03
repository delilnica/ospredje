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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", status=1, prijavljen=prijavljen(), vzd=vzd());
    else:
        vzdevek = request.form["vzdevek"]
        geslo   = request.form["geslo"]
        r = requests.post(api_url + "/login.php", json={
            "vzdevek": vzdevek,
            "geslo": geslo
            })

        fragment = r.json()
        response, status = fragment["response"], fragment["status"]
        success = (r.status_code == 200)
        zeton = response
        print(zeton)

        if success:
            # return redirect(url_for("/"))
            resp = make_response(redirect("/"))
            # resp.set_cookie("zeton", zeton, httponly=True)
            resp.set_cookie("zeton", zeton)
            resp.set_cookie("vzdevek", vzdevek)
            return resp

        return render_template("login.html", status=2, success=success, response=response);

@app.route("/logout", methods=["GET"])
def logout():
    resp = make_response(redirect("/"))
    resp.delete_cookie("zeton")
    return resp

# ref: nalaganje fragmenta
@app.route("/add", methods=["POST"])
def add_fragment():
    ime      = request.form["ime"]
    besedilo = request.form["besedilo"]
    zaseben  = "1" if "zaseben" in request.form else "0"

    if len(ime) < 1 or len(besedilo) < 1:
        error = "Nekatera polja so ostala neizpolnjena. Vrnite se nazaj in jih dopolnite."
        return render_template("add.html", success=False, response=error, koda=0)

    r = requests.post(api_url + "/fragment.php", json={
        "ime": ime,
        "besedilo": besedilo,
        "zaseben": zaseben
        })

    fragment = r.json()
    response, status = fragment["response"], fragment["status"]
    success = (r.status_code == 201)

    if success:
        frag_url = f"/fragment/{response}"
        return render_template("add.html", success=success, url=frag_url, prijavljen=prijavljen(), vzd=vzd())
    else:
        response = r.json()["response"]
        return render_template("add.html", success=success, response=response, status=status, prijavljen=prijavljen(), vzd=vzd())

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", status=1, prijavljen=prijavljen(), vzd=vzd());
    else:
        vzdevek = request.form["vzdevek"]
        enaslov = request.form["enaslov"]
        geslo   = request.form["geslo"]
        r = requests.post(api_url + "/register.php", json={
            "vzdevek": vzdevek,
            "enaslov": enaslov,
            "geslo": geslo
            })

        success = (r.status_code == 201)
        response=""

        if not success:
            fragment = r.json()
            response, status = fragment["response"], fragment["status"]
        else:
            return redirect("/login", code=307)
        # if success:
        #     # return redirect(url_for("/"))
        #     resp = make_response(redirect("/"))
        #     # resp.set_cookie("zeton", zeton, httponly=True)
        #     resp.set_cookie("zeton", zeton)
        #     resp.set_cookie("vzdevek", vzdevek)
        #     return resp

        return render_template("register.html", status=2, success=success, response=response);
