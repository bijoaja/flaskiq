function toggleChatbot() {
  const modal = document.getElementById("chatbot-modal");
  if (modal.classList.contains("hidden")) {
    modal.classList.remove("hidden");
    modal.classList.add("flex");
  } else {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
  }
}

function sendChat() {
  const input    = document.getElementById("chatbot-input");
  const messages = document.getElementById("chatbot-messages");
  const userText = input.value.trim();

  if (!userText) return;

  // User bubble
  messages.innerHTML += `
    <div class="flex justify-end">
      <div class="bg-blue-600 text-white text-xs px-3 py-2 rounded-xl rounded-br-none max-w-[75%]">
        ${escapeHtml(userText)}
      </div>
    </div>`;
  input.value = "";
  messages.scrollTop = messages.scrollHeight;

  // AI bubble
  const aiWrapper = document.createElement("div");
  aiWrapper.className = "flex justify-start";
  const aiBubble = document.createElement("div");
  aiBubble.className = "bg-white border border-gray-200 text-gray-700 text-xs px-3 py-2 rounded-xl rounded-bl-none max-w-[75%] shadow-sm";
  aiBubble.textContent = "";
  aiWrapper.appendChild(aiBubble);
  messages.appendChild(aiWrapper);

  fetch("/api/v1/chatbot", {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify({ message: userText }),
  })
  .then(res => {
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const reader  = res.body.getReader();
    const decoder = new TextDecoder("utf-8");

    function read() {
      reader.read().then(({ done, value }) => {
        if (done) {
          messages.scrollTop = messages.scrollHeight;
          return;
        }
        aiBubble.textContent += decoder.decode(value, { stream: true });
        messages.scrollTop = messages.scrollHeight;
        read();
      });
    }
    read();
  })
  .catch(err => {
    aiBubble.innerHTML = `<span class="text-red-500">Error: ${escapeHtml(err.message)}</span>`;
    messages.scrollTop = messages.scrollHeight;
  });
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.appendChild(document.createTextNode(text));
  return div.innerHTML;
}
