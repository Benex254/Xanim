let episodeNumber = 0;
let translationType = "sub";
let currentAnimeId = 0;
let currentTitle = "";
const player = document.getElementById("player");
const videoPlayer = videojs(player);

document.addEventListener("DOMContentLoaded", function () {
  const options = {};
  var elems = document.querySelectorAll(".dropdown-trigger");
  var instances = M.Dropdown.init(elems, options);
});
function loadEpisode(animeId, animeTitle, episode = null, translation = null) {
  currentTitle = animeTitle;
  currentAnimeId = animeId;
  if (!episode) {
    episode = episodeNumber + 1;
    episodeNumber = episode;
  } else {
    episodeNumber = parseInt(episode);
  }
  if (!translation) {
    translation = translationType;
  } else {
    translationType = translation;
  }

  const params = {
    id: animeId,
    episode,
    translationType: translation,
    animeTitle,
  };

  const queryString = new URLSearchParams(params);
  fetch(`/anime?${queryString}`)
    .then((response) => response.json())
    .then((data) => {
      const sources = [];

      let servers = "";
      // Get a reference to the video element
      data.forEach((animeServer) => {
        const link = animeServer.links[0]["link"];
        if (animeServer.server != "Yt") {
          sources.push(link);
          servers += `<li class="server" data-value="${link}"><a>${animeServer.server}</a></li>`;
        }
      });
      let type = "";
      const link = sources.reverse()[0];
      if (link.includes("m3u8")) {
        type = "application/x-mpegURL";
      } else {
        type = "video/mp4";
      }
      document.getElementById("servers").innerHTML = servers;
      const newSource = {
        src: link,
        type: type,
      };
      player.title = data[0].episode_title;
      videoPlayer.src(newSource);
      videoPlayer.play();
      document.querySelectorAll(".server").forEach(function (item) {
        item.addEventListener("click", function () {
          videoPlayer = videojs(document.getElementById("player"));
          const url = item.getAttribute("data-value");
          let type = "";
          if (item.textContent == "sharepoint") {
            type = "video/mp4";
          } else {
            type = "application/x-mpegURL";
          }
          videoPlayer.src({
            src: url,
            type: type,
          });
          videoPlayer.play();
        });
      });
    })
    .catch((error) => console.error("Error:", error));
}
function nextEpisode(animeId, animeTitle) {
  episode = episodeNumber + 1;
  loadEpisode(animeId, animeTitle, episode);
}
function prevEpisode(animeId, animeTitle) {
  episode = episodeNumber - 1;
  loadEpisode(animeId, animeTitle, episode);
}
videoPlayer.on("ended", function () {
  nextEpisode(currentAnimeId, currentTitle);
  // Your custom logic here, e.g., play next video, show a message, etc.
});
