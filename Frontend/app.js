// Global variables
let sessionCount = 0;
let currentEmotion = '-';

document.addEventListener('DOMContentLoaded', function() {
  initializeApp();
});

function initializeApp() {
  // Add event listeners
  document.getElementById("chat-form").addEventListener("submit", handleChatSubmit);
  document.getElementById("show-trend").addEventListener("click", showSentimentTrend);
  document.getElementById("close-modal").addEventListener("click", closeModal);
  
  // Close modal when clicking outside
  document.getElementById("chart-modal").addEventListener("click", function(e) {
    if (e.target === this) closeModal();
  });
  
  // Update stats panel
  updateStatsPanel();
}

async function handleChatSubmit(e) {
  e.preventDefault();

  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (message === "") return;

  addMessage(message, "user");
  input.value = "";

  // Show typing indicator
  const typingMsg = addMessage("⏳ Analyzing your emotions...", "bot");

  try {
    const apiUrl = window.location.hostname === 'localhost' 
      ? 'http://localhost:5000/analyze'
      : '/api/analyze';
    
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    });

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    typingMsg.remove(); // Remove typing indicator

    if (data.error) {
      addMessage(`⚠️ Error: ${data.error}`, "bot");
      return;
    }

    // Update session stats
    sessionCount++;
    currentEmotion = capitalize(data.emotion);
    updateStatsPanel();

    // Show bot reply
    addMessage(`🤖 ${data.reply}`, "bot");

    // Show detected emotion and confidence
    addMessage(`📊 Emotion Detected: ${capitalize(data.emotion)} (${(data.confidence * 100).toFixed(1)}% confidence)`, "bot");

    // Show Quranic Aayah and translation
    addMessage(`📖 Quranic Verse:\n${data.quranic_aayat}`, "bot");
    addMessage(`🔍 Translation:\n${data.translation}`, "bot");

    // For debugging - show original classification if different
    if (data.original_classification && data.original_classification !== data.emotion) {
      addMessage(`🔧 Note: Initial classification was ${capitalize(data.original_classification)} but was corrected based on context.`, "bot");
    }

  } catch (error) {
    typingMsg.remove();
    addMessage("⚠️ Unable to connect to the analysis service. Please try again later.", "bot");
    console.error("API Error:", error);
  }
}

async function showSentimentTrend() {
  const modal = document.getElementById("chart-modal");
  const canvas = document.getElementById("sentimentChart");
  
  // Show modal
  modal.style.display = "flex";
  
  try {
    const apiUrl = window.location.hostname === 'localhost' 
      ? 'http://localhost:5000/sentiment-trend'
      : '/api/sentiment-trend';
    
    const response = await fetch(apiUrl);
    
    if (!response.ok) {
      throw new Error(`Server returned ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();

    // Destroy previous chart instance if it exists
    if (window.sentimentChartInstance) {
      window.sentimentChartInstance.destroy();
    }
    
    // Create new chart
    window.sentimentChartInstance = new Chart(canvas, {
      type: 'bar',
      data: {
        labels: Object.keys(data).map(key => capitalize(key)),
        datasets: [{
          label: 'Emotion Frequency',
          data: Object.values(data),
          backgroundColor: [
            '#00c6ff', '#ff4d4d', '#a29bfe', '#81ecec',
            '#fab1a0', '#55efc4', '#ffeaa7', '#e17055'
          ],
          borderColor: '#0a0f0d',
          borderWidth: 2,
          borderRadius: 6,
          hoverBackgroundColor: [
            '#00a8ff', '#ff3838', '#8c7ae6', '#00cec9',
            '#fd79a8', '#00b894', '#fdcb6e', '#d63031'
          ]
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: 'rgba(46, 60, 55, 0.3)'
            },
            ticks: {
              color: '#a0a0a0',
              stepSize: 1
            }
          },
          x: {
            grid: {
              color: 'rgba(46, 60, 55, 0.3)'
            },
            ticks: {
              color: '#a0a0a0'
            }
          }
        },
        plugins: {
          legend: {
            labels: {
              color: '#e2e2e2'
            }
          }
        }
      }
    });
  } catch (error) {
    console.error("Error fetching sentiment trend:", error);
    addMessage("⚠️ Unable to load sentiment trends. Please try again later.", "bot");
    closeModal();
  }
}

function closeModal() {
  document.getElementById("chart-modal").style.display = "none";
}

function addMessage(text, sender) {
  const chatBox = document.getElementById("chat-box");
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("chat-message", sender);
  messageDiv.textContent = text;
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
  return messageDiv;
}

function updateStatsPanel() {
  document.getElementById("sessions-count").textContent = sessionCount;
  document.getElementById("current-emotion").textContent = currentEmotion;
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
  // Ctrl+Enter to submit message
  if (e.ctrlKey && e.key === 'Enter') {
    document.getElementById("chat-form").dispatchEvent(new Event('submit'));
  }
  
  // Escape to close modal
  if (e.key === 'Escape') {
    closeModal();
  }
});