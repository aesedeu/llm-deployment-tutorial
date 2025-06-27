async function send() {
    const chat = document.getElementById('chat');
    const input = document.getElementById('input');
    const temperatureInput = document.getElementById('temperature');
    const maxTokensInput = document.getElementById('max_tokens');

    const userMsg = input.value.trim();
    if (!userMsg) return;

    const temperature = parseFloat(temperatureInput.value) || 0.9;
    const max_tokens = parseInt(maxTokensInput.value) || 256;

    // Добавляем сообщение пользователя
    const userElement = document.createElement('div');
    userElement.textContent = `You: ${userMsg}`;
    chat.appendChild(userElement);

    input.value = '';

    // Создаём отдельный элемент для ответа бота
    const botElement = document.createElement('div');
    botElement.textContent = 'Bot: ';
    chat.appendChild(botElement);

    chat.scrollTop = chat.scrollHeight;

    try {
        const response = await fetch("http://localhost:8001/stream", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: userMsg,
                temperature: temperature,
                max_tokens: max_tokens
            })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            // console.log("RAW CHUNK:", chunk);

            botElement.textContent += chunk;
            chat.scrollTop = chat.scrollHeight;
        }
    } catch (error) {
        const errorElement = document.createElement('div');
        errorElement.textContent = `[Error: ${error.message}]`;
        chat.appendChild(errorElement);
    }
}
