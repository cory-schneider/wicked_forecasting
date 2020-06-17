from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_user, current_user, logout_user, login_required
from forecastapp.db_mgmt.forms import PdcnMergeAdd, RemovePdcnPair
from forecastapp.db_mgmt.models import MergedPdcn
from forecastapp import db

db_mgmt = Blueprint('db_mgmt', __name__)

@db_mgmt.route("/db_manager", methods=['GET', 'POST'])
@login_required
def db_manager():
    return render_template('db_manager.html', title='Database Manager', legend='Database Manager')

@db_mgmt.route("/pdcn_pair_add", methods=['GET', 'POST'])
@login_required
def pdcn_pair_add():
    form = PdcnMergeAdd()
    pdcnPairList = MergedPdcn.query.order_by(MergedPdcn.pdcnMain.asc())

    if form.validate_on_submit():
        newPdcnPair = MergedPdcn(pdcnMain=form.pdcnMain.data,
                                 pdcnAlt=form.pdcnAlt.data,
                                 author=current_user)
        db.session.add(newPdcnPair)
        db.session.commit()
        flash('PDCN Pair Added to Database', 'success')
        return redirect(url_for('db_mgmt.pdcn_pair_add'))

    return render_template('pdcn_pair_add.html', title='Add PDCN Pairs',
    form=form, pdcnPairList=pdcnPairList)

@db_mgmt.route("/pdcn_pair_remove", methods=['GET', 'POST'])
@login_required
def pdcn_pair_remove():
    removePair = RemovePdcnPair()
    pdcnPairList = MergedPdcn.query.order_by(MergedPdcn.pdcnMain.asc())

    if removePair.validate_on_submit():
        toRemove = request.form.getlist('removeCheck')
        print(toRemove)
        for pair_id in toRemove:
            pdcnPair = MergedPdcn.query.get_or_404(pair_id)
            db.session.delete(pdcnPair)
        db.session.commit()
        flash('PDCN Pair(s) Removed from Database', 'success')
        return redirect(url_for('db_mgmt.pdcn_pair_remove'))

    return render_template('pdcn_pair_remove.html',
                           title='Remove PDCN Pairs',
                           removePair=removePair,
                           pdcnPairList=pdcnPairList)
