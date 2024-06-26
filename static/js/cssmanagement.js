function autoResize(textarea) {
    textarea.style.height = 'auto'; // Reset height to auto
    textarea.style.height = textarea.scrollHeight + 'px'; // Set height based on content
}
if (window.location.href.endsWith('edit_post.html')) {
    autoResize(textareaElement);
}

// Add event listener for new posts
document.addEventListener('DOMContentLoaded', function () {
    autoResize(textareaElement);
})
document.addEventListener('DOMContentLoaded', function () {
    const basliklar = document.querySelectorAll('.baslik');
    basliklar.forEach(function (baslik) {
        const baslikMetni = baslik.innerText;
        const baslikUzunlugu =  -80 + baslikMetni.length;
        baslik.style.setProperty('left', baslikUzunlugu + 'px');
    });
});
