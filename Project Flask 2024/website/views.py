from flask import Blueprint, render_template, request, flash, jsonify, current_app, session, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Patient
from sqlalchemy.exc import SQLAlchemyError
import json
from .filters import get_added_by_options

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    added_by_options = get_added_by_options()
    selected_added_by = request.args.get('selected_added_by', '')

    if request.method == 'POST':
         
        patientName = request.form.get('patient_name')
        allergy = request.form.get('allergy')
        contact = request.form.get('contact')
        meds = request.form.get('meds')
        additional_notes = request.form.get('additional_notes')

        if len(patientName) < 3:
            flash('Patient name is too short!', category = 'error')
        if len(contact)<3:
            flash('Contact number too short!', category = 'error')
        else:
            meds = meds if meds else 'No meds provided'
            allergy = allergy if allergy else 'No allergy provided'
            additional_notes = additional_notes if additional_notes else 'No additional notes provided'
            new_patient = Patient(patient_name=patientName, allergy=allergy, contact=contact, meds=meds, is_emergency=False, additional_notes=additional_notes,added_by=current_user.first_name, user_id=current_user.id)
            db.session.add(new_patient)
            db.session.commit()
            flash('Patient added!', category='success')
        
        return redirect(url_for('views.home'))
    
    try:
        all_patients = Patient.query.filter(Patient.added_by.ilike(f'%{selected_added_by}%')).all()

        current_app.logger.info(f"All Patients: {all_patients}")
    except SQLAlchemyError as e:
        flash(f'Error fetching patients: {str(e)}', category='error')
        all_patients = []

    return render_template("home.html", user=current_user, all_patients=all_patients, added_by_options=added_by_options, selected_added_by=selected_added_by)



from .emergency_email import send_emergency_notification, is_valid_email

@views.route('/toggle-emergency/<int:patient_id>', methods=['POST'])
@login_required
def toggle_emergency(patient_id):
    patient = Patient.query.get(patient_id)
    if patient:
        if patient.user_id == current_user.id:
            patient.is_emergency = not patient.is_emergency
            db.session.commit()

            if patient.is_emergency == True:
                if is_valid_email(patient.contact)==True:
                    send_emergency_notification(patient)
                else:
                    flash('Patient marked as an emergency but can\'t send an email to the contact. Mail is not available')

        else:
            flash('You cannot toggle emergency status for a patient you haven\'t added!', category='error')

    return redirect(url_for('views.home'))


@views.route('/emergencies')
@login_required
def emergencies():
    emergency_patients = Patient.query.filter_by(is_emergency=True).all()
    return render_template("emergencies.html", user=current_user, emergency_patients=emergency_patients)




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