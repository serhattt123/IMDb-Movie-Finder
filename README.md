# IMDb Movie Finder

A Python-based movie filtering and recommendation project built with **Pandas**, **NumPy**, and **Matplotlib**, using IMDb datasets.

The project was developed as a practical way to learn and apply data cleaning, data analysis, filtering, visualization, and basic recommendation system concepts with Python.

## Features

* Load and process IMDb movie datasets
* Clean missing and invalid data
* Combine IMDb title and rating datasets
* Filter movies based on:

  * Minimum IMDb rating
  * Genre
  * Runtime
  * Release year
  * Minimum number of votes
* Sort results by rating and number of votes
* Display the top matching movies
* Analyze the relationship between IMDb ratings and number of votes
* Visualize movie genre distributions
* Visualize average movie ratings by year
* Find movies similar to a selected movie

## Technologies

* Python
* Pandas
* NumPy
* Matplotlib

## Dataset

This project uses the official IMDb datasets:

* `title.basics.tsv.gz`
* `title.ratings.tsv.gz`

The datasets can be downloaded from the IMDb datasets page:

https://developer.imdb.com/non-commercial-datasets/

The dataset files are **not included in this repository** because of their size and distribution considerations.

After downloading the datasets, place them inside the project's `data` directory:

```text
IMDb-Movie-Finder/
│
├── data/
│   ├── title.basics.tsv.gz
│   └── title.ratings.tsv.gz
│
├── main.py
├── MovieFinderFilter.py
├── RecommendationSystem.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/IMDb-Movie-Finder.git
cd IMDb-Movie-Finder
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Download the IMDb datasets and place them in the `data` folder.

## Usage

Run the main program:

```bash
python main.py
```

The program asks the user for several filtering criteria:

```text
Minimum IMDb rating:
Minimum runtime (minutes):
Maximum runtime (minutes):
Minimum year:
Genres(separate with ','):
```

For example:

```text
Minimum IMDb rating: 8
Minimum runtime (minutes): 90
Maximum runtime (minutes): 180
Minimum year: 2000
Genres(separate with ','): Action,Thriller
```

The program then displays movies matching the selected criteria.

After the filtering process, the user can enter a movie title to receive similar movie recommendations.

## Data Analysis

The project also performs several basic analyses on the IMDb data.

### Genre Distribution

The number of movies belonging to each genre is calculated and visualized using a horizontal bar chart.

### Rating and Vote Correlation

The project calculates the correlation between IMDb ratings and the number of votes.

```python
Movies[["averageRating", "numVotes"]].corr()
```

This helps investigate whether movies with more votes tend to have higher IMDb ratings.

### Average Rating by Year

The project calculates the average rating of movies for each release year after applying a minimum vote threshold.

This is visualized using a line chart.

## Project Structure

```text
IMDb-Movie-Finder/
│
├── main.py
│   └── Loads data, performs analysis and runs the movie finder
│
├── MovieFinderFilter.py
│   └── Contains the movie filtering functionality
│
├── RecommendationSystem.py
│   └── Contains the movie recommendation functionality
│
├── requirements.txt
│   └── Python dependencies
│
├── .gitignore
│   └── Files excluded from Git
│
└── README.md
    └── Project documentation
```

## Future Improvements

Possible future improvements include:

* Improve the recommendation algorithm
* Add more filtering options
* Add weighted IMDb ratings
* Build a graphical user interface
* Create a web interface
* Add content-based recommendation using movie genres and other features
* Experiment with machine learning recommendation models
* Add more detailed data visualizations

## Purpose

This project is primarily a learning project focused on improving practical Python and Pandas skills through a real-world dataset.

It provides a foundation for future work in **data analysis, recommendation systems, and machine learning**.

