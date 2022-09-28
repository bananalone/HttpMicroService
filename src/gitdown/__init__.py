from gitdown.manager import GithubPackageManager


_github_package_manager = GithubPackageManager(use_mirror=True)


def get(package: str):
    return _github_package_manager.get(package)

def list(pattern: str = None, invert: bool = False):
    return _github_package_manager.list(pattern, invert)

def install(package: str):
    return _github_package_manager.install(package)

def reinstall(package: str):
    return _github_package_manager.reinstall(package)

def update(package: str):
    return _github_package_manager.update(package)

def remove(package: str):
    _github_package_manager.remove(package)

def remove_all():
    _github_package_manager.remove_all()
