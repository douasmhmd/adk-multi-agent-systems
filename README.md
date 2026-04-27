# ADK Multi-Agent Systems

Production-grade AI agent projects built with Google's Agent Development Kit (ADK)
and the open-source A2A (Agent-to-Agent) protocol. Demonstrates the full progression
of agentic patterns — from a single specialized agent to a distributed multi-agent
system communicating across frameworks.

## 🎬 Demo Videos

### 🌐 A2A Multi-Agent Research System (LangGraph + ADK)

[![Watch the A2A demo](https://img.youtube.com/vi/ETgYm6SgWHo/maxresdefault.jpg)](https://youtu.be/ETgYm6SgWHo)

▶️ **[Système Multi-Agent IA avec Protocole A2A — LangGraph et ADK qui Communiquent en Python](https://youtu.be/ETgYm6SgWHo)**

### 🌟 Multi-Agent Teaching Assistant (Sequential Pipeline)

[![Watch the multi-agent demo](https://img.youtube.com/vi/pjUKXZHvu4c/maxresdefault.jpg)](https://youtu.be/pjUKXZHvu4c)

▶️ **[Watch on YouTube](https://youtu.be/pjUKXZHvu4c)**

## 📦 Projects

### 🌐 [research_coordinator/](./research_coordinator/) — Distributed Multi-Agent A2A System
A research coordinator that orchestrates **two remote A2A agents** built with different
frameworks (LangGraph + ADK). Demonstrates cross-framework interoperability via the
A2A protocol over HTTP.

**Key concepts:** A2A client · cross-framework · LiteLLM · async orchestration

### 🤝 [a2a_handshake/](./a2a_handshake/) — Cross-Framework A2A Handshake
Two agents from different frameworks (LangGraph + ADK) communicating via A2A.
The simplest demonstration of the A2A protocol's interoperability.

**Key concepts:** AgentCard · AgentExecutor · TaskUpdater · agent discovery

### 🔢 [a2a_math_agent/](./a2a_math_agent/) — A2A-Enabled ADK Agent
Wraps an existing ADK agent (from Chapter 6) into an A2A server, making it accessible
to any A2A-compliant client without modifying the agent's code.

**Key concepts:** wrap-don't-rewrite · MathAgentExecutor · server-side adaptation

### 🌟 [multi-orchestrated-agent/](./multi-orchestrated-agent/) — Sequential Multi-Agent Pipeline
Three specialized agents (grammar, math, summary) collaborating via shared session
state. Local orchestration with `SequentialAgent`.

**Key concepts:** `SequentialAgent` · `output_key` · `before_agent_callback` · template substitution

### [basic_agent/](./basic_agent/) — Single-Agent Math Tutor
A specialized math agent with custom tools, persona, and few-shot examples.
Foundation for understanding ADK's core patterns.

**Key concepts:** `Agent` · `Runner` · `SessionService` · function calling

### [live_agent/](./live_agent/) — Live Voice Math Tutor
Real-time voice agent built with ADK Live, streaming audio bidirectionally
through `LiveRequestQueue` while preserving session state and tools.

**Key concepts:** `InMemoryRunner` · `LiveRequestQueue` · WebSocket streaming

### [specialist_agents/](./specialist_agents/) — A2A Specialist Workers
Standalone A2A servers consumed by `research_coordinator/`:
- **query_generator/** — LangGraph agent generating search queries (port 10002)
- **researcher/** — ADK agent performing web research (port 10003)

## 🛠️ Tech Stack

- **Languages:** Python 3.12
- **Frameworks:** Google ADK · LangGraph
- **Protocols:** A2A (Agent-to-Agent over HTTP)
- **LLMs:** Gemini 2.5 Flash · GPT-4o-mini (via LiteLLM)
- **Web:** Starlette · uvicorn · httpx
- **Tools:** ADK Web (debug UI)

## 🚀 Quick Start

### 1. Setup

```bash
git clone https://github.com/douasmhmd/adk-multi-agent-systems.git
cd adk-multi-agent-systems
python -m venv .adk_venv
.adk_venv\Scripts\activate
pip install google-adk a2a-sdk==0.2.16 langgraph litellm python-dotenv uvicorn httpx
```

### 2. Configure API keys

Create `.env` files in each project folder:
GOOGLE_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key

### 3. Run the multi-agent A2A demo (3 terminals)

```bash
# Terminal 1
cd specialist_agents/query_generator
python server.py

# Terminal 2
cd specialist_agents/researcher
python server.py

# Terminal 3
cd research_coordinator
python main.py
```

## 🧠 Architectural Patterns Demonstrated

| Pattern | Project |
|---|---|
| Single specialized agent | `basic_agent/` |
| Live multimodal interaction | `live_agent/` |
| Sequential local pipeline | `multi-orchestrated-agent/` |
| A2A cross-framework handshake | `a2a_handshake/` |
| A2A wrapper of existing agent | `a2a_math_agent/` |
| **Distributed multi-agent A2A** | `research_coordinator/` + `specialist_agents/` |

## 📚 Credits

Built while following the O'Reilly book *Multimodal Real-Time AI Interaction
Architectures* by **Heiko Hotz** and **Dr. Sokratis Kartakis**, both Generative AI
Global Blackbelts at Google Cloud. This is a personal learning project — credit
for the underlying architectures goes to the book's authors.

## 📄 License

MIT