import { useState } from "react";
import "./App.css";

function App() {
    const [message, setMessage] = useState("");
    const [chat, setChat] = useState([]);

    const sendMessage = async () => {
        if (!message.trim()) return;

        const userMessage = message;

        setChat((prev) => [
            ...prev,
            { sender: "You", text: userMessage },
        ]);

        setMessage("");

        try {
            const response = await fetch("https://llm-chatbot-230j.onrender.com/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    message: userMessage,
                }),
            });

            const data = await response.json();

            setChat((prev) => [
                ...prev,
                { sender: "Bot", text: data.response },
            ]);
        } catch (error) {
            setChat((prev) => [
                ...prev,
                { sender: "Bot", text: "Server Error" },
            ]);
        }
    };

    return (
        <div className="container">

            <h1>Chatbot</h1>

            <div className="chat-box">

                {chat.map((msg, index) => (
                    <div
                        key={index}
                        className={msg.sender === "You" ? "user" : "bot"}
                    >
                        <strong>{msg.sender}:</strong> {msg.text}
                    </div>
                ))}

            </div>

            <div className="input-area">

                <input
                    type="text"
                    placeholder="Type a message..."
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === "Enter") sendMessage();
                    }}
                />

                <button onClick={sendMessage}>
                    Send
                </button>

            </div>

        </div>
    );
}

export default App;