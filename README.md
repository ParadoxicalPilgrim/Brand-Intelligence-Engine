# Brand Intelligence Engine

**Live Application:** [brand-intelligence-engine-4216.streamlit.app](https://brand-intelligence-engine-4216.streamlit.app/)

A multi-agent AI pipeline that transforms a raw, unstructured startup idea into a coherent, useful, and launch-ready brand system. Built as a sophisticated intelligence workflow, this engine avoids the "one-prompt trap" by utilizing specialized AI agents for discovery, strategy, critique, design brief generation, and execution planning.

### Tech Stack & Technologies Used

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI_SDK-412991?style=for-the-badge&logo=openai&logoColor=white)
![OpenRouter API](https://img.shields.io/badge/OpenRouter_API-000000?style=for-the-badge)
![JSON](https://img.shields.io/badge/JSON-Data_Parsing-lightgrey?style=for-the-badge&logo=json&logoColor=black)

---

### Core Workflow & Architecture

The system operates on a deliberate, multi-stage architecture where each AI agent passes structured JSON data to the next:

*   **Agent 1 (The Visionary):** Interviews the founder by dynamically generating context-specific questions based on the raw idea.
*   **Agent 1.5 (The Analyst):** Evaluates the founder's answers to identify market strengths (Green Flags) and blind spots/risks (Red Flags).
*   **Agent 2 (The Strategist):** Defines the brand category, clear value proposition, personality traits, and strict traits to avoid.
*   **Agent 3 (The Critic):** An anti-generic naming engine that generates distinctive brand names and runs them through a ruthless cliche-check.
*   **Agent 4 (The Designer & Marketer):** Translates the strategy into a visual design brief (typography, color mood, imagery style) and launch-ready content (landing page hero, one-line pitch).
*   **Agent 5 (The Operator):** Generates a pragmatic execution path, detailing immediate next steps, MVP approach, and initial customer acquisition strategy.

---

### Key Features

*   **Accident-Proof UI:** Engineered with Streamlit forms and text-areas to prevent accidental submissions via Enter keys.
*   **Robust JSON Parsing:** Custom parser that sanitizes and extracts AI outputs even if the model injects markdown ticks.
*   **Context Preservation:** Later stages build entirely on the decisions of previous stages rather than restarting from zero.

---

### How to Run Locally

1. **Clone the repository:**
   Clone this repository to your local machine and navigate into the folder:
   ```bash
   cd Brand-Intelligence-Engine
