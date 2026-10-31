const API_BASE = "https://python-practice-4cx5.onrender.com";
const $ = (id) => document.getElementById(id);

const authScreen = $("auth-screen"), appShell = $("app-shell");
const authForm = $("auth-form"), authEmail = $("auth-email"), authPassword = $("auth-password");
const authHeading = $("auth-heading"), authSubtitle = $("auth-subtitle"), authSubmit = $("auth-submit");
const authToggle = $("auth-toggle"), authSwitch = $("auth-switch"), authError = $("auth-error");
const chatForm = $("chat-form"), messageInput = $("message-input"), sendButton = $("send-button");
const chatMessages = $("chat-messages"), welcomeSection = $("welcome-section"), typingIndicator = $("typing-indicator");
const conversationList = $("conversation-list"), historyCount = $("history-count");
const sidebar = $("sidebar"), sidebarOverlay = $("sidebar-overlay");
const renameDialog = $("rename-dialog"), renameForm = $("rename-form"), renameInput = $("rename-input");

let token = localStorage.getItem("isaac_access_token");
let userEmail = localStorage.getItem("isaac_user_email") || "";
let isRegisterMode = false;
let conversationId = null;
let conversations = [];
let isSending = false;
let activeRequestController = null;
let lastPrompt = "";
let renamingId = null;
let toastTimer;

function showToast(message) {
    const toast = $("toast");
    toast.textContent = message;
    toast.classList.add("visible");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("visible"), 2600);
}

function setAuthMode(register) {
    isRegisterMode = register;
    authHeading.textContent = register ? "Create your account." : "Welcome back.";
    authSubtitle.textContent = register ? "One account. A workspace for every idea." : "Sign in and pick up where your ideas left off.";
    authSubmit.innerHTML = register ? 'Create account <span>↗</span>' : 'Sign in <span>↗</span>';
    authSwitch.innerHTML = register
        ? 'Already have an account? <button type="button" id="auth-toggle">Sign in</button>'
        : 'New to Isaac AI? <button type="button" id="auth-toggle">Create an account</button>';
    $("auth-toggle").addEventListener("click", () => setAuthMode(!isRegisterMode));
    authPassword.autocomplete = register ? "new-password" : "current-password";
    authError.textContent = "";
}

async function apiRequest(path, options = {}) {
    const headers = { ...(options.headers || {}) };
    if (options.body !== undefined) headers["Content-Type"] = "application/json";
    if (token && options.auth !== false) headers.Authorization = `Bearer ${token}`;
    let response;
    try {
        response = await fetch(`${API_BASE}${path}`, { ...options, headers });
    } catch (error) {
        throw new Error("Could not reach Isaac AI. Check your connection and try again.");
    }
    const raw = await response.text();
    let data = {};
    if (raw) {
        try { data = JSON.parse(raw); } catch { data = { detail: raw }; }
    }
    if (response.status === 401 && options.auth !== false) {
        logout(false);
        throw new Error("Your session expired. Please sign in again.");
    }
    if (!response.ok) {
        const detail = Array.isArray(data.detail)
            ? data.detail.map((item) => item.msg).join("; ")
            : data.detail;
        throw new Error(detail || `Request failed (${response.status}).`);
    }
    return data;
}

function showApp() {
    authScreen.hidden = true;
    appShell.hidden = false;
    $("profile-email").textContent = userEmail || "My account";
    $("profile-avatar").textContent = (userEmail[0] || "U").toUpperCase();
    loadConversations();
}

function showAuth() {
    appShell.hidden = true;
    authScreen.hidden = false;
    authPassword.value = "";
}

function logout(showMessage = true) {
    token = null;
    userEmail = "";
    conversationId = null;
    localStorage.removeItem("isaac_access_token");
    localStorage.removeItem("isaac_user_email");
    showAuth();
    if (showMessage) showToast("You have signed out.");
}

