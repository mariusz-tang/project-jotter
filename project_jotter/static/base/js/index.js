const storage = window.localStorage;

function updateTheme() {
    let theme = "light";
    if (storage.themeSetting == "dark" || (storage.themeSetting != "light" && themeQuery.matches))
        theme = "dark";
    document.documentElement.dataset.theme = theme;
}

function setThemeSetting(setting) {
    storage.themeSetting = setting;
    updateTheme()
}

const themeQuery = window.matchMedia('(prefers-color-scheme: dark)');
themeQuery.addEventListener('change', updateTheme);
updateTheme()
