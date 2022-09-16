
from pathlib import Path
from typing import List, Tuple, Union

from functionfactory.item import Item

class Table:
    def __init__(self) -> None:
        self._table = dict()

    def register(self, module: str, entrypoint: str):
        func_item = Item(module, entrypoint)
        id = self._gen_id(module, entrypoint)
        self._table[id] = func_item
        return self

    def register_batch(self, batch: Union[List, Tuple]):
        for module_entrypoint in batch:
            if isinstance(module_entrypoint, List) or isinstance(module_entrypoint, Tuple):
                self.register(*module_entrypoint)
            elif isinstance(module_entrypoint, dict):
                self.register(module_entrypoint['module'], module_entrypoint['entrypoint'])
        return self

    def unregister(self, module: str, entrypoint: str):
        id = self._gen_id(module, entrypoint)
        if id in self._table:
            del self._table[id]
        return self

    def unregister_batch(self, batch: Union[List, Tuple]):
        for module_entrypoint in batch:
            if isinstance(module_entrypoint, List) or isinstance(module_entrypoint, Tuple):
                self.unregister(*module_entrypoint)
            elif isinstance(module_entrypoint, dict):
                self.unregister(**module_entrypoint)
        return self

    def unregister_all(self):
        self._table = dict()
        return self

    def get(self, module: str, entrypoint: str) -> Item:
        id = self._gen_id(module, entrypoint)
        assert id in self._table, f'unregistered function[{id}]'
        return self._table[id]

    def list_in_module(self, module: str) -> List[Item]:
        func_items = []
        path_module = str(Path(module).absolute())
        for id in self._table:
            func_item: Item = self._table[id]
            if func_item.module == path_module:
                func_items.append(func_item)
        return func_items

    def list_all(self) -> List[Item]:
        return list(self._table.values())

    def _gen_id(self, module: str, entrypoint: str):
        return ':'.join([module, entrypoint])

