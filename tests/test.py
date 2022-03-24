from easy import Easy
import pytest
import os
from werkzeug.test import Client

@pytest.fixture
def app():
    app = Easy("easy_web app")
    return app

@pytest.fixture
def client(app):
    return Client(app)

def test_url(app, client):

    @app.route("/test", methods=["GET", "POST"])
    def index(request):
        return "Hello World"

    rv = client.open("/test", method="GET")
    assert rv.data == b"Hello World"

def test_url_var(app, client):

    @app.route("/posts/<int:post_id>", methods=["GET", "POST"])
    def index(request, post_id):
        return f"Post {post_id}"

    rv = client.open("/posts/42", method="GET")
    assert rv.data == b"Post 42"