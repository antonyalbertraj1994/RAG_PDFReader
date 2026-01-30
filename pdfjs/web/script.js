const output = document.getElementById("selection-output");
const gen_output = document.getElementById("ai-output");


console.log("✅ script.js LOADED1");

const button = document.getElementById("submitBtn");
button.addEventListener("click", handleSubmit);

function handleSubmit() {
  const text = document.getElementById("myTextbox").value;
  getSummary(text)
  alert("You entered: " + text);
}


window.addEventListener("message", async(event) => {
  if (event.data?.type !== "PDF_TEXT_SELECTION") return;

  // clearTimeout(selectionTimeout);

  const { text, page } = event.data;
  output.innerHTML = `<strong>Selected text:</strong><br>${text}`;
  await getSummary(text)
});



// Fetch the summary from the node server. The node server access the gemini API and returns the results
async function getSummary(text) {
  try {
    const backendUrl = window.location.hostname.includes("localhost")
      ? "http://localhost:8000/summary"
      : "https://rag-pdfreader.onrender.com/summary";  
    console.log(`Backendurl1:${backendUrl}`)
      
    const res = await fetch(backendUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    const data = await res.json();
    if (data.error) {
      const output = "Error: " + data.error;
    } else {
      const output = data.summary;
      gen_output.innerHTML = `<strong>Summary Text</strong><br>${output}`;
      console.log(`Summary:${output}`)
    }
  } catch (err) {
    const output = "Fetch error: " + err.message;
  }
}


