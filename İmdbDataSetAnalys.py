import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from MovieFinderFilter import filter_movies
from RecommendationSystem import recommend_movies

from pathlib import Path

DATA_DIR = Path("data")

basics = pd.read_csv(
    DATA_DIR / "title.basics.tsv.gz",
    sep="\t",
    na_values="\\N"
)

ratings = pd.read_csv(
    DATA_DIR / "title.ratings.tsv.gz",
    sep="\t",
    na_values="\\N"
)

Crew = pd.read_csv(
    DATA_DIR / "title.crew.tsv.gz",
    sep="\t",
    na_values="\\N"
)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# print(basics.info())
# print(ratings.info())

basics['runtimeMinutes'] = pd.to_numeric(
    basics['runtimeMinutes'], errors='coerce').astype('Int64')

# print(basics.describe())
# print(ratings.describe())

# tconst is the unique key identifier for each title in the IMDb dataset. It is used to link the basics and ratings datasets together.

# print(basics["primaryTitle"].isna().sum()) #There are 25 NaN title
basics = basics.dropna(subset=["primaryTitle"])


# print('Number of Film with double tconst ' + str(basics["tconst"].duplicated().sum()))  # There are no dublicated tconst

# print('Title Types: ', basics["titleType"].unique())

# print(ratings.isna().sum()) #There is no NaN data in ratings

CombineData = basics.merge(ratings, on="tconst")  # merge the datasets
CombineData = CombineData.merge(Crew, on="tconst")

# print(basics["titleType"].value_counts(normalize=True) * 100)

Movies = CombineData[CombineData["titleType"] == "movie"].copy()

# print(Movies["startYear"].value_counts().sort_index())


print(Movies.sort_values("runtimeMinutes", ascending=False)[
    ["primaryTitle", "runtimeMinutes"]
])

Movies = Movies.dropna(subset=["runtimeMinutes"])
print(Movies.info())

genres_Movies = Movies['genres'].str.split(',')
genre_counts = genres_Movies.explode().value_counts().sort_index()

axes[0].barh(genre_counts.index, genre_counts.values, color="#CA850F")
axes[0].set_title('Genres')

# print(Movies.sort_values("averageRating", ascending=False).head(20)) #We need to give attention to number of Vote.

print('Correlation percentage between Rate and Number of Vote: ' +
      str(Movies[["averageRating", "numVotes"]].corr().iloc[0, 1]*100))

Movies_with_Acceptable_Vote = Movies[Movies['numVotes'] >= 24000]
print(Movies_with_Acceptable_Vote.sort_values(
    "averageRating", ascending=False).head(20)[['originalTitle', 'averageRating', 'numVotes']])

# print(Movies_with_Acceptable_Vote.groupby("startYear")["averageRating"].mean().sort_values(ascending=False))

avg_rating_by_year = Movies_with_Acceptable_Vote.groupby(
    "startYear")["averageRating"].mean()
avg_rating_by_year_sorted = avg_rating_by_year.sort_index()
axes[1].plot(avg_rating_by_year_sorted.index,
             avg_rating_by_year_sorted.values, color="#CA850F")
axes[1].set_title('Average Rating by Year')
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Average Rating')
axes[1].grid(True)

min_rating = float(input("Minimum IMDb rating: "))

min_runtime = int(input("Minimum runtime (minutes): "))
max_runtime = int(input("Maximum runtime (minutes): "))

min_year = int(input("Minimum year: "))

genre = input("Genres(separate with ','): ")
genre = genre.split(',')
genre = [g.strip() for g in genre]


filtered_movies = filter_movies(
    Movies,
    min_rating=min_rating,
    genre=genre,
    min_runtime=min_runtime,
    max_runtime=max_runtime,
    min_year=min_year,
    numVotes=25000,
)

filtered_movies = filtered_movies.sort_values(
    by=["averageRating", "numVotes"],
    ascending=[False, False]
)

print("\n--- RESULTS ---")

if filtered_movies.empty:
    print("No movies have found.")

else:
    print(
        filtered_movies[
            ["originalTitle", "genres", "averageRating",
             "numVotes", "runtimeMinutes", "startYear"]
        ].head(20).to_string(index=False)
    )


while True:
    movie_name = input("Write a movie for similar recommendations (press Enter to quit): ").strip()

    if not movie_name:
        break

    recommendations = recommend_movies(Movies, movie_name, top_n=10)

    if recommendations.empty:
        print("Couldnt Find a Match.")
    else:
        print("\n--- Recommendations ---")
        print(recommendations.to_string(index=False))


plt.show()

