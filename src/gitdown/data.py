import re


class Package:
    BASE_URL = 'https://github.com/'
    MIRROR = 'https://ghproxy.com/https://github.com/'

    def __init__(self, pkg: str) -> None:
        url = self._parse_url(pkg)
        self._url = url
        self._name = self._parse_name(url)
        self._owner, self._repository = self._name.split('/')
        self._mirror = re.sub('https?://(www\.)?github.com/', Package.MIRROR, url)

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url

    @property
    def owner(self):
        return self._owner

    @property
    def repository(self):
        return self._repository

    @property
    def mirror(self):
        return self._mirror
    
    def _parse_url(self, pkg: str):
        # pkg 为GitHub仓库链接
        if re.match('^https?://(www\.)?github.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+/?$', pkg):
            return pkg
        # pkg 为路径地址 ${owner}/${repository}
        elif re.match('^[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$', pkg):
            return Package.BASE_URL + pkg
        else:
            raise Exception(f'illegal package[{pkg}]')

    def _parse_name(self, url: str):
        m = re.match('^https?://(www\.)?github.com/([a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+)/?$', url)
        return m.group(2)


if __name__ == '__main__':
    p = Package('https://github.com/bananalone/HttpMicroService/')
    print(p.name)
    print(p.url)
    print(p.mirror)
    print(p.owner)
    print(p.repository)

