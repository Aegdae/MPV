function toggleLike(postId) {
    fetch(`/like_post/${postId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Erro:', data.error);
            return;
        }

        const likeCount = document.getElementById(`like-count-${postId}`);
        if (likeCount) {
            likeCount.textContent = data.likeCount;
        }

        const likeIcon = document.getElementById(`like-icon-${postId}`);
        if (likeIcon) {
            if (data.liked) {
                likeIcon.classList.add('liked');
                likeIcon.classList.remove('unliked');
            } else {
                likeIcon.classList.add('unliked');
                likeIcon.classList.remove('liked');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".post").forEach(post => {
        const postId = post.dataset.postId;
        const isLiked = post.dataset.liked === "true";
        const likeIcon = document.getElementById(`like-icon-${postId}`);

        if (likeIcon) {
            likeIcon.classList.toggle("liked", isLiked);
            likeIcon.classList.toggle("unliked", !isLiked);
        }
    });
});


document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".follow").forEach(button => {
        button.addEventListener("click", () => {
            const userId = button.getAttribute("data-user-id");
            const isActive = button.classList.contains("active");

            button.disabled = true;

            fetch(`/follow_unfollow/${userId}`, { method: "POST" })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        button.classList.toggle("active");
                        button.textContent = data.isFollowing ? "Seguindo" : "Seguir";
                    } else {
                        console.error("Erro ao seguir/desseguir");
                    }
                })
                .catch(error => console.error("Erro na requisição:", error))
                .finally(() => {
                    button.disabled = false;
                });
        });
    });
});


document.addEventListener("DOMContentLoaded", () => {
    const toggleThemeBtn = document.getElementById("toggle-theme");
    const themeIcon = document.getElementById("theme-icon");
    const body = document.body;

    const savedTheme = localStorage.getItem("theme") || "light";

    body.classList.toggle("dark-mode", savedTheme === "dark");
    themeIcon.classList.add(savedTheme === "dark" ? "fa-sun" : "fa-moon");

    toggleThemeBtn.addEventListener("click", () => {
        const isDark = body.classList.toggle("dark-mode");

        localStorage.setItem("theme", isDark ? "dark" : "light");

        themeIcon.classList.toggle("fa-sun", isDark);
        themeIcon.classList.toggle("fa-moon", !isDark);
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const textArea = document.querySelector('.text');
    
    if (!textArea.value.trim()) {
        textArea.value = '';
    }
});
