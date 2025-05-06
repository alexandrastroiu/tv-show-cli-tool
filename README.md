# TV Show CLI Tool

## Description:
The program is a command-line interface application, it fetches data related to TV shows and movies using
the public API [TVMAZE API](https://api.tvmaze.com) in order to process and visualize it.

## Video Demo:  
<https://youtu.be/XtHSBj0rWoU>

## Key Features and Skills Demonstrated:
#### **Search**:
* Case-insensitive search by movie name via making a GET request to the API
* Implements error handling and provides fallback messages in case the response is invalid, an internal server error occurs or the movie is not found in the database
* Otherwise a message and the basic information about the movie will be displayed on the screen
* Uses the Beautiful Soup library to strip html tags from the information provided by the API, ensuring a clean and readable output
* The program also handles incomplete data in the information provided by the API

#### **Sort**:
* Sorts movies by genre and by rating score in ascending/descending order as specified by the user
* Validates user input
* Filters out movies with no rating score available
* Exports results to CSV for persistent storage and a clear format

#### **Plot**:
* Generates a dynamic bar chart of average ratings by genre using matplotlib
* Randomizes colors of the chart for visual appeal
* Saves the plot as a PNG file for easy sharing

#### User Experience:
* Comprehensive input validation with clear, user-friendly messages
* Handles missing data and invalid commands smoothly


## Technologies and Libraries:
* **Programming language**: Python
* **Python Standard Libraries**: sys, csv, random
* **Third-Party Libraries**: requests, fancify-text, Beautiful Soup, matplotlib

## Project Structure:
* **project.py** - contains the main code of the project written in Python
* **test_project.py** - contains unit tests for five functions from the project.py file
* **requirements.txt** - lists the third party packages used in the project

## Installation:
You must have Python 3.x installed.

1. Clone the repository:
```
git clone https://github.com/alexandrastroiu/tv-show-cli-tool.git
```

2. To install the third-party packages used in the project use the command:
```
pip install -r requirements.txt
```

## Usage:
A valid **search command** is:
```
python project.py --search name - change name for the name of the movie you want to search
python project.py --search "multiple words name" - type like this for a movie name with multiple words
```

A few valid **sort commands** are:
```
python project.py --sort order genre
python project.py --sort asc - sorts available movies in ascending order by rating
python project.py --sort desc - sorts available movies in descending order by rating
python project.py --sort asc Romance - sorts available Romance movies in ascending order by rating
```

The **valid genres** are:
* Adventure, History, Thriller, Drama, Fantasy, Espionage, Western, Sports, Supernatural, Horror
* Romance, Crime, Legal, Family, Medical, Music, Anime, Action, Comedy, Science-Fiction, War, Mystery

The valid **plot command** is:
```
python project.py --plot rating genre
```

## Planned Features
* [ ] Add a graphical user interface