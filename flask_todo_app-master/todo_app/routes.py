from todo_app import app
from flask import url_for, redirect, render_template, request, flash, Response
from .models import User, Task, db
from .login import current_user, login_required, login_user, logout_user


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    print('\n\n INDEX \n\n')
    if current_user.is_authenticated:
        return redirect('home')
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    print('\n\n LOGIN \n\n')
    logout_user()
    if request.method == 'POST':
        user_name = request.form.get('username')
        print(user_name)
        user = User.query.filter_by(user_name=user_name).first()
        print(user)
        if user:
            login_user(user)
            return redirect(url_for('home', uname=user_name))
        else:
            flash('wrong username')
    return render_template('login.html')



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    print('\n\n LOGOUT \n\n')
    logout_user()
    return redirect('index')


@app.route('/home', methods=['GET', 'POST'])
@app.route('/home/<string:uname>', methods=['GET', 'POST'])
@login_required
def home(uname=None):
    print('\n\n HOME \n\n')

    if not current_user.is_authenticated:
        return redirect('index')
    
    task_id = request.args.get('task_id')
    try:    
        task_id = int(task_id)
    except:
        pass

    done_id = request.args.get('done')

    if done_id:
        try:
            task = Task.query.filter_by(id = done_id).first()
            task.done = not task.done
            db.session.commit()
        except:
            db.session.rollback()
    if request.method == 'POST':
        data = request.form.get('newtask')
        if len(data) > 0:
            task = Task(
                data=data,
                user_id = current_user.id
            )
            try:
                db.session.add(task)
                db.session.commit()
            except Exception:
                db.session.rollback()
                flash('Could not add task')
        else:
            flash('No data entered')
    try:
        tasks = Task.query.filter_by(user_id=current_user.id).all()
    except:
        pass
    return render_template(
        'home.html', 
        uname=current_user.user_name,
        tasks = tasks,
        task_id = task_id
    )


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    print('\n\n DELETE \n\n')
    try:
        task_id = request.args.get('task_id')
        if task_id:
            task = Task.query.filter_by(id = task_id).first()
            db.session.delete(task)
            db.session.commit()
    except:
        db.session.rollback()
        flash('Operation not successful')
    return redirect('home')


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        task_id = request.form.get('id')
        data = request.form.get('updated_task_data')
        try:
            task = Task.query.filter_by(id = task_id).first()
            task.data = data
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash('Could not update task')
    else:
        flash('Operation not successful')
    
    return redirect('home')


@app.route('/updateall', methods=['GET', 'POST'])
def updateall():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('update.html',
        uname=current_user.user_name,
        tasks=tasks
    )