async function handleAuth(event) {
    event.preventDefault();
    authError.textContent = "";
    authSubmit.disabled = true;
    authSubmit.textContent = isRegisterMode ? "Creating account..." : "Signing in...";
    const email = authEmail.value.trim();
    const password = authPassword.value;
    try {
        if (isRegisterMode) {
            await apiRequest("/register", {
                method: "POST", auth: false,
                body: JSON.stringify({ email, password })
            });
            setAuthMode(false);
            authEmail.value = email;
            showToast("Account created. Sign in to continue.");
            return;
        }
        const result = await apiRequest("/login", {
            method: "POST", auth: false,
            body: JSON.stringify({ email, password })
        });
        if (!result.access_token) throw new Error("The server did not return an access token.");
        token = result.access_token;
        userEmail = email;
        localStorage.setItem("isaac_access_token", token);
        localStorage.setItem("isaac_user_email", userEmail);
        authForm.reset();
        showApp();
    } catch (error) {
        authError.textContent = error.message;
    } finally {
        authSubmit.disabled = false;
        authSubmit.innerHTML = isRegisterMode ? 'Create account <span>↗</span>' : 'Sign in <span>↗</span>';
    }
}

authForm.addEventListener("submit", handleAuth);
authToggle.addEventListener("click", () => setAuthMode(!isRegisterMode));


