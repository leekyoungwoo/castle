# coding=utf-8
import ast
import copy
import importlib
import json
import os
import re
import urllib.parse
from datetime import datetime
from functools import wraps

import pytz
from flask import current_app, Response, request, g, abort, send_file
from flask_babel import gettext
from inflection import underscore, camelize
from simplejson import dumps as json_dumps

import db


def _make_json(data, status):
    response = Response(
        json_dumps(data, ensure_ascii=False, default=base_encode, sort_keys=True),
        content_type="application/json; charset=utf-8", status=status)
    response.headers['Last-Modified'] = datetime.now()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'

    return response


def _transform_keys(data, key_transformer):
    """
    dict 이나 set 의 value를 camelcase로 변환.
    :param data:
    :param key_transformer:
    :return:
    """
    if isinstance(data, dict):
        transformed = {}
        for key, value in data.items():
            camel_key = key_transformer(key)
            transformed[camel_key] = _transform_keys(value, key_transformer)
        return transformed

    if isinstance(data, (list, tuple)):
        new_data = []
        for i, name in enumerate(data):
            new_data.append(_transform_keys(name, key_transformer))
        return new_data
    return data


def _underscore_repl(match):
    return match.group()[1].upper()


def keys_to_camelcase(data):
    return _transform_keys(data, str_to_camelcase)


def keys_to_snakecase(data):
    return _transform_keys(data, str_to_snakecase)


def str_to_camelcase(str_value, capitalize=False):
    """
    string 을 camelcase로 변환.
    :param str_value:
    :param capitalize:
    :return:
    """
    return camelize(str(str_value), capitalize)


def str_to_snakecase(str_value):
    """
    string 을 snakecase로 변환.
    :param str_value:
    :return:
    """
    return underscore(str_value)


def base_encode(obj):
    """
    simplejson에서 사용하는 JSONEncoder의 하위클래스
    특수값의 인코딩을 처리하는데 사용
    """

    if isinstance(obj, datetime):
        # 모든 datetime을 RFC 1123 형식으로 변환
        return date_to_str(obj)
    elif isinstance(obj, set):
        # set객체는 list로 변환
        return list(obj)
    else:
        return obj


def date_to_str(date):
    """
     datetime의 값을 Config에 정의된 포맷으로 변환.
    """
    return datetime.strftime(
        date, current_app.config['DATE_FORMAT']) if date else None


def epoch_to_date_str(epoch):
    """
    epoch를 config에 정의한 date_format으로 변환.
    :param epoch:
    :return:
    """
    # .replace(tzinfo=pytz.utc)
    return datetime.utcfromtimestamp(int(float(epoch))).strftime(current_app.config['DATE_FORMAT'])


def epoch_to_date_local_str(epoch):
    """
    epoch를 config에 정의한 date_format으로 변환.
    :param epoch:
    :return:
    """
    # .replace(tzinfo=pytz.utc)
    return datetime.fromtimestamp(int(float(epoch)), tz=pytz.timezone(
        'Asia/Seoul')).strftime(current_app.config['DATE_FORMAT'])


def epoch_to_datetime(epoch):
    """
    epoch를 config에 정의한 date_format으로 변환.
    :param epoch:
    :return:
    """
    return datetime.utcfromtimestamp(int(float(epoch)))


def epoch_to_local_datetime(epoch):
    if epoch:
        return datetime.fromtimestamp(int(float(epoch)), tz=pytz.timezone('Asia/Seoul'))
    else:
        return None


def make_response(status, query=None, error=None):
    """
    Response와 Response Data 구조를 정의한다.
    :param query:
    :param status:
    :param error:
    """
    data = dict()
    data['list'] = keys_to_camelcase(query)
    data['error'] = error
    data['status'] = status

    return _make_json(data, status)


def make_raw_response(status, data=None):
    data = keys_to_camelcase(data)
    return _make_json(data, status)


def make_filter(filter_dic, sort_filter=list()):
    result = list()
    if len(filter_dic) > 0:
        for key, value in filter_dic.items():
            if 'search' in key and value and 'searchType' in value and value['searchType']:
                if 'searchText' in value and not value['searchText']:
                    value['searchText'] = ''

                if value['searchType'] in sort_filter:
                    result_dic = make_filter_dict(
                        str_to_snakecase(
                            value['searchType']) + '::TEXT',
                        'ILIKE',
                        '%' + value['searchText'] + '%')
                    result.append(result_dic)

                elif len(value['searchType'].split(',')) > 1:
                    result_dic = make_filter_dict(
                        'concat_space(' + value['searchType'] + ')',
                        'ILIKE',
                        '%' + value['searchText'] + '%')
                    result.append(result_dic)

                else:
                    pass

            elif re.match(r'^\w+Array$', key):
                result_dic = make_filter_dict(str_to_snakecase(key[:-5]), 'IN', value.replace(' ', '').split(','))
                result.append(result_dic)

            elif re.match(r'^\w+Epoch$', key):
                if 'start' in value:
                    result_dic = make_filter_dict(str_to_snakecase(key), '>=', value['start'])
                    result.append(result_dic)

                if 'end' in value:
                    result_dic = make_filter_dict(str_to_snakecase(key), '<=', value['end'])
                    result.append(result_dic)

            else:
                result_dic = make_filter_dict(str_to_snakecase(key), '=', value)
                result.append(result_dic)

    return result


