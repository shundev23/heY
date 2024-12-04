document.getElementById("send-btn").addEventListener("click", async () => {
    const userInput = document.getElementById("user-input").value;
    if(!userInput)return;

    const response = await fetch("/chat",{
        method:"POST",
        headers:{"Content-Type": "application/json"},
        body: JSON.stringify({message: userInput}),      
    });

    const data = await response.json();
    const chatLog = document.getElementById("chat-log");

    chatLog.innerHTML += `<div><strong>You:</strong> ${userInput}</div>`;
    chatLog.innerHTML += `<div><strong>Bot:</strong> ${data.response}</div>`;
    document.getElementById("user-input").value = "";
});