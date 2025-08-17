from flask import Blueprint, render_template

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/login")
def login():
    return render_template("login.html")