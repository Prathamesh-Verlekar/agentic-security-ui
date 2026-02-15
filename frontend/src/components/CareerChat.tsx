import { useCallback, useEffect, useRef, useState } from "react";
import { chatWithCareer } from "../api/client";
import type { ChatMessage, Region } from "../types";

interface Props {
  professionId: string;
  professionTitle: string;
  region?: Region;
}

export default function CareerChat({ professionId, professionTitle, region = "usa" }: Props) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = useCallback(async () => {
    const text = input.trim();
    if (!text || loading) return;

    const userMsg: ChatMessage = { role: "user", content: text };
    const newHistory = [...messages, userMsg];
    setMessages(newHistory);
    setInput("");
    setLoading(true);

    try {
      const res = await chatWithCareer(professionId, newHistory, region);
      if (res.success && res.data) {
        const assistantMsg: ChatMessage = {
          role: "assistant",
          content: res.data.reply,
        };
        setMessages([...newHistory, assistantMsg]);
      } else {
        const errorMsg: ChatMessage = {
          role: "assistant",
          content: "Sorry, I couldn't process your question. Please try again.",
        };
        setMessages([...newHistory, errorMsg]);
      }
    } catch {
      const errorMsg: ChatMessage = {
        role: "assistant",
        content: "Connection error. Please check your internet and try again.",
      };
      setMessages([...newHistory, errorMsg]);
    } finally {
      setLoading(false);
    }
  }, [input, loading, messages, professionId, region]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="career-chat">
      <div className="career-chat-header">
        <span className="career-chat-icon">💬</span>
        <div>
          <h3 className="career-chat-title">Career Counselor</h3>
          <p className="career-chat-subtitle">
            Ask anything about becoming a {professionTitle}
          </p>
        </div>
      </div>

      <div className="career-chat-messages">
        {messages.length === 0 && (
          <div className="career-chat-empty">
            <p>Start a conversation! You can ask about:</p>
            <div className="career-chat-suggestions">
              {[
                `What skills do I need to become a ${professionTitle}?`,
                `What's the salary progression like?`,
                `Is this career a good fit for someone who likes problem-solving?`,
                `What certifications would help?`,
              ].map((suggestion, i) => (
                <button
                  key={i}
                  className="career-chat-suggestion"
                  onClick={() => {
                    setInput(suggestion);
                  }}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`career-chat-bubble ${msg.role === "user" ? "user" : "assistant"}`}
          >
            <div className="career-chat-bubble-role">
              {msg.role === "user" ? "You" : "Counselor"}
            </div>
            <div className="career-chat-bubble-content">{msg.content}</div>
          </div>
        ))}

        {loading && (
          <div className="career-chat-bubble assistant">
            <div className="career-chat-bubble-role">Counselor</div>
            <div className="career-chat-typing">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <div className="career-chat-input-area">
        <input
          type="text"
          className="career-chat-input"
          placeholder={`Ask about the ${professionTitle} career…`}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
        />
        <button
          className="career-chat-send"
          onClick={sendMessage}
          disabled={loading || !input.trim()}
        >
          Send
        </button>
      </div>
    </div>
  );
}
