"""
Admin page routes.
"""

import os

from flask import (
    render_template, redirect, request, abort,
    flash, url_for, current_app, send_from_directory
)
from flask_login import (
    login_user, logout_user, login_required,
    current_user
)
from werkzeug.utils import secure_filename

from . import admin
from ..email import send_email
from ..permissions import admin_required
from .models import Permission, Role, User
from .. import db, bcrypt, login_manager, mail
from .forms import (
    RegistrationForm, LoginForm, ForgotPasswordForm,
    ResetPasswordForm, UpdateProfileForm
)
from .utils import save_picture
from ..main.models import Category, Project, Storie, Client
from ..main.forms import ProjectForm, StorieForm, ClientForm


@admin.route('/', strict_slashes=False)
@admin.route('/dashboard/', strict_slashes=False)
@login_required
@admin_required
def dashboardPage():
    page_title = "Table board"
    return render_template(
        'admin/dashboard.html',
        page_title=page_title,
        current_user=current_user
    )


@admin.route("/login/", methods=['GET', 'POST'], strict_slashes=False)
def loginPage():
    if current_user.is_authenticated:
        return redirect(url_for('main.homePage'))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data.lower()).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash(f"Bienvenu ! Vous êtes connecté en tant que: {user.email.lower()}", "success")
                return redirect(url_for('admin.dashboardPage'))
            else:
                flash("Combinaison nom d'utilisateur/mot de passe invalide.", "danger")
                return redirect(url_for('admin.loginPage'))
        except:
            abort(400)

    page_title = "Connction"

    return render_template(
        'admin/login.html',
        page_title=page_title, form=form
    )


@admin.route("/register/", methods=['GET', 'POST'], strict_slashes=False)
def registerPage():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboardPage'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(email=form.email.data.lower())
            user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            db.session.add(user)
            db.session.commit()
            msg_success = f"""
                Hey {form.email.data},
                votre compte a été créé ! Connectez-vous maintenant !
            """
            flash(msg_success, "success")

            return redirect(url_for('admin.loginPage'))
        except:
            abort(400)
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Une erreur est survenue lors de la création d'un utilisateur: {err_msg}", "danger")

    page_title = "Inscription"

    return render_template(
        'admin/register.html',
        page_title=page_title, form=form
    )


@admin.route('/update/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
@admin_required
def updateAccountPage():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        try:
            current_user.role = Role.query.get(form.role.data)
            current_user.email = form.email.data.lower()
            db.session.add(current_user._get_current_object())
            db.session.commit()
            flash("Votre compte a été mise à jour avec succès.", "success")
            return redirect(url_for('admin.updateAccountPage'))
        except Exception as e:
            return f"Une erreur s'est produite: {e}"
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.role.data = current_user.role_id

    page_title = "Compte Administrateur"

    return render_template(
        'admin/update.html',
        form=form,
        current_user=current_user,
        page_title=page_title,
    )


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        '[Unsta Inc] Réinitialisationd de mot de passe',
        sender=current_app.config['MAIL_SENDER'],
        recipients=[user.email],
        text_body=render_template(
            'admin/email/reset_password.txt', user=user, token=token),
        html_body=render_template(
            'admin/email/reset_password.html', user=user, token=token)
    )


@admin.route("/reset/password/request/", methods=['GET', 'POST'], strict_slashes=False)
def resetRequestPage():
    if current_user.is_authenticated:
        return redirect(url_for('main.homePage'))

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            send_password_reset_email(user)
        flash(
            "Un courriel a été envoyé avec les instructions pour réinitialiser votre mot de passe.",
            'info'
        )
        return redirect(url_for('admin.loginPage'))

    page_title = 'Réinitialiser votre mot de passe'
    return render_template('admin/resetpwd.html', page_title=page_title, form=form)


@admin.route("/reset/password/<token>/", methods=['GET', 'POST'], strict_slashes=False)
def resetPasswordPage(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.homePage'))

    user = User.verify_reset_password_token(token)
    if not user:
        flash("Ce jeton est invalide ou a expiré.", 'warning')
        return redirect(url_for('admin.resetRequestPage'))

    form = ResetPasswordForm()
    try:
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash("Votre mot de passe a été mise à jour avec succès !", "success")
            return redirect(url_for('auth.loginPage'))
    except Exception as e:
        return f"Une erreur s'est produite: {e}"

    page_title = 'Changer votre mot de passe'
    return render_template(
        'admin/changepwd.html',
        page_title=page_title,
        form=form
    )


@admin.route('/logout/', strict_slashes=False)
@login_required
def logoutPage():
    logout_user()
    return redirect(url_for('main.homePage'))


@admin.route('/add/project/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
@admin_required
def addProjectPage():
    page_title = 'Add a completed project'
    form = ProjectForm()
    if (current_user.can(Permission.ADMIN) and form.validate_on_submit()):
        try:
            picture = Project(
                name=form.name.data,
                category=Category.query.get(form.category.data),
                image=save_picture(form.image.data),
                user=current_user._get_current_object()
            )
            db.session.add(picture)
            db.session.commit()
            flash("Project added successfully !", 'success')
            return redirect(request.url)
        except Exception as e:
            return f"An error has occurred : {e}"

    return render_template(
        'admin/project.html',
        form=form,
        page_title=page_title
    )


@admin.route('/add/storie/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
@admin_required
def addStoriePage():
    page_title = 'Add a testimonial'
    form = StorieForm()
    if (current_user.can(Permission.ADMIN) and form.validate_on_submit()):
        try:
            storie = Storie(
                fullname=form.fullname.data,
                status=form.status.data,
                content=form.content.data,
                image=save_picture(form.image.data),
                user=current_user._get_current_object()
            )
            db.session.add(storie)
            db.session.commit()
            flash("Testimonial added successfully !", 'success')
            return redirect(request.url)
        except Exception as e:
            return f"An error has occurred : {e}"

    return render_template(
        'admin/storie.html',
        form=form,
        page_title=page_title
    )


@admin.route('/add/client/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
@admin_required
def addClientPage():
    page_title = 'Ajouter un client'
    form = ClientForm()
    if (current_user.can(Permission.ADMIN) and form.validate_on_submit()):
        try:
            client = Client(
                name=form.name.data,
                image=save_picture(form.image.data),
                user=current_user._get_current_object()
            )
            db.session.add(client)
            db.session.commit()
            flash("Client ajouté avec succès !", 'success')
            return redirect(request.url)
        except Exception as e:
            return f"Une erreur s'est produite: {e}"

    return render_template(
        'admin/partner.html',
        form=form,
        page_title=page_title
    )


@admin.route('/upload/<filename>/', strict_slashes=False)
def upload(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER_PATH'], filename)


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view this page.')
    return redirect(url_for('admin.loginPage'))


def stories():
    return Storie.query.order_by(Storie.timestamp.desc()).limit(8).all()


def clients():
    return Client.query.order_by(Client.timestamp.desc()).limit(8).all()


def projects():
    return Project.query.order_by(Project.timestamp.desc()).limit(8).all()


def categories():
    return Category.query.order_by(Category.id.desc()).all()
