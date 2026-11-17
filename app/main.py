import json
import csv
import io
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import UtilityModel, MonthlyRateModel

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

app = FastAPI(
    title="Philippine Open Energy Data API",
    description=(
        "Proof-of-Concept civic data pipeline for the BetterGovPH Fellowship (Energy Track), "
        "supporting the Department of Energy (DOE) & Mura, Malinis, at Maaasahang Kuryente Coalition. "
        "Provides standardized utility entity registries (PSGC-mapped), monthly rate tracking, "
        "and open data export feeds for DBM COMPASS interoperability."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_json_file(filename: str):
    file_path = DATA_DIR / filename
    if not file_path.exists():
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/", tags=["General"])
def root():
    return {
        "project": "Open Energy Data Layer (Philippines)",
        "track": "BetterGovPH Fellowship 2026-2027 - Energy Track",
        "partners": [
            "Department of Energy (DOE)",
            "Mura, Malinis, at Maaasahang Kuryente Coalition",
            "WeSolve Foundation",
            "DBM COMPASS"
        ],
        "status": "Operational Proof-of-Concept",
        "docs": "/docs",
        "endpoints": {
            "utilities": "/api/v1/utilities",
            "rates": "/api/v1/rates",
            "summary_analytics": "/api/v1/summary",
            "export_csv": "/api/v1/export/csv",
            "export_json": "/api/v1/export/json"
        }
    }

# ---------------------------------------------------------------------------
# Deliverable 1: Master Energy Utility Registry (ERC, DOE, NEA)
# ---------------------------------------------------------------------------
@app.get("/api/v1/utilities", response_model=List[UtilityModel], tags=["Master Utility Registry"])
def get_utilities(
    region: Optional[str] = Query(None, description="Filter by region name or code"),
    utility_type: Optional[str] = Query(None, description="Filter by utility type (e.g. 'Electric Cooperative')")
):
    """
    Returns the master registry of electricity distribution utilities and cooperatives,
    standardized with Philippine Standard Geographic Codes (PSGC).
    """
    utilities = load_json_file("utilities_registry.json")
    results = utilities

    if region:
        results = [
            u for u in results 
            if region.lower() in u["psgc"]["region_name"].lower() or region in u["psgc"]["region_code"]
        ]
    if utility_type:
        results = [
            u for u in results 
            if utility_type.lower() in u["type"].lower()
        ]
    return results

@app.get("/api/v1/utilities/{utility_id}", response_model=UtilityModel, tags=["Master Utility Registry"])
def get_utility_by_id(utility_id: str):
    """Retrieve details for a specific utility by canonical ID."""
    utilities = load_json_file("utilities_registry.json")
    for u in utilities:
        if u["utility_id"].upper() == utility_id.upper():
            return u
    raise HTTPException(status_code=404, detail="Utility not found in master registry.")

# ---------------------------------------------------------------------------
# Deliverable 2: Standardized Monthly Electricity Rates & Generation Charges
# ---------------------------------------------------------------------------
@app.get("/api/v1/rates", response_model=List[MonthlyRateModel], tags=["Electricity Rates"])
def get_monthly_rates(
    utility_id: Optional[str] = Query(None, description="Filter by canonical utility_id"),
    billing_month: Optional[str] = Query(None, description="Filter by billing period (YYYY-MM)")
):
    """
    Returns monthly electricity rates per kWh, including unbundled generation charges.
    """
    rates = load_json_file("monthly_rates.json")
    results = rates

    if utility_id:
        results = [r for r in results if r["utility_id"].upper() == utility_id.upper()]
    if billing_month:
        results = [r for r in results if r["billing_month"] == billing_month]
    return results

@app.get("/api/v1/summary", tags=["Electricity Rates"])
def get_rates_summary():
    """
    Computes summary insights on rate volatility and generation charge impact.
    Directly answers: 'Magkano ba talaga ang bayad natin sa kuryente?'
    """
    rates = load_json_file("monthly_rates.json")
    if not rates:
        return {"count": 0}

    kwh_prices = [r["rate_per_kwh"] for r in rates]
    gen_shares = [r["generation_share_pct"] for r in rates]

    highest = max(rates, key=lambda x: x["rate_per_kwh"])
    lowest = min(rates, key=lambda x: x["rate_per_kwh"])
    avg_price = round(sum(kwh_prices) / len(kwh_prices), 2)
    avg_gen_share = round(sum(gen_shares) / len(gen_shares), 1)

    return {
        "total_monitored_records": len(rates),
        "average_rate_per_kwh": avg_price,
        "average_generation_charge_share_pct": avg_gen_share,
        "highest_rate": {
            "utility": highest["utility_name"],
            "rate_per_kwh": highest["rate_per_kwh"],
            "billing_month": highest["billing_month"]
        },
        "lowest_rate": {
            "utility": lowest["utility_name"],
            "rate_per_kwh": lowest["rate_per_kwh"],
            "billing_month": lowest["billing_month"]
        },
        "asean_context": "Philippine average residential rate reached ~₱12.43/kWh in June 2026, highest in ASEAN."
    }

# ---------------------------------------------------------------------------
# Deliverable 3: Open Data Export & DBM COMPASS Feeds
# ---------------------------------------------------------------------------
@app.get("/api/v1/export/csv", tags=["Open Data Feeds"])
def export_rates_csv():
    """Download standardized rate records as a machine-readable CSV file."""
    rates = load_json_file("monthly_rates.json")
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "rate_id", "utility_id", "utility_name", "billing_month", 
        "rate_per_kwh", "generation_charge", "generation_share_pct", "source_url"
    ])
    for r in rates:
        writer.writerow([
            r["rate_id"],
            r["utility_id"],
            r["utility_name"],
            r["billing_month"],
            r["rate_per_kwh"],
            r["breakdown"]["generation_charge"],
            r["generation_share_pct"],
            r["source_url"]
        ])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=ph_electricity_rates_export.csv"}
    )

@app.get("/api/v1/export/json", tags=["Open Data Feeds"])
def export_rates_json():
    """Download standardized rate records as a machine-readable JSON file."""
    rates = load_json_file("monthly_rates.json")
    return Response(
        content=json.dumps(rates, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=ph_electricity_rates_export.json"}
    )
