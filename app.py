import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Config base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pharma.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Config upload images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.secret_key = 'une_clef_secrete_pour_flash'

db = SQLAlchemy(app)

# Modèle Produit
class Produit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200), nullable=True)

# Route index
@app.route('/')
def index():
    return render_template('index.html')

# Route admin : affichage + ajout produit
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
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
        flash('Produit ajouté avec succès.', 'success')
        return redirect(url_for('admin'))

    produits = Produit.query.all()
    return render_template('admin.html', produits=produits)

# Route catalogue
@app.route('/catalogue')
def catalogue():
    produits = Produit.query.all()
    return render_template('catalogue.html', produits=produits)

# Route suppression produit
@app.route('/supprimer/<int:produit_id>', methods=['POST'])
def supprimer_produit(produit_id):
    produit = Produit.query.get_or_404(produit_id)
    # Suppression fichier image si existe
    if produit.image_url:
        chemin_image = produit.image_url.lstrip('/')
        if os.path.exists(chemin_image):
            try:
                os.remove(chemin_image)
            except Exception as e:
                print(f"Erreur suppression image: {e}")
    db.session.delete(produit)
    db.session.commit()
    flash('Produit supprimé avec succès.', 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



python
Copier
Modifier
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
