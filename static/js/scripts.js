document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('typingTestForm');
    const textArea = document.getElementById('text');
    const startTimeInput = document.getElementById('start_time');
    const originalParagraph = document.getElementById('original-paragraph').textContent;
    const progressBar = document.getElementById('typing-progress');
    const currentSpeed = document.getElementById('current-speed');
    const currentAccuracy = document.getElementById('current-accuracy');

    // Set the start time when the textarea gains focus
    textArea.addEventListener('focus', () => {
        if (!startTimeInput.value) {
            startTimeInput.value = new Date().getTime() / 1000;
        }
    });

    // Ensure the start time is set before form submission
    form.addEventListener('submit', () => {
        if (!startTimeInput.value) {
            startTimeInput.value = new Date().getTime() / 1000;
        }
    });

    // Update typing progress, speed, and accuracy in real-time
    textArea.addEventListener('input', () => {
        const currentTime = new Date().getTime() / 1000;
        const startTime = parseFloat(startTimeInput.value);
        const timeTaken = currentTime - startTime;
        const words = textArea.value.split(/\s+/).filter(word => word.length > 0);
        const wordCount = words.length;
        const wpm = (wordCount / timeTaken) * 60;

        const correctChars = textArea.value.split('').filter((char, index) => char === originalParagraph[index]).length;
        const accuracy = (correctChars / originalParagraph.length) * 100;

        const progress = (textArea.value.length / originalParagraph.length) * 100;

        progressBar.style.width = `${progress}%`;
        progressBar.setAttribute('aria-valuenow', progress);
        currentSpeed.textContent = Math.round(wpm);
        currentAccuracy.textContent = Math.round(accuracy);
    });
});