def make_filter_dict(search_type, operator, text):
    result_dic = dict()
    result_dic['type'] = search_type
    result_dic['operator'] = operator
    result_dic['text'] = text

    return result_dic


def make_sort_query(sort_list, target_list, default):
    if sort_list:
        sort_sql = ''
        for sort in sort_list:
            if 'field' in sort and 'order' in sort and (
                    sort['order'].upper() == 'ASC' or sort['order'].upper() == 'DESC'):
                if sort['field'] in target_list:
                    sort_sql += __make_sort_sql(str_to_snakecase(sort['field']), sort['order'].upper(), True)
                else:
                    sort_sql = '{} ASC\n'.format(default)
                    break
    else:
        sort_sql = '{} ASC\n'.format(default)

    return sort_sql


def __make_sort_sql(target_name, order_type, reverse=False):
    if order_type == 'ASC':
        if reverse:
            order_type = 'DESC NULLS LAST'
    else:
        if reverse:
            order_type = 'ASC NULLS FIRST'

    if target_name == 'reg_ip' or target_name == 'ip':
        target_name += "::INET"

    if target_name == 'serviceTemplateNo':
        target_name += "::INT"

    sql = '{} {}\n'.format(target_name, order_type)

    return sql


def composed_decorators(*decorators):
    def decorated(f):
        for decorator in reversed(decorators):
            f = decorator(f)
        return f

    return decorated


class DebugDecorator:

    def __init__(self, f):
        self.func = f

    def __call__(self, *args, **kwargs):
        ret = self.func(*args, **kwargs)

        if current_app.config['DEBUG']:
            current_app.logger.debug(request)
            current_app.logger.debug(ret.status)
            current_app.logger.debug(ret.headers)
            try:
                current_app.logger.debug(json.dumps(json.loads(ret.get_data(as_text=True)), sort_keys=True, indent=4))
            except BaseException:
                pass

        return ret


def log_decorators(log_title, log_type=None):
    def decorator(func):
        @wraps(func)
        def newFunc(*args, **kwargs):
            req_p = copy.deepcopy(args[0].p) if hasattr(args[0], 'p') else {}
            # if 'sort' in args[0].p and args[0].p:
            #     req_p['sort'] = json.loads(args[0].p['sort'])
            # if 'filter' in args[0].p and args[0].p:
            #     req_p['filter'] = json.loads(args[0].p['filter']) if 'filter' in args[0].p and args[0].p['filter'] else None

            ret = func(*args, **kwargs)
            _log_title = gettext(log_title)
            _log_type = log_type

            if request.headers.getlist("X-Forwarded-For"):
                remote_ip = request.headers.getlist("X-Forwarded-For")[0]
            else:
                remote_ip = request.remote_addr

            if not _log_type:
                _log_type = 4 if 'user' in g and g.user['isAdmin'] else 8

            # 로그인 하였고, 정상적인 결과일 경우 로그 기록
            p = json.loads(ret.data.decode('utf-8'))

            if hasattr(args[0], 'p'):
                if 'userPasswd' in req_p:
                    del req_p['userPasswd']

                if 'beforePasswd' in req_p:
                    del req_p['beforePasswd']

                if 'newPasswd' in req_p:
                    del req_p['newPasswd']

                if 'licenseDetailEnc__func' in req_p:
                    del req_p['licenseDetailEnc__func']

                if 'licenseHashEnc__func' in req_p:
                    del req_p['licenseHashEnc__func']

            log_detail = {
                'req': req_p,
                'res': p['list'] if 'list' in p else p['error']}

            if 'user' in g and not ('error' in p and p['error']):
                db.insert(
                    'system_log', {
                        'user_no': g.user['userNo'],
                        'user_id': g.user['userId'],
                        'user_name': g.user['userName'],
                        'user_email': g.user['userEmail'],
                        'log_type': _log_type,
                        'log_title': _log_title,
                        'log_detail': json_dumper(log_detail),
                        'api_name': args[0].__class__.__name__,
                        'ip': remote_ip})

            return ret

        return newFunc

    return decorator


