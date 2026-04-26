\# ADK Multi-Agent Systems



Two AI agent projects built with Google's open-source Agent Development Kit (ADK)

to learn the patterns of modern agentic systems — from a single specialized agent

to a multi-agent orchestrated pipeline.



\## 📦 Projects



\### 1. \[basic\_agent/](./basic\_agent/) — Single-Agent Math Tutor

A specialized math agent with custom tools, persona, and few-shot examples.

Demonstrates the core ADK pattern: `Agent` + `Runner` + `SessionService`.



\### 2. \[multi-orchestrated-agent/](./multi-orchestrated-agent/) — Teaching Assistant Pipeline

Three specialized agents (grammar, math, summary) working as a `SequentialAgent`

pipeline with shared session state and guardrails.

Demonstrates `output\_key`, `before\_agent\_callback`, and template substitution.



\## 🛠️ Tech Stack



\- Python 3.12

\- Google Agent Development Kit (ADK)

\- Gemini 2.5 Flash

\- ADK Web (debug \& monitoring UI)



\## 📚 Credits



Built while following the O'Reilly book \*Multimodal Real-Time AI Interaction Architectures\*

by co-authors  {As a Generative AI Global Blackbelt at Google Cloud, @Heiko Hotz operates at the cutting edge, driving multi-million dollar AI initiatives for global giants}and {@Dr. Sokratis Kartakis is a Generative AI Global Blackbelt at Google Cloud}. This implementation is a personal learning project — credit for the

core architecture goes to the book's authors.



\## 📄 License



MIT

