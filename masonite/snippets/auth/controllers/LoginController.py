"""A LoginController Module."""

from masonite.auth import Auth
from masonite.view import View
from masonite.request import Request
from masonite.validation import Validator


class LoginController:
    """Login Form Controller."""

    def __init__(self):
        """LoginController Constructor."""
        pass

    def show(self, request: Request, view: View, auth: Auth):
        """Show the login page.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.
            view {masonite.view.View} -- The Masonite view class.
            auth {masonite.auth.auth} -- The Masonite auth class.

        Returns:
            masonite.view.View -- Returns the Masonite view class.
        """
        if request.user():
            return request.redirect('/home')
        return view.render('auth/login', {'app': request.app().make('Application'), 'Auth': auth})

    def store(self, request: Request, auth: Auth, validate: Validator):
        """Login the user.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.
            auth {masonite.auth.auth} -- The Masonite auth class.

        Returns:
            masonite.request.Request -- The Masonite request class.
        """
        # Retrieve the old email value
        request.session.flash('email', request.input('email', ''))

        errors = request.validate(
            validate.required(['email', 'password']),
            validate.email('email')
        )

        if errors:
            return request.back().with_errors(errors)

        if auth.login(request.email, request.password):
            return request.redirect_to('home')

        request.session.flash('message', 'These credentials do not match our records.')
        return request.redirect_to('login')

    def logout(self, request: Request, auth: Auth):
        """Log out the user.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.
            auth {masonite.auth.auth} -- The Masonite auth class.

        Returns:
            masonite.request.Request -- The Masonite request class.
        """
        auth.logout()
        return request.redirect('/login')
