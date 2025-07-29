from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class CustomerInfo(BaseModel):
    name: str
    website: str
    industry: str
    city: str
    state: str
    specialty: Optional[str] = []
    revenue: Optional[int] = []
    numEmployees: Optional[int]

class LeadInfo(BaseModel):
    name: str
    description: str
    website: str
    city: str
    state: str
    specialty: Optional[str] = []
    revenue: Optional[int] = []
    numEmployees: Optional[int]
    leadership: List[str] = []

class ResearchState(BaseModel):
    query: str
    customer_desc: str
    industry: str
    targetEvent: str
    targetLead: str
    lead_desc: str
    leadContact: str
    fitAnalysis: str
    outreachMsg: str




