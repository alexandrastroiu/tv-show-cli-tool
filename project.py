import requests
import sys
from fancify_text import monospaced
from bs4 import BeautifulSoup
import csv
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import random


API_URL = "https://api.tvmaze.com"
DEFAULT = "N/A"


def main():
    try:
        genres = get_genres()
    except ValueError:
        sys.exit(monospaced("Error fetching  genres. Try again!"))
    if len(sys.argv) < 3:
        sys.exit(monospaced("Not enough arguments entered. Try again!"))
    match sys.argv[1].strip().lower():
        case "--search":
            display_search()
        case "--sort":
            validate_sorting(genres)
            create_sorted_file()
            print(
                monospaced(
                    'Sorted list  of movies has been written to "sorted_movies.csv"'
                )
            )
        case "--plot":
            validate_plot()
            create_plot(genres)


def display_search():
    """
    The function displays the information about the movie entered by the user in the search command.

    Parameters:
              None

    Returns:
           None
    """
    if len(sys.argv) > 3:
        sys.exit(
            monospaced(
                "Too many arguments for search. Type one movie per search. Try again!"
            )
        )
    id = search_movie(sys.argv[2].strip().lower())
    try:
        basic_info = movie_info(id)
    except ValueError:
        sys.exit(
            monospaced(
                f"We found no matches in the database for the entry {sys.argv[2]}. Try again!"
            )
        )
    else:
        print(
            monospaced(f"We found a match in the database for the entry {sys.argv[2]}!")
        )
        print("\nName:", monospaced(basic_info["name"]))
        print("Type:", monospaced(basic_info["type"]))
        print("Language:", monospaced(basic_info["language"]))
        print("Genres: " + monospaced(", ".join(basic_info["genres"])))
        print("Status:", monospaced(basic_info["status"]))
        print("Average Runtime: ", monospaced(str(basic_info["averageRuntime"])))
        print("Premiered: ", monospaced(basic_info["premiered"]))
        print("Ended: ", monospaced(basic_info["ended"]))
        print("Rating: ", monospaced(str(basic_info["rating"])))
        print("Summary:", monospaced(basic_info["summary"]))


def create_sorted_file():
    """
    The function writes the sorted list of movies as requested by the user in the file 'sorted_movies.csv'

    Parameters:
              None

    Returns:
           None
    """
    movies = sort_movies()
    with open("sorted_movies.csv", "w") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "rating"])
        writer.writeheader()
        for movie in movies:
            writer.writerow(movie)


def validate_sorting(genres):
    """
    The function checks if the sorting command entered by the user is valid or invalid.

    If the command is invalid the function exists the program using sys.exit.

    Parameters:
              genres (set): A set

    Returns:
           None
    """
    sys.argv[2] = sys.argv[2].strip().lower()
    is_invalid_order = sys.argv[2] not in ["asc", "desc"]
    is_invalid_genre = (
        len(sys.argv) == 4 and sys.argv[3].strip().lower().capitalize() not in genres
    )
    is_invalid_length = len(sys.argv) > 4
    if is_invalid_order:
        sys.exit(
            monospaced(
                "Command is not valid. Second argument entered is not 'asc' or 'desc'. Try again!"
            )
        )
    if is_invalid_genre:
        sys.exit(
            monospaced(
                "Command is not valid. Third argument entered is not found in any movies. Try again!"
            )
        )
    if is_invalid_length:
        sys.exit(
            monospaced("Command is not valid. Too many arguments enetered. Try again!")
        )


