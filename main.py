#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, make_response, render_template, request
import wikipedia
import os
from function import clean_search
from function import GoogleSearch
from function import search_wikipedia

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/message", methods=["POST"])
def message():
    search = clean_search(request.form["search"])
    response = GoogleSearch()
    response.search_google(search)
    if not response:
        return make_response("aucune information trouvée")
    lat, lng, adresse = response.search_google(search)
    wiki_message = search_wikipedia(lat, lng)
    return make_response(
        jsonify({"lat": lat, "lng": lng, "adresse": adresse, "message": wiki_message})
    )


if __name__ == "__main__":
    app.run()
