from flask import Flask, jsonify
from db_data_access import *


app = Flask(__name__)


@app.route("/")
def page_index():
    return "Hello"


@app.route("/movie/<title>")
def get_film_by_title(title: str):
    film = search_by_name(title=title)

    return jsonify(film)


@app.route("/movie/<int:left_year>/to/<int:right_year>")
def get_films_by_years(left_year: int, right_year: int):
    films = search_by_years(left_year, right_year)

    return jsonify(films)


@app.route("/rating/children")
def get_films_for_children():
    ratings = ["G"]
    films = search_by_rating(ratings)

    return jsonify(films)


@app.route("/rating/family")
def get_films_for_family():
    ratings = ["G", "PG", "PG-13"]
    films = search_by_rating(ratings)

    return jsonify(films)


@app.route("/rating/adult")
def get_films_for_adult():
    ratings = ["R", "NC-17"]
    films = search_by_rating(ratings)

    return jsonify(films)


@app.route("/genre/<genre>")
def get_films_by_genre(genre: str):
    films = search_by_genre(genre)

    return jsonify(films)


if __name__ == '__main__':
    app.run()
