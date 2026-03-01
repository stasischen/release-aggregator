# Target Language Audio Skills Plan

## 1. Goal

To define the implementation plan for the Listening and Pronunciation layers within the Lingo curriculum, specifically addressing how to build effective learning experiences *without* relying on real human pronunciation recordings or scoring in the initial MVP phase.

## 2. Rationale: Viability Without Human Assets

Building a robust audio skills curriculum without human recording artists or expert human assessors is not only possible but recommended for the MVP phase.

### Why TTS is Sufficient for Listening MVP
1.  **Consistency & Variety**: High-quality modern TTS (like Google Cloud TTS or Azure Neural TTS) can generate multiple voices, consistent accents, and predictable speeds instantly.
2.  **Focus on Comprehension**: The primary goal at A1/A2 levels is *understanding* intent and extracting information, not analyzing subtle human emotional nuances. TTS is perfectly clear for gist and detail extraction.
3.  **Iteration Speed**: If a sentence needs to be rewritten based on pedagogical feedback, TTS regenerates it instantly. Human re-recording blocks development.

### Why ASR Proxy is Sufficient for Pronunciation MVP
1.  **Lowering the Affective Filter**: Users (especially beginners) are often intimidated by strict pronunciation scoring.
2.  **"Intelligibility" over "Perfection"**: The goal of communicative language learning is to be understood. If standard ASR (Automatic Speech Recognition) can transcribe what the user said matching the target sentence, their pronunciation is functionally "intelligible."
3.  **Technical Feasibility**: Absolute phoneme-level scoring requires specialized, expensive ML models and pristine audio input. ASR proxy scoring relies on existing, trained models (like Whisper or platform-native dictation).

## 3. Implementation Strategy: Listening Layer

### 3.1 TTS Asset Pipeline
*   **Action**: Integrate a programmatic TTS generation step in the `content-pipeline`.
*   **Parameters**: For every audio node, generate variants (e.g., Normal Speed Male, Normal Speed Female, Slow Speed).
*   **Storage**: Store paths to these generated assets in the `content-ko` JSON structures, alongside the text.

### 3.2 Listening Task Design (The "What")
Focus tasks on cognitive processing of the audio, not just transcription.

*   **Gist Tasks (A1/A2)**: Listen to a short dialogue and choose the main topic (e.g., ordering food, asking directions).
*   **Detail Tasks (A1/A2)**: Listen and identify specific information (prices, times, phone numbers, quantities).
*   **Intent Tasks (A2/B1)**: Listen and determine the speaker's core intent (agreeing, complaining, suggesting).

### 3.3 Avoid:
*   Tasks completely dependent on subtle vocal inflections (sarcasm) until B2+ or human audio is available.
*   "Write exactly what you hear" (Dictation) as the *only* task type, as it tests spelling and memory as much as listening.

## 4. Implementation Strategy: Pronunciation/Prosody Layer

### 4.1 The "Intelligibility Proxy" Method (ASR-based Scoring)
1.  **User Input**: User records themselves reading a specific prompt.
2.  **ASR Transcription**: Send the audio to standard ASR.
3.  **Comparison**: Compare the ASR text output to the target text.
    *   *Match*: "Great! You were understood clearly."
    *   *Mismatch*: "The system heard [ASR output]. Let's try saying [Target Text] again, focusing on clarity."

### 4.2 UI/UX Scaffolding (No Scoring Needed)
Provide tools for self-correction before resorting to automated scoring.

*   **Shadowing (跟讀)**: Play the TTS audio. User records themselves. Play both back sequentially for self-comparison. No system grading required.
*   **Visual Rhythm (Prosody Hint)**: In the UI, highlight the stressed syllables or words visually (e.g., bolding) to guide the user's rhythm without needing complex audio analysis.

### 4.3 Avoid:
*   Giving a "score out of 100" for pronunciation. It is often inaccurate and demotivating.
*   Showing detailed phoneme-level error feedback (e.g., "Your 'r' sound was 20% off") using standard ASR. Focus on word-level intelligibility.

## 5. Next Steps

1.  **Define Audio Skill Generators**: Create generator templates for Listening Gist and Listening Detail tasks in the TLG.
2.  **Pipeline Update**: Add TTS generation capabilities to `content-pipeline`.
3.  **App Integration**: Ensure the Lingo frontend can handle audio playback variants and basic ASR recording/comparison flows.

## 6. Compatibility Notes with Existing Specs

1. MVP default remains compatible with `PEDOPT_008_LISTENING_MICRONODE_SPEC.md`:
   - Listening tasks do not require ASR to run.
2. ASR is an optional enhancement for pronunciation intelligibility proxy:
   - Default policy: `asr_proxy_enabled = false` for baseline deployment.
   - Phase-2 policy: `asr_proxy_enabled = true` for supported devices/environments.
