(() => {
    const canvas = document.querySelector('.study canvas');
    const control = document.querySelector('.motion-toggle');
    const context = canvas.getContext('2d');
    if (!context) return;

    const nightPainting = document.querySelector('.study-night');
    const root = document.documentElement;
    const motion = matchMedia('(prefers-reduced-motion: reduce)');
    let width = 0;
    let height = 0;
    let time = 0;
    let frame = 0;
    let lastPaint = 0;
    let visible = false;
    let paused = false;

    const tram = new Image();
    tram.onload = paint;
    tram.src = 'tram.png';

    function drawTram(night) {
        if (!tram.naturalWidth) return;
        context.save();
        context.scale(960 / 1214, 1024 / 1295);
        // The window jambs and the writer's silhouette are in front of the track.
        context.beginPath();
        context.rect(275, 385, 586, 220);
        context.moveTo(382, 604);
        context.lineTo(363, 561);
        context.bezierCurveTo(350, 506, 394, 453, 443, 455);
        context.bezierCurveTo(492, 454, 521, 479, 526, 528);
        context.lineTo(521, 604);
        context.closePath();
        context.clip('evenodd');
        const x = 50 + (410 + time * 47) % 860;
        context.filter = `brightness(${1 - .32 * night})`;
        context.drawImage(tram, x, 455, 225, 112);
        context.restore();
    }

    function paint() {
        if (!width || !height) return;
        context.clearRect(0, 0, width, height);
        context.save();
        context.scale(width / 960, height / 1024);

        // Hold each endpoint briefly so there is time to see the skyline fully lit.
        const phase = (1 - Math.cos(time * Math.PI / 12)) / 2;
        const blend = Math.max(0, Math.min(1, (phase - .1) / .8));
        const night = root.dataset.theme === 'dark' ? 1 - blend : blend;
        nightPainting.style.opacity = night.toFixed(3);
        drawTram(night);

        // Harbour reflections brighten at slightly different moments as dusk falls.
        for (let i = 0; i < 48; i++) {
            const x = 235 + (i * 71) % 434;
            const y = 341 + (i * 31) % 38;
            if (x > 272 && x < 410 && y > 353) continue;
            context.globalAlpha = night * (.25 + .23 * Math.sin(time * 2 + i));
            context.fillStyle = ['#ffc376', '#87e8f4', '#ffa0c4'][i % 3];
            context.fillRect(x, y, 2 + i % 6, 1);
        }
        context.globalAlpha = 1;

        // Map a small agent simulation to the perspective of the painted screen.
        const tick = Math.floor(time * 1.4);
        for (let agent = 0; agent < 9; agent++) {
            const col = (agent * 3 + Math.abs((tick + agent) % 12 - 6)) % 14;
            const row = (agent * 7 + Math.floor(tick / 4)) % 9;
            const x = 751 + col * 10 - row * 1.1;
            const y = 426 + row * 11 + col * 0.85;
            context.fillStyle = ['#2275a2', '#c0782f', '#48875d'][agent % 3];
            context.fillRect(x, y, 5.5, 5.5);
        }

        // Afternoon dust crosses the window light and disappears in the room.
        for (let i = 0; i < 34; i++) {
            const x = 205 + (i * 83 + time * 4) % 455;
            const y = 160 + (i * 57 + time * 2) % 440 + 5 * Math.sin(time + i);
            context.globalAlpha = .25 + .24 * Math.sin(time * .8 + i);
            context.fillStyle = '#fff5d3';
            context.beginPath();
            context.arc(x, y, 1 + i % 3 * .5, 0, 2 * Math.PI);
            context.fill();
        }

        // A slow reflection travels across the surface of the black coffee.
        context.globalAlpha = .46;
        context.strokeStyle = '#fff1c8';
        context.lineWidth = 1.8;
        context.beginPath();
        context.ellipse(198, 565, 13, 2, -.04, time, time + 2.4);
        context.stroke();
        context.restore();
    }

    function resize() {
        const bounds = canvas.getBoundingClientRect();
        width = bounds.width;
        height = bounds.height;
        const density = Math.min(devicePixelRatio || 1, 1.5);
        canvas.width = Math.round(width * density);
        canvas.height = Math.round(height * density);
        context.setTransform(density, 0, 0, density, 0, 0);
        paint();
    }

    function tick(now) {
        if (!lastPaint || now - lastPaint >= 32) {
            if (lastPaint) time += Math.min(now - lastPaint, 80) / 1000;
            paint();
            lastPaint = now;
        }
        frame = requestAnimationFrame(tick);
    }

    function syncPlayback() {
        control.hidden = motion.matches;
        control.textContent = paused ? 'Play background' : 'Pause background';
        const shouldPlay = !paused && !motion.matches && !document.hidden && visible;
        if (shouldPlay && !frame) {
            lastPaint = 0;
            frame = requestAnimationFrame(tick);
        } else if (!shouldPlay && frame) {
            cancelAnimationFrame(frame);
            frame = 0;
        }
    }

    control.addEventListener('click', () => {
        paused = !paused;
        syncPlayback();
    });
    motion.addEventListener('change', syncPlayback);
    document.addEventListener('visibilitychange', syncPlayback);
    new IntersectionObserver(([entry]) => {
        visible = entry.isIntersecting;
        syncPlayback();
    }).observe(canvas);
    new MutationObserver(paint).observe(root, { attributes: true, attributeFilter: ['data-theme'] });
    new ResizeObserver(resize).observe(canvas);
    resize();
    syncPlayback();
})();
