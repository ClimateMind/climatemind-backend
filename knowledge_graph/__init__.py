from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
    
from knowledge_graph import routes, config