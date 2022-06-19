from flask import Flask, request, render_template
from faker import Faker
import requests
import json
import os
import sqlite3
from flsk_srv.db import get_db
import random


fake = Faker("uk_UA")


def create_app(test_config=None):
    # create and configure the app
    flsk_app = Flask(__name__, instance_relative_config=True)
    flsk_app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(flsk_app.instance_path, 'flsk_srv.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        flsk_app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        flsk_app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(flsk_app.instance_path)
    except OSError:
        pass

    @flsk_app.route('/')
    def hw_3():
        return "<p>Welcome to homework 3!</p>"

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
        num_usrs = request.args.get('usrs', type=int, default=100)
        return ''.join(
            [f'<pre>name: {fake.name():<30} email: {fake.ascii_free_email()}</pre>' for item in range(num_usrs)])

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

    from . import db
    db.init_app(flsk_app)

    @flsk_app.route('/names/')
    def art_names():
        dat_bas = get_db()
        dist_art = dat_bas.execute(
            'SELECT DISTINCT artist FROM tracks'
        ).fetchall()
        count_art = dat_bas.execute(
            'SELECT COUNT(DISTINCT artist) FROM tracks'
        ).fetchone()
        return render_template('hw_3/names.html', count_artists=count_art, artists=dist_art)

    @flsk_app.route('/tracks/')
    def count_tracks():
        dat_bas = get_db()
        trks = dat_bas.execute(
            'SELECT artist, title FROM tracks ORDER BY artist DESC'
        ).fetchall()
        count_trks = dat_bas.execute(
            'SELECT COUNT(id) FROM tracks'
        ).fetchone()
        return render_template('hw_3/tracks.html', tracks=trks, count_tracks=count_trks)
        # return f'<p>There are {count_art[0]} different artists in the database:</p> ' \
        #        f'{"".join([f"<p>{unit}</p>" for unit in dist_art])}'

    @flsk_app.route('/genre/')
    def count_genre():
        dat_bas = get_db()
        genres = [item['genrename'] for item in dat_bas.execute(
            'SELECT genrename FROM genres'
        ).fetchall()]
        get_genres = request.args.get('gnr', '')
        if get_genres not in genres:
            get_genres = random.choice(genres)
        trks_genres = dat_bas.execute(
            'SELECT genres.id, tracks.artist, tracks.title FROM genres '
            'LEFT JOIN tracks ON genres.id=tracks.genre_id WHERE genres.genrename=?', (get_genres, )
        ).fetchall()
        count_gnrs = dat_bas.execute(
            'SELECT COUNT(tracks.id) FROM genres '
            'LEFT JOIN tracks ON genres.id=tracks.genre_id WHERE genres.genrename=?', (get_genres,)
        ).fetchone()
        return render_template('hw_3/genre.html', tracks=trks_genres, count_genres=count_gnrs, genre=get_genres)

    @flsk_app.route('/tracks-sec/')
    def tracks_seconds():
        dat_bas = get_db()
        trks_sec = dat_bas.execute(
            'SELECT title, length FROM tracks ORDER BY title DESC'
        ).fetchall()
        return render_template('hw_3/tracks_sec.html', tracks=trks_sec)

    @flsk_app.route('/tracks-sec/statistics/')
    def statistics():
        dat_bas = get_db()
        stat = dat_bas.execute(
            'SELECT SUM(length), AVG(length) FROM tracks'
        ).fetchall()
        return render_template('hw_3/statistics.html', statistic=stat)

    return flsk_app
