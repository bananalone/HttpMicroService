import sqlite3
from pathlib import Path


class Table:
    NAME = 'gitdown'

    def __init__(self, db: str) -> None:
        path_db = Path(db)
        assert path_db.suffix == '.db', f'illegal database[{db}]'
        if not path_db.exists():
            self._create(db)
        self._db = db
        self._cache = {}

    def insert(self, name: str, path: str):
        self._cache[name] = path
        try:
            with sqlite3.connect(self._db) as conn:
                cur = conn.cursor()
                sql = f'insert into {Table.NAME} (name, path) values ("{name}", "{path}");'
                cur.execute(sql)
                conn.commit()
        except Exception as e:
            del self._cache[name]
            raise e

    def remove(self, name: str):
        if name in self._cache:
            del self._cache[name]
        with sqlite3.connect(self._db) as conn:
            cur = conn.cursor()
            sql = f'delete from {Table.NAME} where name = "{name}";'
            cur.execute(sql)
            conn.commit()

    def remove_all(self):
        self._cache = {}
        with sqlite3.connect(self._db) as conn:
            cur = conn.cursor()
            sql = f'delete from {Table.NAME};'
            cur.execute(sql)
            conn.commit()

    def update(self, name: str, path: str):
        self._cache[name] = path
        try:
            with sqlite3.connect(self._db) as conn:
                cur = conn.cursor()
                sql = f'update {Table.NAME} set path = "{path}" where name = "{name}";'
                cur.execute(sql)
                conn.commit()
        except Exception as e:
            del self._cache[name]
            raise e

    def get(self, name: str) -> str | None:
        if name in self._cache:
            return self._cache[name]
        with sqlite3.connect(self._db) as conn:
            cur = conn.cursor()
            sql = f'select path from {Table.NAME} where name = "{name}";'
            cur.execute(sql)
            path = cur.fetchone()
            if path:
                self._cache[name] = path[0]
                return path[0]
        return None

    def list(self, pattern: str = None, invert: bool = False):
        with sqlite3.connect(self._db) as conn:
            cur = conn.cursor()
            like = ''
            if pattern:
                like = f' where name like "%{pattern}%"' if not invert else f' where name not like "%{pattern}%"'
            sql = f'select name, path from {Table.NAME}{like};'
            cur.execute(sql)
            rets = cur.fetchall()
        return rets

    def _create(self, db: str):
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            sql = f'create table {Table.NAME} (name char(100) primary key not null, path char(300) not null);'
            cur.execute(sql)
            conn.commit()


if __name__ == '__main__':
    tab = Table('gitdown.db')
    tab.remove_all()
    print(tab.list())
    tab.insert('bananalone/toolbox', '/home/bananalone/github')
    print(tab.get('bananalone/toolbox'))
    tab.insert('aaa/bbb', 'aaa')
    print(tab.list())
    tab.remove('bananalone/toolbox')
    print(tab.list())
    tab.update('aaa/bbb', 'bbb')
    print(tab.list())
    tab.insert('zxcasdwq/xzvadfasd', 'adsagDSFADSF')
    tab.insert('gwgfasde/adfqge', 'gojusdfag')
    print(tab.list())
    print(tab.list('asd'))
    print(tab.list('asd', True))
    tab.remove_all()

