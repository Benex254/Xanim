from fastanime.AnimeProvider import AnimeProvider
from fastanime.anilist import AniListApi
from flask import current_app, g


def get_provider():
    if "anime_provider" not in g:
        g.anime_provider = AnimeProvider(current_app.config["DEFAULT_PROVIDER"])

    return g.anime_provider


def get_anilist_api():
    if "anilist" not in g:
        g.anilist = AniListApi()

    return g.anilist
