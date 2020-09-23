from flask import request, current_app, g
from flask_babel import gettext
from flask_restful import Resource


from authentication import auth, login_admin_required
from apis import SQL
from db import QUERY

from util import make_response, get_service_no, \
    log_decorators, use_db, use_p, epoch_to_datetime, keys_to_snakecase, \
    make_sort_query, str_to_snakecase, epoch_to_date_str, make_raw_response, process_io_download


class Directory(Resource):
    MAIN_CLASS=True

    def __init__(self):
        self.p = use_p()
        self.db = use_db()

    @auth.login_required
    def get(self):
        p = self.p

        user_no = g.user['userNo']
        user_type = g.user['userType']

        sql, bind_param = SQL.prepare_query(QUERY['directory.yaml']['파일구조 조회'],
                                            {'userNo': user_no, 'userType': user_type})

        res = self.db.query(sql, bind_param)

        return make_response(200, res)

    @auth.login_required
    def post(self):
        p = self.p
        user_no = g.user['userNo']
        user_type = g.user['userType']

        with self.db.cursor() as cus:
            try:
                directory_no = cus.insert('directory_info',
                                          {'parent_directory_no': p['directoryNo'],
                                           'directory_name': p['directoryName'],
                                           'directory_owner': user_no},
                                          returning='directory_no')[0]['directory_no']

                cus.insert('user_directory',
                           {'user_no': user_no, 'directory_no': directory_no})

            except Exception as e:
                # Exception 발생시 Rollback
                current_app.logger.exception(e)
                cus.rollback()
                return make_response(400, error={'code': 2, 'result': 'sql failed'})

        sql, bind_param = SQL.prepare_query(QUERY['directory.yaml']['파일구조 조회'],
                                            {'userNo': user_no, 'userType': user_type})

        res = self.db.query(sql, bind_param)

        return make_response(200, res)

    @auth.login_required
    def put(self):
        p = self.p
        user_no = g.user['userNo']
        user_type = g.user['userType']

        self.db.update('directory_info',
                       {'directory_name': p['directoryName']},
                       {'directory_no': p['directoryNo']})

        sql, bind_param = SQL.prepare_query(QUERY['directory.yaml']['파일구조 조회'],
                                            {'userNo': user_no, 'userType': user_type})

        res = self.db.query(sql, bind_param)

        return make_response(200, res)

    @auth.login_required
    def delete(self):
        p = self.p
        user_no = g.user['userNo']
        user_type = g.user['userType']

        with self.db.cursor() as cus:
            try:
                cus.delete('user_directory', {'user_no': user_no, 'directory_no': p['directoryNo']})

                if user_type == 1:
                    cus.delete('directory_info',
                               {'directory_no': p['directoryNo']})
                else:
                    cus.delete('directory_info',
                               {'directory_no': p['directoryNo'], 'directory_owner': user_no})

            except Exception as e:
                # Exception 발생시 Rollback
                current_app.logger.exception(e)
                cus.rollback()
                return make_response(400, error={'code': 2, 'result': 'sql failed'})

        sql, bind_param = SQL.prepare_query(QUERY['directory.yaml']['파일구조 조회'],
                                            {'userNo': user_no, 'userType': user_type})

        res = self.db.query(sql, bind_param)

        return make_response(200, res)


class Share(Resource):

    def __init__(self):
        self.p = use_p()
        self.db = use_db()

    @auth.login_required
    def post(self):
        p = self.p
        user_no = g.user['userNo']
        user_type = g.user['userType']

        sql, bind_param = SQL.prepare_query(QUERY['directory.yaml']['사용자 유무 확인'], p)
        user_info = self.db.query_one(sql, bind_param)

        if not user_info:
            return make_response(400, error={'code': 1, 'result': 'not user'})

        res = self.db.insert('user_directory',
                             {'user_no': user_info['user_no'],
                              'directory_no': p['directoryNo']},
                             returning='*')[0]
        return make_response(200, res)
