#*-*coding:utf-8*-*

#time:2018-9-28

from flask import Flask,render_template,request,url_for,redirect,session
import config
from exts import db
from models import User,Question
from hashlib import sha1
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    questions = Question.query.order_by('-create_time').all()
    context = {'title':u'首页',"questions":questions}
    return render_template('index.html',**context)

@app.route('/login/', methods=["GET","POST"])
def login():
    if request.method == "GET":

        context = {'title':u'登录页'}
        return render_template('login.html', **context)
    else:
        telephone = request.form.get('telephone')
        password =  request.form.get('pwd')
        p1 = sha1()
        p1.update(password)
        pwd = p1.hexdigest()
        user = User.query.filter(User.telephone==telephone).first()
        if user:
            if pwd == user.password:
                session['user_id'] = user.id
                # 实现登录后重新返回登录前的页面
                url = request.cookies.get('url', '/')
                print 'url:', url
                red = redirect(url)
                # 登录成功后,将原先的url置零.
                red.set_cookie('url','',max_age=-1)

                # return redirect(url_for('index'))
                return red
            else:
                return u'密码有误,请重新填写'
        else:
            return u"登录手机号有误,请重新填写"

@app.route('/register/', methods=["GET","POST"])
def register():
    if request.method == "GET":
        context = {'title':u'注册页'}
        return render_template('register.html', **context)
    else:
        telephone  = request.form.get('telephone')
        username = request.form.get('username')
        password = request.form.get('pwd')
        password2 = request.form.get('pwd2')

        # 判断该手机号码是否已经被注册了.
        user = User.query.filter(User.telephone == telephone).first()
        print 'user:',user
        if user:
            return u'该手机号码已经被注册,请重新换个手机号码'
        else:
            # 两次密码输入需要一致才可以通过
            if password != password2:
                return u'两次密码输入需一致'
            else:
                p1 = sha1()
                p1.update(password)
                pwd = p1.hexdigest()

                print 'pwd:',pwd
                user1 = User(telephone=telephone,username=username,password=pwd)
                # user1 = User(telephone,username,pwd)
                # user1 = User()

                # user1.telephone = telephone
                # user1.username = username
                # user1.password = password
                db.session.add(user1)
                db.session.commit()
                # 若注册成功则跳转到登录页面

                return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        context = {'title':u'发布问答'}
        return render_template('question.html',**context)
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id==user_id).first()
        question.author = user
        # question.author_id = user_id
        db.session.add(question)
        db.session.commit()
        # print 'question.author.telephone:',question.author.telephone

        return redirect(url_for('index'))

@app.route('/detail/<question_id>')
def detail(question_id):
    q = Question.query.filter(Question.id==question_id).first()
    context = {'title':u'详情','question':q}
    return render_template('detail.html',**context)

@app.route('/add_comment/', methods=['POST'])
def add_comment():
    comment = request.form.get('comment')
    pass


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}


if __name__ == '__main__':
    app.run()