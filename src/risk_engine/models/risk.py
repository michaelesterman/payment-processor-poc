from enum import Enum
from pydantic import BaseModel


class VerdictEnum(str, Enum):
    ACCEPTED = "accepted"
    DECLINED = "declined"

class RiskAssessment(BaseModel):
    payment_id: str
    risk_level: float
    verdict: VerdictEnum