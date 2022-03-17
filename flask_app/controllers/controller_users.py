from flask_app import app
from flask import render_template, request, redirect
from flask_app.models.model_user import User


''' DISPLAY: Show all users '''
@app.route('/users')
def read() -> str:
    all_users = User.get_all()
    return render_template('read.html', all_users=all_users)

''' DISPLAY: Show individual user '''
@app.route('/users/<user_id>')
def read_user(user_id: str) -> str:
    data = {
        'id': int(user_id)
    }
    this_user_instance = User.get_user(data)
    return render_template('user.html', user=this_user_instance)


""" DISPLAY: Form for creating new user """
@app.route('/users/new')
def new() -> str:
    return render_template('create.html')

''' ACTION: Create new user. Redirect to page showing the new user '''
@app.route('/users/create', methods=['POST'])
def create():
    form_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
    }
    user_id = User.create(form_data)
    return redirect(f'/users/{str(user_id)}')


""" DISPLAY: Form for updating user """
@app.route('/users/<user_id>/edit')
def edit(user_id: str) -> str:
    data = {
        'id': int(user_id)
    }
    this_user_instance = User.get_user(data)
    return render_template('edit.html', user=this_user_instance)

""" ACTION: Update user. Redirect to read_user() """
@app.route('/users/<user_id>/update', methods=['POST'])
def update_user(user_id: str):
    data = {
        'id': int(user_id),
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }
    User.update_user(data)
    return redirect(f'/users/{user_id}')


""" ACTION: Delete user. Redirect to show all users route """
@app.route('/users/<user_id>/delete')
def delete_user(user_id: str):
    data = {
        'id': int(user_id)
    }
    User.delete_user(data)
    return redirect('/users')