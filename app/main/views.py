from flask import render_template, request, redirect, url_for, abort
from app.main import main
from flask_login import login_required, current_user
from app.main.forms import UpdateProfile, PitchForm, CommentForm
from app import db, photos
from app.models import User, PhotoProfile, Pitch, Comment


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
        # user = pitch_form.user.data

        new_pitch = Pitch(title=title, description=description)
        new_pitch.save_pitch()

        return redirect(url_for('main.index'))

    title = 'New Pitch | One Minute Pitch'
    return render_template('pitch.html', title=title, pitch_form=pitch_form)


# @main.route('/pitch/comment', methods=['GET', 'POST'])
# @login_required
# def comment(pitch_id):
#     comment_form = CommentForm()
#
@main.route('/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    # post = Post.query.get(post_id)
    pitch = Pitch.query.get(id)
    user = User.query.all()
    comments = Comment.query.filter_by(pitches_id=id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        # post_id = post_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(
            comment=comment,
            # post_id=post_id,
            user_id=user_id
        )
        new_comment.save_comment()
        new_comments = [new_comment]
        print(new_comments)
        return redirect(url_for('.comment'))
    return render_template('comment.html', form=form, comments=comments, user=user)


@main.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Pitch.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)
