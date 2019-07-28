"""A PasswordController Module."""

import uuid

from masonite.auth import Auth
from masonite.view import View
from masonite.request import Request
from masonite import env, Mail, Session
from masonite.validation import Validator
from masonite.helpers import password as bcrypt_password

from config.auth import AUTH


class PasswordController:
    """Password Controller."""

    def forget(self, view: View, request: Request, auth: Auth):
        return view.render('auth/forget', {'app': request.app().make('Application'), 'Auth': auth})

    def reset(self, request: Request, auth: Auth):
        token = request.param('token')
        user = AUTH['model'].where('remember_token', token).first()
        if user:
            return view('auth/reset', {'token': token, 'app': request.app().make('Application'), 'Auth': auth})

    def send(self, request: Request, session: Session, mail: Mail, validate: Validator):
        # Retrieve the old email value
        request.session.flash('email', request.input('email', ''))

        errors = request.validate(
            validate.required('email'),
            validate.email('email')
        )

        if errors:
            return request.back().with_errors(errors)

        email = request.input('email')
        user = AUTH['model'].where('email', email).first()

        if user:
            if not user.remember_token:
                user.remember_token = str(uuid.uuid4())
                user.save()
            reset_link = '{}/password/{}/reset'.format(env('SITE', 'http://localhost:8000'), user.remember_token)
            mail.subject('Reset Password Instructions').to(email).template('mail/reset-password', {'reset_link': reset_link}).send()
            session.flash('success', 'Email sent. Follow the instruction in the email to reset your password.')
            return request.redirect('/password')
        else:
            session.flash('error', "We can't find a user with that e-mail address.")
            return request.redirect('/password')

    def update(self, request: Request):
        user = AUTH['model'].where('remember_token', request.param('token')).first()
        if user:
            user.password = bcrypt_password(request.input('password'))
            user.save()
            return request.redirect('/login')
