from knowledge_graph import db


class ZipHazard(db.Model):
    zip = db.Column(db.Integer, primary_key=True)
    hazard = db.Column(db.String, primary_key=True)
    value = db.Column(db.Boolean)

class Hazard(db.Model):
    hazard_type = db.Column(db.String, primary_key=True)
    iri = db.Column(db.String)
    ref_label = db.Column(db.String)
    description = db.Column(db.String)

