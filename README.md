# Open Energy Data Layer (Philippines)
### Civic Technology Pipeline for Open, Transparent, and Comparable Electricity Data
**BetterGovPH Fellowship 2026–2027 | Energy Track Proposal & Proof of Concept**  
*Aligned with the Department of Energy (DOE) & Mura, Malinis, at Maaasahang Kuryente Coalition Challenge*

---

##  Executive Summary
The Philippines has some of the highest electricity rates in Southeast Asia (averaging ₱12.43/kWh in mid-2026). Over 50% to 60% of an electric bill consists of **generation charges**, which fluctuate monthly. However, this critical data is fragmented across 142 distribution utilities (DUs) and electric cooperatives (ECs), buried in PDFs, web tables, and social media notices without standardized entity identifiers across ERC, DOE, and NEA.

This repository provides the **proof-of-concept data engineering pipeline and public API** to:
1. **Unify Entity Records:** Build a Master Registry of all 142 power utilities with Philippine Standard Geographic Codes (PSGC).
2. **Standardize Monthly Rates:** Model a normalized schema capturing monthly kWh rates and generation charges.
3. **Expose Open Data Feeds:** Provide documented REST API endpoints and downloadable CSV/JSON exports for civil society, researchers, and future **DBM COMPASS** integration.

---

##  System Architecture

```
[Raw Sources: ERC, DOE, NEA, 142 Utilities]
       │
       ├──► [1. Entity Registry Parser] ──► Standard PSGC Mapping
       │                                            │
       └──► [2. Rate Ingestion Pipeline] ─────────► [Unified Relational Store]
                                                            │
                                        ┌───────────────────┴───────────────────┐
                                        ▼                                       ▼
                             [3. Public REST API]                    [Open Data Exports]
                          (FastAPI / OpenAPI Spec)                       (CSV / JSON)
                                        │                                       │
                                        ▼                                       ▼
                              [Civil Society / LGUs]                 [DBM COMPASS System]
```

---

##  The 3 Core Deliverables

### 1. Master Utility Registry
Deduplicates electric utilities and maps them to standard PSGC codes (Region, Province, Municipality) so energy data can be cross-referenced with local government budgets and geographic boundaries.
* Endpoint: `GET /api/v1/utilities`
* Search/Filter: by region, province, or utility type (Private DU vs. Electric Cooperative).

### 2. Standardized Monthly Rate Schema
Normalizes published monthly retail rates and unbundles the generation charge so consumers and LGUs can track rate volatility over time.
* Endpoint: `GET /api/v1/rates`
* Key fields: `utility_id`, `billing_period`, `rate_per_kwh`, `generation_charge`, `source_url`.

### 3. Open Data Feeds & Bulk Downloads
Enables external platforms (like DBM COMPASS and eGovPH) and public monitors to retrieve structured datasets programmatically or via direct bulk downloads.
* Endpoints: `GET /api/v1/export/csv` and `GET /api/v1/export/json`

---

##  Project Structure

```text
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application & route definitions
│   └── schemas.py          # Pydantic data models for validation
├── data/
│   ├── utilities_registry.json # Initial seed of distribution utilities with PSGC
│   └── monthly_rates.json      # Sample normalized monthly utility rates
├── EnergyTrackPlan.md       # Comprehensive 3-month development roadmap
├── requirements.txt         # Minimal Python dependencies
└── README.md                # Project documentation
```

---

##  Quickstart (Running Locally)

### 1. Clone the repository and install dependencies
```bash
git clone https://github.com/<your-username>/open-energy-data-ph.git
cd open-energy-data-ph
pip install -r requirements.txt
```

### 2. Start the API server
```bash
uvicorn app.main:app --reload
```

### 3. Explore the Interactive API Documentation
Open your browser and navigate to:
* **Interactive Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc Documentation:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

##  DBM COMPASS Interoperability
Under Executive Order No. 126, s. 2026, DBM COMPASS monitors public expenditures and local government spending. This project integrates seamlessly by:
* Indexing every power utility by its **PSGC geographic code**, enabling COMPASS to correlate local subsidies and energy infrastructure investments with actual power rates.
* Providing **OpenAPI-compliant endpoints** ready for automated data pulling without manual consolidation.

---

##  3-Month Fellowship Roadmap (Dec 2026 – Mar 2027)
* **Month 1:** Complete inventory of all 142 utilities, reconcile ERC/DOE/NEA rosters, seed PostgreSQL database with full PSGC codes.
* **Month 2:** Implement modular parsing scripts for utility rate PDF announcements; establish data validation with coalition analysts.
* **Month 3:** Deploy public API, automate daily/monthly open data dumps, publish integration guides for DBM COMPASS and Demo Day.

---

##  License
Released under the **MIT License** for public benefit and open governance.
