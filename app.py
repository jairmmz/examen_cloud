from urllib import request
from flask import Flask, render_template, flash, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, DateField, RadioField, SelectField
from wtforms.validators import DataRequired, Regexp, InputRequired

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

# Add database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/examen'

# Secret key
app.config['SECRET_KEY'] = 'My super secret that no one is supposed to know'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializa the database
db = SQLAlchemy(app)

# ----------------- Create Model Carrera  -------------
class Carrera(db.Model):
    __tablename__ = 'carrera'
    codigoCarrera = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    duracion = db.Column(db.String(30), nullable=False)
    estudiantes = db.relationship('Estudiante', backref='carrera', lazy=True)
    cursos = db.relationship('Curso', backref='carrera', lazy=True)
   # Create a String
    def __init__(self, nombre, duracion):
        self.nombre = nombre
        self.duracion = duracion
        
# ----------------- Create Model Estudiante -------------
class Estudiante(db.Model):
    __tablename__ = 'estudiante'
    id = db.Column(db.Integer, primary_key=True)
    DNI = db.Column(db.Integer, nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    fecNacimiento = db.Column(db.DateTime, nullable=False)
    sexo = db.Column(db.String(20), nullable=False)
    
    codigoCarrera = db.Column(db.Integer, db.ForeignKey('carrera.codigoCarrera'), nullable=False)
    
   # Create a String
    def __init__(self, DNI, apellidos, nombres, fecNacimiento, sexo, codigoCarrera):
        self.DNI = DNI
        self.apellidos = apellidos
        self.nombres = nombres
        self.fecNacimiento = fecNacimiento
        self.sexo = sexo
        self.codigoCarrera = codigoCarrera

# ------------------- Create Model Curso ---------------------
class Curso(db.Model):
    __tablename__ = 'curso'
    codigoCurso = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    credito = db.Column(db.Integer, nullable=False)
    
    codigoCarrera = db.Column(db.Integer, db.ForeignKey('carrera.codigoCarrera'), nullable=False)
    matriculas = db.relationship('Matricula', backref='curso', lazy=True)
    def __init__(self, nombre, credito, codigoCarrera):
        self.nombre = nombre
        self.credito = credito
        self.codigoCarrera = codigoCarrera

# ------------------- Create Model ---------------------------
class Matricula(db.Model):
    __tablename__ = 'matricula'
    codigoMatricula = db.Column(db.Integer, primary_key=True)
    
    id = db.Column(db.Integer, db.ForeignKey('estudiante.id'), nullable=False)
    codigoCarrera = db.Column(db.Integer, db.ForeignKey('carrera.codigoCarrera'), nullable=False)
    codigoCurso = db.Column(db.Integer, db.ForeignKey('curso.codigoCurso'), nullable=False)
    
    def __init__(self, id, codigoCarrera, codigoCurso):
        self.id = id
        self.codigoCarrera = codigoCarrera
        self.codigoCurso = codigoCurso


# CREATE FORM CLASS
class CarreraForm(FlaskForm):
    nombre = StringField('Nombre', [validators.Length(min=6, max=60)])
    duracion = StringField('Duracion', [validators.Length(min=6, max=60)])
    submit = SubmitField('Submit')

# CREATE FORM CLASS
class EstudianteForm(FlaskForm):
    DNI = StringField("DNI",[validators.Length(min=8, max=8)])
    apellidos = StringField('Apellidos', [validators.Length(min=5, max=60)])
    nombres = StringField('Nombres', [validators.Length(min=4, max=60)])
    fecNacimiento = DateField('Fecha de Nacimiento: ', [validators.DataRequired()])
    sexo = RadioField('Sexo', choices=['Masculino', 'Femenino'], validators=[InputRequired()])
    codigoCarrera = RadioField('Carrera', choices=['Administración', 'Sistemas  '], validators=[InputRequired()])
    submit = SubmitField('Submit')
    
# CREATE FORM CLASS
class CursoForm(FlaskForm):
    nombre = StringField("Nombre",[validators.Length(min=4, max=100)])
    credito = StringField('Credito', [validators.Length(min=2, max=4)])
    codigoCarrera = RadioField('Carrera', choices=['Administración', 'Sistemas  '], validators=[InputRequired()])
    submit = SubmitField('Submit')
    
# CREATE FORM CLASS
class MatriculaForm(FlaskForm):
    id = StringField("id Estudiante",[validators.Length(min=4, max=100)])
    codigoCurso = RadioField('Código Curso', choices=['Física 1', 'ATI'], validators=[InputRequired()])
    codigoCarrera = RadioField('Código Carrera', choices=['Administración', 'Sistemas  '], validators=[InputRequired()])
    submit = SubmitField('Submit')



@app.route('/')
def index():
    first_name = 'Jairo'
    flash("Welcome To Our Website!")
    stuff = 'This is bold text'
    favorite_pizzas = ['Peperoni', 'Queso', 'Italiana', 41]
    return render_template("index.html", first_name=first_name, stuff=stuff, favorite_pizzas=favorite_pizzas)


# ----------- CREACIÓN DE CRUD CARRERA --------------

# Create Add CARRERA
@app.route('/carrera/add', methods=['GET', 'POST'])
def add_carrera():
    nombre = None
    form = CarreraForm()
    #Validate Form
    if form.validate_on_submit():
        carrera = Carrera.query.filter_by(nombre=form.nombre.data).first()
        if carrera is None:
            carrera = Carrera(nombre=form.nombre.data, duracion=form.duracion.data)
            db.session.add(carrera)
            db.session.commit()
            nombre = form.nombre.data
            form.nombre.data = ''
            form.duracion.data = ''
            flash("La carrera guardo correctamente!")
        else:
            flash("El nombre de la carrera ya existe!")
    our_carreras = Carrera.query.order_by(Carrera.codigoCarrera) 
    return render_template('add_carrera.html', form=form, our_carreras=our_carreras)
        

# Update CARRERA
@app.route('/carrera/update/<int:codigoCarrera>', methods=['GET', 'POST'])
def update_carrera(codigoCarrera):
    form = CarreraForm()
    name_update = Carrera.query.get_or_404(codigoCarrera)
    if request.method == "POST":   
        name_update.nombre = request.form['nombre']
        name_update.duracion = request.form['duracion']
        try:
            db.session.commit()
            flash("La carrera se a actualizado satisfactoriamente!")
            return redirect('/carrera/add')
        except:
            flash("Error! in update career!")
            return render_template('update_carrera.html', form=form, name_update=name_update)
    else:
        return render_template('update_carrera.html', form=form, name_update=name_update)

# Delete CARRERA
@app.route('/carrera/delete/<int:codigoCarrera>')
def delete_carrera(codigoCarrera):
    carrera_delete = Carrera.query.get_or_404(codigoCarrera)
    nombre = None
    form = CarreraForm()
    try:
        db.session.delete(carrera_delete)
        db.session.commit()
        flash("La carrera se a eliminado satisfactoriamente :)")

        our_carreras = Carrera.query.order_by(Carrera.codigoCarrera)
        return redirect('/carrera/add')

    except:
        flash("Ops! There was a problem from deleted Career!")
    return render_template('/carrera/add')


# ----------- CREACIÓN DE CRUD ESTUDIANTE --------------
# Create Add ESTUDIANTE
@app.route('/estudiante/add', methods=['GET', 'POST'])
def add_estudiante():
    form = EstudianteForm()
    return render_template('add_estudiante.html', form=form)
        

# Update ESTUDIANTE
@app.route('/estudiante/update', methods=['GET', 'POST'])
def update_estudiante():
    
    return render_template('update_estudiante.html')

# Delete ESTUDIANTE
@app.route('/estudiante/delete')
def delete_estudiante(id):

    return render_template('/estudiante/add')


# ----------- CREACIÓN DE CRUD CURSO --------------
# Create Add CURSO
@app.route('/curso/add', methods=['GET', 'POST'])
def add_curso():
    form = CursoForm()
    return render_template('add_curso.html', form=form)
        

# Update CURSO
@app.route('/curso/update', methods=['GET', 'POST'])
def update_curso():
    
    return render_template('update_curso.html')

# Delete CURSO
@app.route('/curso/delete')
def delete_curso(id):

    return render_template('/curso/add')

# ----------- CREACIÓN DE CRUD MATRICULA --------------

# Create Add MATRICULA
@app.route('/matricula/add', methods=['GET', 'POST'])
def add_matricula():
    form = MatriculaForm()
    return render_template('add_matricula.html', form=form)
        

# Update MATRICULA
@app.route('/matricula/update', methods=['GET', 'POST'])
def update_matricula():
    
    return render_template('update_matricula.html')

# Delete MATRICULA
@app.route('/matricula/delete')
def delete_matricula(id):

    return render_template('/matricula/add')


# ----------- CREACIÓN DE LISTA --------------
# Delete MATRICULA
@app.route('/lista')
def lista():

    return render_template('/lista.html')







# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# INTERNAL SERVER ERROR
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


# Recargar automática para el server.
if __name__ == '__main__':
    app.run(debug=True)
