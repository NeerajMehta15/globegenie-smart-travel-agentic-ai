# 🌍 GlobeGenie

**GlobeGenie** is an Agentic AI system designed to help users plan travel effortlessly — from researching destinations to organizing itineraries, flights, stays, and activities — with conversational intelligence and multi-agent coordination. Built with modularity in mind, GlobeGenie aims to evolve into a general-purpose assistant capable of handling a variety of planning and productivity tasks.

---

## Project Vision

> Build an intelligent, agent-powered assistant that can:
- Understand complex travel requirements via natural language
- Research and recommend destinations, flights, accommodations, and activities
- Optimize itineraries based on user preferences
- Adapt and expand to other verticals (finance, productivity, lifestyle)

- **LLM Backbone**: [Groq + Mistral](https://groq.com/)
- **Orchestration**: LangGraph
- **Embeddings**: MistralAI / HuggingFace Embeddings
- **Frontend**: Streamlit
- **Tool Integrations**: Google Flights API, Weather API, etc.
- **Database**: VectorStore (FAISS / Chroma for RAG), PostgreSQL for metadata

## Flow chart

```mermaid
graph TD
    A[User Request] -->|Input| B[Input Analyzer]
    B -->|Parsed State| O[Orchestrator Agent]
    O -->|Evaluate State| Dec1{Is Destination Known?}
    Dec1 -->|Yes: Light Research| C[Destination Research Agent]
    Dec1 -->|No: Full Research| C
    C -->|Research Data| O
    O -->|Parallel: Schedule| D[Itinerary Planner Agent]
    O -->|Parallel: Costs| E[Budget Analyzer Agent]
    D <-->|Refinements if Needed| E
    D -->|Itinerary| F[Travel Coordinator Agent]
    E -->|Budget Breakdown| F
    F -->|Synthesized Plan| G[Final Travel Plan]
    O -.->|Loop for Missing Info| A

    subgraph "Parallel Processing"
        D[Itinerary Planner Agent]
        E[Budget Analyzer Agent]
    end

    style A fill:#FF9999,stroke:#333333,stroke-width:2px,color:#000000
    style B fill:#66B2FF,stroke:#333333,stroke-width:2px,color:#000000
    style O fill:#FFD700,stroke:#333333,stroke-width:2px,color:#000000
    style Dec1 fill:#D3D3D3,stroke:#333333,stroke-width:2px,color:#000000
    style C fill:#99CC99,stroke:#333333,stroke-width:2px,color:#000000
    style D fill:#FF99CC,stroke:#333333,stroke-width:2px,color:#000000
    style E fill:#FFFF99,stroke:#333333,stroke-width:2px,color:#000000
    style F fill:#66CCCC,stroke:#333333,stroke-width:2px,color:#000000
    style G fill:#FF9999,stroke:#333333,stroke-width:2px,color:#000000
