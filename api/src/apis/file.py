import os
import uuid

from flask import request, current_app, g
from flask_babel import gettext
from flask_restful import Resource


from authentication import auth, login_admin_required
from apis import SQL
from db import QUERY

from util import make_response, get_service_no, \
    log_decorators, use_db, use_p, epoch_to_datetime, keys_to_snakecase, \
    make_sort_query, str_to_snakecase, epoch_to_date_str, make_raw_response, process_io_download, allowed_file


class File(Resource):
    ALLOWED_EXTENSIONS = {'bmp', 'BMP', 'jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG', 'gif', 'GIF'}
    MAIN_CLASS=True

    def __init__(self):
        self.p = use_p()
        self.db = use_db()

    @auth.login_required
    def get(self):
        p = self.p
        user_no = g.user['userNo']

        sql, bind_param = SQL.prepare_query(QUERY['file.yaml']['파일 리스트 조회'], {**p, 'userNo': user_no})
        res = self.db.query(sql, bind_param)

        return make_response(200, res)
        pass

    @auth.login_required
    def post(self):
        p = self.p
        params = dict()

        user_no = g.user['userNo']
        params['userNo'] = user_no

        if 'file' not in request.files or len(request.files) != 1:
            return make_response(200, error=[{'errInfo': 'No parameter OR parameter length is one'}])

        root_dir = current_app.config['FILE_ROOT_DIR']

        file = request.files['file']
        file_name = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]

        params['fileName'] = file.filename
        params['rawName'] = file_name

        if allowed_file(file_name, self.ALLOWED_EXTENSIONS):
            if not os.path.isdir(os.path.join(root_dir, str(user_no))):
                os.makedirs(os.path.join(root_dir, str(user_no)))

            file.save(os.path.join(root_dir, str(user_no), file_name))

            params['fileUrl'] = os.path.join('\\fdata', str(user_no), file_name)
            with self.db.cursor() as cus:
                try:
                    sql, bind_param = SQL.prepare_query(QUERY['file.yaml']['파일 추가'], {**p, **params})
                    res = cus.query(sql, bind_param)
                    return make_response(200, res)

                except Exception as e:
                    current_app.logger.exception(e)
                    os.remove((os.path.join(root_dir, str(user_no), file_name)))
                    cus.rollback()
                    return make_response(200, error={'code': 2, 'error': 'sql failed'})

        else:
            return make_response(200, error={'code': 1, 'error': 'failed'})

    @auth.login_required
    def delete(self):
        p = self.p

        user_no = g.user['userNo']
        sql, bind_param = SQL.prepare_query(QUERY['file.yaml']['파일 삭제'], {**p, 'userNo': user_no})
        res = self.db.query(sql, bind_param)

        return make_response(200, res)