def validate_plot():
    """
    The function validates the plot command entered by the user.

    If the command is not valid the function exists the program using sys.exit.

    Parameters:
              None

    Returns:
           None
    """
    if len(sys.argv) != 4:
        sys.exit(
            monospaced("Valid plot command needs 4 arguments in total. Try again!")
        )
    is_invalid_criteria = sys.argv[2].strip().lower() != "rating"
    is_invalid_data = sys.argv[3].strip().lower() != "genres"
    if is_invalid_criteria:
        sys.exit(
            monospaced(
                "Valid plot command needs 'rating' as third  argument. Try again!"
            )
        )
    if is_invalid_data:
        sys.exit(
            monospaced(
                "Valid plot command needs 'genres' as fourth argument. Try again!"
            )
        )


def remove_html_tags(text):
    """
    The function takes a text containing html tags and returns the text stripped of html tags.

    Parameters:
              text (str): A str

    Returns:
           clean_text (str): Another str which is the original text stripped of html tags
    """
    soup = BeautifulSoup(text, "html.parser")
    clean_text = soup.get_text(separator="")
    return clean_text


def is_valid_response(response):
    """
    The function checks if the response is valid or invalid by checking its status code.

    A valid response has the status code 200, menaing that the request was succcesful.

    Parameters:
              response (Response): A Response object from the requests library

    Returns:
            bool: True if the status code is 200, False if it is not 200
    """
    return response.status_code == 200


def is_ok_server(response):
    """
    The function checks if there is an internal server error or not by checking the status code of the response.

    The server has an internal error if th status code is 500.

    Parameters:
              response (Response): A Response object from the requests library

    Returns:
           bool: True if the status code of the response is not 500, False otherwise
    """
    return response.status_code != 500


def search_movie(name):
    """
    The function searches a movie by name in the database and returns its id if the movie is found or no errors or unexpected situations occur.

    Parameters:
              name (str): A str

    Returns:
           data["id"] (int): The id of the movie if it was found in the database.
           None (NoneType): If any error such as invalid response or interval server error occurs,
                        as well if the movie has no id, no key called id or the data returned about the movie is empty.
    """
    response = requests.get(f"{API_URL}/singlesearch/shows?q={name}")
    if not is_valid_response(response):
        return None
    if not is_ok_server(response):
        return None
    data = response.json()
    if data is None or "id" not in data or data["id"] is None:
        return None
    return data["id"]


def movie_info(id):
    """
    The function returns the basic information about a movie if the movie is found in the database or no errors occur.

    Parameters:
              id (int): An int

    Returns:
           Raises ValueError in case of no id provided, invalid response or internal server error.
           Otherwise returns a dictionary containing key-value pairs with the basic information about the movie.
    """
    if id is None:
        raise ValueError("Invalid ID. The movie might not  be in the database.")
    response = requests.get(f"{API_URL}/shows/{str(id)}")
    if not is_valid_response(response):
        raise ValueError("The request was not succesful. Try again!")
    if not is_ok_server(response):
        raise ValueError("Internal server error. Try again!")
    data = response.json()
    return {
        "name": set_none_values(data.get("name", DEFAULT)),
        "type": set_none_values(data.get("type", DEFAULT)),
        "language": set_none_values(data.get("language", DEFAULT)),
        "genres": set_none_values(data.get("genres", [])),
        "status": set_none_values(data.get("status", DEFAULT)),
        "averageRuntime": set_none_values(data.get("averageRuntime", DEFAULT)),
        "premiered": set_none_values(data.get("premiered", DEFAULT)),
        "ended": set_none_values(data.get("ended", DEFAULT), "Running"),
        "rating": set_none_values(data.get("rating", {}).get("average", DEFAULT)),
        "summary": set_none_values(remove_html_tags(data.get("summary", DEFAULT))),
    }


def set_none_values(value, default=DEFAULT):
    """
    The function returns the same value it was provided, unless the value is None, in that case it returns a default value.

    Parameters:
              value (float, int, str or NoneType): The value to check
              default(str): A str

    Returns:
           value (float, int, str or NoneType): the initial value
           default(str): a string which sets the default value in case the initial value is a NoneType
    """
    return default if value is None else value


