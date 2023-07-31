from main import app


def teardown_module():
    app.dependency_overrides = {}
