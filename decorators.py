#*-*coding=utf-8*-*

from functools import wraps
from flask import redirect,url_for,session,request

# 登录限制的装饰器
def login_required(func):
    @wraps(func)
    def login_func(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            red = redirect(url_for('login'))
            red.set_cookie('url',request.full_path)
            return red
    return login_func