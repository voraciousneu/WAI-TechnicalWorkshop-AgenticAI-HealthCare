import re
from collections import Counter

class DyslexiaAssistAgent:
    def __init__(self):
        self.confidence_level = 0.0

    def observe_text(self, text: str, user_speed: float = None):
        features = self.extract_features(text)
        score = self.estimate_indicator(features, user_speed)
        self.confidence_level = (self.confidence_level * 0.7) + (score * 0.3)

        assistive = self.confidence_level > 0.5
        return {
            "confidence": round(self.confidence_level, 2),
            "assistive_mode": assistive,
            "patterns": features
        }

    def extract_features(self, text):
        text = text.lower()
        patterns = Counter()
        # simple dyslexia-related patterns
        reversals = re.findall(r"\b(b|d|p|q)\b", text)
        if reversals:
            patterns["letter_reversals"] += len(reversals)
        transpositions = re.findall(r"\b(\w{3,6})\b", text)
        for w in transpositions:
            if sorted(w) == list(w[::-1]):
                patterns["transpositions"] += 1
        return dict(patterns)

    def estimate_indicator(self, patterns, speed):
        base = 0.0
        base += patterns.get("letter_reversals", 0) * 0.1
        base += patterns.get("transpositions", 0) * 0.05
        if speed and speed < 100:
            base += 0.2
        return min(1.0, base)

