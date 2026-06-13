import { useState } from "react";
import { askQuestion } from "../api/api";

function ChatBox() {
const [question, setQuestion] = useState("");
const [answer, setAnswer] = useState("");
const [sources, setSources] = useState([]);
const [loading, setLoading] = useState(false);

const handleAsk = async () => {

    if (!question.trim()) return;

    setLoading(true);

    try {

        const response = await askQuestion(question);

        setAnswer(response.data.answer);
        setSources(response.data.sources || []);

    } catch (error) {

        setAnswer("Error getting response");
        setSources([]);
        console.log(error);

    } finally {

        setLoading(false);

    }
};
console.log(sources);
return (
    <div>
        <h2>Ask a Question</h2>

        <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask about your document..."
        />

        <button
            onClick={handleAsk}
            disabled={loading}
        >
            {loading ? "Thinking..." : "Send"}
        </button>

        <h3>Answer</h3>

        <div
            style={{
                marginTop: "15px",
                padding: "15px",
                borderRadius: "10px",
                background: "#0f172a",
                border: "1px solid #334155"
            }}
        >
            <p>{answer}</p>
        </div>

        {sources.length > 0 && (
            <>
                <h3>Sources</h3>

                <ul className="sources-list">
                    {sources.map((source, index) => (
                        <li key={index}>
                            {source}
                        </li>
                    ))}
                </ul>
            </>
        )}
    </div>
);
}

export default ChatBox;
