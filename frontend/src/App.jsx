import "./App.css";
import FileUpload from "./components/FileUpload";
import ChatBox from "./components/ChatBox";

function App() {
return ( <div className="app-container">
    
        <div className="hero-section">
            <h1>Polaris.ME</h1>
            <p>
                AI-Powered Codebase & Documentation Intelligence Platform
            </p>
        </div>

        <div className="card">
            <FileUpload />
        </div>

        <div className="card">
            <ChatBox />
        </div>

    </div>
);

}

export default App;
