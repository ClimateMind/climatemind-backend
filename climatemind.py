from knowledge_graph import app, db
from knowledge_graph.models import User, Scores

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Scores': Scores}

app.run(debug=True, host="0.0.0.0")
