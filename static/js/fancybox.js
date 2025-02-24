"use strict";

document.addEventListener("DOMContentLoaded", () => {
    Fancybox.bind("[data-fancybox='gallery']", {
        Thumbs: {
            autoStart: false,
        },
        Toolbar: {
            display: ["zoom", "fullscreen", "close"],
        },
    });
    console.log("✅ Fancybox initialized successfully!");
});
