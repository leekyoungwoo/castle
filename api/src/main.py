# coding=utf-8
import importlib
import inspect
import logging
import os
import sys

from flasgger import Swagger
from flask import Flask, send_from_directory, request
from flask_babel import Babel
from flask_cors import CORS
from flask_restful import Api

from authentication import auth
from config import CONFIG
from db import init_query_dict
from util import str_to_camelcase

app = Flask(__name__)
init_query_dict()

# 환경변수에 따른 실행모드 설정 START
if os.environ.get('CASTLE_MOD') == 'development':
    app.config.from_object(CONFIG['development'])
else:
    app.config.from_object(CONFIG['production'])

formatter = logging.Formatter(
    '%(name)s|%(filename)s:%(lineno)s > [%(levelname)s] [%(asctime)s] : %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.WARN)
app.logger.addHandler(stream_handler)

babel = Babel(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

api = Api(app)

swagger = Swagger(
    app,
    config=app.config['SWAGGER_CONFIG'],
    decorators=[
        auth.login_required])


@babel.localeselector
def get_locale():
    if 'lang' in request.cookies:
        return request.cookies['lang']
    else:
        return 'ko'


@app.route('/')
@app.route('/api/')
def index_page():
    return 'Welcome To MudFix RESTful web service.' \
           'See doc /api/v1/docs'


# DEVELOP 모드일때 추가 url 라우팅
if app.config['DEBUG']:
    @app.route('/fdata/<path:path>')
    def send_file(path):
        return send_from_directory(app.config['FILE_ROOT_DIR'], path)

importlib.import_module('apis')
# apis 모듈 동적 add_resource
for module in list(m for m in sys.modules.keys() if m.find('apis.') == 0):
    for api_name, obj in inspect.getmembers(sys.modules[module]):
        if inspect.isclass(obj) and 'apis' in obj.__module__ and obj.__module__ == module:
            if hasattr(obj, 'MAIN_CLASS') and obj.MAIN_CLASS:
                api.add_resource(obj, '/api/v1/{}'.format(obj.__name__), endpoint=obj.__name__)
            else:
                url = '/api/v1/{}/{}'.format(str_to_camelcase(obj.__module__.split('.')[-1], True),
                                             obj.__name__)
                api.add_resource(obj, url, endpoint=url)

importlib.import_module('exec')
# exec 모듈 동적 add_resource
for module in list(m for m in sys.modules.keys() if m.find('exec.') == 0):
    for api_name, obj in inspect.getmembers(sys.modules[module]):
        if inspect.isclass(obj) and 'exec' in obj.__module__ and obj.__module__ == module:
            if hasattr(obj, 'MAIN_CLASS') and obj.MAIN_CLASS:
                api.add_resource(obj, '/exec/{}'.format(obj.__name__), endpoint=obj.__name__)
            else:
                url = '/exec/{}/{}'.format(str_to_camelcase(obj.__module__.split('.')[-1], True),
                                           obj.__name__)
                api.add_resource(obj, url, endpoint=url)

if __name__ == '__main__':

    extra_files = None
    if app.config['DEBUG']:
        extra_dirs = ['./query']
        extra_files = extra_dirs[:]
        for extra_dir in extra_dirs:
            for dirname, dirs, files in os.walk(extra_dir):
                for filename in files:
                    filename = os.path.join(dirname, filename)
                    if os.path.isfile(filename):
                        extra_files.append(filename)
                        
    # 디버깅 환경이나 테스트 환경에서는 FileLogging을 사용하지 않는다.
    if not app.config['DEBUG']:
        file_handler = logging.FileHandler(
            app.config['LOG_FILE_PATH'])

        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.WARN)

        app.logger.addHandler(file_handler)

    app.run(host=app.config['HOST'], port=app.config['PORT'], extra_files=extra_files if extra_files else None)
