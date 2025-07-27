import React, {useState} from 'react'
import ChatWindow from './components/ChatWindow'
import './styles/App.css'

function App(){
    const [messages, setMessages] = useState([])
    const [loading, setLoading] = useState(false);

    const addMessage = (msg) => {
        setMessages((prev) => [...prev,msg])
    };
    
    return(
        <div className="app-container">
            <div className="chat-wrapper">
                <h1 className="chat-title">College Chatbot</h1>
                <ChatWindow
                messages={messages}
                addMessage={addMessage}
                loading={loading}
                setLoading={setLoading}
                />
            </div>
        </div>
    );
}

export default App;