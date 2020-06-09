from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_user, current_user, logout_user, login_required
from forecastapp.db_mgmt.forms import PdcnMergeAdd
from forecastapp.models import MergedPdcn
from forecastapp import db


db_mgmt = Blueprint('db_mgmt', __name__)

@db_mgmt.route("/db_manager", methods=['GET', 'POST'])
@login_required
def db_manager():
    return render_template('db_manager.html', title='Database Manager', legend='Database Manager')

@db_mgmt.route("/pdcn_merge_add", methods=['GET', 'POST'])
@login_required
def pdcn_merge_add():
    form = PdcnMergeAdd()
    pdcnPairList = MergedPdcn.query.order_by(MergedPdcn.pdcnMain.asc())
    if form.validate_on_submit():
        newPdcnPair = MergedPdcn(pdcnMain=form.pdcnMain.data, pdcnAlt=form.pdcnAlt.data)
        db.session.add(newPdcnPair)
        db.session.commit()
        flash('PDCN Merge Added', 'success')
        return redirect(url_for('db_mgmt.pdcn_merge_add'))
    return render_template('pdcn_merge_add.html', title='Add PDCN Merge',
    form=form, pdcnPairList=pdcnPairList, legend='Add PDCN Merge')

@db_mgmt.route("/pdcn_merge_remove", methods=['GET', 'POST'])
@login_required
def pdcn_merge_remove():
    pdcnPairList = MergedPdcn.query.order_by(MergedPdcn.pdcnMain.asc())
    return render_template('pdcn_merge_remove.html', title='Remove PDCN Merge',
    legend='Remove PDCN Merge', pdcnPairList=pdcnPairList)
