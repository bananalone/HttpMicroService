from typing import Union, List, Tuple

from functionfactory.item import Item as _Item
from functionfactory.table import Table as _Table


_table = _Table()


def register(module: str, entrypoint: str):
    _table.register(module, entrypoint)


def register_batch(batch: Union[List, Tuple]):
    _table.register_batch(batch)


def unregister(module: str, entrypoint: str):
    _table.unregister(module, entrypoint)


def unregister_batch(batch: Union[List, Tuple]):
    _table.unregister_batch(batch)


def unregister_all():
    _table.unregister_all()


def get(module: str, entrypoint: str) -> _Item:
    return _table.get(module, entrypoint)


def list_in_module(module: str) -> List[_Item]:
    return _table.list_in_module(module)


def list_all() -> List[_Item]:
    return _table.list_all()