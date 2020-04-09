from flask import session, request, make_response

from exception import APIReinitializationError, ParameterException
from utilities import SqlHandler, Encryptor


class AuthAPI:
    __auth_instance = None

    def __init__(self, logger, sql: SqlHandler.SQLHandler):
        if AuthAPI.__auth_instance is not None:
            raise APIReinitializationError('Auth')
        self._logger = logger
        self._sql = sql

    @staticmethod
    def get_instance(logger, sql):
        if AuthAPI.__auth_instance is None:
            AuthAPI.__auth_instance = AuthAPI(logger, sql)
        return AuthAPI.__auth_instance

    def register(self, school_id: str, name: str, password: str, user_type: int):
        if user_type != 0:
            raise ParameterException(400, 'Unsupported user type: {}'.format(user_type))
        proc_name = 'create_student_user'
        md5_pwd = Encryptor.md5(password)
        dataset, code = self._sql.run_proc(proc_name, 1, (school_id, name, md5_pwd))
        return {
            'return code': code
        }

    def login(self, school_id: str, password: str, user_type: int):
        if user_type != 0:
            raise ParameterException(400, 'Unsupported user type: {}'.format(user_type))
        proc_name = 'get_student_user'
        md5_pwd = Encryptor.md5(password)
        dataset, code = self._sql.run_proc(proc_name, 1, (school_id, md5_pwd))
        self._logger.info(str(dataset))
        self._logger.info(code)
        if code == 0:
            session.clear()
            session['school_id'] = school_id
            session['name'] = dataset[0][0]

            r = make_response({
                'success': True,
                'name': dataset[0][0]
            })
            r.headers['Access-Control-Allow-Credentials'] = 'true'
            self._logger.info(str(r.headers))
            return r
        return {
            'success': False
        }