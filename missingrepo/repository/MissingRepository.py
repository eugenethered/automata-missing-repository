from typing import List

from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.options.exception.MissingOptionError import MissingOptionError

from missingrepo.Missing import Missing
from missingrepo.repository.serialize.missing_deserializer import deserialize_missing
from missingrepo.repository.serialize.missing_serializer import serialize_missing

MISSING_KEY = 'MISSING_KEY'


class MissingRepository:

    def __init__(self, options):
        self.options = options
        self.__check_options()
        self.cache = RedisCacheHolder()

    def __check_options(self):
        if self.options is None:
            raise MissingOptionError(f'missing option please provide options {MISSING_KEY}')
        if MISSING_KEY not in self.options:
            raise MissingOptionError(f'missing option please provide option {MISSING_KEY}')

    def store(self, multiple_missing: List[Missing]):
        key = self.options[MISSING_KEY]
        entities_to_store = list([serialize_missing(missing) for missing in multiple_missing])
        self.cache.store(key, entities_to_store)

    def retrieve(self) -> List[Missing]:
        key = self.options[MISSING_KEY]
        raw_entities = self.cache.fetch(key, as_type=list)
        entities = list([deserialize_missing(raw) for raw in raw_entities])
        return entities
