// main.js - Stage 1 Frontend Logic
document.addEventListener("DOMContentLoaded", () => {
  const queryInput = document.getElementById("queryInput");
  const submitBtn = document.getElementById("submitBtn");
  const loading = document.getElementById("loading");
  const responseCard = document.getElementById("responseCard");
  const responseContent = document.getElementById("responseContent");
  const clearBtn = document.getElementById("clearBtn");
  const chips = document.querySelectorAll(".chip");

  // Handle Form Submission
  async function handleQuery(queryText) {
    const text = (queryText || queryInput.value || "").trim();
    if (!text) {
      queryInput.focus();
      return;
    }

    // Set UI to loading state
    submitBtn.disabled = true;
    loading.classList.remove("hidden");
    responseCard.classList.add("hidden");

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });

      const data = await response.json();

      // Render markdown response safely
      if (window.marked && typeof window.marked.parse === "function") {
        responseContent.innerHTML = window.marked.parse(data.response || "No response received.");
      } else {
        responseContent.textContent = data.response;
      }

      // Show response card
      responseCard.classList.remove("hidden");
    } catch (err) {
      responseContent.innerHTML = `<p style="color: #ef4444;"><strong>Error:</strong> Could not connect to the mentor server. Please ensure Flask is running.</p>`;
      responseCard.classList.remove("hidden");
    } finally {
      loading.classList.add("hidden");
      submitBtn.disabled = false;
    }
  }

  // Event Listeners
  submitBtn.addEventListener("click", () => handleQuery());

  queryInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleQuery();
    }
  });

  // Handle quick suggestion chips
  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const query = chip.getAttribute("data-query");
      queryInput.value = query;
      handleQuery(query);
    });
  });

  // Clear button
  clearBtn.addEventListener("click", () => {
    responseCard.classList.add("hidden");
    queryInput.value = "";
    queryInput.focus();
  });
});
