from bookmanager import app
from forms import SignupForm, LoginForm


def test_register(self, email, password, confirm):
    return self.app.post(
        '/register',
        data=dict(email=email, password=password, confirm=confirm),
        follow_redirects=True)