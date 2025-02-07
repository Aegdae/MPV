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


document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menu-toggle");
    const mainSubmenu = document.getElementById("main-submenu");
    const themeToggle = document.getElementById("theme-toggle");
    const themeSubmenu = document.getElementById("theme-submenu");
    const backToMenu = document.getElementById("back-to-menu");


    menuToggle.addEventListener("click", function (event) {
        event.preventDefault();
        mainSubmenu.classList.toggle("active");
        themeSubmenu.classList.remove("active");
    });


    themeToggle.addEventListener("click", function (event) {
        event.preventDefault();
        mainSubmenu.classList.remove("active");
        themeSubmenu.classList.add("active");
    });


    backToMenu.addEventListener("click", function (event) {
        event.preventDefault();
        themeSubmenu.classList.remove("active");
        mainSubmenu.classList.add("active");
    });


    document.addEventListener("click", function (event) {
        if (!menuToggle.contains(event.target) && 
            !mainSubmenu.contains(event.target) && 
            !themeSubmenu.contains(event.target)) {
            mainSubmenu.classList.remove("active");
            themeSubmenu.classList.remove("active");
        }
    });


    const themeSwitcher = document.getElementById('theme-switcher');
    const savedTheme = localStorage.getItem('theme') || 'light';


    document.documentElement.classList.add(savedTheme === 'dark' ? 'dark-mode' : 'light-mode');
    themeSwitcher.checked = savedTheme === 'dark';


    themeSwitcher.addEventListener('change', () => {
        const theme = themeSwitcher.checked ? 'dark' : 'light';
        document.documentElement.classList.toggle('dark-mode', theme === 'dark');
        document.documentElement.classList.toggle('light-mode', theme === 'light');
        localStorage.setItem('theme', theme);
    });

});


document.addEventListener('DOMContentLoaded', function () {
    const textArea = document.querySelector('.text');
    
    if (!textArea.value.trim()) {
        textArea.value = '';
    }
});