import React, {useState, useEffect, useRef} from 'react';
import MessageBubble from './MessageBubble';
import DiveDeeperButton from './DiveDeeperButton';
import {answerQuestion,diveDeeper} from '../api/chatApi';
import '../styles/ChatWindow.css'

function ChatWindow({messages, addMessage, loading, setLoading}) {
    const [input, setInput] = useState('')
    const [lastAnswer, setLastAnswer] = useState('')
    const messageEndRef = useRef(null)
    const [listening,setListening] = useState(false)
    const recognitionRef = useRef(null)


    useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);


    const sendMessage = async(text) => {
        if (!text.trim()) return;

        const userMessage = {role:'user', content:text}
        addMessage(userMessage)
        setInput('')
        setLoading(true)

        try{
            const res = await answerQuestion(text)
            const botText = res || "No response"
            const botMessage = {role:'assistant', content:botText}
            addMessage(botMessage)
            setLastAnswer(botText)
        }

        catch (err) {
                addMessage({role:'assistant', content:'Error fetching response'})
        }

        finally {
            setLoading(false)
        }
    };

    const handleSend = () => {
        sendMessage(input)
    };

    const handleKeyDown = (e) => {
        if (e.key ==='Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSend()
        }
    };

    const handleDiveDeeper = async() => {
        if (!lastAnswer) return 
        setLoading(true)

        try{
            const res = await diveDeeper({previous_answer:lastAnswer})
            const deeper = {role:'assistant', content: res.answer}
            addMessage(deeper)
        }

        catch(e) {
            addMessage({role:'assistant', content: 'Failed to dive deeper'})
        }

        finally{
            setLoading(false)
        }
    };


    const toggleListening = () => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
        if (!SpeechRecognition) {
            alert("Speech recognition not supported in this browser.");
            return;
        }

        if (listening) {
            recognitionRef.current?.stop()
            setListening(false)
            return
        }

        const recognition = new SpeechRecognition()
        recognition.lang = 'en-US'
        recognition.interimResults = false
        recognition.maxAlternatives = 1

        recognition.onresult = (event) => {
            const spokenText = event.results[0][0].transcript
            setInput(spokenText) //Add to input box
            setListening(false)
        }

        recognition.onerror = (event) => {
            console.error("Speech recognition error:", event.error)
            setListening(false)
        }

        recognition.onend = () => {
            setListening(false)
        }

        recognitionRef.current = recognition 
        recognition.start()
        setListening(true)
    }

    return (
        <div className="chat-window">
            <div className="message-container">
                {messages.map((msg,idx) => (
                    <MessageBubble key={idx} role={msg.role} content={msg.content} />
                ))}

                {loading && <MessageBubble role="assistant" content="Typing..." />}
                
                <div ref={messageEndRef} />
            </div>
            
            {lastAnswer && (
                <div className="dive-deeper">
                    <button
                        onClick={handleDiveDeeper}
                        disabled={loading}
                        className={loading ? 'disabled' : ''}
                        >
                        Dive Deeper
                    </button>
                </div>
            )}


            <div className="input-container">
                <textarea 
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask a question..."
                />

                <button
                    onClick={toggleListening}
                    className={`mic-button ${listening ? 'listening' : ''}`}
                    title={listening ? "Stop Listening" : "Start Listening"}
                >
                    {listening ? '🛑' : '🎤'}
                </button>

                <button onClick={handleSend} disabled={loading}>Send</button>
            </div>
        </div>
    );
}

export default ChatWindow;