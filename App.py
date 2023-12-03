from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, Response
from flask_sqlalchemy import SQLAlchemy, pagination
from sqlalchemy import func


app = Flask(__name__)
app.secret_key = "Secret key"

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Exemple avec une base de données SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèle de base de données (exemple)
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

# Créer les tables de la base de données (seulement nécessaire lors de la première exécution)
with app.app_context():
    db.create_all()

@app.route('/')
def Index():
    total_contacts = db.session.query(func.count(Contact.id)).scalar()
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Set the number of items per page
    all_data = Contact.query.paginate(page=page, per_page=per_page)
    return render_template("index.html", contacts=all_data, total_contacts=total_contacts)

@app.route('/ajouter', methods=['POST'])
def Ajouter():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        new_contact = Contact(name=name, phone=phone)
        # Add the user to the database
        db.session.add(new_contact)
        # Commit the changes to the database
        db.session.commit()
        flash('Contact ajouté avec succès')
        return redirect(url_for('Index'))
    
@app.route('/modifier', methods=['POST', 'GET'])
def Modifier():
    if request.method == 'POST':
        contact = Contact.query.get(request.form.get('id'))
        contact.name = request.form['name']
        contact.phone = request.form['phone']
        # Commit the changes to the database
        db.session.commit()
        flash('Contact modifié avec succès')
        return redirect(url_for('Index'))
    
@app.route('/supprimer/<id>/', methods=['POST', 'GET'])
def Supprimer(id):
    if request.method == 'GET':
        contact = Contact.query.get(id)
        db.session.delete(contact)
        db.session.commit()
        flash('Contact supprimé avec succès')
        return redirect(url_for('Index'))

@app.route('/recherche', methods=['GET', 'POST'])
def Recherche():
    if request.method == 'POST':
        search_term = request.form.get('search')
        # Perform the search in the database based on the search_term
        # You can modify the query based on your specific search requirements
        search_results = Contact.query.filter(
            (Contact.name.ilike(f'%{search_term}%')) | (Contact.phone.ilike(f'%{search_term}%'))
        ).all()

        # Correct the total_contacts query to count only searchable contacts
        total_contacts = db.session.query(func.count(Contact.id)).filter(
            (Contact.name.ilike(f'%{search_term}%')) | (Contact.phone.ilike(f'%{search_term}%'))
        ).scalar()

        page = request.args.get('page', 1, type=int)
        per_page = 5  # Set the number of items per page
        all_data = Contact.query.paginate(page=page, per_page=per_page)

        return render_template('index.html', contacts=all_data, search_results=search_results, search_term=search_term, total_contacts=total_contacts)

    # If it's a GET request, render the search form along with the existing contacts
    all_data = Contact.query.all()
    total_contacts = db.session.query(func.count(Contact.id)).scalar()
    return render_template('index.html', contacts=all_data, total_contacts=total_contacts)


# Add a new route to reset the search
@app.route('/annuler_recherche')
def AnnulerRecherche():
    # Clear any stored search term
    return redirect(url_for('Index'))

@app.route('/export_json')
def export_json():
    # Fetch all contacts from the database
    all_contacts = Contact.query.all()

    # Convert the contacts to a list of dictionaries
    contacts_data = [
        {'id': contact.id, 'name': contact.name, 'phone': contact.phone}
        for contact in all_contacts
    ]

    # Create a dictionary to hold the contacts data
    export_data = {'contacts': contacts_data}

    # Convert the dictionary to a JSON string
    json_data = jsonify(export_data)

    # Return the JSON data as a response
    response = Response(json_data.response, content_type='application/json;charset=utf-8')

    # Set the content disposition header to trigger a download
    response.headers['Content-Disposition'] = 'attachment; filename=contacts.json'

    return response

if __name__ == "__main__":
    app.run(debug=True)
