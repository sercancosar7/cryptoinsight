"""Utility functions used across the application."""

from datetime import datetime, timezone


def format_usd(amount: float) -> str:
    """Format a number as USD string. Handles large numbers with abbreviations."""
    if amount >= 1_000_000_000_000:
        return f"${amount / 1_000_000_000_000:.2f}T"
    if amount >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.2f}B"
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.2f}M"
    return f"${amount:,.2f}"


def format_percent(value: float) -> str:
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.2f}%"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def clamp(value: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(value, max_val))


def chunk_list(lst: list, size: int) -> list[list]:
    """Split a list into chunks of the given size."""
    return [lst[i : i + size] for i in range(0, len(lst), size)]
