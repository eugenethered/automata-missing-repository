from core.market.Market import Market
from core.missing.Context import Context
from utility.json_utility import as_data

from missingrepo.Missing import Missing


def deserialize_missing(missing) -> Missing:
    missing_info = as_data(missing, 'missing')
    context = Context.parse(as_data(missing, 'context'))
    market = Market.parse(as_data(missing, 'market'))
    description = as_data(missing, 'description')
    return Missing(missing_info, context, market, description)
