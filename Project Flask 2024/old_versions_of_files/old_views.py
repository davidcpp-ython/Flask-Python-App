from flask import Blueprint, render_template, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from . import db
from .models import Patient
from sqlalchemy.exc import SQLAlchemyError
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    allergy_search_term = request.args.get('allergy_search_term', '')
    meds_search_term = request.args.get('meds_search_term', '')
    added_by_search_term = request.args.get('added_by_search_term', '')

    if request.method == 'POST':
        patientName = request.form.get('patient_name')
        allergy = request.form.get('allergy')
        contact = request.form.get('contact')
        meds = request.form.get('meds')

        if len(patientName) < 3:
            flash('Patient name is too short!', category = 'error')
        if len(contact)<3:
            flash('Contact number too short!', category = 'error')
        else:
            meds = meds if meds else 'No meds provided'
            allergy = allergy if allergy else 'No allergy provided'

            new_patient = Patient(patient_name=patientName, allergy=allergy, contact=contact, meds=meds, added_by=current_user.first_name, user_id=current_user.id)
            db.session.add(new_patient)
            db.session.commit()
            flash('Patient added!', category='success')

    try:
        all_patients = Patient.query.filter(
            (Patient.allergy.ilike(f'%{allergy_search_term}%')) &
            (Patient.meds.ilike(f'%{meds_search_term}%')) &
            (Patient.added_by.ilike(f'%{added_by_search_term}%'))
        ).all()

        current_app.logger.info(f"All Patients: {all_patients}")
    except SQLAlchemyError as e:
        flash(f'Error fetching patients: {str(e)}', category='error')
        all_patients = []

    return render_template("home.html", user=current_user, all_patients=all_patients, allergy_search_term=allergy_search_term, meds_search_term=meds_search_term, added_by_search_term=added_by_search_term)



@views.route('/delete-patient', methods=['POST'])
def delete_patient():
    patient_data = json.loads(request.data)
    patient_id = patient_data['patientId']
    patient = Patient.query.get(patient_id)
    if patient:
        if patient.user_id == current_user.id:
            db.session.delete(patient)
            db.session.commit()
        else:   
            flash('You cannot delete a patient if you haven\'t added them!', category = 'error')  
    return jsonify({})