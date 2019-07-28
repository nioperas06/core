"""The RegisterController Module."""

from app.User import User
from masonite.view import View
from masonite.auth import Auth
from masonite.request import Request
from masonite.validation import Validator
from masonite.auth import MustVerifyEmail
from masonite.managers import MailManager
from config import application, auth as auth_config


class RegisterController:
    """The RegisterController class."""

    def __init__(self):
        """The RegisterController Constructor."""
        pass

    def show(self, request: Request, view: View, auth: Auth):
        """Show the registration page.

        Arguments:
            Request {masonite.request.request} -- The Masonite request class.

        Returns:
            masonite.view.View -- The Masonite View class.
        """
        return view.render('auth/register', {'app': application, 'Auth': auth})

    def store(self, request: Request, mail_manager: MailManager, auth: Auth, validate: Validator):
        """Register the user with the database.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.

        Returns:
            masonite.request.Request -- The Masonite request class.
        """
        # Retrieve the old email and name values
        request.session.flash('name', request.input('name', ''))
        request.session.flash('email', request.input('email', ''))

        errors = request.validate(
            validate.required(['name', 'email', 'password']),
            validate.length('name', max=255),
            validate.email('email'),
            validate.length('email', max=255),
            validate.isnt(
                validate.is_in('email', User.all().pluck('email'))
            ),
            validate.length('password', min=8),
        )

        if errors:
            return request.back().with_errors(errors)

        user = auth.register({
            'name': request.name,
            'email': request.email,
            'password': request.password,
        })

        if isinstance(user, MustVerifyEmail):
            user.verify_email(mail_manager, request)

        # Login the user
        if auth.login(request.input(auth_config.AUTH['model'].__auth__), request.password):
            # Redirect to the homepage
            return request.redirect_to('home')

        # Login failed. Redirect to the register page.
        return request.redirect_to('register')
