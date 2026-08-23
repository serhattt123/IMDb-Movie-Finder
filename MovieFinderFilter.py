def filter_movies(
    movies,
    min_rating=None,
    genre=None,
    min_runtime=None,
    max_runtime=None,
    min_year=None,
    numVotes=None
):

    filtered = movies[movies['numVotes'] >= 24000].copy()

    if min_rating is not None:
        filtered = filtered[
            filtered["averageRating"] >= min_rating
        ]

    if genre is not None:
        genres = [genre] if isinstance(genre, str) else genre
        for selected_genre in genres:
            filtered = filtered[
                filtered["genres"].str.contains(
                    selected_genre,
                    case=False,
                    na=False,
                    regex=False,
                )
            ]

    if min_runtime is not None:
        filtered = filtered[
            filtered["runtimeMinutes"] >= min_runtime
        ]

    if max_runtime is not None:
        filtered = filtered[
            filtered["runtimeMinutes"] <= max_runtime
        ]

    if min_year is not None:
        filtered = filtered[
            filtered["startYear"] >= min_year
        ]

    return filtered
