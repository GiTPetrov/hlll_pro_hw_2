from flask import Flask, request
from faker import Faker
import requests
import json


fake = Faker("uk_UA")
flsk_app = Flask(__name__)


@flsk_app.route('/')
def hw_2():
    return "<p>Welcome to homework 2!</p>"


@flsk_app.route('/requirements/')
def requirements():
    try:
        with open('requirements.txt', 'r') as requir:
            r = requir.readlines()
            if len(r) > 0:
                return ''.join(['<p>' + item[:-1] + '</p>' for item in r])
            else:
                return '"requirements.txt" is empty'
    except FileNotFoundError:
        return '"requirements.txt" doesn\'t exist'


@flsk_app.route('/generate-users/', methods=['GET'])
def generate_users():
    num_usrs = request.args.get('usrs', '')
    if num_usrs.isdigit():
        num_usrs = int(num_usrs)
    else:
        num_usrs = 100
    return ''.join([f'<pre>name: {fake.name():<30} email: {fake.ascii_free_email()}</pre>' for item in range(num_usrs)])


@flsk_app.route('/mean/')
def mean():
    with open('hw.csv', 'r', newline='') as hw_csv:
        hw_lst = hw_csv.readlines()
        hw_lst = [unit[:-1].split(', ') for unit in hw_lst][1:-1]
        hght_in = float()
        wght_pn = float()
        num_lines = 0
        for num, item in enumerate(hw_lst, start=1):
            num_lines = num
            hght_in += float(item[1])
            wght_pn += float(item[2])
        av_hght_cm = hght_in / num_lines * 2.54
        av_wght_kg = wght_pn / num_lines / 2.20462
        return f'<p>Average height: {av_hght_cm} cm</p><p>Average weight: {av_wght_kg} kg</p>'


@flsk_app.route('/space/')
def space():
    get_astronauts = requests.get('http://api.open-notify.org/astros.json')
    if get_astronauts.status_code == 200:
        astronauts = json.loads(get_astronauts.content)
        return f'<p>Now there are {astronauts.get("number")} astronauts in space</p>'
    else:
        print('Server response error!')




