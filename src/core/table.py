
from pathlib import Path
from typing import List, Tuple, Union

from core.item import FunctionItem

class FunctionTable:
    def __init__(self) -> None:
        self._table = dict()

    def register(self, module: str, entrypoint: str):
        func_item = FunctionItem(module, entrypoint)
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

    def get(self, module: str, entrypoint: str) -> FunctionItem:
        id = self._gen_id(module, entrypoint)
        assert id in self._table, f'unregistered function[{id}]'
        return self._table[id]

    def list_in_module(self, module: str) -> List[FunctionItem]:
        func_items = []
        path_module = str(Path(module).absolute())
        for id in self._table:
            func_item: FunctionItem = self._table[id]
            if func_item.module == path_module:
                func_items.append(func_item)
        return func_items

    def list_all(self) -> List[FunctionItem]:
        return list(self._table.values())

    def _gen_id(self, module: str, entrypoint: str):
        return ':'.join([module, entrypoint])

