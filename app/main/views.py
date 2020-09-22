from flask import render_template, request, redirect, url_for, abort
from . import main
from flask_login import login_required, current_user
from .forms import UpdateProfile, PitchForm
from .. import db, photos
from ..models import User, PhotoProfile, Pitch


@main.route('/')
def index():
    pitches = Pitch.query.all()
    return render_template('index.html', pitches=pitches)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user_photo = PhotoProfile(pic_path=path, user=user)
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))


@main.route('/pitch/new', methods=['GET', 'POST'])
@login_required
def pitch():
    """
    View pitch function that returns the pitch page and data
    """
    pitch_form = PitchForm()

    if pitch_form.validate_on_submit():
        title = pitch_form.title.data
        description = pitch_form.description.data

        new_pitch = Pitch(title=title, description=description)
        new_pitch.save_pitch()

        return redirect(url_for('main.index'))

    title = 'New Pitch | One Minute Pitch'
    return render_template('pitch.html', title=title, pitch_form=pitch_form)
