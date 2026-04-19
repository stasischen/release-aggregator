# Stitch UI Prototyping Plan

## Objective
Accelerate the UI design and prototyping phase for the Lingourmet frontend (`lingo-frontend-web`) by leveraging Google Stitch to generate high-fidelity, Tailwind-based HTML mockups. These mockups establish the visual design system (Design Tokens) before being translated into native Flutter widgets.

## Core Design System (Extracted from Home Dashboard)
- **Primary Color:** Deep Crimson Red (`#aa2c32`)
- **Typography:** Plus Jakarta Sans
- **Background:** Surface Bright (`#f5f7f9`)
- **Radius:** 16px (1rem) standard for cards
- **Vibe:** Modern, tactile, engaging, premium.

## Architecture Notes
- **Audio Strategy (Cross-Video)**: Implement a "Dual-Track Audio" system. Use local TTS (e.g., Qwen3TTS) for seamless, 0-latency sliding review. Fall back to the YouTube iframe API only when the user explicitly taps "Watch original video context" to avoid ToS violations and ensure smooth UX.

## Page Inventory
1. **Home / Dashboard**: Central hub with daily streaks and quick tools.
2. **Grammar Alchemy Lab**: Drag-and-drop sandbox for morphology (V5 Atoms).
3. **Teleprompter Shadowing**: Sentence-level audio comparison tool (Dual-Track TTS + YouTube fallback).

## Workflow (The Baton System)
1. Agent provides an enhanced "Super Prompt" tailored for Stitch.
2. User executes the prompt in the Stitch web interface.
3. User returns the HTML/CSS output.
4. Agent saves the HTML to `lingo-frontend-web/docs/stitch_designs/`.
5. Agent translates the layout into Flutter code.

## Related Tasks
See `STITCH_UI_PROTOTYPING_TASKS.json`
