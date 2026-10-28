
const API_BASE = "https://python-practice-4cx5.onrender.com";

// Page elements
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const chatMessages = document.getElementById("chat-messages");
const welcomeSection = document.getElementById("welcome-section");
const typingIndicator = document.getElementById("typing-indicator");

const newChatButton = document.getElementById("new-chat-button");
const clearChatButton = document.getElementById("clear-chat-button");
const suggestionCards = document.querySelectorAll(".suggestion-card");

const sidebar = document.getElementById("sidebar");
const mobileMenuButton = document.getElementById("mobile-menu-button");
const sidebarOverlay = document.getElementById("sidebar-overlay");

// Give this conversation its own ID.
let conversationId = crypto.randomUUID();
let isSending = false;


// Display a message safely in the chat.
function addMessage(role, text, isError = false) {
    const message = document.createElement("div");
    message.classList.add("message", role);

    if (isError) {
        message.classList.add("message-error");
    }

    const avatar = document.createElement("div");
    avatar.classList.add("message-avatar");
    avatar.textContent = role === "user" ? "Y" : "✦";

    const content = document.createElement("div");
    content.classList.add("message-content");

    const roleLabel = document.createElement("strong");
    roleLabel.classList.add("message-role");
    roleLabel.textContent = role === "user" ? "You" : "Isaac AI";

    const messageText = document.createElement("div");
    messageText.classList.add("message-text");
    messageText.textContent = text;

    content.append(roleLabel, messageText);
    message.append(avatar, content);
    chatMessages.appendChild(message);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


// Send a message to the backend.
async function sendMessage(text) {
    const prompt = text.trim();

    if (!prompt || isSending) {
        return;
    }

    isSending = true;
    sendButton.disabled = true;
    messageInput.disabled = true;

    welcomeSection.hidden = true;
    addMessage("user", prompt);

    messageInput.value = "";
    messageInput.style.height = "auto";
    typingIndicator.hidden = false;

    try {
        const response = await fetch(`${API_BASE}/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                prompt: prompt,
                conversation_id: conversationId
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail || `Request failed (${response.status})`
            );
        }

        if (typeof result.answer !== "string") {
            throw new Error("The API response did not contain an answer.");
        }

        addMessage("assistant", result.answer);

    } catch (error) {
        console.error("Isaac AI request failed:", error);

        addMessage(
            "assistant",
            `Sorry, something went wrong: ${error.message}. Please try again.`,
            true
        );
    } finally {
        typingIndicator.hidden = true;
        isSending = false;
        sendButton.disabled = false;
        messageInput.disabled = false;
        messageInput.focus();
    }
}


// Handle the chat form.
chatForm.addEventListener("submit", (event) => {
    event.preventDefault();
    sendMessage(messageInput.value);
});


// Make the textarea grow as you type.
messageInput.addEventListener("input", () => {
    messageInput.style.height = "auto";
    messageInput.style.height =
        `${Math.min(messageInput.scrollHeight, 180)}px`;
});


// Enter sends; Shift + Enter adds a new line.
messageInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        chatForm.requestSubmit();
    }
});


// Quick-prompt cards.
suggestionCards.forEach((card) => {
    card.addEventListener("click", () => {
        const prompt = card.dataset.prompt;

        if (prompt) {
            sendMessage(prompt);
        }
    });
});


// Start a fresh conversation in the interface.
function startNewChat() {
    if (isSending) {
        return;
    }

    conversationId = crypto.randomUUID();
    chatMessages.replaceChildren();
    welcomeSection.hidden = false;
    messageInput.value = "";
    messageInput.style.height = "auto";
    messageInput.focus();
}

newChatButton.addEventListener("click", startNewChat);
clearChatButton.addEventListener("click", startNewChat);


// Mobile sidebar controls.
function closeSidebar() {
    sidebar.classList.remove("open");
    sidebarOverlay.classList.remove("visible");
    mobileMenuButton.setAttribute("aria-expanded", "false");
}

mobileMenuButton.addEventListener("click", () => {
    const isOpen = sidebar.classList.toggle("open");

    sidebarOverlay.classList.toggle("visible", isOpen);
    mobileMenuButton.setAttribute("aria-expanded", String(isOpen));
});

sidebarOverlay.addEventListener("click", closeSidebar);