function addMessage(role, text, isError = false, messageId = null) {
    const message = document.createElement("article");
    message.className = `message ${role}${isError ? " message-error" : ""}`;
    if (messageId !== null) message.dataset.messageId = String(messageId);

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = role === "user" ? (userEmail[0] || "Y").toUpperCase() : "✦";

    const content = document.createElement("div");
    content.className = "message-content";

    const label = document.createElement("strong");
    label.className = "message-role";
    label.textContent = role === "user" ? "You" : "Isaac AI";

    const body = document.createElement("div");
    body.className = "message-text";
    if (role === "assistant" && !isError) {
        body.innerHTML = renderMarkdown(text);
        enhanceCodeBlocks(body);
    } else {
        body.textContent = text;
    }

    content.append(label, body);
    message.append(avatar, content);

    if (!isError && role === "user" && messageId !== null) {
        const actions = document.createElement("div");
        actions.className = "message-actions";
        const edit = document.createElement("button");
        edit.type = "button";
        edit.className = "message-action-button";
        edit.textContent = "✎ Edit and resend";
        edit.addEventListener("click", () => {
    editAndResend(messageId, text, body);
});
        actions.append(edit);
        content.append(actions);
    }

    if (!isError && role === "assistant" && conversationId !== null) {
        const actions = document.createElement("div");
        actions.className = "message-actions";
        const regenerate = document.createElement("button");
        regenerate.type = "button";
        regenerate.className = "message-action-button";
        regenerate.textContent = "↻ Regenerate";
        regenerate.addEventListener("click", regenerateResponse);
        actions.append(regenerate);
        content.append(actions);
    }

    chatMessages.append(message);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function renderConversation(messages = []) {
    chatMessages.replaceChildren();
    welcomeSection.hidden = messages.length > 0;
    lastPrompt = "";
    messages.forEach((message) => {
        if (message.role === "user") lastPrompt = message.content || "";
        if (message.role === "user" || message.role === "assistant") {
            addMessage(message.role, message.content || "", false, message.id ?? null);
        }
    });
}


async function loadConversations() {
    try {
        const data = await apiRequest("/conversations");
        conversations = Array.isArray(data) ? data : (data.conversations || []);
        renderConversationList();
    } catch (error) {
        if (token) showToast(error.message);
    }
}

function renderConversationList() {
    conversationList.replaceChildren();
    historyCount.textContent = String(conversations.length);
    if (!conversations.length) {
        const empty = document.createElement("div");
        empty.className = "history-empty";
        empty.textContent = "Your conversations will appear here.";
        conversationList.append(empty);
        return;
    }
    conversations.forEach((conversation) => {
        const id = conversation.conversation_id ?? conversation.id;
        const row = document.createElement("div");
        row.className = `conversation-item${String(id) === String(conversationId) ? " selected" : ""}`;
        const icon = document.createElement("span"); icon.className = "conversation-icon"; icon.textContent = "✧";
        const title = document.createElement("span"); title.className = "conversation-title"; title.textContent = conversation.title || "New conversation";
        const actions = document.createElement("span"); actions.className = "conversation-actions";
        const rename = document.createElement("button"); rename.className = "mini-action"; rename.type = "button"; rename.title = "Rename"; rename.textContent = "✎";
        rename.addEventListener("click", (event) => { event.stopPropagation(); openRename(id, conversation.title || ""); });
        const remove = document.createElement("button"); remove.className = "mini-action"; remove.type = "button"; remove.title = "Delete"; remove.textContent = "×";
        remove.addEventListener("click", (event) => { event.stopPropagation(); deleteConversation(id); });
        actions.append(rename, remove);
        row.append(icon, title, actions);
        row.addEventListener("click", () => openConversation(id));
        conversationList.append(row);
    });
}

async function openConversation(id) {
    if (isSending) return;
    try {
        const data = await apiRequest(`/conversations/${encodeURIComponent(id)}`);
        conversationId = data.conversation_id ?? id;
        renderConversation(data.messages || []);
        renderConversationList();
        closeSidebar();
    } catch (error) { showToast(error.message); }
}

function startNewChat() {
    if (isSending) return;
    conversationId = null;
    renderConversation([]);
    renderConversationList();
    messageInput.value = "";
    messageInput.style.height = "auto";
    messageInput.focus();
    closeSidebar();
}

async function sendMessage(text) {
    const prompt = text.trim();
    if (!prompt || isSending || !token) return;
    isSending = true;
    lastPrompt = prompt;
    activeRequestController = new AbortController();
    sendButton.disabled = true;
    $("stop-button").hidden = false;
    messageInput.disabled = true;
    welcomeSection.hidden = true;
    addMessage("user", prompt);
    messageInput.value = "";
    messageInput.style.height = "auto";
    typingIndicator.hidden = false;
    try {
        const result = await apiRequest("/ask", {
            method: "POST",
            body: JSON.stringify({ prompt, conversation_id: conversationId }),
            signal: activeRequestController.signal
        });
        if (typeof result.answer !== "string") throw new Error("The API response did not contain an answer.");
        conversationId = result.conversation_id;
        await openConversationAfterMutation();
        await loadConversations();
    } catch (error) {
        if (error.name === "AbortError") showToast("Stopped waiting. The server may still finish its request.");
        else addMessage("assistant", error.message, true);
    } finally {
        typingIndicator.hidden = true;
        isSending = false;
        activeRequestController = null;
        $("stop-button").hidden = true;
        sendButton.disabled = false;
        messageInput.disabled = false;
        messageInput.focus();
    }
}

async function openConversationAfterMutation() {
    if (conversationId === null) return;
    const data = await apiRequest(`/conversations/${encodeURIComponent(conversationId)}`);
    renderConversation(data.messages || []);
    renderConversationList();
}

async function runConversationAction(path, body = undefined, successMessage = "Done.") {
    if (isSending || !conversationId) return false;

    isSending = true;
    sendButton.disabled = true;
    messageInput.disabled = true;
    typingIndicator.hidden = false;
    activeRequestController = new AbortController();
    $("stop-button").hidden = false;

    let success = false;

    try {
        await apiRequest(path, {
            method: "POST",
            ...(body === undefined ? {} : { body: JSON.stringify(body) }),
            signal: activeRequestController.signal
        });

        await openConversationAfterMutation();
        await loadConversations();

        showToast(successMessage);
        success = true;

    } catch (error) {
        if (error.name === "AbortError") {
            showToast("Stopped waiting. The server may still finish its request.");
        } else {
            showToast(error.message);
        }

    } finally {
        typingIndicator.hidden = true;
        isSending = false;
        activeRequestController = null;
        $("stop-button").hidden = true;
        sendButton.disabled = false;
        messageInput.disabled = false;
    }

    return success;
}
function regenerateResponse() {
    if (!conversationId) return;
    runConversationAction(`/conversations/${encodeURIComponent(conversationId)}/regenerate`, undefined, "Response regenerated.");
}

function editAndResend(messageId, oldPrompt, messageBody) {
    if (!conversationId || isSending) return;

    // Don't open multiple editors for the same message.
    if (messageBody.querySelector(".edit-message-area")) return;

    messageBody.replaceChildren();

    const editor = document.createElement("div");
    editor.className = "edit-message-area";

    const textarea = document.createElement("textarea");
    textarea.className = "edit-message-input";
    textarea.value = oldPrompt;
    textarea.rows = Math.max(3, Math.min(8, oldPrompt.split("\n").length + 1));

    const buttons = document.createElement("div");
    buttons.className = "edit-message-buttons";

    const cancelButton = document.createElement("button");
    cancelButton.type = "button";
    cancelButton.textContent = "Cancel";
    cancelButton.className = "edit-cancel-button";

    const saveButton = document.createElement("button");
    saveButton.type = "button";
    saveButton.textContent = "Save & resend";
    saveButton.className = "edit-save-button";

    cancelButton.addEventListener("click", () => {
        messageBody.textContent = oldPrompt;
    });

    saveButton.addEventListener("click", async () => {
        const prompt = textarea.value.trim();

        if (!prompt) {
            showToast("Message cannot be empty.");
            return;
        }

        if (prompt.length > 2000) {
            showToast("Message cannot exceed 2000 characters.");
            return;
        }

        saveButton.disabled = true;
        cancelButton.disabled = true;
        saveButton.textContent = "Sending...";

        const success = await runConversationAction(
            `/conversations/${encodeURIComponent(conversationId)}/edit-and-resend`,
            {
                message_id: messageId,
                prompt: prompt
            },
            "Message updated and response regenerated."
        );

        if (!success) {
            saveButton.disabled = false;
            cancelButton.disabled = false;
            saveButton.textContent = "Save & resend";
        }
    });

    buttons.append(cancelButton, saveButton);
    editor.append(textarea, buttons);
    messageBody.append(editor);

    textarea.focus();
    textarea.setSelectionRange(textarea.value.length, textarea.value.length);
}


chatForm.addEventListener("submit", (event) => { event.preventDefault(); sendMessage(messageInput.value); });
messageInput.addEventListener("input", () => {
    messageInput.style.height = "auto";
    messageInput.style.height = `${Math.min(messageInput.scrollHeight, 180)}px`;
});
messageInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); chatForm.requestSubmit(); }
});
document.querySelectorAll(".suggestion-card").forEach((card) => card.addEventListener("click", () => sendMessage(card.dataset.prompt || "")));

