import sqlite3

from typing import Dict, List, Set

# Подключение к базе данных
connection = sqlite3.connect("netflix.db", check_same_thread=False)
cursor = connection.cursor()


def search_by_name(title: str) -> Dict:
    """Ищет самый свежий фильм с данным названием"""
    if type(title) != str:
        raise TypeError

    # SQL запрос
    query = f"""SELECT title, country, release_year, listed_in, description
               FROM netflix
               WHERE title='{title}'
               ORDER BY release_year
               LIMIT 1"""

    # Извлекаем данные
    fetch_data = cursor.execute(query)
    film = fetch_data.fetchone()

    # Преобразуем данные
    title, country, release_year, listed_in, description = film
    film_data = {
        "title": title,
        "country": country,
        "release_year": release_year,
        "genre": listed_in,
        "description": description
    }

    return film_data


def search_by_years(left_year: int, right_year: int) -> List[Dict]:
    """Ищет все фильмы, выпущенные в указаном промежутке лет"""
    # Обработка ошибок
    if type(left_year) != int or type(right_year) != int:
        raise TypeError
    if right_year < left_year:
        raise TypeError("Неверно указан промежуток")

    # SQL запрос
    query = f"""SELECT title, release_year
               FROM netflix
               WHERE release_year BETWEEN {left_year} AND {right_year}
               LIMIT 100"""

    # Извлекаем данные
    fetch_data = cursor.execute(query)
    films = fetch_data.fetchall()

    # Преобразуем полученные данные
    all_correct_films = []
    for film in films:
        title, release_year = film
        film_data = {
            "title": title,
            "release_year": release_year
        }
        all_correct_films.append(film_data)

    return all_correct_films


def search_by_rating(ratings: List) -> List[Dict]:
    """Ищет все фильмы с нужным рейтингом"""
    if type(ratings) != list:
        raise TypeError
    if len(ratings) == 0:
        raise ValueError

    # SQL запрос
    query = f"""SELECT title, rating, description
               FROM netflix
               WHERE {" OR ".join([f"rating='{ratings[i]}'" for i in range(len(ratings))])}"""

    # Извлекаем данные
    fetch_data = cursor.execute(query)
    films = fetch_data.fetchall()

    # Преобразуем полученные данные
    all_correct_films = []
    for film in films:
        title, rating, description = film
        film_data = {
            "title": title,
            "rating": rating,
            "description": description
        }
        all_correct_films.append(film_data)

    return all_correct_films


def search_by_genre(genre: str) -> List[Dict]:
    """Ищет все фильмы нужного жанра"""
    if type(genre) != str:
        raise TypeError

    # SQL запрос
    query = f"""SELECT title, description
               FROM netflix
               WHERE listed_in LIKE '%{genre}%'"""

    # Извлекаем данные
    fetch_data = cursor.execute(query)
    films = fetch_data.fetchall()

    # Преобразуем полученные данные
    all_correct_films = []
    for film in films:
        title, description = film
        film_data = {
            "title": title,
            "description": description
        }
        all_correct_films.append(film_data)

    return all_correct_films


def get_actors(first_actor: str, second_actor: str) -> Set[str]:
    """Возвращает список актёров, игравших с указанными актёрами"""
    query = f"""SELECT netflix.cast
                FROM netflix
                WHERE netflix.cast LIKE '%{first_actor}%%{second_actor}%'
                OR netflix.cast LIKE '%{second_actor}%%{first_actor}%'"""

    # Извлекаем данные
    fetch_data = cursor.execute(query)
    casts = fetch_data.fetchall()

    # Получаем списко актёров
    actors_cast = dict()
    correct_cast = set()
    for cast in casts:
        actors = list(cast[0].split(", "))
        for actor in actors:
            if actor not in [first_actor, second_actor]:
                if actor in actors_cast:
                    actors_cast[actor] += 1
                else:
                    actors_cast[actor] = 1

    for actor in actors_cast:
        if actors_cast[actor] >= 2:
            correct_cast.add(actor)

    return correct_cast


def get_film(film_type: str, year: int, genre: str) -> List[Dict]:
    """Возвращает картины указанного типа за указанный год в указанном жанре"""
    # Запрос
    query = f"""SELECT title, description
               FROM netflix
               WHERE type='{film_type}'
               AND release_year='{year}'
               AND listed_in LIKE '%{genre}%'"""

    # Получаем данные
    fetch_data = cursor.execute(query)
    films = fetch_data.fetchall()

    # Преобразуем данные в список словарей
    current_films = []
    for film in films:
        title, description = film
        current_films.append({"title": title,
                              "description": description})

    return current_films
