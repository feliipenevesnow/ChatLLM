const toggleThemeBtn = document.getElementById('toggle-theme-btn');
const body = document.body;
const sidebar = document.getElementById('sidebar');
const toggleSidebarBtn = document.getElementById('toggle-sidebar-btn');
const chatBackground = document.getElementById('chat-background');

function getChatIdFromUrl() {
    const pathArray = window.location.pathname.split('/');
    const chatId = pathArray[pathArray.length - 1];
    return chatId;
}

function updateChatList() {
    fetch('/chats/')
    .then(response => response.text())
    .then(html => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newChatNav = doc.querySelector('.chats-nav').innerHTML;
        const chatNavElement = document.querySelector('.chats-nav');
        chatNavElement.innerHTML = newChatNav;

        const currentChatId = getChatIdFromUrl();
        if (currentChatId) {
            chatNavElement.querySelector(`[data-chat-id='${currentChatId}']`).classList.add('active');
        }
    })
    .catch(error => {
        console.error('Erro ao atualizar a lista de chats:', error);
    });
}

function sendMessage(chatId, userInput) {
    const chat = document.getElementById('chat');

    const chatLink = document.querySelector(`.chat-link[data-chat-id='${chatId}'] .chat-name`);
    if (chatLink && chatLink.textContent.trim() === "Novo Chat") {
        chatLink.textContent = userInput;
    }

    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'me');
    userMessage.innerHTML = `<div class="text">${userInput}</div>`;
    chat.appendChild(userMessage);
    chat.scrollTop = chat.scrollHeight;

    const typingIndicator = document.createElement('div');
    typingIndicator.classList.add('message', 'bot');
    typingIndicator.innerHTML = `<div class="text typing-indicator"><span class="dot">.</span><span class="dot">.</span><span class="dot">.</span></div>`;
    chat.appendChild(typingIndicator);
    chat.scrollTop = chat.scrollHeight;

    const textarea = document.getElementById('user-input');
    textarea.value = '';
    textarea.style.height = 'auto';

    fetch(`/mensagens/${chatId}/messages`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            sender_type: 'user',
            message_text: userInput
        })
    })
    .then(response => response.json())
    .then(data => {
        chat.removeChild(typingIndicator);

        const botMessage = document.createElement('div');
        botMessage.classList.add('message', 'bot');
        botMessage.innerHTML = `<div class="text">${data.ai_message.message_text}</div>`;
        chat.appendChild(botMessage);
        chat.scrollTop = chat.scrollHeight;
    })
    .catch(error => {
        console.error('Erro ao enviar a mensagem:', error);
        chat.removeChild(typingIndicator);
    });
}


document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function() {
        document.querySelectorAll('.nav-link').forEach(nav => nav.classList.remove('active'));
        this.classList.add('active');
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const currentChatId = getChatIdFromUrl();
    if (currentChatId) {
        document.querySelector(`[data-chat-id='${currentChatId}']`).classList.add('active');
    }
});


toggleSidebarBtn.addEventListener('click', () => {
    sidebar.classList.toggle('show');
});

document.querySelectorAll('.edit-chat-name').forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();

        let nameElement = this.previousElementSibling;
        let currentName = nameElement.textContent;
        let chatId = this.closest('.nav-link').getAttribute('data-chat-id');

        nameElement.innerHTML = `<input type='text' class='form-control' placeholder='${currentName}'>`;
        let input = nameElement.querySelector('input');
        input.focus();

        input.addEventListener('blur', function() {
            let newName = this.value.trim() || currentName;
            nameElement.textContent = newName;

            fetch(`/chats/${chatId}/update`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title: newName })
            })
            .then(response => {
                if (!response.ok) {
                    console.error('Erro ao atualizar o nome do chat');
                }
            })
            .catch(error => {
                console.error('Erro ao enviar a atualiza��o:', error);
            });
        });
    });
});

toggleThemeBtn.addEventListener('click', () => {
    const body = document.body;
    body.classList.toggle('dark-mode');

    const isDarkMode = body.classList.contains('dark-mode');
    const newTheme = isDarkMode ? 'dark' : 'light';
    chatBackground.src = isDarkMode ? "/static/images/logo_dark.png" : "/static/images/logo.png";

    fetch('/update_theme', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ theme: newTheme })
    })
    .then(response => {
        if (!response.ok) {
            console.error('Erro ao atualizar o tema do usu�rio');
        }
    })
    .catch(error => {
        console.error('Erro ao enviar a atualiza��o do tema:', error);
    });
});


toggleSidebarBtn.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
});

document.getElementById('send-btn').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value.trim();
    const chat = document.getElementById('chat');

    if (userInput) {
        let chatId = getChatIdFromUrl();

        if (!chatId || isNaN(chatId)) {

            fetch('/chats/create', {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                chatId = data.chat_id;
                window.history.pushState(null, '', `/chats/${chatId}`);
                updateChatList();

                setTimeout(() => {
                    const chatLink = document.querySelector(`.chat-link[data-chat-id='${chatId}'] .chat-name`);
                    if (chatLink && chatLink.textContent.trim() === "Novo Chat") {
                        chatLink.textContent = userInput;
                    }

                    sendMessage(chatId, userInput);
                }, 50);
            })
            .catch(error => {
                console.error('Erro ao criar um novo chat:', error);
            });
        } else {
            sendMessage(chatId, userInput);
        }
    }
});

document.getElementById('user-input').addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
});

document.getElementById('user-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        document.getElementById('send-btn').click();
    }
});
