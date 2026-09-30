# ◈ ATSMATRIX // Multi-Agent Research Collision & Neural Graph Engine

[![Live Website](https://img.shields.io/badge/Live%20Demo-anyel1to.github.io-0284c7?style=for-the-badge&logo=google-chrome&logoColor=white)](https://anyel1to.github.io/atsmatrix-agent-visualizeR--ANYEL1TO/)
[![License: MIT](https://img.shields.io/badge/License-MIT-38bdf8.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Engine: 60--120 FPS](https://img.shields.io/badge/Render%20Engine-60--120%20FPS-10b981?style=for-the-badge)](https://anyel1to.github.io/atsmatrix-agent-visualizeR--ANYEL1TO/)
[![Throughput](https://img.shields.io/badge/Throughput-2%2C450%2B%20msg%2Fs-7c3aed?style=for-the-badge)](https://anyel1to.github.io/atsmatrix-agent-visualizeR--ANYEL1TO/)
[![LLM: Google Gemini](https://img.shields.io/badge/AI%20Core-Google%20Gemini-e11d48?style=for-the-badge&logo=google)](https://anyel1to.github.io/atsmatrix-agent-visualizeR--ANYEL1TO/)

> **500+ agents. Sources collide. Truth survives.**  
> An ultra-high-throughput, graph-native multi-agent visualizer and telemetry engine designed by **ATSMATRIX Technologies**. Connect autonomous AI agents (LangGraph, CrewAI, AutoGen, or custom LLMs) and monitor reasoning, citation verification, and memory sync in real time.

---

## 🌐 Live Web App
Experience the live engine in your browser:  
👉 **[https://anyel1to.github.io/atsmatrix-agent-visualizeR--ANYEL1TO/](https://anyel1to.github.io/atsmatrix-agent-visualizeR--ANYEL1TO/)**

---

## 📑 Table of Contents
1. [Core Features](#-core-features)
2. [Architecture Overview](#-architecture-overview)
3. [User Tutorial (Web Interface)](#-user-tutorial-web-interface)
4. [Developer Integration Tutorial](#-developer-integration-tutorial)
   - [Python (LangGraph & Custom Agents)](#1-python-langgraph--custom-agents)
   - [CrewAI Multi-Agent Swarms](#2-crewai-multi-agent-swarms)
   - [cURL & REST Webhooks](#3-curl--rest-webhook)
   - [JavaScript / TypeScript (Node.js & Web)](#4-javascript--typescript)
5. [Event Payload Specification](#-event-payload-specification)
6. [Local Installation & Desktop Build](#-local-installation--desktop-build)
7. [License & Credits](#-license--credits)

---

## ✨ Core Features

- **520+ Active Agents & 180+ Moving Photons**: Real-time canvas physics with continuous data packet flows traveling along cross-cluster bridges.
- **Google Gemini LLM Integration**: Built-in interactive AI chat assistant that streams live Chain-of-Thought reasoning directly into the collision network.
- **5-Phase Pipeline HUD**: Real-time status tracking for `COLLECT` → `MATCH` → `CROSS-LINK` → `VERIFY` → `SYNTH`.
- **Evidence Wall Matrix**: 112 reactive status tiles tracking memory commitments, source verification, and counterparty overlaps.
- **Interactive Physics Engine**: Drag, drop, and rearrange agent clusters on the fly with orbital momentum and spring tension.
- **Dark / Light Cyber Aesthetics**: High-contrast research view with instant theme toggle (`🌓`).
- **Zero-Dependency Deployment**: Single-file architecture ready to run on GitHub Pages, Netlify, Vercel, or local browser.

---

## 🏗️ Architecture Overview

The **ATSMATRIX Collision Engine** structures multi-agent swarms into 4 specialized clusters:

```mermaid
graph TD
    USER([User Objective / Query]) --> C1[1. DISCOVERY_HUB (Cyan)]
    C1 --> C2[2. REASONING_ENGINE (Purple)]
    C2 --> C3[3. VERIFICATION_CORE (Magenta)]
    C3 -- Anomaly / Contradiction --> C2
    C3 -- Verified --> C4[4. SYNTHESIS_BROKER (Blue)]
    C4 --> DELIVERABLE([Consensus Truth Delivered])

    style USER fill:#0f172a,stroke:#0284c7,stroke-width:2px,color:#fff
    style C1 fill:#082f49,stroke:#06b6d4,stroke-width:2px,color:#fff
    style C2 fill:#3b0764,stroke:#a855f7,stroke-width:2px,color:#fff
    style C3 fill:#4c0519,stroke:#f43f5e,stroke-width:2px,color:#fff
    style C4 fill:#0c4a6e,stroke:#38bdf8,stroke-width:2px,color:#fff
    style DELIVERABLE fill:#052e16,stroke:#22c55e,stroke-width:2px,color:#fff


---

## QQQ Alpaca Multi-Agent Paper Trader (starter)

This fork now includes a Python backend that turns the visualizer into the foundation for a QQQ options paper-trading system.

### Safety model

- **Alpaca is the broker and market-data platform.**
- The starter refuses live mode: `ALPACA_PAPER=false` raises an error.
- `TRADING_ENABLED=false` is the default, so approved orders are dry-runs until explicitly enabled.
- Market, news, and options agents produce structured analysis only.
- A deterministic `RiskEngine` gates every order.
- Only `AlpacaPaperExecutor` can submit an order.
- API keys belong in local `.env`; `.env` is gitignored.

### Agents

`MarketAgent` evaluates QQQ technical state (starter ORB/VWAP/relative-volume logic). `NewsAgent` normalizes a supplied news sentiment snapshot. `OptionsAgent` filters call/put candidates and favors tighter spreads / delta near 0.55 when available. `StrategyAgent` combines the structured signals. These are deliberately simple v0 components intended for paper testing and measurement, not claims of profitability.

### Run locally (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python -m pytest
python -m uvicorn backend.main:app --reload
```

Then open `http://127.0.0.1:8000/health`. Keep `TRADING_ENABLED=false` initially. After adding **paper** Alpaca credentials and validating dry-run behavior, setting it to `true` permits risk-approved paper option orders.

### Next implementation phases

1. Pull QQQ bars, snapshots, option chains/Greeks, account state and news directly from Alpaca instead of accepting snapshots through the API.
2. Add persistent decision/order telemetry and connect it to the existing ATSMATRIX frontend.
3. Add fill/position management, exits, session controls and stronger contract-selection rules.
4. Backtest/replay the exact strategy and then run extended paper tests before changing any risk parameters.


### Live ATSMATRIX trading dashboard

FastAPI now serves the existing visualizer at the application root and streams actual orchestrator telemetry over `/ws`. Start the backend:

```powershell
python -m uvicorn backend.main:app --reload
```

Open `http://127.0.0.1:8000` (not the standalone HTML file). The QQQ Agent Control panel shows Market, News, Options, Strategy, Risk and Execution state in real time. The browser reconnects automatically if the WebSocket drops.

For a development smoke test, POST a cycle to `/api/v1/cycle`; the dashboard will animate and log each real backend stage. Until live Alpaca data ingestion is added, that endpoint accepts explicit market/news/options snapshots. Order execution remains dry-run unless `TRADING_ENABLED=true`, and the backend still refuses non-paper mode.


### Market Agent: live QQQ data

With Alpaca paper credentials in `.env`, call `GET /api/v1/market/qqq` to fetch QQQ 1-minute bars and run the Market Agent. It calculates session VWAP, the 09:30-09:35 ET opening range, relative volume against up to five prior comparable sessions, 14-period RSI and 5-minute momentum. The result is also emitted over `/ws` to the ATSMATRIX dashboard.

Use `ALPACA_STOCK_FEED=iex` for the Basic/free real-time feed. Set it to `sip` only when the account has current SIP entitlement.


### Remaining live agents

- `GET /api/v1/news/qqq` fetches recent Alpaca news and runs the News Agent.
- `POST /api/v1/live-cycle` gathers live QQQ market bars, recent news and the option chain, then runs Market -> News -> Options -> Strategy -> Risk -> Execution telemetry.
- Execution stays `DRY_RUN` while `TRADING_ENABLED=false`. Keep this setting during development. The risk engine remains deterministic and is the only gate before the paper executor.
