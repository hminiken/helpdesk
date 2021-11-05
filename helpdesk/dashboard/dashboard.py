
from flask import Flask, Blueprint, render_template, request, redirect, url_for
import json

from helpdesk.dashboard.dashboard_utils import get_closed_last_x_days, get_dashboard_tickets, get_dashboard_tickets_by_assigned, get_dashboard_tickets_by_category, get_dashboard_tickets_by_closed, get_dashboard_tickets_by_created, get_dashboard_tickets_by_subcategory, get_dashboard_total, get_opened_last_x_days

dashboard_bp = Blueprint('dashboard_bp', __name__, 
                        template_folder='templates', 
                        static_folder='static')


@dashboard_bp.route("/")
def dashboard():
    # Get user ticket data

    tickets = get_dashboard_tickets()
    cat_tickets = get_dashboard_tickets_by_category()
    subcat_tickets = get_dashboard_tickets_by_subcategory()
    assigned_tickets = get_dashboard_tickets_by_assigned()
    created_tickets = get_dashboard_tickets_by_created()
    closed_tickets = get_dashboard_tickets_by_closed()

    total_tickets = get_dashboard_total()
    closed_last = get_closed_last_x_days()
    opened_last = get_opened_last_x_days()
    # eco_ontime = get_ECO_ontime()
    # open_npi = get_open_NPIs()
    # task_types = get_task_counts()

    jsonData = []
    jsonData.append(tickets)
    jsonData.append(cat_tickets)
    jsonData.append(subcat_tickets)
    jsonData.append(assigned_tickets)
    jsonData.append(created_tickets)
    jsonData.append(closed_tickets)
    jsonData.append(total_tickets)
    jsonData.append(closed_last)
    jsonData.append(opened_last)
    # jsonData = [tickets, cat_tickets, subcat_tickets, assigned_tickets, created_tickets, closed_tickets]

    data = map(json.dumps, jsonData)

    return render_template('dashboard/index.html', data=jsonData)
    # return render_template('EngineeringMetrics.html',
    #                        data=jsonData)

