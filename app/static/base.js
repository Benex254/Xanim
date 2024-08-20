const searchButton = document.getElementById("search-button");
const searchInput = document.getElementById("search-box");
//
// searchInput.addEventListener('', () => {
//   const searchTerm = searchInput.value;
//   const redirectUrl = 'https://your-search-page.com?q=' + encodeURIComponent(searchTerm);
//   window.location.href = redirectUrl;
// });
searchButton.addEventListener("click", () => {
  const searchTerm = searchInput.value;
  const redirectUrl = "/search?q=" + encodeURIComponent(searchTerm);
  window.location.href = redirectUrl;
});
