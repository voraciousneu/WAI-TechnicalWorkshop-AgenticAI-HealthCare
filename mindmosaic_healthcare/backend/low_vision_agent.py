"""
MindMosaic Healthcare - Low Vision Patient Agentic AI
Agentic AI for Healthcare Accessibility - Low Vision Use Case
"""

import os
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

@dataclass
class PatientProfile:
    """Patient profile for low vision accessibility"""
    patient_id: str
    visual_acuity: str  # mild, moderate, severe, legally_blind
    preferred_voice_settings: Dict[str, Any]
    form_completion_patterns: List[Dict[str, Any]]
    stress_indicators: List[Dict[str, Any]]
    independence_level: float  # 0.0-1.0
    accessibility_needs: List[str]

@dataclass
class FormField:
    """Medical form field structure"""
    field_id: str
    field_type: str  # text, dropdown, checkbox, date, etc.
    label: str
    value: str
    required: bool
    validation_rules: List[str]
    error_message: Optional[str] = None

@dataclass
class MedicalForm:
    """Medical form structure"""
    form_id: str
    form_type: str  # registration, insurance, medical_history, etc.
    fields: List[FormField]
    completion_status: float  # 0.0-1.0
    errors: List[Dict[str, Any]]

class LowVisionHealthcareAgent:
    """
    Agentic AI for Low Vision Healthcare Accessibility
    
    PERCEIVE → REASON → ACT → LEARN cycle for healthcare form assistance
    """
    
    def __init__(self):
        # Initialize Groq LLM
        self.groq_client = None
        self.llm_enabled = False
        self._initialize_llm()
        
        # Agentic state
        self.patient_profiles = {}
        self.form_adaptations = {}
        self.voice_guidance_history = {}
        
        # Low vision accessibility knowledge
        self.visual_acuity_levels = {
            "mild": {"contrast": "enhanced", "font_size": "large", "voice_speed": 0.9},
            "moderate": {"contrast": "high", "font_size": "extra_large", "voice_speed": 0.8},
            "severe": {"contrast": "maximum", "font_size": "huge", "voice_speed": 0.7},
            "legally_blind": {"contrast": "maximum", "font_size": "huge", "voice_speed": 0.6}
        }
        
        self.form_error_types = {
            "required_field_missing": "This field is required",
            "invalid_format": "Please check the format",
            "invalid_date": "Please enter a valid date",
            "invalid_phone": "Please enter a valid phone number",
            "invalid_email": "Please enter a valid email address",
            "insurance_id_invalid": "Please check your insurance ID",
            "date_of_birth_invalid": "Please check your date of birth"
        }
    
    def _initialize_llm(self):
        """Initialize Groq client for healthcare form analysis"""
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            try:
                self.groq_client = Groq(api_key=api_key)
                # Test connection
                test_response = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=1
                )
                self.llm_enabled = True
                print("✅ Low Vision Healthcare Agentic AI enabled with Groq")
            except Exception as e:
                print(f"⚠️ LLM initialization failed: {e}")
                self.llm_enabled = False
        else:
            print("⚠️ No GROQ_API_KEY found - using rule-based analysis only")
            self.llm_enabled = False
    
    def perceive_patient_needs(self, patient_id: str, interaction_data: Dict[str, Any]) -> PatientProfile:
        """
        PERCEIVE: Analyze patient's visual needs and form interaction patterns
        
        Analyzes:
        - Visual acuity level and accessibility requirements
        - Form completion patterns and common errors
        - Stress indicators and support needs
        - Independence level and confidence metrics
        """
        print(f"🔍 PERCEIVING: Analyzing patient {patient_id} visual needs...")
        
        # Extract interaction data
        visual_acuity = interaction_data.get("visual_acuity", "moderate")
        form_interactions = interaction_data.get("form_interactions", [])
        stress_indicators = interaction_data.get("stress_indicators", [])
        completion_times = interaction_data.get("completion_times", [])
        error_patterns = interaction_data.get("error_patterns", [])
        
        # Analyze visual acuity needs
        accessibility_needs = self._determine_accessibility_needs(visual_acuity, interaction_data)
        
        # Analyze form completion patterns
        form_patterns = self._analyze_form_patterns(form_interactions)
        
        # Assess independence level
        independence_level = self._assess_independence_level(completion_times, error_patterns)
        
        # Determine voice preferences
        voice_settings = self._determine_voice_preferences(visual_acuity, interaction_data)
        
        # Create patient profile
        profile = PatientProfile(
            patient_id=patient_id,
            visual_acuity=visual_acuity,
            preferred_voice_settings=voice_settings,
            form_completion_patterns=form_patterns,
            stress_indicators=stress_indicators,
            independence_level=independence_level,
            accessibility_needs=accessibility_needs
        )
        
        self.patient_profiles[patient_id] = profile
        return profile
    
    def reason_about_form_errors(self, form: MedicalForm, patient_profile: PatientProfile) -> Dict[str, Any]:
        """
        REASON: Analyze form errors and determine optimal guidance strategy
        
        Considers:
        - Error severity and impact on form completion
        - Patient's visual acuity and stress level
        - Optimal voice guidance approach
        - Accessibility accommodation priorities
        """
        print(f"🧠 REASONING: Analyzing form errors for patient {patient_profile.patient_id}...")
        
        error_analysis = {
            "critical_errors": [],
            "minor_errors": [],
            "guidance_priority": "high" if len(form.errors) > 3 else "medium",
            "voice_guidance_strategy": "step_by_step",
            "accessibility_accommodations": [],
            "stress_reduction_measures": []
        }
        
        # Categorize errors by severity
        for error in form.errors:
            if error.get("severity") == "critical" or error.get("required", False):
                error_analysis["critical_errors"].append(error)
            else:
                error_analysis["minor_errors"].append(error)
        
        # Determine guidance strategy based on patient needs
        if patient_profile.visual_acuity in ["severe", "legally_blind"]:
            error_analysis["voice_guidance_strategy"] = "detailed_audio_description"
            error_analysis["accessibility_accommodations"].extend([
                "high_contrast", "large_font", "audio_descriptions", "voice_navigation"
            ])
        elif patient_profile.independence_level < 0.5:
            error_analysis["voice_guidance_strategy"] = "supportive_coaching"
            error_analysis["stress_reduction_measures"].extend([
                "encouraging_tone", "progress_praise", "no_pressure_timing"
            ])
        
        # Add visual acuity accommodations
        acuity_settings = self.visual_acuity_levels.get(patient_profile.visual_acuity, {})
        error_analysis["accessibility_accommodations"].extend([
            f"contrast_{acuity_settings.get('contrast', 'enhanced')}",
            f"font_{acuity_settings.get('font_size', 'large')}"
        ])
        
        return error_analysis
    
    def act_with_voice_guidance(self, form: MedicalForm, error_analysis: Dict[str, Any], patient_profile: PatientProfile) -> Dict[str, Any]:
        """
        ACT: Generate voice guidance and accessibility adaptations
        
        Creates:
        - Calm, clear voice instructions for error correction
        - Audio descriptions of form fields and layout
        - Stress-reducing supportive messages
        - Accessibility enhancements for visual needs
        """
        print(f"🎯 ACTING: Generating voice guidance for patient {patient_profile.patient_id}...")
        
        voice_guidance = {
            "audio_instructions": [],
            "error_summaries": [],
            "form_descriptions": [],
            "supportive_messages": [],
            "visual_adaptations": {},
            "navigation_guidance": []
        }
        
        # Generate error correction guidance
        voice_guidance["error_summaries"] = self._generate_error_summaries(
            error_analysis["critical_errors"], 
            patient_profile.visual_acuity
        )
        
        # Create step-by-step audio instructions
        voice_guidance["audio_instructions"] = self._generate_audio_instructions(
            error_analysis["critical_errors"],
            patient_profile.preferred_voice_settings
        )
        
        # Generate form layout descriptions
        voice_guidance["form_descriptions"] = self._generate_form_descriptions(
            form, patient_profile.visual_acuity
        )
        
        # Add supportive and encouraging messages
        voice_guidance["supportive_messages"] = self._generate_supportive_messages(
            patient_profile.independence_level,
            error_analysis["guidance_priority"]
        )
        
        # Apply visual accessibility adaptations
        voice_guidance["visual_adaptations"] = self._apply_visual_adaptations(
            patient_profile.accessibility_needs
        )
        
        # Generate navigation guidance
        voice_guidance["navigation_guidance"] = self._generate_navigation_guidance(
            form, patient_profile.visual_acuity
        )
        
        return voice_guidance
    
    def learn_from_form_completion(self, patient_id: str, completion_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        LEARN: Update agent understanding based on form completion experience
        
        Updates:
        - Patient independence level and confidence
        - Voice guidance effectiveness
        - Error pattern recognition
        - Accessibility accommodation success
        """
        print(f"📚 LEARNING: Updating knowledge from patient {patient_id} form completion...")
        
        # Extract completion metrics
        completion_success = completion_result.get("completed_successfully", False)
        completion_time = completion_result.get("completion_time", 0)
        stress_level = completion_result.get("stress_level", 0.5)
        voice_guidance_effectiveness = completion_result.get("voice_guidance_rating", 0.0)
        independence_improvement = completion_result.get("independence_improvement", 0.0)
        
        # Update patient profile
        if patient_id in self.patient_profiles:
            profile = self.patient_profiles[patient_id]
            
            # Update independence level
            profile.independence_level = min(1.0, profile.independence_level + independence_improvement * 0.1)
            
            # Update form completion patterns
            profile.form_completion_patterns.append({
                "timestamp": datetime.now().isoformat(),
                "completion_success": completion_success,
                "completion_time": completion_time,
                "stress_level": stress_level,
                "voice_guidance_effectiveness": voice_guidance_effectiveness
            })
        
        # Learn guidance effectiveness
        learning_insights = {
            "guidance_effectiveness": {
                "voice_guidance_rating": voice_guidance_effectiveness,
                "completion_improvement": independence_improvement,
                "stress_reduction": 1.0 - stress_level
            },
            "adaptation_recommendations": [],
            "success_patterns": [],
            "improvement_areas": []
        }
        
        # Analyze what worked well
        if completion_success and voice_guidance_effectiveness > 0.8:
            learning_insights["success_patterns"].append("effective_voice_guidance")
        
        if independence_improvement > 0.1:
            learning_insights["success_patterns"].append("independence_building")
        
        # Identify areas for improvement
        if stress_level > 0.7:
            learning_insights["improvement_areas"].append("stress_reduction")
            learning_insights["adaptation_recommendations"].append("calmer_voice_tone")
        
        if not completion_success:
            learning_insights["improvement_areas"].append("guidance_clarity")
            learning_insights["adaptation_recommendations"].append("simpler_instructions")
        
        # Store learning insights
        self.voice_guidance_history[patient_id] = {
            "last_updated": datetime.now().isoformat(),
            "learning_insights": learning_insights,
            "total_completions": len(profile.form_completion_patterns) if patient_id in self.patient_profiles else 0,
            "average_independence": profile.independence_level if patient_id in self.patient_profiles else 0.0
        }
        
        return learning_insights
    
    # Helper methods for each phase
    
    def _determine_accessibility_needs(self, visual_acuity: str, interaction_data: Dict[str, Any]) -> List[str]:
        """Determine accessibility needs based on visual acuity"""
        needs = ["voice_guidance", "audio_descriptions"]
        
        acuity_settings = self.visual_acuity_levels.get(visual_acuity, {})
        
        if acuity_settings.get("contrast") in ["high", "maximum"]:
            needs.append("high_contrast")
        
        if acuity_settings.get("font_size") in ["extra_large", "huge"]:
            needs.append("large_font")
        
        if visual_acuity in ["severe", "legally_blind"]:
            needs.extend(["screen_reader_optimization", "keyboard_navigation"])
        
        return needs
    
    def _analyze_form_patterns(self, form_interactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze patient's form completion patterns"""
        patterns = []
        
        for interaction in form_interactions:
            pattern = {
                "form_type": interaction.get("form_type", "unknown"),
                "completion_time": interaction.get("completion_time", 0),
                "errors_count": len(interaction.get("errors", [])),
                "help_requests": interaction.get("help_requests", 0),
                "voice_guidance_used": interaction.get("voice_guidance_used", False)
            }
            patterns.append(pattern)
        
        return patterns
    
    def _assess_independence_level(self, completion_times: List[int], error_patterns: List[Dict[str, Any]]) -> float:
        """Assess patient's independence level (0.0-1.0)"""
        if not completion_times and not error_patterns:
            return 0.5  # Default moderate independence
        
        # Calculate independence based on completion efficiency and error reduction
        avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else 0
        avg_errors = sum(len(pattern.get("errors", [])) for pattern in error_patterns) / len(error_patterns) if error_patterns else 0
        
        # Normalize to 0.0-1.0 scale (lower time and errors = higher independence)
        time_score = max(0.0, 1.0 - (avg_completion_time / 30.0))  # 30 minutes as baseline
        error_score = max(0.0, 1.0 - (avg_errors / 5.0))  # 5 errors as baseline
        
        return (time_score + error_score) / 2.0
    
    def _determine_voice_preferences(self, visual_acuity: str, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Determine optimal voice settings for patient"""
        acuity_settings = self.visual_acuity_levels.get(visual_acuity, {})
        
        return {
            "voice_speed": acuity_settings.get("voice_speed", 0.8),
            "voice_tone": "calm" if interaction_data.get("stress_level", 0.5) > 0.6 else "professional",
            "pause_duration": 1.5 if visual_acuity in ["severe", "legally_blind"] else 1.0,
            "repeat_instructions": True if visual_acuity in ["severe", "legally_blind"] else False,
            "audio_descriptions": True,
            "progress_updates": True
        }
    
    def _generate_error_summaries(self, critical_errors: List[Dict[str, Any]], visual_acuity: str) -> List[str]:
        """Generate calm, clear error summaries"""
        summaries = []
        
        if not critical_errors:
            summaries.append("Great news! I don't see any errors that need immediate attention.")
            return summaries
        
        # Create supportive error summary
        summaries.append(f"I found {len(critical_errors)} field{'' if len(critical_errors) == 1 else 's'} that need your attention. Don't worry, I'll guide you through each one step by step.")
        
        for i, error in enumerate(critical_errors[:3], 1):  # Limit to 3 for clarity
            field_name = error.get("field_name", "field")
            error_type = error.get("error_type", "missing information")
            
            if visual_acuity in ["severe", "legally_blind"]:
                summaries.append(f"{i}. The {field_name} field needs attention. It appears to be {error_type}.")
            else:
                summaries.append(f"{i}. {field_name}: {error_type}")
        
        return summaries
    
    def _generate_audio_instructions(self, critical_errors: List[Dict[str, Any]], voice_settings: Dict[str, Any]) -> List[str]:
        """Generate step-by-step audio instructions"""
        instructions = []
        
        for i, error in enumerate(critical_errors, 1):
            field_name = error.get("field_name", "this field")
            field_type = error.get("field_type", "text")
            error_message = error.get("error_message", "needs to be completed")
            
            # Create supportive instruction
            instruction = f"Let's fix {field_name}. {error_message}."
            
            # Add specific guidance based on field type
            if field_type == "date":
                instruction += " Please enter your date of birth in MM/DD/YYYY format."
            elif field_type == "phone":
                instruction += " Please enter your phone number as ten digits."
            elif field_type == "email":
                instruction += " Please enter your email address with an @ symbol."
            elif field_type == "insurance_id":
                instruction += " This is usually found on your insurance card."
            
            instructions.append(instruction)
        
        return instructions
    
    def _generate_form_descriptions(self, form: MedicalForm, visual_acuity: str) -> List[str]:
        """Generate audio descriptions of form layout"""
        descriptions = []
        
        if visual_acuity in ["severe", "legally_blind"]:
            descriptions.append(f"This is a {form.form_type} form with {len(form.fields)} sections to complete.")
            
            # Describe form sections
            section_counts = {}
            for field in form.fields:
                section = field.field_type
                section_counts[section] = section_counts.get(section, 0) + 1
            
            for section, count in section_counts.items():
                descriptions.append(f"There are {count} {section} field{'' if count == 1 else 's'} to fill out.")
        
        return descriptions
    
    def _generate_supportive_messages(self, independence_level: float, guidance_priority: str) -> List[str]:
        """Generate encouraging and supportive messages"""
        messages = []
        
        if independence_level < 0.4:
            messages.extend([
                "You're doing great! Take your time with each field.",
                "I'm here to help you every step of the way.",
                "Remember, there's no rush. We'll get through this together."
            ])
        elif guidance_priority == "high":
            messages.extend([
                "I can see several fields that need attention, but don't worry - we'll fix them one by one.",
                "You've got this! Let's tackle these fields together."
            ])
        else:
            messages.extend([
                "Almost there! Just a few more fields to complete.",
                "You're making excellent progress!"
            ])
        
        return messages
    
    def _apply_visual_adaptations(self, accessibility_needs: List[str]) -> Dict[str, Any]:
        """Apply visual accessibility adaptations"""
        adaptations = {
            "font_size": "16px",
            "contrast": "normal",
            "color_scheme": "default",
            "spacing": "normal"
        }
        
        if "high_contrast" in accessibility_needs:
            adaptations["contrast"] = "high"
            adaptations["color_scheme"] = "high_contrast"
        
        if "large_font" in accessibility_needs:
            adaptations["font_size"] = "20px"
            adaptations["spacing"] = "increased"
        
        return adaptations
    
    def _generate_navigation_guidance(self, form: MedicalForm, visual_acuity: str) -> List[str]:
        """Generate navigation guidance for form completion"""
        guidance = []
        
        if visual_acuity in ["severe", "legally_blind"]:
            guidance.extend([
                "You can use the Tab key to move between fields.",
                "Press Enter to submit the form when all fields are complete.",
                "If you need to go back to a previous field, use Shift+Tab."
            ])
        
        return guidance

# Example usage and testing
if __name__ == "__main__":
    # Initialize the low vision healthcare agent
    agent = LowVisionHealthcareAgent()
    
    # Example patient interaction data
    patient_data = {
        "visual_acuity": "moderate",
        "form_interactions": [
            {
                "form_type": "registration",
                "completion_time": 25,
                "errors": [{"field": "insurance_id", "type": "invalid_format"}],
                "help_requests": 2,
                "voice_guidance_used": True
            }
        ],
        "stress_indicators": [{"timestamp": "2024-01-15T10:30:00", "level": 0.7}],
        "completion_times": [25, 20, 30],
        "error_patterns": [
            {"errors": [{"field": "insurance_id", "type": "invalid_format"}]},
            {"errors": [{"field": "phone", "type": "invalid_format"}]}
        ],
        "stress_level": 0.6
    }
    
    # Example medical form with errors
    form_fields = [
        FormField("first_name", "text", "First Name", "Maria", True, ["required"]),
        FormField("last_name", "text", "Last Name", "Garcia", True, ["required"]),
        FormField("insurance_id", "text", "Insurance ID", "12345", True, ["required", "format"]),
        FormField("phone", "text", "Phone Number", "555-123", True, ["required", "phone_format"]),
        FormField("date_of_birth", "date", "Date of Birth", "", True, ["required", "date_format"])
    ]
    
    form = MedicalForm(
        form_id="registration_001",
        form_type="patient_registration",
        fields=form_fields,
        completion_status=0.6,
        errors=[
            {"field_name": "insurance_id", "error_type": "invalid format", "severity": "critical", "required": True, "field_type": "text"},
            {"field_name": "phone", "error_type": "invalid format", "severity": "critical", "required": True, "field_type": "phone"},
            {"field_name": "date_of_birth", "error_type": "missing information", "severity": "critical", "required": True, "field_type": "date"}
        ]
    )
    
    # Run the agentic cycle
    print("🏥 Starting Low Vision Healthcare Agentic AI Demo...")
    
    # PERCEIVE
    profile = agent.perceive_patient_needs("patient_001", patient_data)
    print(f"📊 Patient Profile: {profile.visual_acuity} vision, independence: {profile.independence_level:.2f}")
    
    # REASON
    error_analysis = agent.reason_about_form_errors(form, profile)
    print(f"🧠 Error Analysis: {len(error_analysis['critical_errors'])} critical errors, strategy: {error_analysis['voice_guidance_strategy']}")
    
    # ACT
    voice_guidance = agent.act_with_voice_guidance(form, error_analysis, profile)
    print(f"🎯 Voice Guidance: {len(voice_guidance['audio_instructions'])} instructions, {len(voice_guidance['supportive_messages'])} supportive messages")
    
    # LEARN (simulate completion result)
    completion_result = {
        "completed_successfully": True,
        "completion_time": 18,
        "stress_level": 0.3,
        "voice_guidance_rating": 0.9,
        "independence_improvement": 0.15
    }
    
    learning_insights = agent.learn_from_form_completion("patient_001", completion_result)
    print(f"📚 Learning Insights: {learning_insights['success_patterns']}")
    
    print("✅ Low Vision Healthcare Agentic AI Demo completed!")
    print("\n🎧 Sample Voice Guidance:")
    for i, instruction in enumerate(voice_guidance["audio_instructions"][:2], 1):
        print(f"{i}. \"{instruction}\"")
