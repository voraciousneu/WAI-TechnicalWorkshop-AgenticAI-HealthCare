import re
import json
import os
from collections import Counter
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

class MedicalDyslexiaAgent:
    def __init__(self):
        self.user_profile = {
            "dyslexia_severity": "moderate",  # mild, moderate, severe
            "preferred_adaptations": [],
            "reading_progress": {"texts_read": 0, "comprehension_rate": 0.0},
            "medical_terms_learned": set()
        }
        self.medical_terms_db = self._load_medical_terms()
        
        # Initialize Groq client
        self.groq_client = None
        self.llm_enabled = False
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize Groq client if API key is available"""
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            try:
                self.groq_client = Groq(api_key=api_key)
                # Test the connection with a simple request
                test_response = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=1
                )
                self.llm_enabled = True
                print("✅ LLM integration enabled with Groq")
            except Exception as e:
                print(f"⚠️ LLM initialization failed: {e}")
                self.llm_enabled = False
        else:
            print("⚠️ No GROQ_API_KEY found - using rule-based analysis only")
            self.llm_enabled = False
        
    def _load_medical_terms(self) -> Dict[str, str]:
        """Load common medical terms with simplified definitions"""
        return {
            "nausea": "feeling sick to your stomach",
            "dizziness": "feeling lightheaded or like you might faint",
            "allergic reactions": "when your body reacts badly to something",
            "physician": "doctor",
            "symptoms": "signs that something is wrong with your body",
            "persist": "continue or keep happening",
            "worsen": "get worse",
            "dosage": "how much medicine to take",
            "tablets": "pills",
            "monitor": "watch carefully",
            "side effects": "unwanted things that can happen when you take medicine",
            "prescription": "doctor's order for medicine"
        }

    def analyze_medical_text(self, text: str, user_context: Dict = None) -> Dict[str, Any]:
        """
        Agentic analysis of medical text for dyslexia support with LLM integration
        """
        # 1. PERCEIVE: Analyze text complexity and medical content
        if self.llm_enabled:
            analysis = self._llm_analyze_text(text)
        else:
            analysis = self._perceive_text_complexity(text)
        
        # 2. REASON: Determine appropriate interventions
        interventions = self._reason_about_interventions(analysis, user_context)
        
        # 3. ACT: Generate adapted content and suggestions
        if self.llm_enabled:
            adapted_content = self._llm_adapt_content(text, analysis, interventions)
        else:
            adapted_content = self._act_with_adaptations(text, interventions)
        
        # 4. LEARN: Update user profile based on interaction
        self._learn_from_interaction(text, interventions)
        
        return {
            "original_text": text,
            "complexity_score": analysis["complexity_score"],
            "medical_terms_found": analysis["medical_terms"],
            "simplified_text": adapted_content["simplified"],
            "visual_adaptations": adapted_content["visual"],
            "audio_suggestions": adapted_content["audio"],
            "safety_highlights": adapted_content["safety"],
            "user_progress": self.user_profile["reading_progress"],
            "confidence": analysis["confidence"],
            "llm_enabled": self.llm_enabled,
            "analysis_method": "LLM" if self.llm_enabled else "Rule-based"
        }

    def _perceive_text_complexity(self, text: str) -> Dict[str, Any]:
        """Analyze text complexity and extract medical terms"""
        text_lower = text.lower()
        
        # Find medical terms
        medical_terms = []
        for term, definition in self.medical_terms_db.items():
            if term in text_lower:
                medical_terms.append({"term": term, "definition": definition})
        
        # Calculate complexity score
        complexity_score = 0.0
        
        # Sentence length factor
        sentences = re.split(r'[.!?]+', text)
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        if avg_sentence_length > 15:
            complexity_score += 0.3
        
        # Medical terminology factor
        complexity_score += min(len(medical_terms) * 0.1, 0.4)
        
        # Word difficulty factor (simplified)
        complex_words = ["monitor", "physician", "allergic", "persist", "worsen"]
        for word in complex_words:
            if word in text_lower:
                complexity_score += 0.1
        
        # Dyslexia pattern detection
        dyslexia_indicators = self._detect_dyslexia_patterns(text)
        complexity_score += dyslexia_indicators * 0.2
        
        confidence = min(complexity_score + 0.3, 1.0)  # Base confidence
        
        return {
            "complexity_score": min(complexity_score, 1.0),
            "medical_terms": medical_terms,
            "dyslexia_indicators": dyslexia_indicators,
            "confidence": confidence
        }

    def _detect_dyslexia_patterns(self, text: str) -> float:
        """Detect dyslexia-related reading challenges"""
        text_lower = text.lower()
        score = 0.0
        
        # Letter reversals
        reversals = re.findall(r'\b[bdpq]\b', text_lower)
        score += len(reversals) * 0.1
        
        # Transpositions (simplified detection)
        words = text_lower.split()
        for word in words:
            if len(word) > 3:
                # Check for common transpositions
                if word.replace('rn', 'm') in words or word.replace('m', 'rn') in words:
                    score += 0.1
        
        return min(score, 0.5)

    def _reason_about_interventions(self, analysis: Dict, user_context: Dict) -> Dict[str, Any]:
        """Determine what interventions are needed"""
        interventions = {
            "needs_simplification": analysis["complexity_score"] > 0.4,
            "needs_visual_support": analysis["dyslexia_indicators"] > 0.2,
            "needs_audio_support": analysis["complexity_score"] > 0.3,
            "needs_safety_emphasis": len(analysis["medical_terms"]) > 2,
            "font_size_multiplier": 1.2 if analysis["dyslexia_indicators"] > 0.2 else 1.0,
            "line_height_multiplier": 1.6 if analysis["dyslexia_indicators"] > 0.3 else 1.4
        }
        
        return interventions

    def _act_with_adaptations(self, text: str, interventions: Dict) -> Dict[str, Any]:
        """Generate adapted content and visual suggestions"""
        adapted = {
            "simplified": self._simplify_medical_text(text, interventions),
            "visual": {
                "font_size": f"{int(16 * interventions['font_size_multiplier'])}px",
                "line_height": interventions["line_height_multiplier"],
                "color_scheme": "high_contrast" if interventions["needs_visual_support"] else "default"
            },
            "audio": {
                "should_read_aloud": interventions["needs_audio_support"],
                "reading_speed": 0.8 if interventions["needs_audio_support"] else 1.0,
                "emphasize_terms": interventions["needs_safety_emphasis"]
            },
            "safety": self._extract_safety_instructions(text)
        }
        
        return adapted

    def _simplify_medical_text(self, text: str, interventions: Dict) -> str:
        """Simplify medical text for better comprehension"""
        if not interventions["needs_simplification"]:
            return text
            
        simplified = text
        
        # Replace medical terms with definitions
        for term, definition in self.medical_terms_db.items():
            if term in text.lower():
                # Add definition in parentheses
                pattern = re.compile(re.escape(term), re.IGNORECASE)
                simplified = pattern.sub(f"{term} ({definition})", simplified)
        
        # Break long sentences
        sentences = re.split(r'([.!?]+)', simplified)
        result_sentences = []
        
        for i in range(0, len(sentences), 2):
            if i < len(sentences):
                sentence = sentences[i].strip()
                if len(sentence.split()) > 15:
                    # Simple sentence breaking
                    words = sentence.split()
                    mid_point = len(words) // 2
                    first_part = ' '.join(words[:mid_point])
                    second_part = ' '.join(words[mid_point:])
                    result_sentences.append(first_part + '.')
                    result_sentences.append(second_part + (sentences[i+1] if i+1 < len(sentences) else ''))
                else:
                    result_sentences.append(sentence + (sentences[i+1] if i+1 < len(sentences) else ''))
        
        return ' '.join(result_sentences)

    def _extract_safety_instructions(self, text: str) -> List[str]:
        """Extract critical safety information"""
        safety_terms = ["contact", "emergency", "stop", "immediately", "warning", "caution"]
        safety_sentences = []
        
        sentences = re.split(r'[.!?]+', text)
        for sentence in sentences:
            if any(term in sentence.lower() for term in safety_terms):
                safety_sentences.append(sentence.strip())
        
        return safety_sentences

    def _learn_from_interaction(self, text: str, interventions: Dict):
        """Update user profile based on interaction"""
        self.user_profile["reading_progress"]["texts_read"] += 1
        
        # Simple learning: if high complexity led to many interventions, user may need more support
        if interventions["needs_simplification"] and interventions["needs_visual_support"]:
            if self.user_profile["dyslexia_severity"] == "mild":
                self.user_profile["dyslexia_severity"] = "moderate"
        
        # Track medical terms encountered
        for term in self.medical_terms_db.keys():
            if term in text.lower():
                self.user_profile["medical_terms_learned"].add(term)

    def _llm_analyze_text(self, text: str) -> Dict[str, Any]:
        """Use Groq LLM to analyze medical text complexity and extract insights"""
        try:
            system_prompt = """You are a medical AI assistant specialized in analyzing text for dyslexia accessibility. 
            Analyze the given medical text and provide:
            1. A complexity score (0.0-1.0) based on medical terminology, sentence structure, and reading difficulty
            2. List of medical terms found with simple definitions
            3. Dyslexia-specific challenges (visual processing, phonological awareness, working memory)
            4. Confidence level in your analysis
            
            Respond in JSON format with keys: complexity_score, medical_terms, dyslexia_indicators, confidence"""
            
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Groq's versatile model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this medical text: {text}"}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Parse LLM response
            llm_analysis = json.loads(response.choices[0].message.content)
            
            # Ensure medical_terms is a list of dicts
            if isinstance(llm_analysis.get("medical_terms"), dict):
                medical_terms = [{"term": k, "definition": v} for k, v in llm_analysis["medical_terms"].items()]
            else:
                medical_terms = llm_analysis.get("medical_terms", [])
            
            return {
                "complexity_score": float(llm_analysis.get("complexity_score", 0.5)),
                "medical_terms": medical_terms,
                "dyslexia_indicators": float(llm_analysis.get("dyslexia_indicators", 0.2)),
                "confidence": float(llm_analysis.get("confidence", 0.8))
            }
            
        except Exception as e:
            print(f"⚠️ Groq LLM analysis failed: {e}, falling back to rule-based")
            return self._perceive_text_complexity(text)

    def _llm_adapt_content(self, text: str, analysis: Dict, interventions: Dict) -> Dict[str, Any]:
        """Use Groq LLM to generate adapted content and suggestions"""
        try:
            system_prompt = """You are a medical AI assistant specialized in making medical text accessible for people with dyslexia.
            
            Based on the analysis provided, generate:
            1. A simplified version of the medical text that maintains accuracy but improves readability
            2. Visual adaptation recommendations (font size, line height, color scheme)
            3. Audio suggestions (reading speed, emphasis)
            4. Safety highlights (critical medical information that needs emphasis)
            
            Respond in JSON format with keys: simplified, visual, audio, safety"""
            
            user_prompt = f"""
            Original text: {text}
            Analysis: {json.dumps(analysis)}
            Interventions needed: {json.dumps(interventions)}
            
            Generate dyslexia-friendly adaptations."""
            
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Groq's versatile model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            # Parse LLM response
            llm_adaptations = json.loads(response.choices[0].message.content)
            
            return {
                "simplified": llm_adaptations.get("simplified", text),
                "visual": {
                    "font_size": llm_adaptations.get("visual", {}).get("font_size", "18px"),
                    "line_height": llm_adaptations.get("visual", {}).get("line_height", 1.6),
                    "color_scheme": llm_adaptations.get("visual", {}).get("color_scheme", "high_contrast")
                },
                "audio": {
                    "should_read_aloud": llm_adaptations.get("audio", {}).get("should_read_aloud", True),
                    "reading_speed": llm_adaptations.get("audio", {}).get("reading_speed", 0.8),
                    "emphasize_terms": llm_adaptations.get("audio", {}).get("emphasize_terms", True)
                },
                "safety": llm_adaptations.get("safety", [])
            }
            
        except Exception as e:
            print(f"⚠️ Groq LLM adaptation failed: {e}, falling back to rule-based")
            return self._act_with_adaptations(text, interventions)

# Maintain backward compatibility
DyslexiaAssistAgent = MedicalDyslexiaAgent

