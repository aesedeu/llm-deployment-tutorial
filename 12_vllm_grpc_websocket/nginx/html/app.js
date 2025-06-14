async function sendWS() {
    const chat = document.getElementById('chat');
    const input = document.getElementById('input');
    const userMsg = input.value.trim();
    if (!userMsg) return;

    chat.innerHTML += `\nYou: ${userMsg}`;
    input.value = '';
    chat.innerHTML += `\nBot: `;

    const socket = new WebSocket("ws://localhost:8000/ws");

    socket.onopen = () => {
        socket.send(userMsg);
    };

    socket.onmessage = (event) => {
        chat.innerHTML += event.data;
        chat.scrollTop = chat.scrollHeight;
    };

    socket.onerror = (error) => {
        chat.innerHTML += `\n[Error: ${error.message}]`;
    };

    socket.onclose = () => {
        chat.innerHTML += "\n";
    };
}
