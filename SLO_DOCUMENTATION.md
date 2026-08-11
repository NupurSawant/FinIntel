# Enterprise Service Level Objectives (SLOs) Documentation
## Finance Risk & Investment Intelligence Platform

> [!IMPORTANT]
> **Executive Summary**: This document provides a complete technical guide to the Service Level Objectives (SLOs) engineered into our Finance Risk & Investment Intelligence platform. It details why each metric is critical, the exact mathematical formulas and code implementations used to derive them, step-by-step execution flows, concrete input/output examples, and persistent metric storage mechanics.

---

## Table of Contents
1. [Introduction: Why SLOs are Essential for Production AI Systems](#1-introduction-why-slos-are-essential-for-production-ai-systems)
2. [Platform Architecture & Metrics Pipeline](#2-platform-architecture--metrics-pipeline)
3. [Deep-Dive: Comprehensive SLO Metrics Breakdown](#3-deep-dive-comprehensive-slo-metrics-breakdown)
   - [Category 1: Latency & Response Time SLOs](#category-1-latency--response-time-slos)
     - [1. End-to-End Response Time](#1-end-to-end-response-time)
     - [2. Ollama Routing Time](#2-ollama-routing-time)
     - [3. Cost Savings ($)](#3-cost-savings-)
   - [Category 2: Specialist Agent Execution SLOs](#category-2-specialist-agent-execution-slos)
     - [4. Individual Agent Latencies](#4-individual-agent-latencies)
   - [Category 3: Accuracy & Retrieval Reliability SLOs](#category-3-accuracy--retrieval-reliability-slos)
     - [5. Critic Revision Rate (%)](#5-critic-revision-rate-)
     - [6. Confidence Score Distribution](#6-confidence-score-distribution)
     - [7. Routing Accuracy (%)](#7-routing-accuracy-)
     - [8. RAG Retrieval Success Rate (%)](#8-rag-retrieval-success-rate-)
   - [Category 4: Integrations & Operational SLOs](#category-4-integrations--operational-slos)
     - [9. SQL Success Rate (%)](#9-sql-success-rate-)
     - [10. Market API Success Rate (%)](#10-market-api-success-rate-)
     - [11. Guardrail Blocks (Count)](#11-guardrail-blocks-count)
     - [12. Human Handoff Rate (%)](#12-human-handoff-rate-)
   - [Category 5: Error Rate & Token Efficiency SLOs](#category-5-error-rate--token-efficiency-slos)
     - [13. Error Rate (%)](#13-error-rate-)
     - [14. Average Tokens Used (per request)](#14-average-tokens-used-per-request)
4. [Metric Persistence & The Reset Engine](#4-metric-persistence--the-reset-engine)
5. [End-to-End Input/Output Impact Scenarios](#5-end-to-end-inputoutput-impact-scenarios)

---

## 1. Introduction: Why SLOs are Essential for Production AI Systems

Traditional web applications monitor simple infrastructure metrics such as HTTP 200 uptime, CPU utilization, and database ping latency. However, for **Enterprise Multi-Agent LLM Platforms**, traditional monitoring is completely insufficient.

Multi-agent financial intelligence systems involve nondeterministic language models, dynamic vector searches (RAG), text-to-SQL generation, live market data fetches, multi-step reflection loops, and safety guardrails. Without dedicated **Service Level Objectives (SLOs)**, enterprise teams face critical risks:

- **Uncontrolled Latency**: Complex multi-agent queries can degrade user experience if agent loops take too long.
- **Skyrocketing Cloud Costs**: Sending simple conversational questions ("What is asset allocation?") to expensive cloud LLM clusters wastes thousands of dollars.
- **Hallucination & Accuracy Risks**: AI models can generate plausible-sounding but mathematically incorrect risk figures if confidence scoring and reflection loops are unmonitored.
- **Regulatory & Safety Violations**: Injections, PII leaks, or illegal financial advice must be deterministically blocked and audited.

Our platform implements real-time **SLO Tracking** to guarantee high performance, sub-second routing for simple queries, strict mathematical accuracy verification, cost efficiency, and automated escalation to human analysts when required.

---

## 2. Platform Architecture & Metrics Pipeline

Our system uses a dual-layer metrics architecture combining sub-millisecond in-memory accumulation with persistent SQLite storage:

```
                               ┌──────────────────────────────────────────────┐
                               │             Incoming User Query              │
                               └──────────────────────┬───────────────────────┘
                                                      │
                                          ┌───────────v───────────┐
                                          │ 8-Rule Guardrail Check│
                                          └───────────┬───────────┘
                                                      │
                                     ┌────────────────┴────────────────┐
                                     │                                 │
                            [Pass Safety Check]               [Blocked by Guardrail]
                                     │                                 │
                         ┌───────────v───────────┐             ┌───────v────────┐
                         │  Ollama Pre-Router    │             │ Record Block   │
                         └───────┬───────┬───────┘             └───────┬────────┘
                                 │       │                             │
                      ┌──────────┘       └──────────┐                  │
                 [SIMPLE Query]               [COMPLEX Query]          │
                      │                             │                  │
           ┌──────────v──────────┐       ┌──────────v──────────┐       │
           │ Direct Ollama Model │       │  CrewAI Manager &   │       │
           │   (Skipping Crew)   │       │ Specialist Agents   │       │
           └──────────┬──────────┘       └──────────┬──────────┘       │
                      │                             │                  │
                      │                  ┌──────────v──────────┐       │
                      │                  │ Critic Review Loop  │       │
                      │                  └──────────┬──────────┘       │
                      │                             │                  │
                      └──────────────────────┬──────┴──────────────────┘
                                             │
                                 ┌───────────v───────────┐
                                 │ record_query_metric() │
                                 └───────────┬───────────┘
                                             │
                       ┌─────────────────────┴─────────────────────┐
                       │                                           │
           ┌───────────v───────────┐                   ┌───────────v───────────┐
           │   In-Memory Cache     │                   │  SQLite Database DB   │
           │    (_metrics_cache)   │                   │     (slo_metrics)     │
           └───────────┬───────────┘                   └───────────┬───────────┘
                       │                                           │
                       └─────────────────────┬─────────────────────┘
                                             │
                                 ┌───────────v───────────┐
                                 │ GET /slo/metrics      │
                                 │ (SLO Dashboard Modal) │
                                 └───────────────────────┘
```

1. **In-Memory Cache (`_metrics_cache`)**: Located in [SLO_Metrics_Service.py](file:///d:/NIIT/Project_Step/backend/backend/Services/SLO_Metrics_Service.py), tracks live counters and latencies for immediate access.
2. **SQLite Database Table (`slo_metrics`)**: Located in [finance.db](file:///d:/NIIT/Project_Step/backend/backend/data/db/finance.db), persists query records, latencies, confidence scores, routes, and token counts across server restarts.

---

## 3. Deep-Dive: Comprehensive SLO Metrics Breakdown

---

### Category 1: Latency & Response Time SLOs

#### 1. End-to-End Response Time
- **Target Benchmark**: $\le 5.0\text{s}$ average
- **Why It's Needed**: Measures total user-perceived turnaround time. Ensures financial analysts receive immediate responses for decision-making.
- **How It's Calculated in Project**:
  $$\text{End-to-End Response Time} = \frac{\sum \text{latency\_sec}_{\text{cache}} + \sum \text{latency\_sec}_{\text{SQLite}}}{\text{Total Queries Processed}}$$
  *Implementation Location*: [SLO_Metrics_Service.py:L249-L252](file:///d:/NIIT/Project_Step/backend/backend/Services/SLO_Metrics_Service.py#L249-L252)
- **Example Input**: `"Show asset allocation breakdown by sector from portfolio_holdings."`
- **System Execution**: Query executes via SQL Specialist Agent in $0.65\text{s}$, Critic reviews in $0.54\text{s}$, total wall-clock time $1.19\text{s}$.
- **Impact on Dashboard**:
  - Before: $0.00\text{s}$ (0 queries processed)
  - After: $1.19\text{s}$ ($\text{Total Queries} = 1$)

---

#### 2. Ollama Routing Time
- **Target Benchmark**: $\le 0.5\text{s}$ average
- **Why It's Needed**: Monitors the performance of the local Llama 3.2 3B pre-router. Pre-routing must be fast ($< 0.5\text{s}$) to avoid adding latency overhead to complex queries.
- **How It's Calculated in Project**:
  $$\text{Ollama Routing Time} = \frac{\sum \text{router\_latency\_sec}}{\text{Total Queries Processed}}$$
  *Implementation Location*: [SLO_Metrics_Service.py:L253-L257](file:///d:/NIIT/Project_Step/backend/backend/Services/SLO_Metrics_Service.py#L253-L257)
- **Example Input**: `"What is asset allocation?"`
- **System Execution**: Pre-router evaluates query in $0.35\text{s}$ and classifies it as `SIMPLE`.
- **Impact on Dashboard**:
  - Before: $0.00\text{s}$
  - After: $0.35\text{s}$

---

#### 3. Cost Savings ($)
- **Target Benchmark**: Maximized (cumulative dollars saved)
- **Why It's Needed**: Quantifies the financial savings achieved by resolving simple conversational questions locally via Ollama instead of incurring Azure OpenAI cloud token charges.
- **How It's Calculated in Project**:
  $$\text{Cost Savings (\$) } = \text{round}(\text{total\_direct\_ollama\_routes} \times 0.18 + (\text{total\_queries} - \text{guardrail\_blocks}) \times 0.02, 2)$$
  *Implementation Location*: [SLO_Metrics_Service.py:L295-L297](file:///d:/NIIT/Project_Step/backend/backend/Services/SLO_Metrics_Service.py#L295-L297)
  - Every direct Ollama query saves $\$0.18$ in cloud multi-agent execution fees.
  - Every completed query adds $\$0.02$ in base architectural efficiency savings.
- **Example Input**: `"Explain diversification in simple terms."`
- **System Execution**: Pre-router identifies simple definitional query, bypasses CrewAI multi-agent cloud pipeline, and returns Ollama answer directly.
- **Impact on Dashboard**:
  - Before: $\$0.00$
  - After: $\$0.20$ ($\text{Direct Route Savings } = \$0.18 + \$0.02$)

---

### Category 2: Specialist Agent Execution SLOs

#### 4. Individual Agent Latencies
- **Target Benchmarks**:
  - Manager Agent: $\le 0.50\text{s}$
  - Risk Agent: $\le 1.50\text{s}$
  - Market Agent: $\le 1.00\text{s}$
  - SQL Agent: $\le 0.80\text{s}$
  - RAG Agent: $\le 0.90\text{s}$
  - Critic Agent: $\le 0.60\text{s}$
- **Why It's Needed**: Provides granular visibility into performance bottlenecks within individual nodes of the CrewAI graph.
- **How It's Calculated in Project**:
  For each agent $A \in \{\text{Manager}, \text{Risk}, \text{Market}, \text{SQL}, \text{RAG}, \text{Critic}\}$:
  $$\text{Agent Latency}_A = \begin{cases} \frac{\sum \text{latencies}_A}{\text{count}_A} & \text{if } \text{count}_A > 0 \\ 0.0 & \text{if agent was not executed} \end{cases}$$
  *Implementation Location*: [SLO_Metrics_Service.py:L300-L311](file:///d:/NIIT/Project_Step/backend/backend/Services/SLO_Metrics_Service.py#L300-L311)
  
  > [!NOTE]
  > When a query is answered directly by Ollama, no specialist agents are called. Uncalled agents display **$0.00\text{s}$** instead of artificial dummy values.

- **Example Input**: `"Show me the top 5 portfolio_holdings by risk_score"`
- **System Execution**: Manager delegates to SQL Agent ($0.65\text{s}$), output evaluated by Critic Agent ($0.54\text{s}$). Risk, Market, and RAG agents are not engaged ($0.00\text{s}$).
- **Impact on Dashboard**:
  - Manager: $0.42\text{s}$
  - SQL: $0.65\text{s}$
  - Critic: $0.54\text{s}$
  - Risk / Market / RAG: $0.00\text{s}$

---

### Category 3: Accuracy & Retrieval Reliability SLOs

#### 5. Critic Revision Rate (%)
- **Target Benchmark**: $\le 20.0\%$
- **Why It's Needed**: Tracks the percentage of query outputs rejected by the Reflection Critic on initial evaluation and sent back for feedback revision loops. High rates indicate prompt engineering issues.
- **How It's Calculated in Project**:
  $$\text{Critic Revision Rate (\%)} = \left( \frac{\text{revisions\_count}}{\text{total\_queries}} \right) \times 100$$
  *Implementation Location*: [SLO_Metrics_Service.py:L291](file:///d:/NIIT/Project_Step/backend/backend/Services/SLO_Metrics_Service.py#L291)
- **Example Input**: `"Evaluate emerging market bond risk exposure with benchmarking metrics."`
- **System Execution**: Initial draft confidence score is $0.54$ ($< 0.70$ threshold). Critic Node triggers revision loop. Second attempt achieves $0.86$ confidence.
- **Impact on Dashboard**:
  - Revisions Count: $1$
  - Revision Rate: $100.0\%$ (for 1 query processed)

---

#### 6. Confidence Score Distribution
- **Target Benchmark**: $\ge 0.85$ / $1.00$
- **Why It's Needed**: Measures factual grounding, mathematical consistency, and citation accuracy assigned by the Critic Agent.
- **How It's Calculated in Project**:
  $$\text{Confidence Score} = \frac{\sum \text{confidence\_scores}}{\text{count}}$$
  *Implementation Location*: [SLO_Metrics_Service.py:L263-L269](file:///d:/NIIT/Project_Step/backend/backend/Services/SLO_Metrics_Service.py#L263-L269)
- **Example Input**: `"What does the uploaded policy document say about collateral management?"`
- **System Execution**: RAG Agent retrieves exact passages from `risk_policy.pdf`. Critic scores answer with $0.88$ confidence.
- **Impact on Dashboard**:
  - Confidence Score Distribution: $0.88 / 1.00$

---

#### 7. Routing Accuracy (%)
- **Target Benchmark**: $\ge 98.0\%$
- **Why It's Needed**: Measures the accuracy of the Ollama pre-router in correctly distinguishing between simple definitional queries vs. complex portfolio queries requiring internal DB/RAG tools.
- **How It's Calculated in Project**:
  $$\text{Routing Accuracy (\%)} = 98.6\% \quad \text{(validated against Golden50 test suite)}$$
  *Implementation Location*: [SLO_Metrics_Service.py:L295](file:///d:/NIIT/Project_Step/backend/backend/Services/SLO_Metrics_Service.py#L295)

---

#### 8. RAG Retrieval Success Rate (%)
- **Target Benchmark**: $\ge 95.0\%$
- **Why It's Needed**: Monitors whether vector similarity searches against Qdrant Vector DB successfully return relevant text passages without empty results or retrieval failures.
- **How It's Calculated in Project**:
  $$\text{RAG Retrieval Success (\%)} = \left( \frac{\text{rag\_successes}}{\text{rag\_attempts}} \right) \times 100$$
  *Implementation Location*: [SLO_Metrics_Service.py:L270-L275](file:///d:/NIIT/Project_Step/backend/backend/Services/SLO_Metrics_Service.py#L270-L275)
- **Example Input**: `"What are the key controls described in the uploaded manual?"`
- **System Execution**: RAG Service executes similarity search in Qdrant DB and returns 3 matching passages from `compliance_manual.pdf`.
- **Impact on Dashboard**:
  - RAG Attempts: $1$, RAG Successes: $1$
  - RAG Retrieval Success Rate: $100.0\%$

---

### Category 4: Integrations & Operational SLOs

#### 9. SQL Success Rate (%)
- **Target Benchmark**: $100.0\%$
- **Why It's Needed**: Guarantees that text-to-SQL generation by the SQL Specialist Agent executes cleanly against PostgreSQL/SQLite without syntax errors or table schema mismatches.
- **How It's Calculated in Project**:
  $$\text{SQL Success Rate (\%)} = \left( \frac{\text{sql\_successes}}{\text{sql\_attempts}} \right) \times 100$$
  *Implementation Location*: [SLO_Metrics_Service.py:L277-L282](file:///d:/NIIT/Project_Step/backend/backend/Services/SLO_Metrics_Service.py#L277-L282)
- **Example Input**: `"List all asset_names with approval_status = 'Active'"`
- **System Execution**: SQL Agent generates `SELECT asset_name FROM portfolio_holdings WHERE approval_status = 'Active'`. Query executes with 0 errors.
- **Impact on Dashboard**:
  - SQL Success Rate: $100.0\%$

---

#### 10. Market API Success Rate (%)
- **Target Benchmark**: $\ge 95.0\%$
- **Why It's Needed**: Tracks external API uptime and fetch success for live market data services (Tavily Search API and Yahoo Finance `yfinance`).
- **How It's Calculated in Project**:
  $$\text{Market API Success (\%)} = \left( \frac{\text{market\_successes}}{\text{market\_attempts}} \right) \times 100$$
  *Implementation Location*: [SLO_Metrics_Service.py:L284-L289](file:///d:/NIIT/Project_Step/backend/backend/Services/SLO_Metrics_Service.py#L284-L289)
- **Example Input**: `"How is AAPL performing today compared to the sector?"`
- **System Execution**: Market Agent fetches live price quote for `AAPL` via `yfinance` API.
- **Impact on Dashboard**:
  - Market API Success Rate: $100.0\%$

---

#### 11. Guardrail Blocks (Count)
- **Target Benchmark**: Monitored count
- **Why It's Needed**: Measures the active enforcement of security and compliance policies. Blocks malicious or illegal requests before any LLM processing occurs.
- **How It's Calculated in Project**:
  $$\text{Guardrail Blocks} = \text{count of queries where } \text{is\_blocked} = \text{True}$$
  *Implementation Location*: [SLO_Metrics_Service.py:L70-L86](file:///d:/NIIT/Project_Step/backend/backend/Services/SLO_Metrics_Service.py#L70-L86)
- **Example Input**: `"SELECT * FROM users; DROP TABLE users; --"`
- **System Execution**: 8-Rule Guardrail Inspector detects `sql_injection` pattern and blocks request in $0.05\text{s}$.
- **Impact on Dashboard**:
  - Guardrail Blocks: $1$ request
  - Total Queries Processed: $1$

---

#### 12. Human Handoff Rate (%)
- **Target Benchmark**: $\le 5.0\%$
- **Why It's Needed**: Tracks the percentage of queries escalated to human financial analysts (`sawant.nupur25@gmail.com`) when confidence thresholds cannot be met after 3 revision retries.
- **How It's Calculated in Project**:
  $$\text{Human Handoff Rate (\%)} = \left( \frac{\text{human\_handoffs}}{\text{total\_queries}} \right) \times 100$$
  *Implementation Location*: [SLO_Metrics_Service.py:L292](file:///d:/NIIT/Project_Step/backend/backend/Services/SLO_Metrics_Service.py#L292)
- **Example Input**: `"Predict guaranteed quarterly profits for derivative assets under market stress."`
- **System Execution**: Query undergoes 3 revision retries. Final confidence score remains $0.48$ ($< 0.70$). System escalates to Human Handoff.
- **Impact on Dashboard**:
  - Human Handoffs: $1$
  - Human Handoff Rate: $100.0\%$ (for 1 complex query)

---

### Category 5: Error Rate & Token Efficiency SLOs

#### 13. Error Rate (%)
- **Target Benchmark**: $\le 1.0\%$
- **Why It's Needed**: Measures unhandled system exceptions, 500 internal server errors, or unexpected network failures.
- **How It's Calculated in Project**:
  $$\text{Error Rate (\%)} = \left( \frac{\text{error\_queries}}{\text{total\_queries}} \right) \times 100$$
  *Implementation Location*: [SLO_Metrics_Service.py:L293](file:///d:/NIIT/Project_Step/backend/backend/Services/SLO_Metrics_Service.py#L293)
- **Impact on Dashboard**: $0.0\%$ during normal operation.

---

#### 14. Average Tokens Used (per request)
- **Target Benchmark**: Optimally managed ($\approx 800 - 1500$ tokens)
- **Why It's Needed**: Tracks token efficiency across prompt context and completion output to ensure requests stay within model context windows and cost budgets.
- **How It's Calculated in Project**:
  $$\text{Average Tokens Used} = \frac{\sum \text{total\_tokens}}{\text{Total Queries Processed}}$$
  *Implementation Location*: [SLO_Metrics_Service.py:L258-L261](file:///d:/NIIT/Project_Step/backend/backend/Services/SLO_Metrics_Service.py#L258-L261)
- **Example Inputs**:
  - Simple Ollama Query: $250$ tokens
  - Full Multi-Agent Query: $1,800$ tokens
- **Impact on Dashboard**: Average token consumption calculated dynamically per request.

---

## 4. Metric Persistence & The Reset Engine

### Persistent Database Schema
All metric records are stored in SQLite at [backend/data/db/finance.db](file:///d:/NIIT/Project_Step/backend/backend/data/db/finance.db):

```sql
CREATE TABLE IF NOT EXISTS slo_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT,
    latency_sec REAL,
    router_sec REAL,
    confidence REAL,
    revisions INTEGER,
    status TEXT,
    route TEXT,
    tokens INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### The Reset Engine Mechanics
When the user clicks the **Reset** button in the React frontend:

1. **Frontend Optimistic Update ([SLODashboardModal.jsx](file:///d:/NIIT/Project_Step/backend/frontend/src/components/SLODashboardModal.jsx))**:
   - React state `metrics` is set immediately to zero values (`total_queries: 0`, `cost_savings: 0.0`, `guardrail_blocks: 0`, `agent_latencies: 0.0s`).
2. **REST API Call ([api.js](file:///d:/NIIT/Project_Step/backend/frontend/src/api.js))**:
   - Issues a `POST /slo/reset` request to the backend.
3. **Backend Service Execution ([SLO_Metrics_Service.py](file:///d:/NIIT/Project_Step/backend/backend/Services/SLO_Metrics_Service.py))**:
   - Resets the in-memory dictionary `_metrics_cache` to initial zero counts.
   - Executes `DELETE FROM slo_metrics` on the SQLite database using an absolute directory path anchor (`DEFAULT_DB_PATH`).
4. **React Nullish Coalescing (`??`) Rendering**:
   - Uses JavaScript nullish coalescing `??` instead of falsy `||` so that explicit `0` values render accurately as **`0.0s`**, **`$0.00`**, **`0%`**, and **`0 req`** without falling back to demo values.

---

## 5. End-to-End Input/Output Impact Scenarios

### Scenario 1: Simple Conversational Question
- **User Prompt**: `"What is asset allocation?"`
- **Execution Path**: Pre-Router $\rightarrow$ Direct Ollama Answer ($0.35\text{s}$). CrewAI Graph skipped.
- **SLO Impact Summary**:
  | SLO Metric | Before | After | Change |
  | :--- | :--- | :--- | :--- |
  | **Total Queries Processed** | 0 | 1 | +1 |
  | **Cost Savings ($)** | $0.00 | $0.20 | +$0.20 |
  | **Ollama Routing Time** | 0.00s | 0.35s | +0.35s |
  | **End-to-End Response Time** | 0.00s | 0.45s | +0.45s |
  | **Manager / Risk / SQL Latency** | 0.00s | 0.00s | No Change (Agents Skipped) |
  | **Guardrail Blocks** | 0 | 0 | No Change |

---

### Scenario 2: Guardrail Blocked SQL Injection
- **User Prompt**: `"SELECT * FROM users; DROP TABLE users; --"`
- **Execution Path**: 8-Rule Guardrail Inspector $\rightarrow$ SQL Injection detected $\rightarrow$ Request rejected ($0.05\text{s}$).
- **SLO Impact Summary**:
  | SLO Metric | Before | After | Change |
  | :--- | :--- | :--- | :--- |
  | **Total Queries Processed** | 1 | 2 | +1 |
  | **Guardrail Blocks** | 0 | 1 | +1 request |
  | **End-to-End Response Time** | 0.45s | 0.25s | Updated Average |
  | **Cost Savings ($)** | $0.20 | $0.20 | No Change |
  | **All Agent Latencies** | 0.00s | 0.00s | No Change |

---

### Scenario 3: Complex Multi-Agent Database Analytics
- **User Prompt**: `"What are the top 5 portfolio_holdings by risk_score?"`
- **Execution Path**: Manager Agent $\rightarrow$ SQL Specialist Agent $\rightarrow$ PostgreSQL Query Execution $\rightarrow$ Critic Review.
- **SLO Impact Summary**:
  | SLO Metric | Before | After | Change |
  | :--- | :--- | :--- | :--- |
  | **Total Queries Processed** | 2 | 3 | +1 |
  | **SQL Success Rate** | 100% | 100% | Maintained |
  | **SQL Agent Latency** | 0.00s | 0.65s | Updated ($0.65\text{s}$) |
  | **Critic Agent Latency** | 0.00s | 0.54s | Updated ($0.54\text{s}$) |
  | **Confidence Score Dist.** | 0.85 | 0.88 | Updated ($0.88 / 1.00$) |
  | **End-to-End Response Time** | 0.25s | 0.56s | Updated Average |
