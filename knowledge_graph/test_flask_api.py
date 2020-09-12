import os
import tempfile

import pytest

from knowledge_graph import routes

# todo: finish this test...
@pytest.fixture
def client():
    db_fd, routes.app.config["DATABASE"] = tempfile.mkstemp()
    routes.app.config["TESTING"] = True

    with routes.app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(routes.app.config["DATABASE"])
