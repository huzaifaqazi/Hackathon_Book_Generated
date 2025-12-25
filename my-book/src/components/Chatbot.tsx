import React, { useState, useEffect } from 'react';

interface Message {
  text: string;
  sender: 'user' | 'bot';
  sources?: { url: string; title: string }[];
}

const Chatbot: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');

  useEffect(() => {
    setMessages([
      { text: "Hello, I'm your AI assistant for this book. Ask me anything!", sender: 'bot' },
    ]);
  }, []);

  const toggleChatbot = () => {
    setIsOpen(!isOpen);
  };

  const handleSendMessage = async () => {
    const queryText = input || selectedText;
    if (!queryText.trim()) return;

    const userMessage: Message = { text: queryText, sender: 'user' };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setInput('');

    try {
      const response = await fetch('http://localhost:8000/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: queryText,
          selected_text: selectedText || undefined,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP Error ${response.status}`);
      }

      const data = await response.json();


      if (!data || typeof data.response !== 'string') {
        throw new Error('Invalid response format');
      }

      const botResponse: Message = {
        text: data.response,
        sender: 'bot',
        sources: Array.isArray(data.sources)
          ? data.sources.map((src: any) => ({
              url: src.url || '',
              title: src.title || src.url || 'Source',
            }))
          : [],
      };

      setMessages((prev) => [...prev, botResponse]);
    } catch (error) {
      console.error('Chatbot error:', error);
      setMessages((prev) => [
        ...prev,
        { text: "Sorry, I'm having trouble connecting right now.", sender: 'bot' },
      ]);
    } finally {
      setIsLoading(false);
      setSelectedText('');
    }
  };

  // Capture selected text from book content only
  useEffect(() => {
    const handleSelectionChange = () => {
      const selection = window.getSelection();
      if (!selection || selection.toString().length === 0) {
        // Nothing selected, or selection cleared
        setSelectedText(''); // Clear if selection is empty
        return;
      }

      const selectedText = selection.toString();
      const anchorNode = selection.anchorNode;

      if (!anchorNode) {
        return; // No anchor node found
      }

      // Find the main content area of the book.
      // Assuming Docusaurus content is within a <main> tag or a div with class 'markdown-body'.
      const mainContentElement = document.querySelector('main');
      const markdownBodyElement = document.querySelector('.markdown-body'); // Fallback/alternative

      let isInBookContent = false;
      let currentNode: Node | null = anchorNode;

      // Traverse up the DOM tree from the anchor node
      while (currentNode) {
        if (currentNode === mainContentElement || (currentNode instanceof Element && currentNode.classList.contains('markdown-body'))) {
          isInBookContent = true;
          break;
        }
        currentNode = currentNode.parentNode;
      }

      if (isInBookContent) {
        setSelectedText(selectedText); // Update only if selection is from book content
      } else {
        // If selection is NOT in book content, clear selectedText
        setSelectedText('');
      }
    };

    document.addEventListener('mouseup', handleSelectionChange);
    return () => document.removeEventListener('mouseup', handleSelectionChange);
  }, []);

  return (
    <>
      {!isOpen && (
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
            zIndex: 1000,
          }}
        >
          💬
        </button>
      )}

      {isOpen && (
        <div
          style={{
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            width: '350px',
            height: '500px',
            backgroundColor: 'white',
            borderRadius: '10px',
            boxShadow: '0 5px 15px rgba(0,0,0,0.3)',
            display: 'flex',
            flexDirection: 'column',
            zIndex: 1000,
          }}
        >
          {/* Header */}
          <div
            style={{
              padding: '10px',
              backgroundColor: '#007bff',
              color: 'white',
              display: 'flex',
              justifyContent: 'space-between',
            }}
          >
            <strong>Book Chatbot</strong>
            <button
              onClick={toggleChatbot}
              style={{ background: 'none', border: 'none', color: 'white', fontSize: '18px' }}
            >
              ×
            </button>
          </div>

          {/* Messages */}
          <div style={{ flex: 1, padding: '10px', overflowY: 'auto' }}>
            {selectedText && (
              <div style={{ background: '#fffbe6', padding: '8px', marginBottom: '10px' }}>
                <small>Selected: {selectedText.slice(0, 100)}...</small>
                <button
                  onClick={() => setSelectedText('')}
                  style={{ float: 'right', border: 'none', background: 'none' }}
                >
                  ×
                </button>
              </div>
            )}

            {messages.map((msg, i) => (
              <div key={i} style={{ textAlign: msg.sender === 'user' ? 'right' : 'left', marginBottom: '10px' }}>
                <span
                  style={{
                    padding: '8px 12px',
                    borderRadius: '15px',
                    display: 'inline-block',
                    backgroundColor: msg.sender === 'user' ? '#007bff' : '#e0e0e0',
                    color: msg.sender === 'user' ? 'white' : 'black',
                  }}
                >
                  {msg.text}
                </span>

                {msg.sources && msg.sources.length > 0 && (
                  <ul style={{ fontSize: '0.8em', marginTop: '5px' }}>
                    {msg.sources.map((s, idx) => (
                      <li key={idx}>
                        <a href={s.url} target="_blank" rel="noopener noreferrer">
                          {s.title}
                        </a>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            ))}

            {isLoading && <div>Typing...</div>}
          </div>

          {/* Input */}
          <div style={{ display: 'flex', padding: '10px' }}>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Ask a question..."
              disabled={isLoading}
              style={{ flex: 1, marginRight: '5px' }}
            />
            <button onClick={handleSendMessage} disabled={isLoading }>
              Send
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default Chatbot;
