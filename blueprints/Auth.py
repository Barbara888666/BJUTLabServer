from flask import Blueprint, request

from api.API import BJUTLabAPI
from utilities import Log, get_form_data_by_key

AuthBP = Blueprint('Auth', __name__, url_prefix='/Auth')
api = BJUTLabAPI.get_instance()
logger = Log.get_logger(__name__)


@AuthBP.route('/register', methods=('POST',))
def register():
    form = request.form
    school_id = get_form_data_by_key(form, 'school_id')
    name = get_form_data_by_key(form, 'name')
    password = get_form_data_by_key(form, 'password')
    user_type = int(get_form_data_by_key(form, 'type'))
    return api.auth.register(school_id, name, password, user_type)


@AuthBP.route('/login', methods=('POST',))
def login():
    form = request.form
    school_id = get_form_data_by_key(form, 'school_id')
    password = get_form_data_by_key(form, 'password')
    user_type = int(get_form_data_by_key(form, 'type'))
    return api.auth.login(school_id, password, user_type)