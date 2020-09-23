# coding=utf-8
import json
import time
from datetime import datetime, timedelta

from flask import request, current_app, g
from flask_babel import gettext
from flask_restful import Resource

from authentication import get_one_user, generate_auth_token, authenticate, check_passwd
from util import make_response, use_db, use_p, json_dumper, system_log, get_system_config, is_json, ip_range_check


class Login(Resource):
    MAIN_CLASS = True

    def __init__(self):
        self.db = use_db()
        self.p = use_p()

    def post(self):
        p = self.p

        response_data = {
            'loginResult': 0,
            'loginMessage': '',
            'userData': None
        }
        response = make_response(200, [response_data])
        response.set_cookie(
            'token',
            value='',
            expires=''
        )

        user = get_one_user(p['userId'])
        g.user = user

        if not user:
            # Email 불일치
            response_data['loginResult'] = 4
            response_data['loginMessage'] = gettext('이메일/비밀번호가 일치하지 않습니다.')
            response = make_response(200, [response_data])

            return response

        else:
            user_no = user['userNo']
            passwd = str(user_no) + p['userPasswd']

            # 비밀번호 불일치
            if not check_passwd(passwd, user['userPasswd']):

                response_data['loginResult'] = 4
                response_data['loginMessage'] = gettext('이메일/비밀번호가 일치하지 않습니다.')
                response = make_response(200, [response_data])

                del user['userPasswd']
                
                return response

            from uuid import uuid4
            uuid = str(uuid4())

            token = generate_auth_token(
                user, 86400, uuid=uuid)

            response_data['loginResult'] = 1
            response_data['sessionTimeout'] = 86400
            response_data['loginMessage'] = 'Login Success'
            response_data['userData'] = user
            
            response = make_response(200, [response_data])
            
            response.set_cookie(
                'token',
                value=token.decode('ascii'),
                expires=datetime.utcnow() +
                timedelta(seconds=86400))

            return response
            

# 로그인 상태 확인
class CheckLogin(Resource):
    def __init__(self):

        self.db = use_db()

    def post(self):
        """
로그인 상태 확인
---
tags:
  - Login
        """
        if authenticate():
            user_data = g.user

            del user_data['userPasswd']

            response = {
                'loginResult': 1,
                'loginMessage': '',
                'sessionTimeout': 86400,
                'userData': user_data
            }
            
        else:
            response = {
                'loginResult': 0,
                'loginMessage': '',
            }

        return make_response(200, [response])


# 로그아웃
class Logout(Resource):
    def get(self):
        """
로그아웃
---
tags:
  - Login
responses:
  200:
    schema:
      type: object
      properties:
        status:
          type: integer
          default: 결과코드
"""
        response = make_response(200, {})

        response.set_cookie(
            'token',
            value='',
            expires=''
        )

        return response
