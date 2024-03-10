from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from .models import Patient
from . import db

def get_added_by_options():
    try:
        added_by_options = db.session.query(Patient.added_by).distinct().all()
        added_by_options = [option[0] for option in added_by_options if option[0] is not None]
        return added_by_options
    except SQLAlchemyError as e:
        current_app.logger.error(f'Error fetching added_by options: {str(e)}')
        return []