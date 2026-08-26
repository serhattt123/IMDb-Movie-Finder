"""
Content based movie recommendation function for the IMDb project.
Given a movie title, finds similar movies based on:
    1) genre overlap   
    2) IMDb rating closeness
    3) release year closeness
    4) Crew of the movie
"""

import numpy as np
import pandas as pd


def genre_string_set(genre_set):
    if pd.isna(genre_set):
        return set()
    else:
        return set(g.strip() for g in genre_set.split(','))


def jaccard_similarity(set_a, set_b):
    """
    Jaccard similarity between two sets:
    size of the overlap, divided by the size of everything combined
    """
    if not set_a and not set_b:
        return 0.0
    else:
        intersection = len(set_a & set_b)
        union = len(set_a | set_b)
        return intersection / union


def crew_id_set(directors_string, writers_string):
    """
    Combine director + writer ids into a single set.
    """
    ids = set()
    for s in (directors_string, writers_string):
        if not pd.isna(s):
            ids.update(x.strip() for x in s.split(','))
    return ids


def recommend_movies(movies_df, title, top_n=10,
                     genre_weight=0.45, rating_weight=0.35, year_weight=0.05,
                     crew_weight=0.15, year_decay=15, min_votes=1000):
    matches = movies_df[
        movies_df['primaryTitle'].str.lower() == title.strip().lower()]

    if matches.empty:

        # fallback in case of a typo or a shortened title
        matches = movies_df[
            movies_df['primaryTitle'].str.lower().str.contains(
                title.strip().lower(), na=False)]

    if matches.empty:
        print(f"'{title}' couldnt find a match.")
        return pd.DataFrame()
    if len(matches) > 1:
        # same title can belong to multiple movies
        # picks the one with the most votes, it's probably the one meant
        target = matches.sort_values("numVotes", ascending=False).iloc[0]
        print(f"There are more than one movies named '{title}', the one with the most votes have chosen: "
              f"{target['primaryTitle']} ({target['startYear']})")

    else:
        target = matches.iloc[0]

    target_genres = genre_string_set(target['genres'])
    target_rating = target['averageRating']
    target_year = target['startYear']

    candidates = movies_df[movies_df['tconst'] != target['tconst']].copy()
    candidates = candidates[candidates['numVotes'] >= 10000]

    candidate_genre_sets = candidates['genres'].apply(genre_string_set)
    candidates['genre_sim'] = candidate_genre_sets.apply(
        lambda g: jaccard_similarity(target_genres, g))

# keep only movies that share at least one genre.
    candidates = candidates[candidates['genre_sim'] > 0]

    candidates['rating_sim'] = 1 - \
        (target_rating - candidates['averageRating']).abs() / 10

    year_diff = (target_year - candidates['startYear']).abs()
    candidates['year_sim'] = np.exp(-year_diff / year_decay)

    target_crew = crew_id_set(target['directors'], target['writers'])

    candidate_crew_sets = candidates.apply(
        lambda row: crew_id_set(row['directors'], row['writers']), axis=1)
    candidates['crew_sim'] = candidate_crew_sets.apply(
        lambda c: jaccard_similarity(target_crew, c))


# combine into one score
    candidates['score'] = (
        genre_weight * candidates['genre_sim'] +
        rating_weight * candidates['rating_sim'] +
        year_weight * candidates['year_sim'] +
        crew_weight * candidates['crew_sim']
    )

    result = candidates.sort_values(
        by=['score', 'numVotes'], ascending=[False, False]
    ).head(top_n)

    return result[[
        'primaryTitle', 'genres', 'averageRating', 'startYear',
        'numVotes', 'genre_sim', 'rating_sim', 'year_sim', 'score'
    ]]

