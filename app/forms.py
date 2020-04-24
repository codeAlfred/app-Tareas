from wtforms import Form
from wtforms import StringField, PasswordField, BooleanField, HiddenField, TextAreaField
from wtforms.fields.html5 import EmailField
# validar nuestros campos
from wtforms import validators
from .models import User

# validando que el usuario codi no esta permitido registrar
def codi_validator(form, field):
    if field.data == 'codi' or field.data == 'Codi':
        raise validators.ValidationError('el username codi no es permitido.')

# validacion para el campo honeypot - metodo antispam
def length_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('Solo los humanos pueden completar el registro!')

class LoginForm(Form):
    username = StringField('Username', [validators.length(min=4, max=50, message='El usuario se encuentra fuera de rango')])
    password = PasswordField('Password', [validators.Required(message='el password es requerido')])


class RegisterForm(Form):
    username = StringField('Username', [validators.length(min=4, max=50), codi_validator])
    email = EmailField('Correo electronico', [validators.length(min=6, max=100), validators.Required(message='el email es requerido'),validators.Email(message='Ingrese un email vaido.')])
    password = PasswordField('Password', [ validators.Required('el password es requerido'), validators.EqualTo('confirm_password', message= 'La contraseña no coincide.')])
    confirm_password = PasswordField('Confirm password')
    accept = BooleanField('Acepto terminos y condiciones', [validators.DataRequired()])
    honeypot = HiddenField("", [ length_honeypot] )

    def validate_username(self, username):
        if User.get_by_username(username.data):
            raise validators.ValidationError('El username ya se encuentra en uso.')
        
    def validate_email(self, email):
        if User.get_by_email(email.data):
            raise validators.ValidationError('El email ya se encuentra en uso.')
        
    # sobreescribiendo el metodo validate, el cual retorna siempre un booleano
    def validate(self):
        # validamos todas las validaciones predifinidas
        if not Form.validate(self):
            return False
        
        if len(self.password.data) < 3:
            self.password.errors.append('El password es demasiado corto')
            return False
        
        return True

# formulario para las tareas
class TaskForm(Form):
    title = StringField('Titulo', [validators.length(min=4, max=50, message='Título fuera de rango.'), validators.DataRequired(message='El titulo es requerido.')])
    description = TextAreaField('Descripcion', [ validators.DataRequired('La descripcion es requerida.')], render_kw={'rows':5 })
    