function openRename(id, title) {
    renamingId = id;
    renameInput.value = title;
    renameDialog.showModal();
    renameInput.focus();
    renameInput.select();
}
renameForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const title = renameInput.value.trim();
    if (!title || !renamingId) return;
    try {
        await apiRequest(`/conversations/${encodeURIComponent(renamingId)}`, {
            method: "PATCH", body: JSON.stringify({ title })
        });
        const item = conversations.find((conversation) => String(conversation.conversation_id ?? conversation.id) === String(renamingId));
        if (item) item.title = title;
        renderConversationList();
        renameDialog.close();
        showToast("Conversation renamed.");
    } catch (error) { showToast(error.message); }
});
$("rename-cancel").addEventListener("click", () => renameDialog.close());

async function deleteConversation(id) {
    if (!confirm("Delete this conversation? This cannot be undone.")) return;
    try {
        await apiRequest(`/conversations/${encodeURIComponent(id)}`, { method: "DELETE" });
        conversations = conversations.filter((item) => String(item.conversation_id ?? item.id) !== String(id));
        if (String(conversationId) === String(id)) startNewChat();
        renderConversationList();
        showToast("Conversation deleted.");
    } catch (error) { showToast(error.message); }
}

function closeSidebar() {
    sidebar.classList.remove("open");
    sidebarOverlay.classList.remove("visible");
}
$("new-chat-button").addEventListener("click", startNewChat);
$("clear-chat-button").addEventListener("click", startNewChat);
$("logout-button").addEventListener("click", () => logout());
$("mobile-menu-button").addEventListener("click", () => { sidebar.classList.add("open"); sidebarOverlay.classList.add("visible"); });
$("mobile-close").addEventListener("click", closeSidebar);
sidebarOverlay.addEventListener("click", closeSidebar);
document.addEventListener("keydown", (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") { event.preventDefault(); startNewChat(); }
    if (event.key === "Escape") closeSidebar();
});


