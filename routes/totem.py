from flask import Blueprint, render_template

totem = Blueprint("totem", __name__)

# Home do usuario (Totem)
@totem.route("/totem")
def home():
    return render_template("/totem/totem.html")