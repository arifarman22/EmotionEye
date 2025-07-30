document.getElementById("chat-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (message === "") return;

  addMessage(message, "user");
  input.value = "";

  // Show typing indicator
  const typingMsg = addMessage("⏳ Thinking...", "bot");

  try {
    const response = await fetch("http://localhost:5000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    typingMsg.remove(); // Remove typing indicator
    addMessage(data.reply, "bot");
  } catch (error) {
    typingMsg.remove();
    addMessage("⚠️ Error connecting to the server.", "bot");
    console.error(error);
  }
});

document.getElementById("show-trend").addEventListener("click", async function () {
  const canvas = document.getElementById("sentimentChart");
  canvas.style.display = canvas.style.display === "none" ? "block" : "none";

  if (canvas.style.display === "block") {
    try {
      const response = await fetch("http://localhost:5000/sentiment-trend");
      const data = await response.json();

      new Chart(canvas, {
        type: 'bar',
        data: {
          labels: ['Positive', 'Negative', 'Neutral'],
          datasets: [{
            label: 'Sentiment Count',
            data: [data.POSITIVE, data.NEGATIVE, data.NEUTRAL],
            backgroundColor: ['#00c6ff', '#ff4d4d', '#cccccc']
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1
              }
            }
          }
        }
      });
    } catch (error) {
      console.error("Error fetching sentiment trend:", error);
    }
  }
});

// Add Message to Chat Box
function addMessage(text, sender) {
  const chatBox = document.getElementById("chat-box");
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");
  messageDiv.textContent = text;
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
  return messageDiv;
}