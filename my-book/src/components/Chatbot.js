import React, { useState, useEffect } from 'react';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');

  useEffect(() => {
    if (!sessionId) {
      setSessionId(localStorage.getItem('chatbotSessionId') || `session-${Date.now()}`);
    }
  }, [sessionId]);

  useEffect(() => {
    if (sessionId) {
      localStorage.setItem('chatbotSessionId', sessionId);
    }
  }, [sessionId]);

  const handleSendMessage = async () => {
    if (input.trim() === '' && selectedText.trim() === '') return;

    const userMessage = { sender: 'user', text: input || selectedText };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/v1/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: input, session_id: sessionId, selected_text: selectedText }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const botMessage = { sender: 'bot', text: data.response, sources: data.sources };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
      setSessionId(data.session_id);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'bot', text: 'Sorry, something went wrong. Please try again.' },
      ]);
    } finally {
      setIsLoading(false);
      setSelectedText(''); // Clear selected text after sending
    }
  };

  const toggleChatbot = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      // When opening, capture selected text from the page
      const selection = window.getSelection().toString().trim();
      if (selection) {
        setSelectedText(selection);
      }
    }
  };

  return (
    <>
      {/* Floating Chat Button */}
      <button
        onClick={toggleChatbot}
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '50%',
          width: '60px',
          height: '60px',
          fontSize: '24px',
          cursor: 'pointer',
          boxShadow: '0 2px 10px rgba(0,0,0,0.2)',
          zIndex: 1000,
        }}
      >
        💬
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div
          style={{
            position: 'fixed',
            bottom: '90px',
            right: '20px',
            width: '350px',
            height: '500px',
            backgroundColor: 'white',
            border: '1px solid #ccc',
            borderRadius: '8px',
            boxShadow: '0 5px 15px rgba(0,0,0,0.3)',
            display: 'flex',
            flexDirection: 'column',
            zIndex: 1000,
          }}
        >
          {/* Chat Header */}
          <div
            style={{
              padding: '10px',
              backgroundColor: '#f0f0f0',
              borderBottom: '1px solid #ccc',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <strong>Book Chatbot</strong>
            <button
              onClick={toggleChatbot}
              style={{ background: 'none', border: 'none', fontSize: '18px', cursor: 'pointer' }}
            >
              &times;
            </button>
          </div>

          {/* Messages Display */}
          <div style={{ flex: 1, padding: '10px', overflowY: 'auto', borderBottom: '1px solid #eee' }}>
            {selectedText && (
              <div style={{ marginBottom: '10px', padding: '8px', backgroundColor: '#fffbe6', borderRadius: '5px' }}>
                <small>Selected Text: "{selectedText.substring(0, 100)}..."</small>
                <button onClick={() => setSelectedText('')} style={{ float: 'right', background: 'none', border: 'none', cursor: 'pointer' }}>&times;</button>
              </div>
            )}
            {messages.map((msg, index) => (
              <div
                key={index}
                style={{
                  marginBottom: '10px',
                  textAlign: msg.sender === 'user' ? 'right' : 'left',
                }}
              >
                <span
                  style={{
                    display: 'inline-block',
                    padding: '8px 12px',
                    borderRadius: '15px',
                    backgroundColor: msg.sender === 'user' ? '#007bff' : '#e0e0e0',
                    color: msg.sender === 'user' ? 'white' : 'black',
                  }}
                >
                  {msg.text}
                </span>
                {msg.sources && msg.sources.length > 0 && (
                  <div style={{ fontSize: '0.8em', marginTop: '5px', color: '#555' }}>
                    <p>Sources:</p>
                    <ul>
                      {msg.sources.map((source, srcIndex) => (
                        <li key={srcIndex}>
                          <a href={source.url} target="_blank" rel="noopener noreferrer">
                            {source.title || source.url}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
            {isLoading && (
              <div style={{ textAlign: 'left', marginBottom: '10px' }}>
                <span
                  style={{
                    display: 'inline-block',
                    padding: '8px 12px',
                    borderRadius: '15px',
                    backgroundColor: '#e0e0e0',
                    color: 'black',
                  }}
                >
                  Typing...
                </span>
              </div>
            )}
          </div>

          {/* Message Input */}
          <div style={{ padding: '10px', display: 'flex' }}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder={selectedText ? 'Ask about selected text...' : 'Ask a question...'}
              style={{ flex: 1, padding: '8px', border: '1px solid #ccc', borderRadius: '4px', marginRight: '5px' }}
              disabled={isLoading}
            />
            <button
              onClick={handleSendMessage}
              style={{
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                padding: '8px 15px',
                cursor: 'pointer',
              }}
              disabled={isLoading}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default Chatbot;
