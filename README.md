# ADK Multi-Agent Systems

AI agent projects built with Google's open-source Agent Development Kit (ADK),
demonstrating modern agentic patterns from single-agent specialists to
multi-agent orchestrated pipelines.

## 🎬 Demo Video   (DOUAS-MOHAMED)

[![Watch the demo](https://img.youtube.com/vi/pjUKXZHvu4c/maxresdefault.jpg)](https://youtu.be/pjUKXZHvu4c)

▶️ **[Watch the full demo on YouTube](https://youtu.be/pjUKXZHvu4c)**

## 📦 Projects

### 🌟 [multi-orchestrated-agent/](./multi-orchestrated-agent/) — Multi-Agent Teaching Assistant
A `SequentialAgent` pipeline of three specialized agents (grammar, math, summary)
collaborating through shared session state to deliver adaptive, kid-friendly responses.

**Key concepts:** `SequentialAgent` · `output_key` · `before_agent_callback` · template substitution

### [basic_agent/](./basic_agent/) — Single-Agent Math Tutor
A specialized math agent with custom tools, persona, and few-shot examples.
Foundation for understanding ADK's core patterns.

**Key concepts:** `Agent` · `Runner` · `SessionService` · function calling

### [live_agent/](./live_agent/) — Live Voice Math Tutor
Real-time voice agent built with ADK Live, streaming audio bidirectionally
through `LiveRequestQueue` while preserving session state and tools.

**Key concepts:** `InMemoryRunner` · `LiveRequestQueue` · WebSocket streaming

## 🛠️ Tech Stack

- Python 3.12
- Google Agent Development Kit (ADK)
- Gemini 2.5 Flash + Live (native audio)
- ADK Web (debug & monitoring UI)

## 📚 Credits


Built while following the O'Reilly book \*Multimodal Real-Time AI Interaction Architectures\*

by co-authors  {As a Generative AI Global Blackbelt at Google Cloud, @Heiko Hotz operates at the cutting edge, driving multi-million dollar AI initiatives for global giants}and {@Dr. Sokratis Kartakis is a Generative AI Global Blackbelt at Google Cloud}. This implementation is a personal learning project — credit for the

core architecture goes to the book's authors.

## 📄 License

MIT