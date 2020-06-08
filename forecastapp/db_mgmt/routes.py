from flask import render_template, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from forecastapp.db_mgmt.forms import PdcnMergeAdd


db_mgmt = Blueprint('db_mgmt', __name__)

@db_mgmt.route("/pdcn_merge_add")
@login_required
def pdcn_merge_add():
    form = PdcnMergeAdd()
    return render_template('pdcn_merge_add.html', title='Add PDCN Merge',
    form=form, legend='Add PDCN Merge')
