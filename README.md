# TaxWise AI: Intelligent Tax Saving Guide for Beginners 🇮🇳

TaxWise AI is a responsive Indian income-tax guidance prototype for beginners, students, and young professionals.

The platform combines the **five mandatory architectural pillars**:
1. **RAG (Retrieval-Augmented Generation)**: Local TF-IDF retrieval over curated tax passages, filtered by financial year and returned with source metadata. The current prototype does not ingest PDFs or use an external vector database.
2. **NLP + LLM Conversational Layer**: Natural language question understanding with an "Explain Like I'm a Beginner" toggle and multi-turn context retention.
3. **Rule-Based Tax Calculation Engine**: Versioned by Financial Year (`FY 2024-25` and `FY 2025-26`). Deterministic calculations that never rely on LLMs for financial arithmetic.
4. **Personalized Tax-Saving Recommendation Engine**: Evaluates financial profiles against statutory rules and classifies opportunities into *Eligible*, *Potentially Eligible*, *Requires Additional Information*, and *Not Applicable*.
5. **Explainable AI (XAI) Layer**: Visible "Why am I seeing this?" transparency expander detailing triggering inputs, rules, logic, and missing information for every recommendation.

---

## 🏛️ System Architecture

```text
                                USER
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │    Web Application    │
                     │  Dashboard & Chat UI  │
                     └───────────┬───────────┘
                                 │
          ┌──────────────────────┴──────────────────────┐
          ▼                                             ▼
Natural Language Question                     Financial Profile & Inputs
          │                                             │
          ▼                                             ▼
      NLP + LLM                                 Rule-Based Engine
          │                                             │
          ▼                                             ▼
     RAG Pipeline                                Tax Calculation
          │                                             │
          ▼                                             ▼
  Tax Knowledge Base                          Recommendation Engine
          │                                             │
          └──────────────────────┬──────────────────────┘
                                 │
                                 ▼
                        Explainable AI Layer
                                 │
                                 ▼
                        Final User Response
```

---

## 📦 Project Structure

```text
TaxWise AI/
├── app.py                      # Flask server & REST API endpoints
├── tax_engine.py               # Deterministic Rule-Based Tax Calculator (TaxCalculator class)
├── recommendation_engine.py    # Personalized Tax Recommendation & Ranking Engine
├── explainable_ai.py           # Explainable AI layer ("Why am I seeing this?")
├── rag_engine.py               # In-memory TF-IDF retrieval over maintained passages
├── ai_assistant.py             # NLP + LLM assistant with Gemini API & grounded knowledge base
├── education_content.py        # Tax Education Center & Document Explainer data
├── admin_engine.py             # Admin telemetry, rule versioning, and document viewer
├── auth.py                     # User authentication, password hashing, and profile management
├── database.py                 # SQLite database schema, versioned tax rules, and models
├── test_taxwise.py             # Comprehensive test suite covering calculations, RAG, and APIs
├── PROJECT_DOCUMENTATION.md    # 26-chapter technical documentation specification
├── requirements.txt            # Python dependencies
├── .env.example                # Environment configuration template
├── templates/
│   └── index.html              # Modern, responsive single-page application with 10 navigation views
└── static/
    ├── css/
    │   └── style.css           # Premium FinTech design system (Navy/Blue/Green, responsive)
    └── js/
        └── app.js              # 8-step wizard controller, Chart.js donut chart, RAG chat controller
```

---

## ⚡ Quick Start Guide

### 1. Prerequisites
- Python 3.10 or higher installed.

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Configure Local Secrets
```powershell
Copy-Item .env.example .env
```
Set a private random `SECRET_KEY` and a separate `ADMIN_API_TOKEN` in `.env`. Leave `SESSION_COOKIE_SECURE=0` for local HTTP; set it to `1` when serving the app over HTTPS.

### 4. Run the Automated Test Suite
```powershell
python test_taxwise.py
```

### 5. Run the Application
```powershell
python app.py
```

Open your browser at:
👉 **[http://localhost:5000](http://localhost:5000)**

## Prototype Boundaries
- Knowledge passages and their citation metadata are maintained in code; PDF/web ingestion, embedding generation, and persistent vector indexing are not implemented.
- Source links currently point to the Income Tax Department portal, not to an independently verified document page for every passage. Verify current statutes before relying on a tax claim.
- Password changes require an authenticated session and the current password. Email-based forgotten-password recovery is not configured.
- Admin telemetry and rule writes require the separately configured `ADMIN_API_TOKEN`.
- Tax estimates are not certified filing calculations; the supported years are FY 2024-25 and FY 2025-26.

---

## ⚖️ Disclaimer

TaxWise AI provides educational information and estimates based on the information available in its knowledge base. Tax rules may change, and eligibility depends on individual circumstances. Always verify current rules using official sources or consult a qualified tax professional before filing or making financial decisions.
