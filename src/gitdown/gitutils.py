import sys
import subprocess
from pathlib import Path


def git_clone(url: str, out: str = None, depth: int = None):
    args = ['git', 'clone', url]
    if out:
        args.append(out)
    if depth:
        args += ['--depth', str(depth)]
    ret = subprocess.run(args, stdout=sys.stdout, stderr=sys.stderr, encoding='utf-8')
    return True if ret.returncode == 0 else False


def git_pull(repository_path: str, depth: int = None):
    path = Path(repository_path)
    assert path.exists(), f'{path} not exists'
    if depth:
        args = ['/bin/bash', '-c', f'cd {repository_path} && git pull --depth {depth}']
    else:
        args = ['/bin/bash', '-c', f'cd {repository_path} && git pull']
    ret = subprocess.run(args, stdout=sys.stdout, stderr=sys.stderr, encoding='utf-8')
    return True if ret.returncode == 0 else False

    

if __name__ == '__main__':
    from data import Package
    pkg = Package('bananalone/install')
    # git_clone(pkg.mirror, 'downloads/bananalone/install')
    git_pull('downloads/bananalone/install', 1)
