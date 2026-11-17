from typing import Optional, Dict
from pydantic import BaseModel, Field

class PSGCInfo(BaseModel):
    region_name: str
    region_code: str
    coverage_summary: str

class RegulatorIDs(BaseModel):
    erc_id: Optional[str] = None
    doe_id: Optional[str] = None
    nea_id: Optional[str] = None

class UtilityModel(BaseModel):
    utility_id: str = Field(..., description="Canonical standard utility identifier")
    name: str
    type: str = Field(..., description="Private Distribution Utility or Electric Cooperative")
    regulator_ids: RegulatorIDs
    psgc: PSGCInfo
    status: str = "Active"

class RateBreakdown(BaseModel):
    generation_charge: float
    transmission_charge: float
    system_loss_charge: float
    distribution_charge: float
    subsidies_and_taxes: float

class MonthlyRateModel(BaseModel):
    rate_id: str
    utility_id: str
    utility_name: str
    billing_month: str = Field(..., description="Format: YYYY-MM")
    rate_per_kwh: float
    breakdown: RateBreakdown
    generation_share_pct: float
    source_url: str
    source_format: str
    verified: bool = True
