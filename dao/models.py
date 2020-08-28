from knowledge_graph import db


class ZipHazard(db.Model):
    zip_code = db.Column(db.Integer, primary_key=True)
    aff_hurricane_flag = db.Column(db.Boolean)
    aff_deadly_heat_flag = db.Column(db.Boolean)
    aff_wildfire_flag = db.Column(db.Boolean)
    aff_air_life_flag = db.Column(db.Boolean)
    aff_air_health_sensitive_flag = db.Column(db.Boolean)
    aff_air_health_flag = db.Column(db.Boolean)


class Hazard:
    hazard_type = db.Column(db.String, primary_key=True)
    iri = db.Column(db.String)
    ref_label = db.Column(db.String)
    description = db.Column(db.String)

