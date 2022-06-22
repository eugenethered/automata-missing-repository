import logging
import unittest

from cache.holder.RedisCacheHolder import RedisCacheHolder
from cache.provider.RedisCacheProviderWithHash import RedisCacheProviderWithHash
from core.missing.Context import Context

from missingrepo.Missing import Missing
from missingrepo.repository.MissingRepository import MissingRepository


class MissingRepositoryTestCase(unittest.TestCase):

    def setUp(self) -> None:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger('MissingRepository').setLevel(logging.DEBUG)

        options = {
            'REDIS_SERVER_ADDRESS': '192.168.1.90',
            'REDIS_SERVER_PORT': 6379,
            'MISSING_KEY': 'test:mv:missing'
        }

        self.cache = RedisCacheHolder(options, held_type=RedisCacheProviderWithHash)
        self.repository = MissingRepository(options)

    def tearDown(self):
        self.cache.delete('test:mv:missing')

    def test_should_create_and_retrieve_missing(self):
        missing = Missing(missing='BTCOTC', context=Context.EXCHANGE, market='test', description='Missing instrument exchange config for instrument BTCOTC')
        self.repository.create(missing)
        stored_missing = self.repository.retrieve()
        self.assertEqual(missing, stored_missing[0])

    def test_should_store_multiple_missing(self):
        missing_exchange_config = Missing(missing='BTCOTC', context=Context.EXCHANGE, market='test', description='Missing instrument exchange config for instrument BTCOTC')
        missing_trade_config = Missing(missing='OTC/BTC', context=Context.TRADE, market='test', description='Missing trade config for instrument OTC/BTC')
        multiple_missing = [missing_exchange_config, missing_trade_config]
        self.repository.store(multiple_missing)
        stored_multiples = self.repository.retrieve()
        multiple_missing.sort(key=lambda m: m.missing)
        stored_multiples.sort(key=lambda m: m.missing)
        self.assertEqual(multiple_missing, stored_multiples)

    def test_should_batch_store_missing(self):
        missing_1 = Missing('BTCOTC', Context.EXCHANGE, 'test', 'Missing 1')
        self.repository.create(missing_1)
        missing_2 = Missing('BTCOTC', Context.EXCHANGE, 'test', 'Missing 2')
        self.repository.create(missing_2)
        all_missing = self.repository.retrieve()
        self.assertEqual(all_missing, [missing_1])

    def test_should_already_missing(self):
        missing_1 = Missing('BTCOTC', Context.EXCHANGE, 'test', 'Missing 1')
        self.repository.create(missing_1)
        self.assertTrue(self.repository.is_already_missing(missing_1))

    def test_should_delete_missing(self):
        missings = [
            Missing(missing='OTC/BTC', context=Context.EXCHANGE, market='test', description='testing'),
            Missing(missing='BTC/OTC', context=Context.EXCHANGE, market='test', description='testing')
        ]
        self.repository.store(missings)
        self.assertTrue(len(self.repository.retrieve()), 2)
        missing_to_delete = Missing(missing='OTC/BTC', context=Context.EXCHANGE, market='test', description='testing')
        self.repository.delete(missing_to_delete)
        self.assertTrue(len(self.repository.retrieve()), 1)


if __name__ == '__main__':
    unittest.main()
