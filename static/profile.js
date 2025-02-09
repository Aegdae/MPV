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


document.addEventListener("DOMContentLoaded", function () {
    const editButton = document.getElementById("edit-profile-button");
    const editMenu = document.getElementById("edit-profile-menu");
    const form = document.getElementById("edit-profile-form");

    editButton.addEventListener("click", function () {
        editMenu.classList.toggle("hidden");
    });


    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = {
            user_account: document.getElementById("user_account").value.trim(),
            user_name: document.getElementById("user_name").value.trim(),
            bio: document.getElementById("bio").value.trim(),
        };

        fetch(form.action, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById("display-user-account").textContent = data.user_account;
                editMenu.classList.add("hidden");
                
                window.location.reload()
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error("Erro:", error));
    });

    document.addEventListener("click", function (event) {
        if (!editMenu.contains(event.target) && event.target !== editButton) {
            editMenu.classList.add("hidden");
        }
    });
});




document.addEventListener("DOMContentLoaded", function () {
    const translations = {
        en: {
            home: "Home",
            profile: "Profile",
            settings: "Settings",
            logout: "Logout",
            theme: "Theme",
            themeLabel: "Dark Mode",
            editProfile: "Edit Profile",
            save: "Save",
            usernamePlaceholder: "Username",
            namePlaceholder: "Name",
            bioPlaceholder: "Bio",
            posts: "Posts",
            followers: "Followers",
            following: "Following",
            follow: "Follow",
            followingText: "Following",
            noPosts: "This user hasn't posted anything yet.",
            more: "More",
            language: "Language",
            chooseLanguage: "Choose the language"
        },
        pt: {
            home: "Página Inicial",
            profile: "Perfil",
            settings: "Configurações",
            logout: "Sair",
            theme: "Tema",
            themeLabel: "Modo Escuro",
            editProfile: "Editar Perfil",
            save: "Salvar",
            usernamePlaceholder: "Usuário",
            namePlaceholder: "Nome",
            bioPlaceholder: "Bio",
            posts: "Posts",
            followers: "Seguidores",
            following: "Seguindo",
            follow: "Seguir",
            followingText: "Seguindo",
            noPosts: "Este usuário ainda não publicou nada.",
            more: "Mais",
            language: "Idioma",
            chooseLanguage: "Escolha o idioma:"
        }
    };

    function changeLanguage(lang) {
        document.querySelector("#home-link").textContent = translations[lang].home;
        document.querySelector("#profile-link").textContent = translations[lang].profile;
        document.querySelector("#menu-toggle").textContent = translations[lang].more;
        document.querySelector("#theme-toggle").textContent = translations[lang].theme;
        document.querySelector("#theme-label").textContent = translations[lang].themeLabel;
        document.querySelector("#settings-toggle").textContent = translations[lang].settings;
        document.querySelector("#logout-link").textContent = translations[lang].logout;
        document.querySelector("#edit-profile-button").textContent = translations[lang].editProfile;
        document.querySelector("#display-user-account").placeholder = translations[lang].usernamePlaceholder;
        document.querySelector("#user_name").placeholder = translations[lang].namePlaceholder;
        document.querySelector("#bio").placeholder = translations[lang].bioPlaceholder;
        document.querySelector("#num-posts").textContent = translations[lang].posts + ":";
        document.querySelector("#followers").textContent = translations[lang].followers + ":";
        document.querySelector("#following").textContent = translations[lang].following + ":";
        document.querySelector("#language-toggle").textContent = translations[lang].language
        document.querySelector("#language-span").textContent = translations[lang].language
        document.querySelector("#language-label").textContent = translations[lang].chooseLanguage
        document.querySelector("#save-edit-profile").textContent = translations[lang].save
        
        const followButton = document.querySelector(".follow");
        if (followButton) {
            followButton.textContent = followButton.textContent.trim() === "Seguindo" || followButton.textContent.trim() === "Following"
                ? translations[lang].followingText
                : translations[lang].follow;
        }

        const noPostsMessage = document.querySelector(".feed-user > p");
        if (noPostsMessage && noPostsMessage.textContent.includes("Este usuário ainda não publicou nada")) {
            noPostsMessage.textContent = translations[lang].noPosts;
        }
    }

    const savedLanguage = localStorage.getItem("language") || "pt";
    changeLanguage(savedLanguage);

    let languageSelector = document.getElementById("language-selector");
    if (!languageSelector) {
        languageSelector = document.createElement("select");
        languageSelector.id = "language-selector";
        languageSelector.innerHTML = ` <option value="pt">Português</option> <option value="en">English</option> `;
        languageSelector.style.marginLeft = "10px";
        
        const nav = document.querySelector(".nav");
        if (nav) {
            nav.appendChild(languageSelector);
        }
    }

    languageSelector.value = savedLanguage;

    languageSelector.addEventListener("change", function (event) {
        const selectedLanguage = event.target.value;
        changeLanguage(selectedLanguage);
        localStorage.setItem("language", selectedLanguage);
    });
});