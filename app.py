import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask import redirect, url_for, flash
from models import Produit
from extensions import db


app = Flask(__name__)

# Config base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pharma.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Config upload images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = SQLAlchemy(app)

# Route index
@app.route('/')
def index():
    # Tu peux rediriger vers le catalogue, ou rendre une page index.html
    # return redirect(url_for('catalogue'))
    # Ou si tu as un template index.html :
    return render_template('index.html')

# Modèle Produit
class Produit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200), nullable=True)

# Route admin : ajout + suppression produits
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Suppression produit
        if 'delete_id' in request.form:
            prod_id = int(request.form['delete_id'])
            produit = Produit.query.get(prod_id)
            if produit:
                # Supprimer fichier image si existant
                if produit.image_url:
                    try:
                        os.remove(produit.image_url.lstrip('/'))
                    except Exception:
                        pass
                db.session.delete(produit)
                db.session.commit()
            return redirect(url_for('admin'))

        # Ajout produit
        nom = request.form['nom']
        description = request.form['description']
        type_produit = request.form['type']

        image_file = request.files.get('image')
        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            chemin_image = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(chemin_image)
            image_url = '/' + chemin_image.replace('\\', '/')
        else:
            image_url = ''

        nouveau_produit = Produit(nom=nom, description=description, type=type_produit, image_url=image_url)
        db.session.add(nouveau_produit)
        db.session.commit()
        return redirect(url_for('admin'))

    produits = Produit.query.all()
    return render_template('admin.html', produits=produits)

# Route catalogue pour affichage dynamique
@app.route('/catalogue')
def catalogue():
    produits = Produit.query.all()
    return render_template('catalogue.html', produits=produits)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


# Route supprimer_produit
@app.route('/supprimer/<int:produit_id>', methods=['POST'])
def supprimer_produit(produit_id):
    produit = Produit.query.get_or_404(produit_id)
    db.session.delete(produit)
    db.session.commit()
    flash('Produit supprimé avec succès.', 'success')
    return redirect(url_for('admin'))
