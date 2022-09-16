import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Callable
import importlib


class Item:
    def __init__(self, module: str, entrypoint: str) -> None:
        self._module, self._entrypoint = str(Path(module).absolute()), entrypoint
        self._loaded_module = self._attempt_load_module(self._module)
        self._func = self._attempt_load_func(self._entrypoint, self._loaded_module)

    @property
    def module(self):
        return self._module

    @property
    def entrypoint(self):
        return self._entrypoint

    @property
    def doc(self):
        return self._func.__doc__
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self._func(*args, **kwds)

    def _attempt_load_module(self, module: str) -> ModuleType:
        path_module = Path(module)
        assert path_module.exists(), f'path[{str(path_module)}] not found'
        assert path_module.is_file() and path_module.suffix[1:] == 'py', f'module[{str(path_module)} should be a python file'
        module_name = path_module.stem
        module_root = path_module.parent
        assert not (module_root / '__init__.py').exists(), f'can not import submodule[{str(path_module)}]'
        if str(module_root.absolute()) not in sys.path and str(module_root.relative_to(Path.cwd())) not in sys.path:
            sys.path.insert(0, str(module_root))
        loaded_module = importlib.import_module(module_name)
        return loaded_module
        
    def _attempt_load_func(self, entrypoint: str, loaded_module: ModuleType) -> Callable:
        assert entrypoint in dir(loaded_module), f'entrypoint[{entrypoint}] not found in {self._module}'
        func = eval(f'loaded_module.{entrypoint}')
        assert '__call__' in dir(func), f'entrypoint[{entrypoint}] in {self._module} is not a function'
        return func


