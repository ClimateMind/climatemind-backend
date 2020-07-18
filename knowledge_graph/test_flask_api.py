import os
import tempfile

import pytest

from knowledge_graph import flask_api

#todo: finish this test...
@pytest.fixture
def client():
    db_fd, flask_api.app.config['DATABASE'] = tempfile.mkstemp()
    flask_api.app.config['TESTING'] = True

    with flask_api.app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(flask_api.app.config['DATABASE'])