import unittest

from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.market.Market import Market
from core.missing.Context import Context

from missingrepo.Missing import Missing
from missingrepo.repository.MissingRepository import MissingRepository


class MissingRepositoryTestCase(unittest.TestCase):

    def setUp(self) -> None:
        options = {
            'REDIS_SERVER_ADDRESS': '192.168.1.90',
            'REDIS_SERVER_PORT': 6379,
            'MISSING_KEY': 'test:missing'
        }
        self.cache = RedisCacheHolder(options)
        self.repository = MissingRepository(options)

    def tearDown(self):
        self.cache.delete('test:missing')

    def test_should_store_and_retrieve_missing(self):
        missing = Missing(missing='BTCOTC', context=Context.EXCHANGE, market=Market.BINANCE, description='Missing instrument exchange config for instrument BTCOTC')
        self.repository.store([missing])
        stored_missing = self.repository.retrieve()
        self.assertEqual(missing, stored_missing[0])

    def test_should_store_multiple_missing(self):
        missing_exchange_config = Missing(missing='BTCOTC', context=Context.EXCHANGE, market=Market.BINANCE, description='Missing instrument exchange config for instrument BTCOTC')
        missing_trade_config = Missing(missing='OTC/BTC', context=Context.TRADE, market=Market.BINANCE, description='Missing trade config for instrument OTC/BTC')
        multiple_missing = [missing_exchange_config, missing_trade_config]
        self.repository.store(multiple_missing)
        stored_multiples = self.repository.retrieve()
        self.assertEqual(multiple_missing, stored_multiples)


if __name__ == '__main__':
    unittest.main()
