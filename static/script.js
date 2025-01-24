function toggleLike(postId) {
    const likeButton = document.getElementById(`like-button-${postId}`);
    const likeIcon = document.getElementById(`like-icon-${postId}`);
    const likeCount = document.getElementById(`like-count-${postId}`);

    fetch(`/like_post/${postId}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.liked) {
                likeIcon.classList.add("liked");
                likeIcon.classList.remove("unliked");
            } else {
                likeIcon.classList.remove("liked");
                likeIcon.classList.add("unliked");
            }
            likeCount.textContent = data.likeCount;

            updatePostLikeState(postId, data.liked);
        })
        .catch(error => console.error("Erro ao atualizar curtidas:", error));
}

$(document).ready(function() {
    $('.post').each(function() {
        const postId = $(this).data('post-id');
        const isLiked = $(this).data('liked');
        const likeIcon = document.getElementById(`like-icon-${postId}`);

        if (isLiked) {
            likeIcon.classList.add("liked");
            likeIcon.classList.remove("unliked");
        } else {
            likeIcon.classList.remove("liked");
            likeIcon.classList.add("unliked");
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const followButtons = document.querySelectorAll('.follow');

    followButtons.forEach(button => {
        button.addEventListener('click', () => {
            const userId = button.getAttribute('data-user-id');
            const isActive = button.classList.contains('active');

            fetch(`/follow_unfollow/${userId}`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        button.classList.toggle('active');
                        button.textContent = data.isFollowing ? 'Seguindo' : 'Seguir';
                    } else {
                        console.error('Erro ao seguir/desseguir');
                    }
                })
                .catch(error => console.error('Erro na requisição:', error));
        });
    });
});





document.addEventListener('DOMContentLoaded', () => {
    const toggleThemeBtn = document.getElementById('toggle-theme');
    const themeIcon = document.getElementById('theme-icon');
    const body = document.body;

    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.classList.add(savedTheme);
        themeIcon.className = savedTheme === 'dark-mode' ? 'fas fa-sun': 'fas fa-moon';
    } else {
        themeIcon.className = 'fas fa-moon';
    }

    toggleThemeBtn.addEventListener('click', () => {
        body.classList.toggle('dark-mode');

        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('theme', 'dark-mode');
            themeIcon.className = 'fas fa-sun';
        } else {
            localStorage.removeItem('theme');
            themeIcon.className = 'fas fa-moon';
        }
    });
});