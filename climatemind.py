from knowledge_graph import app, db
from knowledge_graph.models import User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

app.run(debug=True, host="0.0.0.0")
