const toggle = document.getElementById("chatbot-toggle");
const box = document.getElementById("chatbot-box");
const closeBtn = document.getElementById("chatbot-close");
const input = document.getElementById("chat-input");
const messages = document.getElementById("chatbot-messages");

toggle.onclick = () => {
  box.style.display = "flex";
  toggle.style.display = "none";
};

closeBtn.onclick = () => {
  box.style.display = "none";
  toggle.style.display = "block";
};

function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = sender;
  div.innerHTML = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

function sendMessage() {
  const userText = input.value.trim();
  if (!userText) return;

  addMessage(userText, "user");
  input.value = "";

  // small delay for natural feel
  setTimeout(() => {
    const reply = botReply(userText);
    addMessage(reply, "bot");
  }, 500);
}

function botReply(text) {
  text = text.toLowerCase().trim();

  // ✅ MAIN FIX: detect "skill, location"
  const skillLocationRegex = /^([a-z\s]+),\s*([a-z\s]+)$/i;
  const match = text.match(skillLocationRegex);

  if (match) {
    const skill = match[1];
    const location = match[2];

    return `🔍 <b>Job Search Started</b><br>
            Skill: <b>${skill}</b><br>
            Location: <b>${location}</b><br><br>
            👉 Scroll the page to see matching jobs<br>
            👉 Complete your profile for better matches`;
  }

  if (text.includes("salary")) {
    return `💰 <b>Approximate Salary Ranges</b><br>
            Python Developer: ₹4–8 LPA<br>
            Java Developer: ₹3–7 LPA<br>
            Frontend Developer: ₹3–6 LPA`;
  }

  if (text.includes("resume")) {
    return `📄 <b>Resume Tips</b><br>
            • Add real projects<br>
            • Mention skills clearly<br>
            • Keep it 1–2 pages`;
  }

  if (text.includes("interview")) {
    return `🎤 <b>Interview Preparation</b><br>
            • Django ORM<br>
            • REST APIs<br>
            • OOP concepts<br>
            • SQL basics`;
  }

  if (text.includes("apply")) {
    return `📝 <b>How to Apply</b><br>
            1. Login<br>
            2. Complete your profile<br>
            3. Click Apply on a job`;
  }

  return `🤖 I can help you with:<br>
          • Job search (python, chennai)<br>
          • Salary details<br>
          • Resume tips<br>
          • Interview questions`;
}
