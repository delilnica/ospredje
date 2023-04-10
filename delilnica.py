from flask import Flask, render_template, request, url_for, flash, redirect
from markupsafe import escape
import requests

api_url = "http://localhost:8000/v1"

app = Flask("delilnica")

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/fragment/<string:raw_fragment_id>")
def get_fragment(raw_fragment_id: str):
    fid = escape(raw_fragment_id)
    print(f"Pridobivam cifro {fid}...")

    r = requests.get(api_url + "/fragment/" + fid, timeout=5.0)
    r.raise_for_status()

    success = r.json()["success"]
    if success:
        fragment = r.json()["fragment"]
        return render_template("fragment.html",
                               success=success,
                               title=fragment["title"],
                               author=fragment["author"],
                               text=fragment["text"]
                               )
    else:
        reason = r.json()["reason"]
        return render_template("fragment.html", success=success, reason=reason)

@app.route("/add", methods=["POST"])
def add_fragment():
    title=request.form["title"]
    author=request.form["author"]
    text=request.form["text"]
    is_private="true" if "is_private" in request.form else "false"

    if len(title) < 1 or len(author) < 1 or len(text) < 1:
        error = "Nekatera polja so ostala neizpolnjena. Vrnite se nazaj in jih dopolnite."
        return render_template("add.html", success=False, reason=error)

    r = requests.post(api_url + "/add", json={"title": title, "author": author, "text": text, "is_private": is_private})
    r.raise_for_status()

    success = r.json()["success"]

    if success:
        frag_url = "/fragment/" + str(r.json()["fid"])
        return render_template("add.html", success=success, url=frag_url)
    else:
        reason = r.json()["reason"]
        return render_template("add.html", success=success, reason=reason)
