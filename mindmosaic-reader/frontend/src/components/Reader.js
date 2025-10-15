import React, { useState, useEffect } from "react";
import { analyzeMedicalText, getUserProfile } from "../api";

export default function MedicalReadingAssistant() {
  const [text, setText] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [userProfile, setUserProfile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isReading, setIsReading] = useState(false);
  const [currentUtterance, setCurrentUtterance] = useState(null);

  // Demo medical text
  const demoText = `Take 2 tablets by mouth twice daily with food. Monitor for side effects including nausea, dizziness, and allergic reactions. Contact your physician if symptoms persist or worsen.`;

  useEffect(() => {
    const delayDebounce = setTimeout(async () => {
      if (text.trim().length > 10) {
        setIsAnalyzing(true);
        try {
          console.log("Sending text for analysis:", text);
          const result = await analyzeMedicalText(text);
          console.log("Received analysis result:", result);
          setAnalysis(result);
          
          // Apply visual adaptations
          if (result.visual_adaptations) {
            document.body.style.fontSize = result.visual_adaptations.font_size;
            document.body.style.lineHeight = result.visual_adaptations.line_height;
            
            if (result.visual_adaptations.color_scheme === "high_contrast") {
              document.body.style.backgroundColor = "#f8f8f8";
              document.body.style.color = "#333";
            }
          }

          // Auto-read if audio support is needed
          if (result.audio_suggestions?.should_read_aloud) {
            speakText("Medical reading assistant activated. Let me read this aloud.");
            setTimeout(() => speakText(result.simplified_text), 1500);
          }
        } catch (error) {
          console.error("Analysis error:", error);
          // Set a fallback analysis result
          setAnalysis({
            original_text: text,
            complexity_score: 0.5,
            medical_terms_found: [],
            simplified_text: text,
            visual_adaptations: { font_size: "16px", line_height: 1.5, color_scheme: "default" },
            audio_suggestions: { should_read_aloud: false, reading_speed: 1.0, emphasize_terms: false },
            safety_highlights: [],
            user_progress: { texts_read: 0, comprehension_rate: 0.0 },
            confidence: 0.0,
            llm_enabled: false,
            analysis_method: "Error - Rule-based fallback",
            error: error.message
          });
        } finally {
          setIsAnalyzing(false);
        }
      } else {
        setAnalysis(null);
        // Reset styles
        document.body.style.fontSize = "";
        document.body.style.lineHeight = "";
        document.body.style.backgroundColor = "";
        document.body.style.color = "";
      }
    }, 1500);
    return () => clearTimeout(delayDebounce);
  }, [text]);

  useEffect(() => {
    // Load user profile and test API connection
    getUserProfile()
      .then(profile => {
        console.log("User profile loaded:", profile);
        setUserProfile(profile);
      })
      .catch(error => {
        console.error("Failed to load user profile:", error);
      });
  }, []);

  const speakText = (text) => {
    // Stop any current speech
    window.speechSynthesis.cancel();
    
    const utter = new SpeechSynthesisUtterance(text);
    utter.rate = 0.8;
    utter.pitch = 1.0;
    
    // Set up event listeners
    utter.onstart = () => {
      setIsReading(true);
      setCurrentUtterance(utter);
    };
    
    utter.onend = () => {
      setIsReading(false);
      setCurrentUtterance(null);
    };
    
    utter.onerror = () => {
      setIsReading(false);
      setCurrentUtterance(null);
    };
    
    window.speechSynthesis.speak(utter);
  };

  const pauseReading = () => {
    if (window.speechSynthesis.speaking) {
      window.speechSynthesis.pause();
      setIsReading(false);
    }
  };

  const resumeReading = () => {
    if (window.speechSynthesis.paused) {
      window.speechSynthesis.resume();
      setIsReading(true);
    }
  };

  const stopReading = () => {
    window.speechSynthesis.cancel();
    setIsReading(false);
    setCurrentUtterance(null);
  };

  const loadDemoText = () => {
    setText(demoText);
  };

  const resetStyles = () => {
    document.body.style.fontSize = "";
    document.body.style.lineHeight = "";
    document.body.style.backgroundColor = "";
    document.body.style.color = "";
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "1200px", margin: "0 auto" }}>
      <header style={{ marginBottom: "2rem", textAlign: "center" }}>
        <h1 style={{ color: "#2c3e50", marginBottom: "0.5rem" }}>
          🏥 Medical Reading Assistant
        </h1>
        <p style={{ color: "#7f8c8d", fontSize: "1.1rem" }}>
          Agentic AI for Dyslexia-Friendly Medical Information
        </p>
      </header>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "2rem", marginBottom: "2rem" }}>
        {/* Input Section */}
        <div>
          <h3 style={{ color: "#34495e", marginBottom: "1rem" }}>Medical Text Input</h3>
          <div style={{ marginBottom: "1rem" }}>
            <button 
              onClick={loadDemoText}
              style={{
                padding: "0.5rem 1rem",
                backgroundColor: "#3498db",
                color: "white",
                border: "none",
                borderRadius: "4px",
                cursor: "pointer",
                marginRight: "1rem"
              }}
            >
              Load Demo Text
            </button>
            <button 
              onClick={() => { setText(""); setAnalysis(null); resetStyles(); }}
              style={{
                padding: "0.5rem 1rem",
                backgroundColor: "#95a5a6",
                color: "white",
                border: "none",
                borderRadius: "4px",
                cursor: "pointer"
              }}
            >
              Clear
            </button>
          </div>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste medical instructions, prescription labels, or health information here..."
            rows={12}
            style={{ 
              width: "100%", 
              fontSize: "1rem", 
              lineHeight: "1.5",
              padding: "1rem",
              border: "2px solid #bdc3c7",
              borderRadius: "8px",
              fontFamily: "Arial, sans-serif"
            }}
          />
          {isAnalyzing && (
            <div style={{ marginTop: "1rem", color: "#3498db", fontStyle: "italic" }}>
              🤖 AI Agent analyzing text...
            </div>
          )}
        </div>

        {/* Analysis Results */}
        <div>
          <h3 style={{ color: "#34495e", marginBottom: "1rem" }}>AI Analysis & Adaptations</h3>
          {analysis ? (
            <div style={{ backgroundColor: "#ecf0f1", padding: "1rem", borderRadius: "8px" }}>
              {/* Complexity & Confidence */}
              <div style={{ marginBottom: "1rem" }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.5rem" }}>
                  <span><strong>Complexity Score:</strong></span>
                  <span style={{ 
                    backgroundColor: analysis.complexity_score > 0.6 ? "#e74c3c" : analysis.complexity_score > 0.3 ? "#f39c12" : "#27ae60",
                    color: "white",
                    padding: "0.2rem 0.5rem",
                    borderRadius: "4px"
                  }}>
                    {(analysis.complexity_score * 100).toFixed(0)}%
                  </span>
                </div>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.5rem" }}>
                  <span><strong>Confidence:</strong></span>
                  <span style={{ color: "#27ae60", fontWeight: "bold" }}>
                    {(analysis.confidence * 100).toFixed(0)}%
                  </span>
                </div>
              </div>

              {/* Medical Terms Found */}
              {analysis.medical_terms_found?.length > 0 && (
                <div style={{ marginBottom: "1rem" }}>
                  <strong>Medical Terms Detected:</strong>
                  <div style={{ marginTop: "0.5rem" }}>
                    {analysis.medical_terms_found.map((term, idx) => (
                      <div key={idx} style={{ 
                        backgroundColor: "#d5dbdb", 
                        padding: "0.3rem 0.5rem", 
                        margin: "0.2rem 0",
                        borderRadius: "4px",
                        fontSize: "0.9rem"
                      }}>
                        <strong>{term.term}:</strong> {term.definition}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Safety Highlights */}
              {analysis.safety_highlights?.length > 0 && (
                <div style={{ marginBottom: "1rem" }}>
                  <strong style={{ color: "#e74c3c" }}>⚠️ Safety Instructions:</strong>
                  <div style={{ marginTop: "0.5rem" }}>
                    {analysis.safety_highlights.map((safety, idx) => (
                      <div key={idx} style={{ 
                        backgroundColor: "#fadbd8", 
                        padding: "0.5rem", 
                        margin: "0.2rem 0",
                        borderRadius: "4px",
                        borderLeft: "4px solid #e74c3c"
                      }}>
                        {safety}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Analysis Method */}
              <div style={{ marginTop: "1rem", padding: "0.5rem", backgroundColor: analysis.llm_enabled ? "#e8f5e8" : "#fff3cd", borderRadius: "4px" }}>
                <strong>🤖 Analysis Method:</strong> {analysis.analysis_method || "Unknown"}
                {analysis.llm_enabled ? (
                  <span style={{ color: "#27ae60", marginLeft: "0.5rem" }}>⚡ Groq LLM Enhanced</span>
                ) : (
                  <span style={{ color: "#856404", marginLeft: "0.5rem" }}>⚠️ Rule-based Only</span>
                )}
              </div>

              {/* User Progress */}
              {analysis.user_progress && (
                <div style={{ marginTop: "1rem", padding: "0.5rem", backgroundColor: "#d5f4e6", borderRadius: "4px" }}>
                  <strong>📊 Reading Progress:</strong><br/>
                  Texts analyzed: {analysis.user_progress.texts_read}
                </div>
              )}
            </div>
          ) : (
            <div style={{ 
              backgroundColor: "#f8f9fa", 
              padding: "2rem", 
              borderRadius: "8px",
              textAlign: "center",
              color: "#6c757d"
            }}>
              Enter medical text to see AI analysis and dyslexia-friendly adaptations
            </div>
          )}
        </div>
      </div>

      {/* Simplified Text Display */}
      {analysis?.simplified_text && analysis.simplified_text !== text && (
        <div style={{ marginTop: "2rem" }}>
          <h3 style={{ color: "#34495e", marginBottom: "1rem" }}>📖 Simplified Version</h3>
          <div style={{
            backgroundColor: "#e8f5e8",
            padding: "1.5rem",
            borderRadius: "8px",
            border: "2px solid #27ae60",
            fontSize: analysis.visual_adaptations?.font_size || "1rem",
            lineHeight: analysis.visual_adaptations?.line_height || "1.5"
          }}>
            {analysis.simplified_text}
          </div>
          <div style={{ marginTop: "1rem", textAlign: "center" }}>
            <div style={{ display: "flex", justifyContent: "center", gap: "0.5rem", flexWrap: "wrap" }}>
              {!isReading ? (
                <button 
                  onClick={() => speakText(analysis.simplified_text)}
                  style={{
                    padding: "0.8rem 1.5rem",
                    backgroundColor: "#27ae60",
                    color: "white",
                    border: "none",
                    borderRadius: "6px",
                    cursor: "pointer",
                    fontSize: "1rem",
                    display: "flex",
                    alignItems: "center",
                    gap: "0.5rem"
                  }}
                >
                  🔊 Read Aloud
                </button>
              ) : (
                <>
                  <button 
                    onClick={pauseReading}
                    style={{
                      padding: "0.8rem 1.5rem",
                      backgroundColor: "#f39c12",
                      color: "white",
                      border: "none",
                      borderRadius: "6px",
                      cursor: "pointer",
                      fontSize: "1rem",
                      display: "flex",
                      alignItems: "center",
                      gap: "0.5rem"
                    }}
                  >
                    ⏸️ Pause
                  </button>
                  <button 
                    onClick={resumeReading}
                    style={{
                      padding: "0.8rem 1.5rem",
                      backgroundColor: "#3498db",
                      color: "white",
                      border: "none",
                      borderRadius: "6px",
                      cursor: "pointer",
                      fontSize: "1rem",
                      display: "flex",
                      alignItems: "center",
                      gap: "0.5rem"
                    }}
                  >
                    ▶️ Resume
                  </button>
                  <button 
                    onClick={stopReading}
                    style={{
                      padding: "0.8rem 1.5rem",
                      backgroundColor: "#e74c3c",
                      color: "white",
                      border: "none",
                      borderRadius: "6px",
                      cursor: "pointer",
                      fontSize: "1rem",
                      display: "flex",
                      alignItems: "center",
                      gap: "0.5rem"
                    }}
                  >
                    ⏹️ Stop
                  </button>
                </>
              )}
            </div>
            {isReading && (
              <div style={{ marginTop: "0.5rem", color: "#27ae60", fontSize: "0.9rem" }}>
                🔊 Reading aloud...
              </div>
            )}
          </div>
        </div>
      )}

      {/* User Profile Display */}
      {userProfile && (
        <div style={{ marginTop: "2rem", padding: "1rem", backgroundColor: "#f8f9fa", borderRadius: "8px" }}>
          <h4 style={{ color: "#34495e", marginBottom: "0.5rem" }}>👤 User Profile</h4>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "1rem" }}>
            <div>
              <strong>Dyslexia Severity:</strong> {userProfile.dyslexia_severity}
            </div>
            <div>
              <strong>Texts Analyzed:</strong> {userProfile.reading_progress?.texts_read || 0}
            </div>
            <div>
              <strong>Medical Terms Learned:</strong> {userProfile.medical_terms_learned?.size || 0}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

