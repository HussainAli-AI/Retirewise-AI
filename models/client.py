"""Client profile data models."""
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class MaritalStatus(str, Enum):
    MARRIED = "Married"
    SINGLE = "Single"
    WIDOWED = "Widowed"
    DIVORCED = "Divorced"


class ClientProfile(BaseModel):
    """Core demographic and case data for a client."""
    client_id: str = Field(..., description="Unique client identifier")
    name: str = Field(..., description="Full client name")
    current_age: int = Field(..., ge=18, le=110, description="Current age in years")
    retirement_age: int = Field(..., ge=30, le=110, description="Planned or actual retirement age")
    planning_horizon_age: int = Field(85, ge=50, le=120, description="Life expectancy / planning horizon age")
    marital_status: MaritalStatus = Field(MaritalStatus.MARRIED, description="Marital status")
    dependents_count: int = Field(0, ge=0, description="Number of financially dependent individuals")
    adviser_name: str = Field("Adviser", description="Name of financial adviser")
    notes: Optional[str] = Field(None, description="Adviser case notes")

    @property
    def is_already_retired(self) -> bool:
        return self.current_age >= self.retirement_age

    @property
    def years_to_retirement(self) -> int:
        return max(0, self.retirement_age - self.current_age)

    @property
    def retirement_duration_years(self) -> int:
        return max(1, self.planning_horizon_age - max(self.current_age, self.retirement_age))
