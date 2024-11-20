"use strict";
document.addEventListener("DOMContentLoaded", () => {
    const zoomButtons = document.querySelectorAll(".zoom-btn");
    const images = document.querySelectorAll(".zoomable");
    // Apply zoom functionality
    zoomButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const zoomType = button.dataset.zoomType; // "in" or "out"
            const targetId = button.dataset.targetId;
            if (!targetId) {
                console.error("Target ID not found on zoom button");
                return;
            }
            const targetImage = document.getElementById(targetId);
            if (!targetImage) {
                console.error(`Image with ID ${targetId} not found`);
                return;
            }
            const currentScale = Number(targetImage.dataset.scale) || 1;
            let newScale = currentScale;
            if (zoomType === "in") {
                newScale = Math.min(currentScale + 0.1, 3); // Limit max zoom
            }
            else if (zoomType === "out") {
                newScale = Math.max(currentScale - 0.1, 1); // Limit min zoom
            }
            // Apply scaling with transformation origin centered
            targetImage.style.transform = `scale(${newScale})`;
            targetImage.style.transformOrigin = "center center"; // Keep scaling centered
            targetImage.dataset.scale = newScale.toString();
            // Ensure buttons stay visible
            const imageContainer = targetImage.closest(".image-container");
            if (imageContainer) {
                imageContainer.style.position = "relative"; // Keep container context
            }
        });
    });
});
