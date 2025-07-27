import React, { useState, useEffect } from 'react';
import '../styles/MessageBubble.css';

export default function MessageBubble({ role, content }) {
  const [isSpeaking, setIsSpeaking] = useState(false);

  const speak = () => {
    if (!window.speechSynthesis) return;

    const utterance = new SpeechSynthesisUtterance(content);
    utterance.lang = 'en-US';
    utterance.rate = 1;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  };

  const stopSpeaking = () => {
    window.speechSynthesis.cancel();
    setIsSpeaking(false);
  };

  return (
    <div className={`message-bubble ${role}`}>
      <div className="bubble-content">
        <span>
          <strong>{role === 'user' ? 'You' : 'Bot'}:</strong> {content}
        </span>

        {role === 'assistant' && (
          <>
            {!isSpeaking ? (
              <button className="speak-btn" onClick={speak} title="Read Aloud">
                🔊
              </button>
            ) : (
              <button className="speak-btn stop-btn" onClick={stopSpeaking} title="Stop Audio">
                🛑
              </button>
            )}
          </>
        )}
      </div>
    </div>
  );
}
