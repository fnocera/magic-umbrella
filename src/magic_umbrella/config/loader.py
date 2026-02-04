"""Configuration loader for customers, projects, and categories."""

import os
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


class Customer(BaseModel):
    """Customer configuration."""

    name: str
    aliases: list[str] = Field(default_factory=list)
    domains: list[str] = Field(default_factory=list)
    color: str = "#B2BEC3"


class Project(BaseModel):
    """Project configuration."""

    name: str
    aliases: list[str] = Field(default_factory=list)
    customer: Optional[str] = None
    type: str = "internal"  # customer, internal
    active: bool = True


class MeetingType(BaseModel):
    """Meeting type/category configuration."""

    name: str
    description: str = ""
    keywords: list[str] = Field(default_factory=list)
    color: str = "#B2BEC3"
    priority: int = 0


class ConfigLoader:
    """Loads and manages configuration from YAML files."""

    def __init__(self, config_dir: Optional[str] = None):
        """Initialize config loader.

        Args:
            config_dir: Directory containing config files (defaults to ./config)
        """
        if config_dir is None:
            config_dir = os.getenv("CONFIG_DIR", "./config")

        self.config_dir = Path(config_dir)

        # Load all configurations
        self.customers = self._load_customers()
        self.projects = self._load_projects()
        self.meeting_types = self._load_meeting_types()

    def _load_yaml(self, filename: str) -> dict:
        """Load and parse YAML file.

        Args:
            filename: Name of the YAML file to load

        Returns:
            Parsed YAML data as dictionary
        """
        filepath = self.config_dir / filename

        if not filepath.exists():
            return {}

        with open(filepath) as f:
            data = yaml.safe_load(f)

        return data or {}

    def _load_customers(self) -> list[Customer]:
        """Load customer configurations.

        Returns:
            List of Customer objects
        """
        data = self._load_yaml("customers.yaml")
        customers_data = data.get("customers", [])

        return [Customer(**c) for c in customers_data]

    def _load_projects(self) -> list[Project]:
        """Load project configurations.

        Returns:
            List of Project objects
        """
        data = self._load_yaml("projects.yaml")
        projects_data = data.get("projects", [])

        return [Project(**p) for p in projects_data]

    def _load_meeting_types(self) -> list[MeetingType]:
        """Load meeting type configurations.

        Returns:
            List of MeetingType objects sorted by priority (highest first)
        """
        data = self._load_yaml("categories.yaml")
        types_data = data.get("meeting_types", [])

        meeting_types = [MeetingType(**mt) for mt in types_data]

        # Sort by priority (highest first)
        return sorted(meeting_types, key=lambda x: x.priority, reverse=True)

    def get_customers(self) -> list[Customer]:
        """Get all customers.

        Returns:
            List of Customer objects
        """
        return self.customers

    def get_customer_by_name(self, name: str) -> Optional[Customer]:
        """Find customer by name or alias.

        Args:
            name: Customer name or alias to search for

        Returns:
            Customer object if found, None otherwise
        """
        name_lower = name.lower()

        for customer in self.customers:
            if customer.name.lower() == name_lower:
                return customer

            if any(alias.lower() == name_lower for alias in customer.aliases):
                return customer

        return None

    def get_projects(self) -> list[Project]:
        """Get all active projects.

        Returns:
            List of Project objects
        """
        return [p for p in self.projects if p.active]

    def get_project_by_name(self, name: str) -> Optional[Project]:
        """Find project by name or alias.

        Args:
            name: Project name or alias to search for

        Returns:
            Project object if found, None otherwise
        """
        name_lower = name.lower()

        for project in self.projects:
            if not project.active:
                continue

            if project.name.lower() == name_lower:
                return project

            if any(alias.lower() == name_lower for alias in project.aliases):
                return project

        return None

    def get_meeting_types(self) -> list[MeetingType]:
        """Get all meeting types sorted by priority.

        Returns:
            List of MeetingType objects
        """
        return self.meeting_types