function stopGeneration() {
    // This aborts the browser request. With the current synchronous FastAPI
    // endpoint, it cannot guarantee cancellation of the Groq request on the server.
    if (activeRequestController) activeRequestController.abort();
}
$("stop-button").addEventListener("click", stopGeneration);

async function exportConversation(format) {
    if (!conversationId) {
        showToast("Send a message first to create a conversation.");
        return;
    }
    try {
        const data = await apiRequest(`/conversations/${encodeURIComponent(conversationId)}`);
        const messages = data.messages || [];
        const title = (data.title || "Isaac AI conversation").replace(/[\\/:*?"<>|]/g, "-");
        const transcript = messages.map((m) =>
            `${m.role === "user" ? "You" : "Isaac AI"}\n\n${m.content || ""}`
        ).join("\n\n----------------------------------------\n\n");

        if (format === "txt") {
            const blob = new Blob([`${title}\n${"=".repeat(title.length)}\n\n${transcript}`], {
                type: "text/plain;charset=utf-8"
            });
            downloadBlob(blob, `${title}.txt`);
        } else if (format === "pdf") {
            if (!window.jspdf?.jsPDF) {
                showToast("PDF exporter is still loading. Try again in a moment.");
                return;
            }
            const doc = new window.jspdf.jsPDF({ unit: "mm", format: "a4" });
            const margin = 15;
            const pageWidth = doc.internal.pageSize.getWidth();
            const pageHeight = doc.internal.pageSize.getHeight();
            const maxWidth = pageWidth - margin * 2;
            let y = 20;
            doc.setFont("helvetica", "bold");
            doc.setFontSize(16);
            doc.text(title, margin, y);
            y += 12;
            messages.forEach((m) => {
                const speaker = m.role === "user" ? "You" : "Isaac AI";
                doc.setFont("helvetica", "bold");
                doc.setFontSize(11);
                if (y > pageHeight - margin) { doc.addPage(); y = 20; }
                doc.text(speaker, margin, y);
                y += 6;
                doc.setFont("helvetica", "normal");
                doc.setFontSize(10);
                const lines = doc.splitTextToSize(String(m.content || ""), maxWidth);
                lines.forEach((line) => {
                    if (y > pageHeight - margin) { doc.addPage(); y = 20; }
                    doc.text(line, margin, y);
                    y += 5;
                });
                y += 5;
            });
            doc.save(`${title}.pdf`);
        }
        showToast(`Conversation exported as ${format.toUpperCase()}.`);
    } catch (error) {
        showToast(error.message);
    }
}

function downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.append(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
}

$("export-txt-button").addEventListener("click", () => exportConversation("txt"));
$("export-pdf-button").addEventListener("click", () => exportConversation("pdf"));

if (token) showApp(); else showAuth();
marked.setOptions({
    breaks: true,
    gfm: true
});


function renderMarkdown(content) {
    const html = marked.parse(content);
    return DOMPurify.sanitize(html);
}

function enhanceCodeBlocks(container) {
    const codeBlocks = container.querySelectorAll("pre");

    codeBlocks.forEach((pre) => {
        const code = pre.querySelector("code");

        if (!code) return;

        // Apply syntax highlighting
        if (window.hljs) {
            hljs.highlightElement(code);
        }

        // Prevent duplicate copy buttons
        if (pre.querySelector(".copy-code-button")) return;

        const copyButton = document.createElement("button");
        copyButton.className = "copy-code-button";
        copyButton.type = "button";
        copyButton.textContent = "Copy";

        copyButton.addEventListener("click", async () => {
            try {
                await navigator.clipboard.writeText(code.innerText);
                copyButton.textContent = "Copied!";

                setTimeout(() => {
                    copyButton.textContent = "Copy";
                }, 1800);
            } catch (error) {
                showToast("Could not copy code. Check clipboard permissions.");
            }
        });

        pre.append(copyButton);
    });
}
