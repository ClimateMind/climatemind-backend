from knowledge_graph import app, db
from knowledge_graph.models import Users, Scores, Sessions  # TODO Lrf, Zip, Iri


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": Users,
        "Scores": Scores,
        "Sessions": Sessions,
        #        "LRF": Lrf,
        #        "Zip": Zip,
        #        "Iri": Iri,
    }


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
