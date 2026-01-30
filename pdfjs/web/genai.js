import { GoogleGenerativeAI } from "https://esm.run";

// 1. Setup AI
const API_KEY = "AIzaSyDkBTe0sxNx7-ngrwBN7ugf3RNxyw8C2wg";
const genAI = new GoogleGenerativeAI(API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

const iframe = document.getElementById('pdf-viewer');
const displayArea = document.getElementById('selected-word-display');

// 2. Listen for PDF selection
iframe.onload = () => {
    const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;

    iframeDoc.addEventListener('mouseup', async () => {
        const selection = iframe.contentWindow.getSelection().toString().trim();

        if (selection.length > 0) {
            displayArea.innerText = "Thinking..."; // Loading state

            try {
                // 3. Call Google AI
                const prompt = `Explain this word or phrase found in a PDF: ${selection}`;
                const result = await model.generateContent(prompt);
                const response = await result.response;

                // 4. Update the right-side panel
                displayArea.innerHTML = `<strong>AI Analysis:</strong><br>${response.text()}`;
            } catch (error) {
                displayArea.innerText = "Error: " + error.message;
            }
        }
    });
};
