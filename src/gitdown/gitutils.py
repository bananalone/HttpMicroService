import re
import subprocess
import sys


class Downloader:
    def __init__(self, mirror: str = None, depth: int = None) -> None:
        if mirror:
            self._mirror = mirror if mirror.endswith('/') else mirror+'/'
        else:
            self._mirror = None
        self._depth = depth
        self._url_pattern = re.compile('https?://(www\.)?github.com/')

    def _attempt_parse_args(self, url: str, out: str = None):
        assert self._url_pattern.match(url), f'illegal url[{url}]'
        if self._mirror:
            url = self._url_pattern.sub(self._mirror, url)
        args = ['git', 'clone']
        if self._depth:
            args.extend(['--depth', str(self._depth)])
        args.append(url)
        if out:
            args.append(out)
        
        return args      

    def download(self, url: str, out: str = None):
        args = self._attempt_parse_args(url, out)
        print(' '.join(args))
        ret = subprocess.run(args, stdout=sys.stdout)
        assert ret.returncode == 0, ret.stdout
        

if __name__ == '__main__':
    mirror = 'https://ghproxy.com/https://github.com'
    deepth = 1
    loader = Downloader(mirror, deepth)
    loader.download('https://github.com/bananalone/HttpMicroService')
