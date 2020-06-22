from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_user, current_user, logout_user, login_required
from forecastapp.database.forms import PdcnMergeAdd, RemovePdcnPair, WslrFamAdd, WslrFamRemove
from forecastapp.database.models import PdcnPair, WholesalerFamily
from forecastapp import db

database = Blueprint('database', __name__)

@database.route("/database_manager", methods=['GET', 'POST'])
@login_required
def database_manager():
    return render_template('database_manager.html', title='Database Manager', legend='Database Manager')

@database.route("/pdcn_pair_add", methods=['GET', 'POST'])
@login_required
def pdcn_pair_add():
    form = PdcnMergeAdd()
    pdcnPairList = PdcnPair.query.order_by(PdcnPair.pdcnMain.asc())

    if form.validate_on_submit():
        newPdcnPair = PdcnPair(pdcnMain=form.pdcnMain.data,
                                 pdcnAlt=form.pdcnAlt.data,
                                 author=current_user)
        db.session.add(newPdcnPair)
        db.session.commit()
        flash('PDCN Pair Added to Database', 'success')
        return redirect(url_for('database.pdcn_pair_add'))

    return render_template('pdcn_pair_add.html',
                           title='Add PDCN Pairs',
                           form=form,
                           pdcnPairList=pdcnPairList)

@database.route("/pdcn_pair_remove", methods=['GET', 'POST'])
@login_required
def pdcn_pair_remove():
    removePair = RemovePdcnPair()
    pdcnPairList = PdcnPair.query.order_by(PdcnPair.pdcnMain.asc())

    if removePair.validate_on_submit():
        toRemove = request.form.getlist('removeCheck')
        print(toRemove)
        for pair_id in toRemove:
            pdcnPair = PdcnPair.query.get_or_404(pair_id)
            db.session.delete(pdcnPair)
        db.session.commit()
        flash('PDCN Pair(s) Removed from Database', 'success')
        return redirect(url_for('database.pdcn_pair_remove'))

    return render_template('pdcn_pair_remove.html',
                           title='Remove PDCN Pairs',
                           removePair=removePair,
                           pdcnPairList=pdcnPairList)

@database.route("/wslr_fam_add", methods=['GET', 'POST'])
@login_required
def wslr_fam_add():
    form = WslrFamAdd()
    wslrFamList = WholesalerFamily.query.order_by(WholesalerFamily.name.asc())

    if form.validate_on_submit():
        newWslrFam = WholesalerFamily(name=form.name.data,
                                 nums=form.nums.data,
                                 author=current_user)
        db.session.add(newWslrFam)
        db.session.commit()
        flash('Wholesaler Family Added to Database', 'success')
        return redirect(url_for('database.wslr_fam_add'))

    return render_template('wslr_fam_add.html',
                           title='Add WSLR Fam',
                           form=form,
                           wslrFamList=wslrFamList)

@database.route("/wslr_fam_remove", methods=['GET', 'POST'])
@login_required
def wslr_fam_remove():
    removeFam = WslrFamRemove()
    wslrFamList = WholesalerFamily.query.order_by(WholesalerFamily.name.asc())

    if removeFam.validate_on_submit():
        toRemove = request.form.getlist('removeCheck')
        print(toRemove)
        for fam_id in toRemove:
            wslrFam = WholesalerFamily.query.get_or_404(fam_id)
            db.session.delete(wslrFam)
        db.session.commit()
        flash('WSLR Fam(s) Removed from Database', 'success')
        return redirect(url_for('database.wslr_fam_remove'))

    return render_template('wslr_fam_remove.html',
                           title='Remove Wholesaler Families',
                           removeFam=removeFam,
                           wslrFamList=wslrFamList)
