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

          // Note: Auto-read has been disabled - user must click "Read Aloud" button
          // Audio will only play when user explicitly clicks the "Read Aloud" button
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
    <div style={{ 
      padding: "2rem", 
      maxWidth: "1200px", 
      margin: "0 auto",
      background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      minHeight: "100vh",
      borderRadius: "0"
    }}>
      <header style={{ 
        marginBottom: "2rem", 
        textAlign: "center",
        background: "rgba(255, 255, 255, 0.95)",
        padding: "2rem",
        borderRadius: "20px",
        boxShadow: "0 20px 40px rgba(0,0,0,0.1)",
        backdropFilter: "blur(10px)"
      }}>
        <h1 style={{ 
          color: "#2c3e50", 
          marginBottom: "0.5rem",
          fontSize: "2.5rem",
          fontWeight: "700",
          background: "linear-gradient(45deg, #667eea, #764ba2)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
          backgroundClip: "text"
        }}>
          🏥 Medical Reading Assistant
        </h1>
        <p style={{ 
          color: "#5a6c7d", 
          fontSize: "1.2rem",
          fontWeight: "500"
        }}>
          🤖 Agentic AI for Dyslexia-Friendly Medical Information
        </p>
      </header>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "2rem", marginBottom: "2rem" }}>
        {/* Input Section */}
        <div style={{
          background: "rgba(255, 255, 255, 0.95)",
          padding: "1.5rem",
          borderRadius: "15px",
          boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
          backdropFilter: "blur(10px)"
        }}>
          <h3 style={{ 
            color: "#2c3e50", 
            marginBottom: "1rem",
            fontSize: "1.3rem",
            fontWeight: "600"
          }}>📝 Medical Text Input</h3>
          <div style={{ marginBottom: "1rem" }}>
            <button 
              onClick={loadDemoText}
              style={{
                padding: "0.7rem 1.2rem",
                background: "linear-gradient(45deg, #667eea, #764ba2)",
                color: "white",
                border: "none",
                borderRadius: "25px",
                cursor: "pointer",
                marginRight: "1rem",
                fontWeight: "600",
                boxShadow: "0 4px 15px rgba(102, 126, 234, 0.3)",
                transition: "all 0.3s ease"
              }}
            >
              🚀 Load Demo Text
            </button>
            <button 
              onClick={() => { setText(""); setAnalysis(null); resetStyles(); }}
              style={{
                padding: "0.7rem 1.2rem",
                background: "linear-gradient(45deg, #ff6b6b, #ee5a24)",
                color: "white",
                border: "none",
                borderRadius: "25px",
                cursor: "pointer",
                fontWeight: "600",
                boxShadow: "0 4px 15px rgba(255, 107, 107, 0.3)",
                transition: "all 0.3s ease"
              }}
            >
              🗑️ Clear
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
              border: "2px solid #e1e8ed",
              borderRadius: "15px",
              fontFamily: "Arial, sans-serif",
              background: "rgba(255, 255, 255, 0.8)",
              backdropFilter: "blur(5px)",
              boxShadow: "inset 0 2px 10px rgba(0,0,0,0.05)",
              transition: "all 0.3s ease"
            }}
          />
          {isAnalyzing && (
            <div style={{ 
              marginTop: "1rem", 
              color: "#667eea", 
              fontStyle: "italic",
              fontWeight: "600",
              textAlign: "center",
              padding: "0.5rem",
              background: "rgba(102, 126, 234, 0.1)",
              borderRadius: "10px"
            }}>
              🤖 Agentic AI analyzing text...
            </div>
          )}
        </div>

        {/* Analysis Results */}
        <div style={{
          background: "rgba(255, 255, 255, 0.95)",
          padding: "1.5rem",
          borderRadius: "15px",
          boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
          backdropFilter: "blur(10px)"
        }}>
          <h3 style={{ 
            color: "#2c3e50", 
            marginBottom: "1rem",
            fontSize: "1.3rem",
            fontWeight: "600"
          }}>🤖 Agentic AI Analysis & Adaptations</h3>
          {analysis ? (
            <div style={{ 
              background: "linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)", 
              padding: "1.5rem", 
              borderRadius: "12px",
              border: "1px solid rgba(255,255,255,0.2)",
              boxShadow: "0 5px 15px rgba(0,0,0,0.08)"
            }}>
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
                <strong>🤖 Analysis Method:</strong> {analysis.llm_enabled ? "Agentic AI using LLM" : "Rule-based Analysis"}
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
              background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", 
              padding: "2rem", 
              borderRadius: "12px",
              textAlign: "center",
              color: "white",
              fontWeight: "500"
            }}>
              <div style={{ fontSize: "2rem", marginBottom: "1rem" }}>🤖</div>
              Enter medical text to see Agentic AI analysis and dyslexia-friendly adaptations
            </div>
          )}
        </div>
      </div>

      {/* Simplified Text Display */}
      {analysis?.simplified_text && analysis.simplified_text !== text && (
        <div style={{ 
          marginTop: "2rem",
          background: "rgba(255, 255, 255, 0.95)",
          padding: "2rem",
          borderRadius: "20px",
          boxShadow: "0 15px 35px rgba(0,0,0,0.1)",
          backdropFilter: "blur(10px)"
        }}>
          <h3 style={{ 
            color: "#2c3e50", 
            marginBottom: "1.5rem",
            fontSize: "1.5rem",
            fontWeight: "600",
            textAlign: "center"
          }}>📖 Simplified Version</h3>
          <div style={{
            background: "linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%)",
            padding: "2rem",
            borderRadius: "15px",
            border: "2px solid #27ae60",
            fontSize: analysis.visual_adaptations?.font_size || "1rem",
            lineHeight: analysis.visual_adaptations?.line_height || "1.5",
            boxShadow: "0 5px 15px rgba(39, 174, 96, 0.2)"
          }}>
            {analysis.simplified_text}
          </div>
          <div style={{ marginTop: "1rem", textAlign: "center" }}>
            <div style={{ display: "flex", justifyContent: "center", gap: "0.5rem", flexWrap: "wrap" }}>
              {!isReading ? (
                <button 
                  onClick={() => speakText(analysis.simplified_text)}
                  style={{
                    padding: "1rem 2rem",
                    background: "linear-gradient(45deg, #27ae60, #2ecc71)",
                    color: "white",
                    border: "none",
                    borderRadius: "25px",
                    cursor: "pointer",
                    fontSize: "1.1rem",
                    display: "flex",
                    alignItems: "center",
                    gap: "0.5rem",
                    fontWeight: "600",
                    boxShadow: "0 6px 20px rgba(39, 174, 96, 0.3)",
                    transition: "all 0.3s ease"
                  }}
                >
                  🔊 Read Aloud
                </button>
              ) : (
                <>
                  <button 
                    onClick={pauseReading}
                    style={{
                      padding: "1rem 1.5rem",
                      background: "linear-gradient(45deg, #f39c12, #e67e22)",
                      color: "white",
                      border: "none",
                      borderRadius: "25px",
                      cursor: "pointer",
                      fontSize: "1rem",
                      display: "flex",
                      alignItems: "center",
                      gap: "0.5rem",
                      fontWeight: "600",
                      boxShadow: "0 4px 15px rgba(243, 156, 18, 0.3)",
                      transition: "all 0.3s ease"
                    }}
                  >
                    ⏸️ Pause
                  </button>
                  <button 
                    onClick={resumeReading}
                    style={{
                      padding: "1rem 1.5rem",
                      background: "linear-gradient(45deg, #3498db, #2980b9)",
                      color: "white",
                      border: "none",
                      borderRadius: "25px",
                      cursor: "pointer",
                      fontSize: "1rem",
                      display: "flex",
                      alignItems: "center",
                      gap: "0.5rem",
                      fontWeight: "600",
                      boxShadow: "0 4px 15px rgba(52, 152, 219, 0.3)",
                      transition: "all 0.3s ease"
                    }}
                  >
                    ▶️ Resume
                  </button>
                  <button 
                    onClick={stopReading}
                    style={{
                      padding: "1rem 1.5rem",
                      background: "linear-gradient(45deg, #e74c3c, #c0392b)",
                      color: "white",
                      border: "none",
                      borderRadius: "25px",
                      cursor: "pointer",
                      fontSize: "1rem",
                      display: "flex",
                      alignItems: "center",
                      gap: "0.5rem",
                      fontWeight: "600",
                      boxShadow: "0 4px 15px rgba(231, 76, 60, 0.3)",
                      transition: "all 0.3s ease"
                    }}
                  >
                    ⏹️ Stop
                  </button>
                </>
              )}
            </div>
            {isReading && (
              <div style={{ 
                marginTop: "1rem", 
                color: "#27ae60", 
                fontSize: "1rem",
                fontWeight: "600",
                textAlign: "center",
                padding: "0.5rem",
                background: "rgba(39, 174, 96, 0.1)",
                borderRadius: "10px"
              }}>
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

