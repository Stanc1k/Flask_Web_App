from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

# Initialize the Flask app and configure the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///automobiliai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Models
class Automobilis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gamintojas = db.Column(db.String(100), nullable=False)
    modelis = db.Column(db.String(100), nullable=False)
    spalva = db.Column(db.String(50), nullable=False)
    metai = db.Column(db.Integer, nullable=False)
    kaina = db.Column(db.Float, nullable=False)


# Create the database
with app.app_context():
    db.create_all()


# Routes
@app.route('/')
def index():
    automobiliai = Automobilis.query.all()
    bendra_kaina = db.session.query(db.func.sum(Automobilis.kaina)).scalar()  # Tiesioginė suma
    return render_template('index.html', automobiliai=automobiliai, bendra_kaina=bendra_kaina)


@app.route('/automobiliai/<int:id>')
def automobilis_detail(id):
    automobilis = Automobilis.query.get_or_404(id)
    return render_template('automobilis_detail.html', automobilis=automobilis)


@app.route('/ieskoti', methods=['GET', 'POST'])
def ieskoti():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        automobiliai = Automobilis.query.filter(
            Automobilis.gamintojas.like(f"%{keyword}%") |
            Automobilis.modelis.like(f"%{keyword}%")
        ).all()
        return render_template('index.html', automobiliai=automobiliai)
    return redirect(url_for('index'))


@app.route('/prideti', methods=['GET', 'POST'])
def prideti():
    if request.method == 'POST':
        gamintojas = request.form['gamintojas']
        modelis = request.form['modelis']
        spalva = request.form['spalva']
        metai = request.form['metai']
        kaina = request.form['kaina']

        naujas_automobilis = Automobilis(
            gamintojas=gamintojas,
            modelis=modelis,
            spalva=spalva,
            metai=metai,
            kaina=kaina
        )
        db.session.add(naujas_automobilis)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('prideti.html')


@app.route('/redaguoti/<int:id>', methods=['GET', 'POST'])
def redaguoti(id):
    automobilis = Automobilis.query.get_or_404(id)

    if request.method == 'POST':
        automobilis.gamintojas = request.form['gamintojas']
        automobilis.modelis = request.form['modelis']
        automobilis.spalva = request.form['spalva']
        automobilis.metai = request.form['metai']
        automobilis.kaina = request.form['kaina']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('redaguoti.html', automobilis=automobilis)


@app.route('/istrinti/<int:id>', methods=['POST'])
def istrinti(id):
    automobilis = Automobilis.query.get_or_404(id)
    db.session.delete(automobilis)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/api2/automobiliai')
def get_automobiliai():
    automobiliai = Automobilis.query.all()
    automobiliai_data = [
        {
            "id": auto.id,
            "gamintojas": auto.gamintojas,
            "modelis": auto.modelis,
            "spalva": auto.spalva,
            "metai": auto.metai,
            "kaina": auto.kaina
        }
        for auto in automobiliai
    ]
    return jsonify(automobiliai_data)


if __name__ == '__main__':
    app.run(debug=True)
