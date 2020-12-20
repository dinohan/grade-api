from flask import Flask, render_template, request, jsonify
from collections import OrderedDict
from flask_cors import CORS
import configparser
import pysaint
import json
import sys

config = configparser.ConfigParser()
config.read('config.properties')


app = Flask(__name__)
CORS(app, resources={r'*': {'origins': '*'}})
# app.config['JSON_AS_ASCII'] = False


def strToScore(str):
    if str == 'A+':
        return 4.5
    elif str == 'A0':
        return 4.3
    elif str == 'A-':
        return 4.0
    elif str == 'B+':
        return 3.5
    elif str == 'B0':
        return 3.3
    elif str == 'B-':
        return 3.0
    elif str == 'C+':
        return 2.5
    elif str == 'C0':
        return 2.3
    elif str == 'C-':
        return 2.0
    elif str == 'D+':
        return 1.5
    elif str == 'D0':
        return 1.3
    elif str == 'D-':
        return 1.0
    else:
        return 0


def avgGrade(grades):
    sum = 0
    i = 0
    for grade in grades:
        sum += float(grade['과목학점']) * strToScore(grade['등급'])
        if strToScore(grade['등급']) > 0:
            i += float(grade['과목학점'])
    if i == 0:
        return 0
    return sum / i


@app.route('/')
def index():
    # grades = pysaint.grade('20192880', '$Ehguq317qkqh')
    # ans = OrderedDict()
    return dinohan()


def getGrade(idNumber, pw):
    grades = pysaint.grade(idNumber, pw)
    ans = OrderedDict()
    ans['avg'] = avgGrade(grades)
    ans['class_list'] = []
    for grade in grades:
        ans['class_list'].append({'id': grade['과목코드'],
                                  'year': grade['이수학년도'],
                                  'semester': grade['이수학기'],
                                  'title': grade['과목명'],
                                  'credit': grade['과목학점'],
                                  'score': grade['성적'],
                                  'grade': grade['등급'],
                                  'professor': grade['교수명']})

    return json.dumps(ans, ensure_ascii=False, indent='\t')


@ app.route('/api')
def api():
    idNumber = request.args.get('id', '')
    pw = request.args.get('pw', '')
    if idNumber == '' or pw == '':
        return 'parameter error'
    return getGrade(idNumber, pw)


@ app.route('/api/dinohan')
def dinohan():
    return getGrade(config['MY_INFO']['id'], config['MY_INFO']['pw'])


if __name__ == '__main__':
    app.run(host='0.0.0.0')
