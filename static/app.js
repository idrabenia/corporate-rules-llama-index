const form = document.getElementById("chat-form");
const input = document.getElementById("question");
const sendBtn = document.getElementById("send");
const messages = document.getElementById("messages");
const sourceList = document.getElementById("source-list");

const suggestions = {
  "suggest-1": "How many vacation days do I get?",
  "suggest-2": "What are the lunch hours?",
  "suggest-3": "How do I report a sick day?",
};

function appendMessage(text, role) {
  const div = document.createElement("div");
  div.className = `message ${role}`;
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
  return div;
}

function renderSources(texts) {
  sourceList.innerHTML = "";
  texts.forEach((t) => {
    const li = document.createElement("li");
    li.textContent = t;
    sourceList.appendChild(li);
  });
}

async function ask(question) {
  appendMessage(question, "user");
  const typing = appendMessage("Thinking", "bot");
  typing.classList.add("typing");
  sendBtn.disabled = true;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Request failed");
    }

    const data = await res.json();
    typing.classList.remove("typing");
    typing.textContent = data.answer;
    renderSources(data.source_texts);
  } catch (err) {
    typing.classList.remove("typing");
    typing.textContent = `Error: ${err.message}`;
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const question = input.value.trim();
  if (!question) return;
  input.value = "";
  ask(question);
});

for (const [id, text] of Object.entries(suggestions)) {
  document.getElementById(id).addEventListener("click", () => ask(text));
}