# 模版渲染
import datetime
import json
import time

from flask import Flask, render_template, flash, session, url_for
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = "zzzz"


@app.route("/", methods=['get', 'post'])
def index():
    projects = [
        {"name": "project_1", "id": 23, "create_time": int(time.time())},
        {"name": "project_2", "id": 24, "create_time": int(time.time())},
        {"name": "project_3", "id": 25, "create_time": int(time.time())}
    ]
    flash('欢迎来到首页！')
    flash('欢迎来到德莱联盟！')
    return render_template('index.html',
                           p=projects,
                           title='起一个随便的名字',
                           msgone=None,
                           test_json='{"a_key": "a_value"}')  # 传的参数，可以直接在返回的html里面使用{{}}获取


@app.route("/login/<username>", methods=['get', 'post'])
def login(username):
    session['user'] = username
    return redirect(url_for('index'))


# 自定义过滤器
# @app.template_filter('s_time')
def strf_time(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


# 集中注册
app.add_template_filter(strf_time, 's_time')


# 自定义测试
@app.template_test()
def jsoned(my_str):
    try:
        json.loads(my_str)
        return True
    except ValueError:
        return False


@app.template_test('end_with')
def end_with(a_str, suffix):
    return a_str.lower().endwith(suffix.lower())

# {% if  name is end_with('me') %}
#     <h2>"{{ name }}" ends with "me". </h2>
# {% endif %}


# 环境处理器，储存类似于g,session,config那种全局的环境变量，方便前端调用
# 一般返回一个字典
@app.context_processor
def add_ctx():
    def c_time_func(timestamp):
        return datetime.datetime.fromtimestamp(timestamp)
    return {"user": ["user1", "user2"], "c_time_key": c_time_func}


if __name__ == '__main__':
    app.run(debug=True)