def get_genres():
    """
    The function returns a set containing all the different genres available,
    if any errors occur or no data is returned by the server it raises ValueError.

    Parameters:
              None

    Returns:
           genres (set): a set of all the genres available
           Otherwise, it raises ValueError if any error occurs or if the server returns empty data.
    """
    response = requests.get(f"{API_URL}/shows")
    if not is_valid_response(response):
        raise ValueError("The request was not succesful. Try again!")
    if not is_ok_server(response):
        raise ValueError("Internal server error. Try again!")
    genres = set()
    data = response.json()
    if data is None:
        raise ValueError("The response was empty. Try again!")
    for show in data:
        for genre in show["genres"]:
            genres.add(genre)
    return genres


def filter_movies_rating():
    """
    The function returns a list of all movies which have a rating, it raises ValueError in case an error occurs.

    Parameters:
              None

    Returns:
           Returns a list of all movies with rating available.
           Otherwise, when an error occurs it raises ValueError.
    """
    response = requests.get(f"{API_URL}/shows")
    if not is_valid_response(response):
        raise ValueError("The request was not succesful. Try again!")
    if not is_ok_server(response):
        raise ValueError("Internal server error. Try again!")
    data = response.json()
    return [
        movie
        for movie in data
        if "rating" in movie
        and movie["rating"] is not None
        and movie["rating"]["average"] is not None
    ]


def sort_movies():
    """
    The function returns a list of dictionaries representing a list of movies sorted as requested by the user.

    Parameters:
              None

    Returns:
            top_movies(list): The list of sorted movies.
    """
    data = filter_movies_rating()
    top_movies = []

    for movie in sorted(
        data,
        key=lambda movie: movie["rating"]["average"],
        reverse=(sys.argv[2] == "desc"),
    ):
        try:
            if (
                "genres" in movie
                and sys.argv[3].strip().lower().capitalize() in movie["genres"]
            ):
                top_movies.append(
                    {"name": movie["name"], "rating": movie["rating"]["average"]}
                )
        except IndexError:
            top_movies.append(
                {"name": movie["name"], "rating": movie["rating"]["average"]}
            )
    return top_movies


def get_average_ratings_genre():
    """
    The function a dictionary containing key-value pairs of each genre and its average rating.

    Parameters:
              None

    Returns:
           new_dict(dict) : A dictionary of genre-averag rating pairs.
    """
    data = filter_movies_rating()
    genre_dict = {}
    new_dict = {}

    for movie in data:
        rating = movie["rating"]["average"]
        for current_genre in movie["genres"]:
            if current_genre not in genre_dict:
                genre_dict[current_genre] = {"count": 0, "rating": 0}
            genre_dict[current_genre]["count"] += 1
            genre_dict[current_genre]["rating"] += rating
    for genre in genre_dict:
        new_dict[genre] = genre_dict[genre]["rating"] / genre_dict[genre]["count"]
    return new_dict


def get_random_color():
    """
    The function returns a random color using the random library functions.

    Parameters:
              None

    Returns:
           A tuple containinf 3 float type values between 0 and 1, which represents a color.
    """
    return (random.random(), random.random(), random.random())


def create_plot(genres):
    """
    The function creates a bar plot and saves it in a file called 'plot.png' and prints a message to the user.

    Parameters:
              genres (set): A set containing all genres available

    Returns:
           None
    """
    left = [number for number in range(len(genres))]
    dict_ratings = get_average_ratings_genre()
    height = [dict_ratings[genre] for genre in dict_ratings]
    plt.bar(
        left,
        height,
        tick_label=list(dict_ratings.keys()),
        width=0.6,
        color=[get_random_color() for _ in range(len(genres))],
    )
    plt.xlabel("Genres")
    plt.ylabel("Average rating by genre")
    plt.title("Rating-Genre Bar chart")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("plot.png")
    print(monospaced("Plot saved as 'plot.png'"))


if __name__ == "__main__":
    main()
