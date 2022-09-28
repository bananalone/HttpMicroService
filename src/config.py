from pathlib import Path

import yaml


class Config:
    CONF_TYPE = ['yaml', 'yml']

    def __init__(self, path: str | Path, autosave=True) -> None:
        self._path = path if isinstance(path, Path) else Path(path)
        self._config = self._attempt_load(self._path)
        if not self._config:
            raise Exception(f'path: {path.as_posix()} error')
        self._autosave = autosave

    def commit(self):
        with open(self._path.as_posix(), 'w', encoding='utf-8') as f:
            yaml.dump(self._config, f, allow_unicode=True, sort_keys=False)

    def _attempt_load(self, path: Path) -> dict | None:
        if path.suffix.lower()[1:] not in Config.CONF_TYPE:
            return None
        with open(path.as_posix(), encoding='utf-8') as f:
            config = yaml.load(f, yaml.Loader)
        return config

    def __getitem__(self, key):
        return self._config[key]

    def __setitem__(self, key, value):
        self._config[key] = value
        if self._autosave:
            self.commit()

    def __delitem__(self, key):
        del self._config[key]
        if self._autosave:
            self.commit()


if __name__ == '__main__':
    conf = Config('configs/config copy.yaml')
    conf['rules'] = {
        'hello': {
            'module': '~/hello.py',
            'entrypoint': 'hello',
            'response_type': 'json'
        }
    }
    rules = conf['rules']
    rules['hello2'] = {
        'module': '~/hello2.py',
        'entrypoint': 'hello',
        'response_type': 'json'
    }
    conf['rules'] = rules

