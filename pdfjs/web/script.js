const output = document.getElementById("selection-output");
const gen_output = document.getElementById("ai-output");


console.log("✅ script.js LOADED");

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
    const res = await fetch("http://localhost:8000/summary", {
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



//getSummary("How are u doing? What is ur name ")


// // const GEMINI_API_KEY = "AIzaSyDkBTe0sxNx7-ngrwBN7ugf3RNxyw8C2wg";

// // // Example Gemini call
// // async function summarizeText(text) {
// //   const response = await fetch(
// //     "https://gemini.googleapis.com/v1alpha2/models/text-bison-001:generate",
// //     {
// //       method: "POST",
// //       headers: {
// //         "Content-Type": "application/json",
// //         "Authorization": "Bearer AIzaSyDkBTe0sxNx7-ngrwBN7ugf3RNxyw8C2wg" // <-- Put your Gemini API key here
// //       },
// //       body: JSON.stringify({
// //         prompt: `Summarize the following text in 2-3 sentences:\n\n${text}`,
// //         temperature: 0.5,
// //         maxOutputTokens: 200
// //       })
// //     }
// //   );

// //   const data = await response.json();

// //   const summary = data?.candidates?.[0]?.content || "No summary received";
// //   console.log("Summary:", summary);
// //   return summary;
// // }







// script.js
