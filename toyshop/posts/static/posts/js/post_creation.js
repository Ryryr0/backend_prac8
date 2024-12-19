document.addEventListener('DOMContentLoaded', () => {
    const fileDropZone = document.getElementById('fileDropZone');
    const fileInput = document.getElementById('fileInput');
    const addFileBtn = document.getElementById('addFileBtn');
    const fileNameDisplay = document.getElementById('fileName');

    const textarea = document.querySelector('.text-input');

    // Handle drag-and-drop functionality
    fileDropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileDropZone.classList.add('dragover');
    });

    fileDropZone.addEventListener('dragleave', () => {
        fileDropZone.classList.remove('dragover');
    });

    fileDropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        fileDropZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            fileNameDisplay.textContent = `Selected file: ${files[0].name}`;
        }
    });

    // Handle file selection via button
    addFileBtn.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            fileNameDisplay.textContent = `Selected file: ${fileInput.files[0].name}`;
        }
    });

    // if (textarea) {
    //     textarea.addEventListener("input", function () {
    //         const scrollTop = window.scrollY;

    //         this.style.height = "auto";
    //         this.style.height = this.scrollHeight + "px";

    //         window.scrollTo(0, scrollTop);
    //     });
    // } else {
    //     console.error("Textarea element not found!");
    // }
});
