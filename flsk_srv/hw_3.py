from flask import Blueprint, request, render_template
from flsk_srv.db import get_db
import random


bp = Blueprint('hw_3', __name__)


@bp.route('/names/')
def art_names():
    dat_bas = get_db()
    dist_art = dat_bas.execute(
        'SELECT DISTINCT artist FROM tracks'
    ).fetchall()
    count_art = dat_bas.execute(
        'SELECT COUNT(DISTINCT artist) FROM tracks'
    ).fetchone()
    return render_template('hw_3/names.html', count_artists=count_art, artists=dist_art)


@bp.route('/tracks/')
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


@bp.route('/genre/')
def count_genre():
    dat_bas = get_db()
    genres = [item['genrename'] for item in dat_bas.execute(
        'SELECT genrename FROM genres'
    ).fetchall()]
    get_genres = request.args.get('gnr')
    if get_genres not in genres:
        get_genres = random.choice(genres)
    trks_genres = dat_bas.execute(
        'SELECT genres.id, tracks.artist, tracks.title FROM genres '
        'LEFT JOIN tracks ON genres.id=tracks.genre_id WHERE genres.genrename=?', (get_genres,)
    ).fetchall()
    count_gnrs = dat_bas.execute(
        'SELECT COUNT(tracks.id) FROM genres '
        'LEFT JOIN tracks ON genres.id=tracks.genre_id WHERE genres.genrename=?', (get_genres,)
    ).fetchone()
    return render_template('hw_3/genre.html', tracks=trks_genres, count_genres=count_gnrs, genre=get_genres)


@bp.route('/tracks-sec/')
def tracks_seconds():
    dat_bas = get_db()
    trks_sec = dat_bas.execute(
        'SELECT title, length FROM tracks ORDER BY title DESC'
    ).fetchall()
    return render_template('hw_3/tracks_sec.html', tracks=trks_sec)


@bp.route('/tracks-sec/statistics/')
def statistics():
    dat_bas = get_db()
    stat = dat_bas.execute(
        'SELECT SUM(length), AVG(length) FROM tracks'
    ).fetchall()
    return render_template('hw_3/statistics.html', statistic=stat)