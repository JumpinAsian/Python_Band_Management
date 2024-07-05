from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.band import Band
from flask_app.models.user import User


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user = User.get_user_by_id({"id": session['user_id']})
        bands = Band.get_all_bands()
        return render_template('dashboard.html',
                               user=user,
                               bands=bands)
    return redirect('/')


@app.route('/new/band')
def new_band():
    if 'user_id' in session:
        user = User.get_user_by_id({"id": session['user_id']})
        return render_template('create.html',
                               user=user)
    return redirect('/')


@app.route('/create/band', methods=['POST'])
def create_band():
    if 'user_id' in session:
        if Band.validate_band(request.form):
            data = {
                'band_name': request.form['band_name'],
                'music_genre': request.form['music_genre'],
                'home_city': request.form['home_city'],
                'user_id': session['user_id']
            }
            print(data)
            Band.save(data)
            return redirect('/dashboard')
        return redirect('/new/band')
    return redirect('/')


@app.route('/edit/band/<int:id>')
def edit_band(id):
    if 'user_id' in session:
        user = User.get_user_by_id({"id": session['user_id']})
        band = Band.get_band_by_id({'id': id})
        return render_template('edit.html',
                               band=band,
                               user=user)
    return redirect('/')


@app.route('/update/band/<int:id>', methods=['POST'])
def update_bands(id):
    if 'user_id' in session:
        if Band.validate_band(request.form):
            data = {
                'band_name': request.form['band_name'],
                'music_genre': request.form['music_genre'],
                'home_city': request.form['home_city'],
                'id': id
            }
            Band.update_band(data)
            print(data)
            return redirect('/dashboard')
        return redirect(f'/edit/band/{id}')
    return redirect('/')


@app.route('/delete/band/<int:id>')
def delete_band(id):
    if 'user_id' in session:
        Band.delete({'id': id})
        return redirect('/dashboard')
    return redirect('/')


@app.route('/mybands')
def mybands():
    if 'user_id' in session:
        user = User.get_user_by_id({"id": session['user_id']})
        bands = Band.get_all_bands()
        return render_template('mybands.html',
                               bands=bands,
                               user=user)
    return redirect('/')
