// send-pdf.js
(async function sendPdfToServer() {
    // Wait for PDF.js to initialize
    function waitForPDF() {
        return new Promise((resolve) => {
            const check = () => {
                if (window.PDFViewerApplication && PDFViewerApplication.pdfDocument) {
                    resolve(PDFViewerApplication.pdfDocument);
                } else {
                    setTimeout(check, 100); // check again after 100ms
                }
            };
            check();
        });
    }

    const pdfDoc = await waitForPDF();

    try {
        // Get the raw PDF data as Uint8Array
        const pdfData = await pdfDoc.getData(); // returns Uint8Array

        // Convert to Blob
        const pdfBlob = new Blob([pdfData], { type: "application/pdf" });

        // Prepare FormData
        const formData = new FormData();
        formData.append("pdf", pdfBlob, "loaded.pdf");

        // Send to server
        const res = await fetch("/upload-pdf", {
            method: "POST",
            body: formData
        });

        const result = await res.json();
        console.log("PDF uploaded successfully:", result);
    } catch (err) {
        console.error("Error uploading PDF:", err);
    }
})();
