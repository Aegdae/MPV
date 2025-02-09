document.addEventListener("DOMContentLoaded", function () {
    const translations = {
        en: {
            registerText: "Don't have an account? <a href='{{ url_for('loginView.register') }}'>Sign up</a>",
            forgotText: "<a href='{{ url_for('loginView.forgot_password') }}'>Forgot password?</a>",
            errorMessage: "Incorrect email or password."
        },
        pt: {
            registerText: "Não tem uma conta? <a href='{{ url_for('loginView.register') }}'>Cadastre-se</a>",
            forgotText: "<a href='{{ url_for('loginView.forgot_password') }}'>Esqueceu a senha?</a>",
            errorMessage: "E-mail ou senha incorretos."
        }
    };

    function toggleDropdown() {
        const dropdown = document.getElementById("language-dropdown");
        dropdown.classList.toggle("active");
    }

    function changeLanguage(lang) {
        document.getElementById("register-text").innerHTML = translations[lang].registerText;
        document.getElementById("forgot-text").innerHTML = translations[lang].forgotText;

        const errorMessageElement = document.getElementById("error-message");
        if (errorMessageElement) {
            errorMessageElement.innerHTML = translations[lang].errorMessage;
        }

        const languageBtn = document.getElementById("language-btn");
        if (lang === 'pt') {
            languageBtn.innerText = "Português";
        } else {
            languageBtn.innerText = "English";
        }

        localStorage.setItem("language", lang);

        const dropdown = document.getElementById("language-dropdown");
        dropdown.classList.remove("active");
    }

    const savedLanguage = localStorage.getItem("language") || "pt";
    changeLanguage(savedLanguage);

    window.toggleDropdown = toggleDropdown;
    window.changeLanguage = changeLanguage;
});