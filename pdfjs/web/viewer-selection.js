// viewer-selection.js
// let lastSelection = "";

// document.addEventListener("selectionchange", () => {
//   const selection = window.getSelection();
//   if (!selection || selection.isCollapsed) return;

//   const text = selection.toString().trim();
//   if (!text || text === lastSelection) return;

//   lastSelection = text;

//   console.log("PDF Selection:", text);

//   // Send to parent (side panel, extension, etc.)
//   window.parent.postMessage(
//     {
//       type: "PDF_TEXT_SELECTION",
//       text,
//       page:
//         window.PDFViewerApplication?.pdfViewer?.currentPageNumber
//     },
//     "*"
//   );
// });

// viewer-selection.js

// let lastSelection = "";

// document.addEventListener("selectionchange", () => {
//   const selection = window.getSelection();
//   if (!selection || selection.isCollapsed) return;

//   const text = selection.toString().trim();
//   if (!text || text === lastSelection) return;

//   lastSelection = text;

//   window.parent.postMessage(
//     {
//       type: "PDF_TEXT_SELECTION",
//       text,
//       page:
//         window.PDFViewerApplication?.pdfViewer?.currentPageNumber
//     },
//     "*"
//   );
// });

console.log("✅ script1.js LOADED");

let lastSelection = "";

// Track if the user is currently dragging/selecting
let isDragging = false;

// Detect when mouse drag starts
document.addEventListener("mousedown", () => {
  isDragging = true;
});

// Detect when mouse drag ends (mouse button released)
document.addEventListener("mouseup", () => {
  if (!isDragging) return; // ignore if no drag happened

  const selection = window.getSelection();
  if (!selection || selection.isCollapsed) {
    isDragging = false;
    return;
  }

  const text = selection.toString().trim();
  if (!text || text === lastSelection) {
    isDragging = false;
    return;
  }

  lastSelection = text;

  console.log("PDF Selection:", text);

  // Send selection to parent
  window.parent.postMessage(
    {
      type: "PDF_TEXT_SELECTION",
      text,
      page: window.PDFViewerApplication?.pdfViewer?.currentPageNumber
    },
    "*"
  );

  // Reset drag flag
  isDragging = false;
});

document.getElementById("secondaryOpenFile").addEventListener("click", () => {
  console.log("Open File button pressed")
});
