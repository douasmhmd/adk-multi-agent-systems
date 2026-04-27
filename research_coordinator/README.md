\# Research Coordinator — Distributed Multi-Agent A2A System



A research coordinator that orchestrates \*\*two remote A2A agents\*\* built with different

frameworks. Demonstrates the full power of the A2A protocol: cross-framework

interoperability for production multi-agent systems.



\## 🎬 Demo Video



▶️ \*\*\[Watch the demo on YouTube](https://youtu.be/YOUR\_VIDEO\_ID)\*\*



\## 🏗️ Architecture

User

↓

ResearchCoordinator (ADK + OpenAI GPT-4o-mini)

├──→ QueryGenerator (LangGraph, port 10002)  → search queries

└──→ Researcher    (ADK, port 10003)         → web research

↓

Synthesized 3-paragraph summary



The coordinator uses a single tool, `delegate\_research`, which:

1\. \*\*Strategize\*\* — calls QueryGenerator (LangGraph) to break the topic into queries

2\. \*\*Execute\*\* — calls Researcher (ADK) for each query in a loop

3\. \*\*Synthesize\*\* — the coordinator's LLM combines results into a final summary



All inter-agent communication uses the \*\*A2A protocol over HTTP\*\*.



\## 🔑 Key Concepts



| Concept | Purpose |

|---|---|

| `A2AClient` + `A2ACardResolver` | Discover and connect to remote A2A agents |

| `delegate\_research` tool | Encapsulates the full multi-agent orchestration |

| `call\_remote\_agent` helper | Reusable A2A request-response pattern |

| `LiteLlm` | LLM-agnostic interface (Gemini or OpenAI) |

| Cross-framework | LangGraph + ADK communicating seamlessly |



\## 📁 Folder Structure

research\_coordinator/

├── agent.py              # ADK Agent with delegate\_research tool

├── a2a\_tools.py          # A2A client logic + helper functions

├── main.py               # Runner that tests the coordinator

├── .env                  # API keys (not committed)

└── README.md



\## 🚀 How to Run



\### Prerequisites



\- The two specialist agents must be running:

&#x20; - `specialist\_agents/query\_generator/` on port 10002

&#x20; - `specialist\_agents/researcher/` on port 10003



\### Steps



Open \*\*3 terminals\*\* with the venv activated:



```bash

\# Terminal 1: LangGraph QueryGenerator

cd specialist\_agents/query\_generator

python server.py



\# Terminal 2: ADK Researcher

cd specialist\_agents/researcher

python server.py



\# Terminal 3: Coordinator

cd research\_coordinator

python main.py

```



\### Expected Output

\--- Starting research for: 'A2A Protocol' ---

Step 1: Delegating to QueryGeneratorAgent (LangGraph)...

\--> Received queries:



What is A2A Protocol?

Recent news about A2A Protocol



Step 2: Delegating to ResearcherAgent (ADK)...



Executing query: 'What is A2A Protocol?'

Executing query: 'Recent news about A2A Protocol'



=== FINAL ANSWER ===

\[3-paragraph synthesis from the coordinator's LLM]



\## 🔧 LLM Configuration



This project uses \*\*OpenAI GPT-4o-mini via LiteLLM\*\* to avoid Gemini free-tier quota

limits during heavy multi-agent workflows.



To switch back to Gemini:



```python

\# In agent.py and specialist\_agents/researcher/agent\_logic.py

from google.adk.agents import Agent

agent = Agent(model="gemini-2.5-flash", ...)

```



To use OpenAI (current setup):



```python

from google.adk.models.lite\_llm import LiteLlm

agent = Agent(model=LiteLlm(model="openai/gpt-4o-mini"), ...)

```



\## 🛠️ Tech Stack



\- Python 3.12

\- Google Agent Development Kit (ADK)

\- LangGraph (specialist agent)

\- A2A SDK (`a2a-sdk==0.2.16`)

\- LiteLLM (multi-LLM support)

\- OpenAI GPT-4o-mini

\- Starlette + uvicorn



\## 📚 Credits



Built while following the O'Reilly book \*Multimodal Real-Time AI Interaction

Architectures\* by \*\*Heiko Hotz\*\* and \*\*Dr. Sokratis Kartakis\*\*, both Generative AI

Global Blackbelts at Google Cloud. The architecture (Figure 8-1) and orchestration

pattern come from the book; this is a personal learning implementation.



\## 📄 License



MIT

Sauvegarde.

⚠️ Remplace YOUR\_VIDEO\_ID par l'ID de ta nouvelle vidéo une fois publiée.

📋 Étape 2 : README racine mis à jour

cd ..

notepad README.md

Remplace TOUT par :

markdown# ADK Multi-Agent Systems



Production-grade AI agent projects built with Google's Agent Development Kit (ADK)

and the open-source A2A (Agent-to-Agent) protocol. Demonstrates the full progression

of agentic patterns — from a single specialized agent to a distributed multi-agent

system communicating across frameworks.



\## 🎬 Demo Videos





\### A2A Multi-Agent Research System (distributed)



▶️ \*\*\[Watch on YouTube](https://youtu.be/watch?v=ETgYm6SgWHo)\*\*



\### Multi-Agent Teaching Assistant (local pipeline)



\[!\[Watch the demo](https://img.youtube.com/vi/pjUKXZHvu4c/maxresdefault.jpg)](https://youtu.be/pjUKXZHvu4c)



▶️ \*\*\[Watch on YouTube](https://youtu.be/pjUKXZHvu4c)\*\*





\## 📦 Projects



\### 🌐 \[research\_coordinator/](./research\_coordinator/) — Distributed Multi-Agent A2A System

A research coordinator that orchestrates \*\*two remote A2A agents\*\* built with different

frameworks (LangGraph + ADK). Demonstrates cross-framework interoperability via the

A2A protocol over HTTP.



\*\*Key concepts:\*\* A2A client · cross-framework · LiteLLM · async orchestration



\### 🤝 \[a2a\_handshake/](./a2a\_handshake/) — Cross-Framework A2A Handshake

Two agents from different frameworks (LangGraph + ADK) communicating via A2A.

The simplest demonstration of the A2A protocol's interoperability.



\*\*Key concepts:\*\* AgentCard · AgentExecutor · TaskUpdater · agent discovery



\### 🔢 \[a2a\_math\_agent/](./a2a\_math\_agent/) — A2A-Enabled ADK Agent

Wraps an existing ADK agent (from Chapter 6) into an A2A server, making it accessible

to any A2A-compliant client without modifying the agent's code.



\*\*Key concepts:\*\* wrap-don't-rewrite · MathAgentExecutor · server-side adaptation



\### 🌟 \[multi-orchestrated-agent/](./multi-orchestrated-agent/) — Sequential Multi-Agent Pipeline

Three specialized agents (grammar, math, summary) collaborating via shared session

state. Local orchestration with `SequentialAgent`.



\*\*Key concepts:\*\* `SequentialAgent` · `output\_key` · `before\_agent\_callback` · template substitution



\### \[basic\_agent/](./basic\_agent/) — Single-Agent Math Tutor

A specialized math agent with custom tools, persona, and few-shot examples.

Foundation for understanding ADK's core patterns.



\*\*Key concepts:\*\* `Agent` · `Runner` · `SessionService` · function calling



\### \[live\_agent/](./live\_agent/) — Live Voice Math Tutor

Real-time voice agent built with ADK Live, streaming audio bidirectionally

through `LiveRequestQueue` while preserving session state and tools.



\*\*Key concepts:\*\* `InMemoryRunner` · `LiveRequestQueue` · WebSocket streaming



\### \[specialist\_agents/](./specialist\_agents/) — A2A Specialists

Standalone A2A servers consumed by `research\_coordinator/`:

\- \*\*query\_generator/\*\* — LangGraph agent generating search queries (port 10002)

\- \*\*researcher/\*\* — ADK agent performing web research (port 10003)



\## 🛠️ Tech Stack



\- \*\*Languages:\*\* Python 3.12

\- \*\*Frameworks:\*\* Google ADK · LangGraph

\- \*\*Protocols:\*\* A2A (Agent-to-Agent over HTTP)

\- \*\*LLMs:\*\* Gemini 2.5 Flash · GPT-4o-mini (via LiteLLM)

\- \*\*Web:\*\* Starlette · uvicorn · httpx

\- \*\*Tools:\*\* ADK Web (debug UI)



\## 🚀 Quick Start



\### 1. Setup



```bash

git clone https://github.com/douasmhmd/adk-multi-agent-systems.git

cd adk-multi-agent-systems

python -m venv .adk\_venv

.adk\_venv\\Scripts\\activate

pip install google-adk a2a-sdk==0.2.16 langgraph litellm python-dotenv uvicorn httpx

```



\### 2. Configure API keys



Create `.env` files in each project folder with:

GOOGLE\_API\_KEY=your\_gemini\_key

OPENAI\_API\_KEY=your\_openai\_key



\### 3. Run a multi-agent A2A demo (3 terminals)



```bash

\# Terminal 1

cd specialist\_agents/query\_generator

python server.py



\# Terminal 2

cd specialist\_agents/researcher

python server.py



\# Terminal 3

cd research\_coordinator

python main.py

```



\## 🧠 Architectural Patterns Demonstrated



| Pattern | Project |

|---|---|

| Single specialized agent | `basic\_agent/` |

| Live multimodal interaction | `live\_agent/` |

| Sequential local pipeline | `multi-orchestrated-agent/` |

| A2A cross-framework handshake | `a2a\_handshake/` |

| A2A wrapper of existing agent | `a2a\_math\_agent/` |

| \*\*Distributed multi-agent A2A\*\* | `research\_coordinator/` + `specialist\_agents/` |



\## 📚 Credits



Built while following the O'Reilly book \*Multimodal Real-Time AI Interaction

Architectures\* by \*\*Heiko Hotz\*\* and \*\*Dr. Sokratis Kartakis\*\*, both Generative AI

Global Blackbelts at Google Cloud. This is a personal learning project — credit

for the underlying architectures goes to the book's authors.



\## 📄 License



MIT

