import functools

from flask import (
    Blueprint,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.fa import get_provider, get_anilist_api

bp = Blueprint("/", __name__, url_prefix="/")


@bp.route("/")
@bp.route("watch")
def redirect_to_home():
    return redirect(url_for("/.home"))


@bp.route("home")
def home():
    anime_provider = get_provider()
    anilist_api = get_anilist_api()

    success, trending = anilist_api.get_trending()
    if not success:
        trending = {}

    success, recently_updated = anilist_api.get_most_recently_updated()
    if not success:
        recently_updated = {}
    return render_template(
        "/home.html", trending=trending, recentlyUpdated=recently_updated
    )


@bp.route("search")
def search_page():
    anime_provider = get_provider()
    anilist_api = get_anilist_api()
    search_term = request.args.get("q")
    s, search_results = anilist_api.search(query=search_term)
    if not s or not search_results:
        search_results = ""
    return render_template("/search.html", searchResults=search_results)


def anime_title_percentage_match(
    possible_user_requested_anime_title: str, anime
) -> float:
    """Returns the percentage match between the possible title and user title

    Args:
        possible_user_requested_anime_title (str): an Animdl search result title
        title (str): the anime title the user wants

    Returns:
        int: the percentage match
    """
    from fastanime.Utility.data import anime_normalizer
    from thefuzz import fuzz

    if normalized_anime_title := anime_normalizer.get(
        possible_user_requested_anime_title
    ):
        possible_user_requested_anime_title = normalized_anime_title
    # compares both the romaji and english names and gets highest Score
    title_a = str(anime["title"]["romaji"])
    title_b = str(anime["title"]["english"])
    percentage_ratio = max(
        fuzz.ratio(title_a.lower(), possible_user_requested_anime_title.lower()),
        fuzz.ratio(title_b.lower(), possible_user_requested_anime_title.lower()),
    )
    return percentage_ratio


@bp.route("watch/<int:animeId>")
def watch_anime(animeId: int):
    anime_provider = get_provider()
    anilist_api = get_anilist_api()
    success, anime_data = anilist_api.get_anime(animeId)

    if not success or not anime_data:
        return ""
    anime_info = anime_data["data"]["Page"]["media"][0]
    search_results = anime_provider.search_for_anime(
        anime_info["title"]["romaji"], "sub"
    )

    anime = {}
    if search_results:
        from fastanime.Utility.utils import anime_title_percentage_match

        _anime = max(
            search_results["results"],
            key=lambda anime: anime_title_percentage_match(anime["title"], anime_info),
        )
        anime = anime_provider.get_anime(_anime["id"])
        if not anime:
            anime = {}

    return render_template(
        "/watch.html",
        anime=anime,
        animeInfo=anime_info,
    )


@bp.route("anime")
def get_anime():
    id = request.args["id"]
    translation_type = request.args["translationType"]
    episode_number = request.args["episode"]
    anime_title = request.args["animeTitle"]
    anime_provider = get_provider()
    episode_streams = anime_provider.get_episode_streams(
        {"id": id, "title": anime_title}, episode_number, translation_type
    )
    streams = []
    if episode_streams:
        streams = [stream for stream in episode_streams]
    return streams
