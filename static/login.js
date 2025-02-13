document.addEventListener("DOMContentLoaded", function () {

    const urls = {
        registerUrl: "/register",
        forgotPasswordUrl: "/forgot_password"
    };

    const translations = {
        en: {
            registerText: `Don't have an account? <a href="${urls.registerUrl}">Sign up</a>`,
            forgotText: `<a href="${urls.forgotPasswordUrl}">Forgot password?</a>`,
            errorMessage: "Incorrect email or password."
        },
        pt: {
            registerText: `Não tem uma conta? <a href="${urls.registerUrl}">Cadastre-se</a>`,
            forgotText: `<a href="${urls.forgotPasswordUrl}">Esqueceu a senha?</a>`,
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