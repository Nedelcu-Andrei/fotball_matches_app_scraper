# Football Matches & Odds Scraper ⚽

A Python application that fetches, parses and validates football match and odds data from an external API.  
Designed as a modular backend/data-ingestion tool — with caching, data validation, mock-data support and full test coverage.

## 🚀 What it does

- Fetches live data: fixtures (games) and betting odds.  
- Parses raw API responses into clean, validated Python data models.  
- Saves raw responses (JSON or fallback plain-text) for later inspection or re-processing.  
- Supports **mock-mode** (load from saved raw data) — ideal for offline testing or development.  
- Provides a **robust backend pipeline** with logging, error handling and caching.  

---

## 🔧 Key Features & Highlights

- **Modular architecture** — clear separation: API client → parser → data models → format/data output.  
- **Strict data validation** using dataclasses: type validation, date/time parsing, odds format checks.  
- **Mock-data support** — use previous real API dumps to test and iterate without hitting the live API.  
- **Raw data caching** — preserves API responses for debugging, auditing or re-running logic.  
- **Automated testing** — full test suite using pytest: ensures correctness of parsing, validation and core logic.  
- **Clean backend-ready design** — no UI dependencies, suitable for integration into larger systems or data pipelines.  
- **GitHub-friendly project layout** — .gitignore, unit tests, consistent structure, version control best practices.  

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.10+  
- (Optional) virtualenv or venv for environment isolation  

### Installation & Setup

```bash
# Clone the repo
git clone https://github.com/Nedelcu-Andrei/fotball_matches_app_scraper.git
cd fotball_matches_app_scraper

# (optional) Create a virtual environment
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\\Scripts\\activate    # Windows

# Install dependencies
pip install -r requirements.txt
