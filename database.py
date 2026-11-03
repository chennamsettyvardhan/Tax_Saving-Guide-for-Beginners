"""
TaxWise AI - Database Layer
Implements SQLite relational storage for Users, TaxProfiles, FinancialInputs,
TaxRules, Recommendations, Documents, and ChatHistory.
Designed to be modular, versioned by financial year, and lightweight.
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "taxwise.db")


def get_db_connection() -> sqlite3.Connection:
    """Returns a connection to the SQLite database with dictionary rows."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initializes all database tables matching the project architecture."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. TaxProfiles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tax_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        financial_year TEXT NOT NULL DEFAULT 'FY 2025-26',
        income REAL NOT NULL DEFAULT 0.0,
        employment_type TEXT NOT NULL DEFAULT 'salaried',
        age INTEGER NOT NULL DEFAULT 28,
        other_income REAL NOT NULL DEFAULT 0.0,
        regime TEXT NOT NULL DEFAULT 'new',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # 3. FinancialInputs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS financial_inputs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category TEXT NOT NULL,
        amount REAL NOT NULL DEFAULT 0.0,
        description TEXT,
        financial_year TEXT NOT NULL DEFAULT 'FY 2025-26',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # 4. TaxRules Table (Versioned by Financial Year)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tax_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        financial_year TEXT NOT NULL,
        rule_name TEXT NOT NULL,
        rule_type TEXT NOT NULL,
        conditions TEXT,
        limits REAL,
        source TEXT NOT NULL,
        effective_date TEXT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 5. Recommendations Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        recommendation_type TEXT NOT NULL,
        reason TEXT NOT NULL,
        status TEXT NOT NULL,
        rule_reference TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # 6. Documents Table (For RAG Tax Knowledge Base)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        source TEXT NOT NULL,
        financial_year TEXT NOT NULL DEFAULT 'FY 2025-26',
        category TEXT NOT NULL,
        content TEXT NOT NULL,
        metadata TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 7. ChatHistory Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        sources TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
    );
    """)

    conn.commit()
    conn.close()


def seed_default_tax_rules() -> None:
    """Seeds official tax rules versioned by financial year if not already present."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tax_rules")
    count = cursor.fetchone()[0]

    if count == 0:
        rules = [
            # FY 2025-26 Rules
            (
                "FY 2025-26",
                "Section 80C Deduction",
                "deduction",
                json.dumps({"regime": "old", "eligible_instruments": ["EPF", "PPF", "ELSS", "Life Insurance", "Tuition Fee", "Home Loan Principal"]}),
                150000.0,
                "Income Tax Act, 1961 - Section 80C",
                "2025-04-01"
            ),
            (
                "FY 2025-26",
                "Section 80D Health Insurance",
                "deduction",
                json.dumps({"regime": "old", "self_limit": 25000, "senior_parent_limit": 50000, "max_total": 100000}),
                100000.0,
                "Income Tax Act, 1961 - Section 80D",
                "2025-04-01"
            ),
            (
                "FY 2025-26",
                "Section 80CCD(1B) NPS Additional Deduction",
                "deduction",
                json.dumps({"regime": "old", "tier": "Tier-1", "additional_over_80c": True}),
                50000.0,
                "Income Tax Act, 1961 - Section 80CCD(1B)",
                "2025-04-01"
            ),
            (
                "FY 2025-26",
                "Section 24(b) Home Loan Interest",
                "deduction",
                json.dumps({"regime": "old", "property_type": "self-occupied"}),
                200000.0,
                "Income Tax Act, 1961 - Section 24(b)",
                "2025-04-01"
            ),
            (
                "FY 2025-26",
                "Section 80E Education Loan Interest",
                "deduction",
                json.dumps({"regime": "old", "limit_type": "no_upper_cap", "duration_years": 8}),
                None,
                "Income Tax Act, 1961 - Section 80E",
                "2025-04-01"
            ),
            (
                "FY 2025-26",
                "Section 80G Charitable Donations",
                "deduction",
                json.dumps({"regime": "old", "modes": ["cheque", "digital", "demand_draft"]}),
                None,
                "Income Tax Act, 1961 - Section 80G",
                "2025-04-01"
            ),
            (
                "FY 2025-26",
                "Standard Deduction (New Regime)",
                "standard_deduction",
                json.dumps({"regime": "new", "employment_type": "salaried"}),
                75000.0,
                "Finance Act 2024 / 2025 - Section 16(ia)",
                "2025-04-01"
            ),
            (
                "FY 2025-26",
                "Standard Deduction (Old Regime)",
                "standard_deduction",
                json.dumps({"regime": "old", "employment_type": "salaried"}),
                50000.0,
                "Finance Act 2019 / 2024 - Section 16(ia)",
                "2025-04-01"
            ),
            (
                "FY 2025-26",
                "Section 87A Rebate (New Regime)",
                "rebate",
                json.dumps({"regime": "new", "max_taxable_income": 1200000.0, "marginal_relief": True}),
                60000.0,
                "Income Tax Act, 1961 - Section 87A / Budget 2025",
                "2025-04-01"
            ),
            (
                "FY 2025-26",
                "Section 87A Rebate (Old Regime)",
                "rebate",
                json.dumps({"regime": "old", "max_taxable_income": 500000.0}),
                12500.0,
                "Income Tax Act, 1961 - Section 87A",
                "2025-04-01"
            ),
            # FY 2024-25 Rules
            (
                "FY 2024-25",
                "Section 87A Rebate (New Regime)",
                "rebate",
                json.dumps({"regime": "new", "max_taxable_income": 700000.0, "marginal_relief": True}),
                25000.0,
                "Finance Act 2023 / 2024 - Section 87A",
                "2024-04-01"
            ),
            (
                "FY 2024-25",
                "Standard Deduction (New Regime)",
                "standard_deduction",
                json.dumps({"regime": "new", "employment_type": "salaried"}),
                75000.0,
                "Budget 2024 - Section 16(ia)",
                "2024-07-23"
            )
        ]

        cursor.executemany("""
        INSERT INTO tax_rules (financial_year, rule_name, rule_type, conditions, limits, source, effective_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, rules)
        conn.commit()

    conn.close()


# Initialize database automatically on import
init_db()
seed_default_tax_rules()
