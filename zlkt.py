#*-*coding:utf-8*-*

#time:2018-9-28

from flask import Flask,render_template
import config


app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def index():
    return render_template('index.html')