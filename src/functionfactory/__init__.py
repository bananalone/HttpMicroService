from typing import Union, List, Tuple

from functionfactory.item import Item as _Item
from functionfactory.table import Table as _Table


_table = _Table()


def get(module: str, entrypoint: str):
    func = _table.get(module, entrypoint)
    if func:
        return func
    else:
        return _table.register(module, entrypoint).get(module, entrypoint)
