const toggleThemeBtn = document.getElementById('toggle-theme-btn');
const body = document.body;
const sidebar = document.getElementById('sidebar');
const toggleSidebarBtn = document.getElementById('toggle-sidebar-btn');
const chatBackground = document.getElementById('chat-background');



toggleSidebarBtn.addEventListener('click', () => {
    sidebar.classList.toggle('show');
});



toggleThemeBtn.addEventListener('click', () => {
    body.classList.toggle('dark-mode');

    if (body.classList.contains('dark-mode')) {
        chatBackground.src = "/static/images/logo_dark.png";
    } else {
        chatBackground.src = "/static/images/logo.png";
    }
});


toggleSidebarBtn.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
});

document.getElementById('send-btn').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value.trim();
    if (userInput) {
        const chat = document.getElementById('chat');


        const userMessage = document.createElement('div');
        userMessage.classList.add('message', 'me');
        userMessage.innerHTML = `
            <div class="text">${userInput}</div>
        `;
        chat.appendChild(userMessage);


        const botMessage = document.createElement('div');
        botMessage.classList.add('message', 'bot');
        botMessage.innerHTML = `
            <div class="text">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</div>
        `;
        chat.appendChild(botMessage);

        chat.scrollTop = chat.scrollHeight;

        document.getElementById('user-input').value = '';
    }
});


document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function() {

        document.querySelectorAll('.nav-link').forEach(nav => nav.classList.remove('active'));

        this.classList.add('active');
    });
});
