from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Exemple catalogue (remplacez par une DB)
PRODUCTS = [
    {"id":1, "name":"Paracétamol 1 g", "price":2.99, "img":"paracetamol.jpg"},
    {"id":2, "name":"Vitamine C 1000", "price":9.50, "img":"vitaminec.jpg"},
    {"id":3, "name":"Crème solaire SPF50", "price":12.90, "img":"creme.jpg"},
]

@app.route("/")
def home():
    return render_template("index.html", products=PRODUCTS)

@app.route("/product/<int:pid>")
def product(pid):
    p = next((p for p in PRODUCTS if p["id"]==pid), None)
    if not p: return "Produit introuvable", 404
    return render_template("product.html", product=p)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product_id = int(request.form["product_id"])
    # Ici vous ajoutez à la session ou DB
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
