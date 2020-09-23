from flask import request, current_app, g
from flask_babel import gettext
from flask_restful import Resource
from passlib.apps import custom_app_context as pwd_context


from authentication import auth, login_admin_required
from apis import SQL
from db import QUERY

from util import make_response, get_service_no, \
    log_decorators, use_db, use_p, epoch_to_datetime, keys_to_snakecase, \
    make_sort_query, str_to_snakecase, epoch_to_date_str, make_raw_response, process_io_download


class User(Resource):
    MAIN_CLASS=True

    def __init__(self):
        self.p = use_p()
        self.db = use_db()

    @auth.login_required
    def get(self):
        p = self.p

        user_no = g.user['userNo']
        user_type = g.user['userType']

        if user_type != 1:
            return make_response(200, error={'code': 1, 'error': '관리자 접근권한'})

        sql, bind_param = SQL.prepare_query(QUERY['user.yaml']['유저 리스트 조회'], {**p, 'userNo': user_no})
        res = self.db.query(sql, bind_param)

        return make_response(200, res)

    @auth.login_required
    def post(self):
        p = self.p

        user_type = g.user['userType']

        if user_type != 1:
            return make_response(200, error={'code': 1, 'error': '관리자 접근권한'})

        with self.db.cursor() as cus:
            try:
                user_info = cus.insert('user_info', {'user_id': p['userId']}, returning='*')[0]
                root_directory = cus.insert('directory_info', {'directory_name': p['userName'],
                                                               'directory_owner': user_info['user_no']}, returning='*')[0]
                cus.insert('user_directory', {'user_no': user_info['user_no'], 'directory_no': root_directory['directory_no']})
                if 'userPasswd' in p and p['userPasswd']:
                    p['userPasswd'] = pwd_context.hash(str(user_info['user_no']) + p['userPasswd'])

                sql, bind_param = SQL.prepare_query(QUERY['user.yaml']['사용자 추가'], {**p, 'userNo': user_info['user_no']})
                cus.execute(sql, bind_param)

            except Exception as e:
                current_app.logger.exception(e)
                cus.rollback()
                return make_response(200, error={'code': 2, 'error': 'sql failed'})

        sql, bind_param = SQL.prepare_query(QUERY['user.yaml']['유저 리스트 조회'], {**p})
        res = self.db.query(sql, bind_param)

        return make_response(200, res)

    @auth.login_required
    def put(self):
        p = self.p

        user_type = g.user['userType']

        if user_type != 1:
            return make_response(200, error={'code': 1, 'error': '관리자 접근권한'})

        if 'userPasswd' in p and p['userPasswd']:
            p['userPasswd'] = pwd_context.hash(str(p['userNo']) + p['userPasswd'])

        sql, bind_param = SQL.prepare_query(QUERY['user.yaml']['사용자 수정'], {**p})
        self.db.execute(sql, bind_param)
        sql, bind_param = SQL.prepare_query(QUERY['user.yaml']['유저 리스트 조회'], {**p})
        res = self.db.query(sql, bind_param)

        return make_response(200, res)

    @auth.login_required
    def delete(self):
        p = self.p

        user_type = g.user['userType']

        if user_type != 1:
            return make_response(200, error={'code': 1, 'error': '관리자 접근권한'})

        self.db.update('user_info', {'is_enable': 0}, {'user_no': p['userNo']})
        sql, bind_param = SQL.prepare_query(QUERY['user.yaml']['유저 리스트 조회'], {**p})
        res = self.db.query(sql, bind_param)

        return make_response(200, res)


class Edit(Resource):

    def __init__(self):
        self.p = use_p()
        self.db = use_db()

    @auth.login_required
    def post(self):
        p = self.p
        user_no = g.user['userNo']
        user_type = g.user['userType']

        sql, bind_param = SQL.prepare_query(QUERY['user.yaml']['내 정보 수정'], {**p, 'userNo': user_no})
        res = self.db.query(sql, bind_param)

        return make_response(200, res)

    @auth.login_required
    def delete(self):
        p = self.p
        user_no = g.user['userNo']
        user_type = g.user['userType']

        sql, bind_param = SQL.prepare_query(QUERY['user.yaml']['회원 탈퇴'], {**p, 'userNo': user_no})
        res = self.db.query(sql, bind_param)

        return make_response(200, res)
