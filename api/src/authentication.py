# coding=utf-8
import binascii
import hashlib
from functools import wraps

from flask import g, current_app, abort, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired,
    URLSafeTimedSerializer)
from passlib.apps import custom_app_context as pwd_context

import db
import util

auth = HTTPBasicAuth()


def get_one_user(user_id):
    bind_param = []

    sql = """\
SELECT user_no
    ,user_id
    ,user_passwd
    ,user_name
    ,user_email
    ,user_phone
    ,user_type
    ,is_enable
    ,login_fail_count
    ,extra_info
    ,date_part('epoch', modify_date) AS modify_epoch
    ,date_part('epoch', reg_date) AS reg_epoch
    ,date_part('epoch', modify_date) AS passwd_update_epoch
    ,0 AS is_admin
FROM user_info 
WHERE TRUE
    AND is_enable = 1
    AND lower(user_id) = lower(%s)
"""
    bind_param.append(user_id)

    user = db.query_one(sql, bind_param)

    return util.keys_to_camelcase(user)


def generate_auth_token(user, expiration=600, is_admin=0, service_no=None, uuid=None, change_service=False):
    data = {}
    if is_admin:
        data['admin'] = 1

    if service_no:
        data['serviceNo'] = service_no

    if uuid:
        data['uuid'] = uuid

    data['changeService'] = change_service
    data['id'] = user['userId']

    s = Serializer(
        current_app.config['SECRET_KEY'],
        salt=current_app.config['SECURITY_PASSWORD_SALT'],
        expires_in=expiration)
    return s.dumps(data)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(
        email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(
            token, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token

    user = get_one_user(data['id'])

    if not current_app.config['DUPLICATE_LOGIN'] and not data['changeService']:
        try:
            if 'uuid' not in data or not user['extraInfo']['uuid'] == data['uuid']:
                return None  # duplicate Login
        except Exception:
            return None

    return user


@auth.verify_password
def verify_password(username_or_token, password):
    try:
        # 1. Cookie가 존재한다면 Cookie를 사용
        if 'token' in request.cookies:
            user = verify_auth_token(request.cookies['token'])
        elif 'token' in request.args:
            user = verify_auth_token(request.args['token'])
        else:
            # 2. header에 던져준다면 그방법대로 사용
            user = verify_auth_token(username_or_token)

        if not user:
            # 3. username과 password로 인증 시도 Basic 인증은 Admin만 적용
            user = get_one_user(username_or_token)
            if not user:
                return abort(401)
            elif not check_passwd(str(user['userNo']) + password, user['userPasswd']):
                return abort(401)
            else:
                pass

        g.user = user

    except TypeError as e:
        current_app.logger.exception(e)
        return abort(401)

    return True


# 함수 안에서 사용 전용.
def authenticate(username_or_token=None, password=None):
    try:
        user = None
        # 1. Cookie가 존재한다면 Cookie를 사용
        if 'token' in request.cookies:
            user = verify_auth_token(request.cookies['token'])
        else:
            # 2. header에 던져준다면 그방법대로 사용
            if username_or_token:
                user = verify_auth_token(username_or_token)

        if not user:
            # 3. username과 password로 인증 시도 Basic 인증은 Admin만 적용
            if username_or_token:
                user = get_one_user(username_or_token)
            if not user:
                return False
            elif not check_passwd(password, user['userPasswd']):
                return False
            else:
                pass
        g.user = user

    except TypeError as e:
        current_app.logger.exception(e)
        return False

    return True


def check_passwd(p1, p2):
    passwd_ok = True

    # if current_app.config['IS_GS']:
    #     from hmac import compare_digest
    #     if not compare_digest(hashlib.sha512(
    #         str(p1).encode()).digest(),
    #             binascii.unhexlify(p2)):
    #         passwd_ok = False
    # else:
    #     passwd_ok = pwd_context.verify(p1, p2)

    passwd_ok = pwd_context.verify(p1, p2)

    return passwd_ok


def verify_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in g or 'isAdmin' not in g.user or not g.user['isAdmin']:
            return abort(401)
        return f(*args, **kwargs)
    return decorated


login_admin_required = util.composed_decorators(auth.login_required, verify_admin)
