from . import db
import datetime

from flask_login import UserMixin

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(113), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_At = db.Column(db.DateTime, default=datetime.datetime.now())
    tasks = db.relationship('Task', lazy='dynamic')

    # esta funcion retornara true cuando coincida mabas passwaord
    def verify_password(self, password):
        return check_password_hash(self.encrypted_password, password)

    # generar una propiedad llamada password, atraves de esta propiedad un cliente podra asignar una contraseña a su usuario
    @property
    def password(self):
        pass
    # propiedad para asignar un valor
    @password.setter
    def password(self, value):
        self.encrypted_password = generate_password_hash(value)

    def __str__(self):
        return self.username

    @classmethod
    def created_element(cls, username, password, email):
        user= User(username=username, password=password, email=email)

        # regitrar usuario en mi bd
        db.session.add(user)
        db.session.commit()

        return user

    # metodo que nos permite saber si un usuario con un user en particular existe en la BD
    @classmethod
    def get_by_username(cls, username):
        return User.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return User.query.filter_by(email=email).first()

    @classmethod
    def get_by_id(cls, id):
        return User.query.filter_by(id=id).first()


# crear la tabla tareas - tasks
class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    create_At = db.Column(db.DateTime, default=datetime.datetime.now())

    # propiedad para acortar la descripcion en nuestra lista de tareas
    @property
    def little_description(self):
        if len(self.description) > 25:
            return self.description[0:24]+"..."
        return self.description

     # metodo de clase para crear nuevas tareas
    @classmethod
    def create_element(cls, title, description, user_id):
        # instanciamos la clase
        task = Task(title=title, description=description, user_id=user_id)
        # lo agregamos a nuestra base de datos
        db.session.add(task)
        db.session.commit()

        return task

    @classmethod
    def get_by_id(cls, id):
        return Task.query.filter_by(id=id).first()

    @classmethod
    def update_element(cls, id, title, description):
        task = Task.get_by_id(id)

        if task is None:
            return False

        task.title = title
        task.description = description

        # guardamos los cambios
        # lo agregamos a nuestra base de datos
        db.session.add(task)
        db.session.commit()

        return task
    
    @classmethod
    def delete_element(cls, id):
        task = Task.get_by_id(id)
        
        if task is None:
            return False

        db.session.delete(task)
        db.session.commit()
        
        return True
    
