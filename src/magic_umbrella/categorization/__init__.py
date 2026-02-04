"""Categorization module for meeting classification (rules + LLM)."""

from magic_umbrella.categorization.rule_classifier import (
    MeetingClassification,
    RuleBasedClassifier,
)

__all__ = ["RuleBasedClassifier", "MeetingClassification"]
