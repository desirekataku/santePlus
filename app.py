from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from extensions import db
import os

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///produits.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret123'  # Change ce mot de passe secret pour plus de sécurité

db.init_app(app)

from models import Produit

with app.app_context():
    db.create_all()

# ------------------- ROUTES -----------------------

@app.route("/")
def catalogue():
    return render_template("catalogue.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == "admin123":  # 💬 Change le mot de passe ici
            session["admin"] = True
            return redirect(url_for("admin"))
        else:
            return render_template("login.html", error="Mot de passe incorrect")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("login"))
    return render_template("admin.html")

# ------------------- API PRODUITS -----------------------

@app.route("/api/produits", methods=["GET", "POST"])
def produits():
    if request.method == "GET":
        produits = Produit.query.all()
        return jsonify([p.to_dict() for p in produits])
    else:
        if not session.get("admin"):
            return jsonify({"error": "Non autorisé"}), 403
        data = request.json
        produit = Produit(**data)
        db.session.add(produit)
        db.session.commit()
        return jsonify(produit.to_dict()), 201

@app.route("/api/produits/<int:id>", methods=["DELETE"])
def delete_produit(id):
    if not session.get("admin"):
        return jsonify({"error": "Non autorisé"}), 403
    produit = Produit.query.get(id)
    if produit:
        db.session.delete(produit)
        db.session.commit()
        return jsonify({"message": "Supprimé"}), 200
    return jsonify({"error": "Introuvable"}), 404

if __name__ == "__main__":
    app.run(debug=True)
