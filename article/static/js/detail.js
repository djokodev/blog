function copyArticleUrl() {
    var articleUrlInput = document.getElementById("articleUrl");
    articleUrlInput.select();
    document.execCommand("copy");
    alert("Lien copié !");
    var containerShare = document.getElementById("container-share");
    containerShare.classList.add("hidden");
}

document.querySelector('.icon-right').addEventListener('click', function(e) {
    e.stopPropagation()
    e.preventDefault()
    var containerShare = document.getElementById("container-share");
    containerShare.classList.remove("hidden");
});
