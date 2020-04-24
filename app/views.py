from flask import Blueprint
from flask import render_template, request, flash, redirect, url_for, abort

from flask_login import login_user, logout_user, login_required, current_user

from .forms import LoginForm, RegisterForm, TaskForm

from .models import User, Task

from . import login_manager

page = Blueprint('page',__name__)

# obtener un usuario a partir de su Id
@login_manager.user_loader
def load_user(id):
    return User.get_by_id(id)

# trabajando con el arror 404
@page.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@page.route('/')
def index():
    return render_template('index.html', title='Index')

@page.route('/logout')
def logout():
    # destruir la sesion
    logout_user()
    flash('Cerraste sesion exitosamente')
    return redirect(url_for('.login'))

# ruta para el login
@page.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated: #el usuario actual
        return redirect(url_for('.tasks'))


    form = LoginForm(request.form) #request.form obtendra los datos enviados del formulario
    # validar si la peticion se hizo por el metodo POST
    if request.method =='POST' and form.validate():
        user = User.get_by_username(form.username.data)
        # verificara que el usuario exista en la base de datos
        if user and user.verify_password(form.password.data):
            # login_user recibe como argumento un objeto de tipo user mixin
            login_user(user)
            flash('Usuario autenticado exitosamente')
        else:
            flash('Usuario o Password invalidos', 'error')

    return render_template('auth/login.html', title='Login', form=form, active='login')

@page.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated: #el usuario actual
        return redirect(url_for('.tasks'))

    # obtener los datos del formulario con -> request.form
    form=RegisterForm(request.form)

    if request.method =='POST':
        if form.validate():
            user=User.created_element(form.username.data, form.password.data, form.email.data )
            flash("usuario registrado exitosamente")
            # una ves el usuario se haya registrado sera redirigido a tareas
            login_user(user)
            return redirect(url_for('.tasks'))
            # print(user.id)

    return render_template('auth/register.html', title='Registro', form=form, active='register')

# ----- ruta para las tareas
@page.route('/tasks')
@page.route('/tasks/<int:page>')
@login_required
# paginacion de las tareas:
#  page=1 - me permite conocer en que pagina me encuentro
#  per_page=2 - me permitira conocer cuantos elementos mostrar por pagina
def tasks(page=1, per_page=2 ):
    # creamos una variable que almacene todas las tareas de un usuario autenticado
    # tasks = current_user.tasks
    #
    pagination = current_user.tasks.paginate(page, per_page=per_page)
    # obtendremos los elementos del objeto pagination
    tasks = pagination.items


    return render_template('/task/list.html', title = 'Tareas', tasks=tasks, pagination=pagination, page=page, active='tasks')

@page.route('/tasks/new', methods=['GET', 'POST'])
@login_required
def new_task():
    # le enviamos los datos ingresados en el formulario con request.form
    form = TaskForm(request.form)
    # validamos el metodo
    if request.method == 'POST':
        # validamos el formulario
        if form.validate():
            # creamos el elemento.. created_elemnt
            task = Task.create_element(form.title.data, form.description.data, current_user.id)
            # validamos si el elemento se creo de manera exitosa
            if task:
                form.title.data=" "
                form.description.data=" "
                flash('Tarea creada con exito')
                # flash(TASK_CREATED)

    return render_template('task/new.html', title='Nueva Tarea', form=form, active='new_task')

# mostrar mejor nuestras tareas
@page.route('/tasks/show/<int:task_id>')
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    return render_template('task/show.html', title='Tarea', task=task)




@page.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    # obtener el objeto a partir del id
    task = Task.query.get_or_404(task_id)
    # validad que solo el usuario pueda editar la tarea
    if task.user_id != current_user.id:
        abort(404)

        #a traves del objeto obj llenamos nuestro formulario con los datos de nuestra BD
    form = TaskForm(request.form, obj=task)
    if request.method == 'POST' and form.validate():
        task = Task.update_element(task.id, form.title.data, form.description.data)
        if task:
            flash('Tarea actualizada exitosamente.')


    return render_template('task/edit.html', title='Editar tarea', form=form)

@page.route('/tasks/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
     # validad que solo el usuario pueda editar la tarea
    if task.user_id != current_user.id:
        abort(404)
    
    if Task.delete_element(task.id):
        flash('tarea eliminada exitosamente')
    
    return redirect(url_for('.tasks'))



