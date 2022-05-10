from dataclasses import dataclass

from core.market.Market import Market
from core.missing.Context import Context


@dataclass
class Missing:
    missing: str
    context: Context
    market: Market
    description: str
