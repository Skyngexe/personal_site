(() => {
    const root = document.documentElement;
    const theme = document.getElementById('themeToggle');
    function updateTheme(value) {
        root.dataset.theme = value;
        theme.setAttribute('aria-label', value === 'dark' ? 'Switch to daylight' : 'Switch to dusk');
    }
    updateTheme(root.dataset.theme || 'light');
    theme.addEventListener('click', () => {
        updateTheme(root.dataset.theme === 'dark' ? 'light' : 'dark');
        localStorage.setItem('theme', root.dataset.theme);
    });

    // Bookmarks from the single-page edition still lead to their original sections.
    if (location.pathname.endsWith('/work.html') && location.hash === '#experience') {
        location.replace('experience.html#experience');
    }
    if (document.querySelector('.cover')) {
        const routes = { writing: 'writing', research: 'work', projects: 'work', experience: 'experience',
            about: 'about', interests: 'about', skills: 'about', contact: 'about' };
        const section = location.hash.slice(1);
        if (Object.hasOwn(routes, section)) location.replace(routes[section] + '.html#' + section);
    }

    const filters = Array.from(document.querySelectorAll('.category-link'));
    const entries = document.querySelectorAll('#writing article[data-category]');
    filters.forEach(filter => {
        filter.href = filter.dataset.page;
        filter.setAttribute('aria-pressed', 'false');
        filter.setAttribute('role', 'button');
        filter.addEventListener('keydown', event => {
            if (event.key === ' ') { event.preventDefault(); filter.click(); }
        });
        filter.addEventListener('click', event => {
            if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
            event.preventDefault();
            const active = filter.getAttribute('aria-pressed') === 'false';
            filters.forEach(item => item.setAttribute('aria-pressed', String(active && item === filter)));
            entries.forEach(entry => { entry.hidden = active && entry.dataset.category !== filter.dataset.category; });
        });
    });
})();
