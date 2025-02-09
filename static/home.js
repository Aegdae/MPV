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


document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menu-toggle");
    const mainSubmenu = document.getElementById("main-submenu");
    const themeToggle = document.getElementById("theme-toggle");
    const themeSubmenu = document.getElementById("theme-submenu");
    const backToThemeMenu = document.getElementById("back-to-theme-menu");
    const languageToggle = document.getElementById("language-toggle");
    const languageSubmenu = document.getElementById("language-submenu");
    const backToLanguageMenu = document.getElementById("back-to-language-menu");

    menuToggle.addEventListener("click", function (event) {
        event.preventDefault();
        mainSubmenu.classList.toggle("active");
        themeSubmenu.classList.remove("active");
        languageSubmenu.classList.remove("active");
    });

    themeToggle.addEventListener("click", function (event) {
        event.preventDefault();
        mainSubmenu.classList.remove("active");
        themeSubmenu.classList.add("active");
    });

    languageToggle.addEventListener("click", function (event) {
        event.preventDefault();
        mainSubmenu.classList.remove("active");
        languageSubmenu.classList.add("active");
    });

    backToThemeMenu.addEventListener("click", function (event) {
        event.preventDefault();
        themeSubmenu.classList.remove("active");
        mainSubmenu.classList.add("active");
    });

    backToLanguageMenu.addEventListener("click", function (event) {
        event.preventDefault();
        languageSubmenu.classList.remove("active");
        mainSubmenu.classList.add("active");
    });

    document.addEventListener("click", function (event) {
        if (!menuToggle.contains(event.target) &&
            !mainSubmenu.contains(event.target) &&
            !themeSubmenu.contains(event.target) &&
            !languageSubmenu.contains(event.target)) {
            mainSubmenu.classList.remove("active");
            themeSubmenu.classList.remove("active");
            languageSubmenu.classList.remove("active");
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



document.addEventListener("DOMContentLoaded", function () {
    const contentToggle = document.getElementById("content-toggle");
    const contentSubmenu = document.getElementById("content-submenu");

    if (contentToggle) {
        contentToggle.addEventListener("click", function (event) {
            event.preventDefault();
            contentSubmenu.classList.toggle("active");
        });
    }

    document.addEventListener("click", function (event) {
        if (!contentSubmenu.contains(event.target) && !contentToggle.contains(event.target)) {
            contentSubmenu.classList.remove("active");
        }
    });

    const deleteLink = document.querySelector("#delete-button");

    if (deleteLink) {
        deleteLink.addEventListener("click", function (event) {
            event.preventDefault();  
            event.stopPropagation(); 
            const postId = deleteLink.getAttribute("data-post-id");
            if (confirm("Tem certeza que deseja excluir esta postagem?")) {
                fetch(`/delete_post/${postId}`, { method: "DELETE" })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            const postElement = document.getElementById(`post-${postId}`);
                            if (postElement) {
                                postElement.remove();
                            }
                            location.reload();
                        } else {
                            alert(data.message);
                        }
                    })
                    .catch(error => console.error("Erro ao excluir postagem:", error));
            }
        });
    }
});



