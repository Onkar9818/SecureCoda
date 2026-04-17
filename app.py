from flask import Flask
from routes.dashboard import dashboard
# from services.scheduler import start_scheduler
from services.remediation import delete_row
import logging
from services.scheduler import scan
from services.coda_client import get_docs
from services.remediation import unpublish_doc


app = Flask(__name__)

logging.basicConfig(filename='logs/app.log', level=logging.INFO)

app.register_blueprint(dashboard)

@app.route("/scan")
def run_scan():
    scan()
    return {"status": "Scan complete"}

@app.route("/test")
def test():
    return {"docs": get_docs()}

@app.route("/fix/<doc_id>")
def fix(doc_id):
    unpublish_doc(doc_id)
    return {"status": "fixed"}



@app.route("/delete/<doc_id>/<table_id>/<row_id>")
def delete(doc_id, table_id, row_id):
    delete_row(doc_id, table_id, row_id)
    return {"status": "deleted"}

if __name__ == "__main__":
    
    app.run(debug=True)