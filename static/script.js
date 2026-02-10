// Simple loading feedback
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", () => {
            const btn = document.querySelector("button");
            btn.innerText = "Analyzing...";
            btn.disabled = true;
        });
    }
});
const fileInput = document.getElementById("imageUpload");
const fileName = document.getElementById("file-name");

if (fileInput) {
    fileInput.addEventListener("change", () => {
        fileName.textContent = fileInput.files[0]
            ? fileInput.files[0].name
            : "No file selected";
    });
}
