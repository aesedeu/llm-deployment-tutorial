async function send() {
    const chat = document.getElementById('chat');
    const input = document.getElementById('input');
    const temperatureInput = document.getElementById('temperature');
    const maxTokensInput = document.getElementById('max_tokens');

    const userMsg = input.value.trim();
    if (!userMsg) return;

    const temperature = parseFloat(temperatureInput.value) || 0.9;
    const max_tokens = parseInt(maxTokensInput.value) || 256;

    chat.innerHTML += `\nYou: ${userMsg}`;
    input.value = '';
    chat.innerHTML += `\nBot: `;

    try {
        const response = await fetch("/v1/completions", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                // model: "gpt2",
                // model: "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                prompt: userMsg,
                max_tokens: max_tokens,
                temperature: temperature,
                stream: true
            })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            for (const line of chunk.split("\n")) {
                if (line.startsWith("data: ")) {
                    const json = line.slice("data: ".length).trim();
                    if (json === "[DONE]") break;
                    const parsed = JSON.parse(json);
                    const delta = parsed.choices?.[0]?.text || "";
                    chat.innerHTML += delta;
                }
            }

            chat.scrollTop = chat.scrollHeight;
        }

        chat.innerHTML += "\n";
    } catch (error) {
        chat.innerHTML += `\n[Error: ${error.message}]`;
    }
}
