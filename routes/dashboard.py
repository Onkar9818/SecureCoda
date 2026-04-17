from flask import Blueprint, render_template, jsonify
import services.scheduler as scheduler

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def home():
    return render_template("dashboard.html")

@dashboard.route('/alerts')
def get_alerts():
    return jsonify(scheduler.alerts)