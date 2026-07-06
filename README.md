# 🏍️ Enterprise AI Agent for Manufacturing Industry: An LLM-powered GraphRAG Assistant for architecting Smarter Supply Chains and Shop Floor Operations.

An advanced, self-healing **Enterprise AI Agent** built for the **Manufacturing Industry** to automate regulatory compliance and logistics mapping. This project leverages **LLM Grounding with Knowledge Graphs** (**GraphRAG**) to execute complex **multi-hop queries** across global automotive standards with total **hallucinations** reduction. 

Powered by **LLM orchestrators LangChain and LangGraph**, the system splits runtime responsibilities between **Llama 3.1 (NLU)** for structural database query generation and **Gemma 2 (NLG)** for grounded natural language synthesis.

---

## 📖 Capstone Writeup

### 1. Introduction: Driving Enterprise Compliance in High-Stakes Automotive Logistics
In the modern **Manufacturing Industry**, regulatory non-compliance introduces massive operational and financial risks, directly translating to severe bottlenecks, halted production lines, and millions in lost revenue. For an **Enterprise** powerhouse like Ducati, navigating the labyrinth of global standards—such as the intricate UNECE Regulation No 41 and its specific Annex frameworks—is traditionally a slow, human-intensive process plagued by data silos. Traditional search architectures fail because legal frameworks are interconnected networks, not flat files. Standard large language models fall short when deployed raw, as they frequently invent details when tasked with parsing highly specific, multi-layered industrial legal codes. To solve this critical business challenge, this project introduces a specialized **Enterprise AI Agent** designed to automate regulatory mapping, analyze compliance constraints, and instantly surface actionable pipeline guidance. Rather than simple pattern-matching, this specialized **AI** system uses advanced **LLM Grounding with Knowledge Graphs** to completely remove **hallucinations**, ensuring that compliance officers, logistics managers, and shop-floor engineers get verified, authoritative answers with zero fabricated information. By bridging unstructured operational inquiries with a 450+ node Neo4j graph database, this **agent** serves as an intelligent compliance copilot where real business capital and product delivery timelines are on the line.

### 2. Methodology: Dual-Model Orchestration and Graph Retrieval Architecture
The technical foundation of this solution shifts away from simple prompt-engineering into a robust, deterministic state machine driven by premier **LLM orchestrators LangChain and LangGraph**. The system runs on a tailored, three-node cyclical workflow that splits linguistic duties between two specialized models to achieve optimal precision: **Llama 3.1 (NLU)** for structural database query generation and **Gemma 2 (NLG)** for natural language speech synthesis. When a user submits an operational inquiry through the custom Streamlit frontend (`app_10.py`), the request is passed into the central pipeline manager (`orchestrator_4.py`). In the first stage, **Llama 3.1 (NLU)** acts as an isolated database driver, translating the raw text prompt into precise Cypher syntax by matching the request against an injected, strict graph schema context containing precise entity relationships like `:Vehicle`, `:Requirement`, and `:Applicable test procedure`. This query is then handled by Node 2, which cleans and runs the statement directly against a live Neo4j instance. If the database execution returns valid structural records, the collected path coordinates are forwarded straight to Node 3. Here, **Gemma 2 (NLG)** takes the raw database pairs (Source ID → Relationship Type → Target ID) and synthesizes a clear, contextual response. The complete application state is securely managed by a LangGraph memory blueprint, allowing seamless data flow between the separate computing layers while maintaining full auditability.

### 3. Innovation: Self-Healing Query Loops and Multi-Hop GraphRAG Realization
The core innovation of this project lies in its self-healing, dual-tier recovery pipeline, moving far beyond traditional **GraphRAG** implementations that break down when an exact string match fails. In standard configurations, if an LLM generates a database query that is syntactically invalid or returns zero records, the application crashes or leaves the user with an empty response. This **Enterprise** framework solves that limitation by embedding an active conditional routing agent (`route_after_db`) directly into the graph topology. If Node 2 registers a database exception or captures an empty data object, it flips an internal state variable called `fallback_attempt` to `True` and routes the execution back to Node 1. During this fallback loop, the **agent** shifts from a rigid property filter to an expansive keyword-based neighborhood search using fuzzy matching logic (e.g., checking if node properties contain strings like 'motorcycle' or 'sound'). This capability unlocks reliable **Multi-hop queries**, allowing the system to traverse multiple relationship steps across the database to extract adjacent context clusters. By pulling the broader organizational neighborhood surrounding a topic into the prompt window, the **LLM** receives a highly descriptive factsheet. This architecture achieves major **hallucinations** reductions, since the text-generation engine is physically blocked from inventing data points; it can only summarize the multi-hop paths verified by the graph database.

### 4. Conclusion: A Scalable, Production-Ready Compliance Asset
By fusing local **LLM** orchestration with graph technologies, this capstone project successfully demonstrates how intelligent **agent** systems can automate highly technical business workflows where precision is non-negotiable. Moving from raw experimentation to a structured, portfolio-ready product, the architecture handles the messy realities of enterprise data by combining a self-healing LangGraph backend with a fast, modern Streamlit corporate dashboard layout. Splitting tasks between **Llama 3.1 (NLU)** for code generation and **Gemma 2 (NLG)** for explanation ensures optimal efficiency, while the Neo4j implementation provides absolute data grounding to protect the organization from erroneous outputs. For the automotive **Manufacturing Industry**, this solution slashes the time required to analyze complex regulations from days to seconds, directly protecting supply chain logistics, preventing production friction, and optimizing corporate compliance costs. The resulting prototype delivers a highly scalable, robust framework, proving the immense business value of grounding autonomous systems with secure graph data networks.