document.addEventListener("DOMContentLoaded", function () {
    const translations = {
        en: {
            homeLink: "Home",
            profileLink: "Profile",
            settingsLink: "Settings",
            logoutLink: "Logout",
            forYouText: "For you",
            postPlaceholder: "What are you thinking?",
            tweetButton: "Post",
            themeToggle: "Theme",
            languageLabel: "Language",
            deleteText: "Delete",
            darkModeText: "Dark Mode",
            more: "More",
            language: "Language",
            chooseLanguage: "Choose the language",
            edit: "Edit"
        },
        pt: {
            homeLink: "Página Inicial",
            profileLink: "Perfil",
            settingsLink: "Configurações",
            logoutLink: "Sair",
            forYouText: "Para você",
            postPlaceholder: "Escreva o que você está pensando...",
            tweetButton: "Postar",
            themeToggle: "Tema",
            languageLabel: "Idioma",
            deleteText: "Apagar",
            darkModeText: "Modo Escuro",
            more: "Mais",
            language: "Idioma",
            chooseLanguage: "Escolha o idioma:",
            edit: "Editar"
        }
    };

    function changeLanguage(lang) {
        document.getElementById("home-link").textContent = translations[lang].homeLink;
        document.getElementById("profile-link").textContent = translations[lang].profileLink;
        document.getElementById("settings-toggle").textContent = translations[lang].settingsLink;
        document.getElementById("logout-link").textContent = translations[lang].logoutLink;
        document.getElementById("for-you-text").textContent = translations[lang].forYouText;
        document.getElementById("post-placeholder").placeholder = translations[lang].postPlaceholder;
        document.getElementById("tweet-button").textContent = translations[lang].tweetButton;
        document.getElementById("theme-toggle").textContent = translations[lang].themeToggle;
        document.getElementById("theme-label").textContent = translations[lang].darkModeText;
        document.querySelector("#menu-toggle").textContent = translations[lang].more
        document.querySelector("#language-toggle").textContent = translations[lang].language
        document.querySelector("#language-span").textContent = translations[lang].language
        document.querySelector("#language-label").textContent = translations[lang].chooseLanguage
        document.querySelector("#edit-button").textContent = translations[lang].edit

        const deleteButtons = document.querySelectorAll("#delete-button");
        deleteButtons.forEach(button => {
            button.textContent = translations[lang].deleteText;
        });
    }

    const savedLanguage = localStorage.getItem("language") || "pt";
    changeLanguage(savedLanguage);

    const languageSelector = document.getElementById("language-selector");
    languageSelector.value = savedLanguage;
    

    languageSelector.addEventListener("change", function (event) {
        const selectedLanguage = event.target.value;
        changeLanguage(selectedLanguage);
        localStorage.setItem("language", selectedLanguage);
    });
});





document.addEventListener("DOMContentLoaded", function () {
    const editButtons = document.querySelectorAll('.button-edit');
    
    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            const postId = this.getAttribute('data-post-id');

            // Esconde o conteúdo do post
            const postContent = document.getElementById(`content-${postId}`);
            if (postContent) {
                postContent.classList.add('hidden'); // Esconde o conteúdo do post
            }

            // Exibe o textarea de edição (no mesmo lugar do conteúdo original)
            const editContainer = document.getElementById(`post-container-${postId}`);
            if (editContainer) {
                editContainer.classList.remove('hidden'); // Mostra o container de edição
            }

            // Esconde o botão de editar
            const editButton = document.getElementById(`edit-button-${postId}`);
            if (editButton) {
                editButton.classList.add('hidden'); // Esconde o botão de editar
            }

            // Exibe os botões de salvar e cancelar
            const saveButton = document.getElementById(`save-button-${postId}`);
            if (saveButton) {
                saveButton.classList.remove('hidden'); // Mostra o botão de salvar
            }

            const cancelButton = document.getElementById(`cancel-button-${postId}`);
            if (cancelButton) {
                cancelButton.classList.remove('hidden'); // Mostra o botão de cancelar
            }
        });
    });
});

function cancelEdit(postId) {
    const editContainer = document.getElementById(`post-container-${postId}`);
    if (editContainer) {
        editContainer.classList.add('hidden');
    }

    const postContent = document.getElementById(`content-${postId}`);
    if (postContent) {
        postContent.classList.remove('hidden');
    }

    const saveButton = document.getElementById(`save-button-${postId}`);
    if (saveButton) {
        saveButton.classList.add('hidden');
    }

    const cancelButton = document.getElementById(`cancel-button-${postId}`);
    if (cancelButton) {
        cancelButton.classList.add('hidden');
    }

    const editButton = document.getElementById(`edit-button-${postId}`);
    if (editButton) {
        editButton.classList.remove('hidden');
    }
}