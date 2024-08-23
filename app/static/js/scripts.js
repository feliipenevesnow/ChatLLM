const toggleThemeBtn = document.getElementById('toggle-theme-btn');
const body = document.body;
const sidebar = document.getElementById('sidebar');
const toggleSidebarBtn = document.getElementById('toggle-sidebar-btn');
const chatBackground = document.getElementById('chat-background');

// Alternar tema claro/escuro e trocar imagem
toggleThemeBtn.addEventListener('click', () => {
    body.classList.toggle('dark-mode');

    if (body.classList.contains('dark-mode')) {
        chatBackground.src = "/static/images/logo_dark.png";
    } else {
        chatBackground.src = "/static/images/logo.png";
    }
});

// Alternar menu lateral retrátil
toggleSidebarBtn.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
});

document.getElementById('send-btn').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value.trim();
    if (userInput) {
        const chat = document.getElementById('chat');

        // Cria a mensagem do usuário
        const userMessage = document.createElement('div');
        userMessage.classList.add('message', 'me');
        userMessage.innerHTML = `
            <div class="text">${userInput}</div>
        `;
        chat.appendChild(userMessage);

        // Cria a resposta do bot
        const botMessage = document.createElement('div');
        botMessage.classList.add('message', 'bot');
        botMessage.innerHTML = `
            <div class="text">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</div>
        `;
        chat.appendChild(botMessage);

        // Rolagem automática para a última mensagem
        chat.scrollTop = chat.scrollHeight;

        // Limpa o campo de entrada
        document.getElementById('user-input').value = '';
    }
});

// Alternar classe 'active' nos links de chat
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function() {
        // Remove a classe 'active' de todos os links
        document.querySelectorAll('.nav-link').forEach(nav => nav.classList.remove('active'));

        // Adiciona a classe 'active' ao link clicado
        this.classList.add('active');
    });
});