---

## 🏗️ 1. Generative AI System Architecture

[User Input via Streamlit UI]
│
▼
┌──────────────────────┐
│   LangGraph State    │◄─────────────────┐
└──────────────────────┘                  │
│                             │
▼                             │
[Node 1: Llama 3.1 NLU]                  │
Translates Prompt to Cypher               │
│                             │
▼                             │
[Node 2: Neo4j Executor]                  │ (If empty records/error,
Runs Query Against Database                │  triggers Fallback Mode)
│                             │
├─────────────────────────────┘
│ (If records found)
▼
[Node 3: Gemma 2 NLG]
Synthesizes Grounded Answer
│
▼
[Clean Response Rendered to UI]

---

## 🛠️ Tech Stack & Prerequisites

Before running the application, ensure you have the following frameworks and models installed locally:

* **Backend Orchestration:** Python 3.10+, `langgraph`, `langchain`, `langchain-neo4j`, `langchain-ollama`, `requests`
* **Frontend Web Framework:** `streamlit`
* **Graph Infrastructure:** Neo4j Desktop (Local instance containing a minimum of 450+ entities and 16,000+ structural relationship pairs)
* **Local Inference Engines (Ollama):**
  * `llama3.1:latest` (Serving as the structural NLU compiler)
  * `gemma-2:latest` (Serving as the narrative NLG synthesizer)

---

## 🚀 Getting Started & Local Deployment

Follow these steps to reproduce the local deployment environment for judging and evaluation purposes.

### 1. Clone the Project Repository
```bash
    git clone <your-public-repo-url>
    cd <project-directory>

2. Configure Your Local Graph Database Instance

Ensure your local Neo4j Desktop database is active. Modify the authentication variables at the top of orchestrator_4_comments_ship.py if your local configurations differ:

PYTHON
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USERNAME = "neo4j"
    NEO4J_PASSWORD = "YourDatabasePasswordHere"

3. Install Dependencies

Install all required libraries using pip:

    pip install streamlit langgraph langchain langchain-neo4j langchain-ollama requests

4. Verification of Branding Graphic Assets

Verify that the following graphic branding assets reside within the root directory of your project folder:

    ducati_logo.png — Corporate header navigation bar logo

    AI_Agent_Logo.png — Assistant user profile avatar icon

    ducati_panigale.png — Pre-conversation landing placeholder wallpaper image

5. Launch the Enterprise Agent Dashboard

Execute the pipeline application framework via Streamlit:

CMD

    streamlit run app_10_comments_ship.py

📁 Repository Structure & Code Overview

The codebase is split into two modular layers containing extensive comments regarding design choices, runtime loops, and state properties:

    app_10_comments_ship.py (Frontend UI Layer): Configures the global dashboard layout grid, handles image assets into browser-safe Base64 streams, applies custom responsive CSS cards, persists session history lists, and renders markdown text components cleanly.

    orchestrator_4_comments_ship.py (LangGraph Backend Engine):

        AgentState: Manages the structural contract memory data arrays across processing blocks.

        nlu_generate_cypher (Node 1): Injects valid schema definitions into local Llama 3.1 prompt spaces.

        execute_graph_query (Node 2): Automatically cleans markdown syntax text and runs query blocks against Neo4j.

        route_after_db (Conditional Edge): Evaluates query result densities to choose fallback paths or summary execution blocks.

        nlg_synthesize_response (Node 3): Leverages Gemma 2 to distill raw database rows down into verified compliance statements.


🤖 Sample Enterprise Queries to Test

The solution addresses critical business problems with cost and logistics efficiency on the line. Test the agent with these verified industry questions:

    1.	Which test type requirements apply to Two-Wheel Motorcycles regarding sound level?
    2.	What requirements are associated with Component Type-Approval for motorcycle parts?
    3.	How does Unece Regulation No 41 connect to Part A of Annex V?
    4.	Which test procedures must be executed to fulfill the Ix Test Type requirements?
    5.	What specific vehicle requirements are linked directly to noise and sound emissions limits?
    6.	Which vehicle configurations or models fall under the jurisdiction of Part A of Annex V?
    7.	What regulatory requirements apply to Two-Wheel Motorcycles regarding official approval documentation?
    8.	List all Applicable test procedures currently associated with Unece Regulation No 41.
    9.	Which requirements dictate the mandatory testing framework for motorcycle sound level validation?
    10.	Which specific regulatory articles or annexes define the compliance framework for L-Category Two-Wheel vehicles?


📊 Knowledge Graph Schema Visualization

To see a dense, multi-colored graph displaying all major compliance categories across your 6,000 entities inside Neo4j Browser (Query Tab), run the following optimized query:

Cypher

    MATCH (n)
    WHERE n:Vehicle 
        OR n:Article 
        OR n:Annex 
        OR n:`Applicable test procedure` 
        OR n:Requirement
        OR n:Approval
        OR n:Act
        OR n:Agreement
    MATCH (n)-[r]->(m)
    RETURN n, r, m
    LIMIT 6000;
