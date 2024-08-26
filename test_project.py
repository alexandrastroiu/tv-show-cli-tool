from project import (
    remove_html_tags,
    search_movie,
    movie_info,
    set_none_values,
    get_genres,
)


def test_remove_html_tags():
    assert remove_html_tags("<p></p><a></a></b><i></i><title></title><br>") == ""
    assert remove_html_tags("<>") == "<>"
    assert remove_html_tags("text without tags!") == "text without tags!"


def test_search_movie():
    assert search_movie("Under the Dome") == 1
    assert search_movie("Hawaii Five-0") == 24
    assert search_movie("NCIS: New Orleans") == 45
    assert search_movie("Parks and Recreation") == 174
    assert search_movie("xyzz") is None
    assert search_movie("Lost in Translation") is None
    assert search_movie("LOST IN TRANSLATION") is None


def test_movie_info():
    assert movie_info(174) == {
        "name": "Parks and Recreation",
        "type": "Scripted",
        "language": "English",
        "genres": ["Comedy"],
        "status": "Ended",
        "averageRuntime": 30,
        "premiered": "2009-04-09",
        "ended": "2015-02-24",
        "rating": 8.2,
        "summary": "Parks and Recreation is a comedy series based around the main character Leslie Knope (a bureaucrat) in the parks department of Pawnee.",
    }
    assert movie_info(216) == {
        "name": "Rick and Morty",
        "type": "Animation",
        "language": "English",
        "genres": ["Comedy", "Adventure", "Science-Fiction"],
        "status": "Running",
        "averageRuntime": 30,
        "premiered": "2013-12-02",
        "ended": "Running",
        "rating": 8.8,
        "summary": "Rick is a mentally gifted, but sociopathic and alcoholic scientist and a grandfather to Morty; an awkward, impressionable, and somewhat spineless teenage boy. Rick moves into the family home of Morty, where he immediately becomes a bad influence.",
    }


def test_set_none_values():
    assert set_none_values(None) == "N/A"
    assert set_none_values(None, "VALUE") == "VALUE"
    assert set_none_values("str") == "str"
    assert set_none_values("str", "VALUE") == "str"


def test_get_genres():
    assert get_genres() == {
        "Horror",
        "Espionage",
        "Sports",
        "Family",
        "Medical",
        "Mystery",
        "History",
        "Legal",
        "Supernatural",
        "Romance",
        "Adventure",
        "Western",
        "Fantasy",
        "Anime",
        "Comedy",
        "Drama",
        "Science-Fiction",
        "Music",
        "Action",
        "Thriller",
        "War",
        "Crime",
    }
