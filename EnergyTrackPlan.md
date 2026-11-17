# Open Energy Data Layer: 3-Month Implementation Plan
**BetterGovPH Fellowship 2026–2027 | Energy Track**  
*Partner: Department of Energy (DOE) × Mura, Malinis, at Maaasahang Kuryente Coalition*

---

## 1. Scope & Objective
This plan outlines a lean, disciplined data engineering roadmap for a solo developer to deliver the three core components specified in the official DOE challenge pitch (Slide 40):
1. **Master Utility Registry** (Entity standardization across ERC, DOE, and NEA)
2. **Monthly Electricity Rate Ingestion** (Standardized schema for 142 electric utilities)
3. **Open Data Feeds & Download API** (Structured public access & DBM COMPASS integration)

**Guiding Principles:** No complex multi-cloud infrastructure, no unnecessary AI buzzwords, no monolithic portals. Focus purely on clean schemas, reliable ingestion scripts, and standard REST APIs.

---

## 2. Technical Stack (Minimal & Resilient)
* **Ingestion & Processing:** Python (`pandas`, `pdfplumber`, `BeautifulSoup4`)
* **Storage / Database:** PostgreSQL (or SQLite for lightweight local development)
* **API Framework:** FastAPI (auto-generates OpenAPI / Swagger docs)
* **Standards:** Philippine Standard Geographic Code (PSGC), ISO 8601 dates, OpenAPI 3.0

---

## 3. The 3 Core Deliverables

### Deliverable 1: Master Energy Utility Registry
* **Problem Addressed:** 142 electric utilities and cooperatives sit across DOE, ERC, and NEA with conflicting names and no common ID.
* **Scope of Work:**
  * Collect existing rosters from DOE, ERC, and NEA.
  * Deduplicate and assign a unified canonical identifier (`utility_id`).
  * Tag each entity with its official Philippine Standard Geographic Code (`psgc_code` - region, province, municipality).
* **Output:**
  * Clean, seedable relational table: `utilities_master`
  * REST endpoint: `GET /api/v1/utilities` (filterable by region/province).

### Deliverable 2: Electricity Rate Data Collection & Schema
* **Problem Addressed:** Utilities publish rates in unstructured formats (PDFs, social media notices, static tables); generation charges (50–60% of bills) are hard to isolate and compare.
* **Scope of Work:**
  * Design a normalized schema: `[utility_id, billing_month, rate_per_kwh, generation_charge, source_url, verified_status]`.
  * Build modular parsers for available utility rate tables and monthly PDF releases.
  * Implement basic integrity checks (e.g., flag missing values, outlier rate spikes).
* **Output:**
  * Normalized historical and monthly rate dataset.
  * REST endpoint: `GET /api/v1/rates` (query by utility, month, or region).

### Deliverable 3: DOE Data Feeds & Download API
* **Problem Addressed:** DOE's renewable energy contracts and priority project dashboards are manually updated and lack bulk machine-readable access.
* **Scope of Work:**
  * Build automated export pipelines converting verified utility rates and DOE project summaries into downloadable static formats (CSV and JSON).
  * Document all endpoints according to OpenAPI standards so external systems (DBM COMPASS, eGovPH, CSOs) can ingest feeds directly.
* **Output:**
  * Bulk download endpoints: `GET /api/v1/export/csv` and `GET /api/v1/export/json`.
  * Publicly accessible OpenAPI/Swagger specification.

---

## 4. 3-Month Sprint Roadmap (December 2026 – March 2027)

```
[Month 1: Registry & PSGC] ──► [Month 2: Ingestion & Schema] ──► [Month 3: API & COMPASS Handover]
```

### Month 1: Discovery, Registry & Geo-Tagging (Weeks 1–4)
* **Week 1:** Align with DOE technical focal person and coalition data analysts; inventory available lists from ERC, DOE, and NEA.
* **Week 2:** Deduplicate entity names and assign unique canonical utility IDs.
* **Week 3:** Map utilities and franchise areas to PSA Standard Geographic Codes (PSGC).
* **Week 4:** Finalize and seed the master PostgreSQL database table; deliver initial registry export.

### Month 2: Rate Ingestion & Normalization (Weeks 5–8)
* **Week 5:** Establish the relational schema for monthly rates and generation charges.
* **Week 6:** Develop Python extraction scripts for pilot utility rate PDFs and web tables.
* **Week 7:** Run data validation checks with the coalition data analyst (reconcile records and units).
* **Week 8:** Ingest historical data for pilot utilities and electric cooperatives.

### Month 3: API Delivery, Documentation & Handover (Weeks 9–12)
* **Week 9:** Build and test FastAPI endpoints (`/utilities`, `/rates`, `/exports`).
* **Week 10:** Set up automated script generating daily/monthly static CSV and JSON dumps.
* **Week 11:** Write clear technical documentation, data dictionary, and DBM COMPASS integration guide.
* **Week 12:** Final Demo Day rehearsal, open-source code release, and project handover.

---

## 5. DBM COMPASS Interoperability
* **Common Identifier:** By standardizing around PSGC location codes, DBM COMPASS can seamlessly join energy rates with local government budget releases (LGSF/NTA) without modifying COMPASS's internal architecture.
* **Programmatic Integration:** COMPASS backend services can query the OpenAPI-compliant REST endpoints directly to display regional energy indicators.

---

## 6. Solo Delivery Capacity & Risk Management
* **Scope Discipline:** Focus strictly on data standardization and API ingestion. Complex UI dashboards or full scraping of 100% of all obscure coops are phased as stretch goals.
* **Weekly Commitment:** 15–20 hours per week (fully sufficient for scripting, schema design, and weekly 1-hour government syncs).
* **Dependency Fallback:** If agency API access is delayed, the pipeline functions reliably on public web tables and PDF filings using local ingestion scripts.
