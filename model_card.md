# Model Card: AI DJ Agent

## 1. Reflection and Ethics

**What are the limitations or biases in your system?**
The system is fundamentally constrained by a very small, hard-coded dataset of 18 songs and 15 artist facts. Furthermore, the Agent must map complex natural language requests into a rigid schema (`genre`, `mood`, `energy`). This can cause algorithmic bias where nuanced or hybrid musical tastes are flattened into overly simplistic, generic categories. 

**Could your AI be misused, and how would you prevent that?**
Yes, like most LLMs, the Agent could be subjected to prompt injection attacks attempting to bypass the "DJ persona" to generate harmful text, or attempting to force unexpected tool calls. To prevent this, I would implement input sanitization, tighter system prompt guardrails, and ensure strict parameter validation inside the Python tool functions before executing any logic.

**What surprised you while testing your AI's reliability?**
I was pleasantly surprised by how accurately the Agent was able to extract numerical `energy` scores from vague natural language. For example, it intuitively mapped words like "chill" or "exhausted" to an energy float of `< 0.3` without me needing to write explicit few-shot examples mapping words to specific decimals.

## 2. AI Collaboration Reflection

**Describe your collaboration with AI during this project:**
I collaborated closely with an AI coding assistant to evolve my basic Module 1-3 Python script into a complete Agentic RAG system. I defined the architectural goals and features, and the AI helped write the boilerplate for the Streamlit UI, configure the Gemini tool-calling logic, and build the test harness.

**Identify one instance when the AI gave a helpful suggestion:**
The AI suggested wrapping my existing `src/recommender.py` scoring algorithm into an accessible tool for the LLM. This was incredibly helpful, as my initial thought might have been to paste the entire CSV into the prompt, which would have been inefficient and scaled poorly.

**Identify one instance where its suggestion was flawed or incorrect:**
During the setup phase, the AI attempted to automatically run a `pytest` bash command in the terminal before ensuring the virtual environment was activated and dependencies were installed, which predictably resulted in a `command not found` error.

## 3. Portfolio Artifact

**What this project says about me as an AI engineer:**
This project demonstrates my ability to take a traditional, rules-based recommendation engine and modernize it using Agentic AI workflows. By integrating a Large Language Model via dynamic tool-calling and wrapping it in a clean Streamlit UI, I proved I can build end-to-end, user-centric AI applications that successfully bridge unstructured natural language with strict, structured backend logic.
