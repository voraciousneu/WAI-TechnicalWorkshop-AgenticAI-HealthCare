import React, { useState, useEffect } from "react";
import { analyzeText } from "../api";

export default function Reader() {
  const [text, setText] = useState("");
  const [feedback, setFeedback] = useState(null);

  useEffect(() => {
    const delayDebounce = setTimeout(async () => {
      if (text.trim().length > 10) {
        const result = await analyzeText(text);
        setFeedback(result);

        if (result.assistive_mode) {
          speakText("Assistive mode activated. Let me read this aloud.");
          speakText(text);
          document.body.style.lineHeight = "1.8";
          document.body.style.fontSize = "22px";
        }
      }
    }, 1200);
    return () => clearTimeout(delayDebounce);
  }, [text]);

  const speakText = (text) => {
    const utter = new SpeechSynthesisUtterance(text);
    utter.rate = 0.9;
    window.speechSynthesis.speak(utter);
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>Mind Mosaic Reader</h2>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste or type your reading passage..."
        rows={8}
        style={{ width: "100%", fontSize: "1.1rem", lineHeight: "1.4" }}
      />
      {feedback && (
        <div style={{ marginTop: "1rem" }}>
          <p><b>Confidence:</b> {feedback.confidence}</p>
          <p><b>Assistive Mode:</b> {feedback.assistive_mode ? "Active" : "Off"}</p>
          <p><b>Patterns:</b> {JSON.stringify(feedback.patterns)}</p>
        </div>
      )}
    </div>
  );
}

