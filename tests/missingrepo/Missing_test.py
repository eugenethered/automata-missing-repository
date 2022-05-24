import unittest

from core.missing.Context import Context

from missingrepo.Missing import Missing


class MissingTestCase(unittest.TestCase):

    def test_should_compare_missing_by_values_excluding_description(self):
        missing = Missing('BTCOTC', Context.EXCHANGE, 'test', '1 - Missing instrument')
        other_missing = Missing('BTCOTC', Context.EXCHANGE, 'test', '2 - Missing instrument')
        self.assertEqual(missing, other_missing)


if __name__ == '__main__':
    unittest.main()