def system_log(p, log_title, log_category, log_type=None):
    _log_type = log_type

    if request.headers.getlist("X-Forwarded-For"):
        remote_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        remote_ip = request.remote_addr

    if not _log_type:
        _log_type = 4 if 'user' in g and g.user['isAdmin'] else 8

    if isinstance(p, dict) and 'userPasswd' in p:
        del p['userPasswd']

    cv_log_title = gettext(log_title)

    # 로그인 하였으면 기록
    if 'user' in g:
        db.insert(
            'system_log', {
                'user_no': g.user['userNo'],
                'user_id': g.user['userId'],
                'user_name': g.user['userName'],
                'user_email': g.user['userEmail'],
                'log_type': _log_type,
                'log_title': cv_log_title,
                'log_detail': json_dumper(p),
                'api_name': log_category,
                'ip': remote_ip})


def json_dumper(data):
    return json_dumps(data, ensure_ascii=False, default=base_encode, sort_keys=True)


def get_service_no(service_no=None):
    if g.user['isAdmin']:
        if service_no:
            return service_no
        else:
            return None
    else:
        # user 객체 체크
        if getattr(g, 'user') and 'serviceNo' in g.user:
            return g.user['serviceNo']
        else:
            abort(401)


def get_user_no(user_no=None):
    if g.user['isAdmin']:
        if user_no:
            return user_no
        else:
            return None
    else:
        # user 객체 체크
        if getattr(g, 'user') and 'userNo' in g.user:
            return g.user['userNo']
        else:
            abort(401)


def process_download(file_name):
    return send_file(file_name, as_attachment=True)


def process_io_download(byte_io, mimetype, file_name):
    res = send_file(byte_io, mimetype)
    res.headers.add('content-length', byte_io.getbuffer().nbytes)
    res.headers["Accept"] = mimetype

    if request.referrer and 'api/docs' in request.referrer:
        _, ext = os.path.splitext(file_name)
        res.headers["Content-Disposition"] = "attachment; " \
                                             "filename={}".format(
            'file_sample' + ext
        )
    else:
        res.headers["Content-Disposition"] = "attachment; " \
                                             "filename*=UTF-8''{quoted_filename}".format(
            quoted_filename=urllib.parse.quote(file_name.encode('utf8'))
        )
    return res


def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_extensions


def use_db():
    _db = importlib.import_module('db')
    _db.connect(database=current_app.config['DB_NAME'])

    return _db


def use_p():
    try:
        if request.args:
            p = request.args.to_dict().copy()
        elif request.form:
            p = request.form.copy()
        elif request.data:
            p = json.loads(force_decode(request.data))
        elif request.get_json():
            p = request.get_json()
        else:
            p = {}
    except Exception:
        p = {}

    return p


def get_system_config(parameter=None):
    bind_param = []

    sql = """
SELECT parameter
    ,COALESCE(value, default_value) AS value
FROM system_config
"""

    if parameter:
        sql += """
        WHERE parameter = %s
"""
        bind_param.append(parameter)

    return db.query_dict(sql, 'parameter', bind_param)


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    value = re.sub(r'[-\s]+', '-', value)

    return value


def striplist(l):
    return [x.strip() for x in l]


def check_param_is_none(p, target, rm_space=False):
    ret = str(p[target]).strip() if target in p and p[target] else None
    if ret and rm_space:
        ret = re.sub(r'\s{2,}', ' ', ret)
    return ret


# 강제디코딩
def force_decode(string):
    for i in ['utf8', 'cp949']:
        try:
            return string.decode(i)
        except UnicodeDecodeError:
            pass


def get_language():
    if request.accept_languages[0][0].find('ja'):
        return 'ja'
    else:
        return 'ko'


def extract_target(target, query_result):
    result = []
    for info in query_result:
        dict_set = dict((k, info[k]) for k in list(info.keys()) if k.lower().find(target) != -1 or k == 'reg_epoch')
        result.append(dict_set)

    return result


def semiflatten(multi):
    """MutiDict를 일반 dict로 변환"""
    if multi:
        result = multi.to_dict(flat=False)
        for k, v in result.items():
            if len(v) == 1:
                result[k] = v[0]
        return result
    else:
        return multi


def guess_type(s):
    try:
        value = ast.literal_eval(s)
    except ValueError:
        return str
    else:
        return type(value)


# n진법 변환
def convert_n_way(n, base=36):
    T = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    q, r = divmod(n, base)
    if q == 0:
        return T[r]
    else:
        return convert_n_way(q, base) + T[r]

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        current_app.logger.error('{} : invalid json', myjson)
        return False
    return True


def ip_range_check(remote_ip, target_ip_list):
    is_ok = False
    for target_ip in target_ip_list:
        chk = 0
        for ip, ti in zip(remote_ip.split('.'), target_ip.split('.')):
            if ti.find('~') > 0:
                start_ip, end_ip = ti.split('~')
            else:
                start_ip = end_ip = ti

            if int(start_ip) <= int(ip) <= int(end_ip):
                chk += 1
            else:
                continue

        if chk == 4:
            is_ok = True

    if is_ok:
        return True
    else:
        return False