# WAI-TechnicalWorkshop-AgenticAI-HealthCare
Women in AI technical workshop on using agentic AI in detecting user needs within healthcare and education space 

## Usecase 1 (Dyslexia

```

Goal:
local React + Python (FastAPI) document reader that embeds the DyslexiaAssistAgent class and executes the adaptive assistive flow through the text reading exercise.


Agent Overview:

Instead of asking questions, the agent:

Observes text input — as the user reads, types, or edits text.

Analyzes reading and writing patterns, e.g.:

letter reversals (b/d, p/q),

transpositions (form/from),

omissions or skipped words,

spelling approximations and phoneme-grapheme mismatches,

prolonged time per word (keystroke timing if available).

Estimates reading fluency by analyzing how quickly text is read or typed (if you capture reading speed, eye-tracking, or audio).

Triggers assistive actions (text-to-speech, spacing/font changes, highlighting, pacing aids) automatically when indicators appear.

Engages the user with gentle coaching messages like

“Would you like me to read the next sentence aloud?”
“Try focusing on one line at a time — want a highlight ruler?”

```

###Run backend locally
```
cd backend
pip install fastapi uvicorn
uvicorn app:app --reload
```

###Run frontend locally
```
cd frontend
npm install
npm start

```

###End Result
```
When you type or paste text:

It sends the text to backend /analyze.

Backend returns confidence and assistive_mode.

If assistive_mode is true, the app:

Activates TTS (reads aloud),

Adjusts line spacing and font,

Shows feedback indicators and encouragement.

```


###Future Key refinements
```
Record typing speed or keystroke latency to refine fluency scoring.

Add local caching of sessions to let the agent “learn” over time.

Integrate Whisper ASR for speech-based reading.

Store metrics (confidence trends, triggers) to personalize assistance per user.

```


