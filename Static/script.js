function toggleLike(postId) {
    const likeButton = document.getElementById(`like-button-${postId}`);
    const likeIcon = document.getElementById(`like-icon-${postId}`);
    const likeCount = document.getElementById(`like-count-${postId}`);

    fetch(`/like_post/${postId}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            // Alterar o ícone da curtida
            if (data.liked) {
                likeIcon.classList.add("liked");
                likeIcon.classList.remove("unliked");
            } else {
                likeIcon.classList.remove("liked");
                likeIcon.classList.add("unliked");
            }
            // Atualizar a contagem de curtidas
            likeCount.textContent = data.likeCount;

            // Atualizar os posts nas outras páginas
            updatePostLikeState(postId, data.liked);
        })
        .catch(error => console.error("Erro ao atualizar curtidas:", error));
}



$(document).ready(function() {
    // Itera sobre todos os posts para garantir que os estados iniciais de curtidas sejam corretos
    $('.post').each(function() {
        const postId = $(this).data('post-id'); // Assumindo que cada post tem um data-post-id
        const isLiked = $(this).data('liked'); // Se o post já foi curtido

        const likeIcon = document.getElementById(`like-icon-${postId}`);

        // Se o post foi curtido, marca o ícone de "curtido"
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

            // Enviar requisição ao servidor para seguir ou deixar de seguir
            fetch(`/follow_unfollow/${userId}`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    // Verificar o estado após a resposta
                    if (data.success) {
                        // Alternar o estado do botão
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


const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

fetch('/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({ username: 'user', password: 'pass' })
});