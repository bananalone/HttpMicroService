import shutil
from pathlib import Path

from gitdown.data import Package
from gitdown.gitutils import git_clone, git_pull
from gitdown.sqlutils import Table


class GithubPackageManager:
    DB = 'gitdown.db'
    def __init__(self, root: str=(Path.home() / '.gitdown').as_posix(), use_mirror=False) -> None:
        p_root = Path(root)
        if not p_root.exists():
            p_root.mkdir(parents=True)
        self._root = p_root
        self._table = Table((self._root / GithubPackageManager.DB).as_posix())
        self._use_mirror = use_mirror

    def get(self, package: str):
        pkg = Package(package) 
        return self._table.get(pkg.name)

    def list(self, pattern:str = None, invert: bool = False):
        return self._table.list(pattern, invert)

    def install(self, package: str) -> bool:
        pkg = Package(package)
        if self._table.get(pkg.name):
            raise Exception(f'{package} has already installed')
        cloned = self._clone(pkg)
        pkg_path = self._pkg_path(pkg).as_posix()
        if cloned:
            self._table.insert(pkg.name, pkg_path)
            return True
        shutil.rmtree(pkg_path)
        return False

    def reinstall(self, package: str) -> bool:
        pkg = Package(package)
        pkg_path = self._table.get(pkg.name)
        if not pkg_path:
            raise Exception(f'{package} not install')
        Path(pkg_path).rmdir()
        return self._clone(pkg, pkg_path)

    def update(self, package: str) -> bool:
        pkg = Package(package)
        pkg_path = self._table.get(pkg.name)
        return git_pull(pkg_path, 1)

    def remove(self, package: str) -> bool:
        pkg = Package(package)
        self._remove_pkg(pkg.name)
        self._table.remove(pkg.name)

    def remove_all(self):
        for name, _ in self._table.list():
            self._remove_pkg(name)
        self._table.remove_all()

    def _clone(self, pkg: Package):
        out = self._pkg_path(pkg)
        if self._use_mirror:
            cloned = git_clone(pkg.mirror, out, 1)
        else:
            cloned = git_clone(pkg.url, out, 1)
        return cloned

    def _pkg_path(self, pkg: Package) -> Path:
        return self._root / pkg.owner / pkg.repository

    def _remove_pkg(self, name: str):
        pkg_path = self._table.get(name)
        if pkg_path:
            shutil.rmtree(pkg_path)
            parent = Path(pkg_path).parent
            try:
                next(parent.glob('*'))
            except StopIteration:
                shutil.rmtree(parent.as_posix())
