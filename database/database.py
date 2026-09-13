"""SQLite database operations for RetireWise AI."""
import sqlite3
import json
from typing import List, Optional, Dict, Any
from models.client import ClientProfile
from models.financial_profile import FinancialProfile
from models.assessment import SuitabilityAssessmentResult


class Database:
    """Manages SQLite storage for clients, financial profiles, and suitability assessments."""

    def __init__(self, db_path: str = "retirewise.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Creates necessary tables if they do not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS clients (
                    client_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    current_age INTEGER NOT NULL,
                    retirement_age INTEGER NOT NULL,
                    planning_horizon_age INTEGER NOT NULL,
                    marital_status TEXT NOT NULL,
                    dependents_count INTEGER NOT NULL,
                    adviser_name TEXT NOT NULL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS financial_profiles (
                    client_id TEXT PRIMARY KEY,
                    profile_json TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (client_id) REFERENCES clients (client_id) ON DELETE CASCADE
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS assessments (
                    assessment_id TEXT PRIMARY KEY,
                    client_id TEXT NOT NULL,
                    assessment_json TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (client_id) REFERENCES clients (client_id) ON DELETE CASCADE
                )
                """
            )
            conn.commit()

    def save_client(self, client: ClientProfile) -> None:
        """Inserts or updates a client profile."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO clients (
                    client_id, name, current_age, retirement_age, planning_horizon_age,
                    marital_status, dependents_count, adviser_name, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    client.client_id,
                    client.name,
                    client.current_age,
                    client.retirement_age,
                    client.planning_horizon_age,
                    client.marital_status.value,
                    client.dependents_count,
                    client.adviser_name,
                    client.notes,
                ),
            )
            conn.commit()

    def get_client(self, client_id: str) -> Optional[ClientProfile]:
        """Retrieves a client by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients WHERE client_id = ?", (client_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return ClientProfile(
                client_id=row["client_id"],
                name=row["name"],
                current_age=row["current_age"],
                retirement_age=row["retirement_age"],
                planning_horizon_age=row["planning_horizon_age"],
                marital_status=row["marital_status"],
                dependents_count=row["dependents_count"],
                adviser_name=row["adviser_name"],
                notes=row["notes"],
            )

    def list_clients(self) -> List[ClientProfile]:
        """Returns all registered clients."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [
                ClientProfile(
                    client_id=r["client_id"],
                    name=r["name"],
                    current_age=r["current_age"],
                    retirement_age=r["retirement_age"],
                    planning_horizon_age=r["planning_horizon_age"],
                    marital_status=r["marital_status"],
                    dependents_count=r["dependents_count"],
                    adviser_name=r["adviser_name"],
                    notes=r["notes"],
                )
                for r in rows
            ]

    def save_financial_profile(self, profile: FinancialProfile) -> None:
        """Saves or updates a client's Fact-Find financial profile."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO financial_profiles (client_id, profile_json, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                """,
                (profile.client_id, profile.model_dump_json()),
            )
            conn.commit()

    def get_financial_profile(self, client_id: str) -> Optional[FinancialProfile]:
        """Retrieves financial profile for client."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT profile_json FROM financial_profiles WHERE client_id = ?", (client_id,))
            row = cursor.fetchone()
            if not row:
                return None
            data = json.loads(row["profile_json"])
            return FinancialProfile(**data)

    def save_assessment(self, assessment: SuitabilityAssessmentResult) -> None:
        """Saves structured suitability assessment results."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO assessments (assessment_id, client_id, assessment_json, created_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                """,
                (assessment.assessment_id, assessment.client_id, assessment.model_dump_json()),
            )
            conn.commit()

    def get_latest_assessment(self, client_id: str) -> Optional[SuitabilityAssessmentResult]:
        """Retrieves the latest assessment for a client."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT assessment_json FROM assessments WHERE client_id = ? ORDER BY created_at DESC LIMIT 1",
                (client_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            data = json.loads(row["assessment_json"])
            return SuitabilityAssessmentResult(**data)
