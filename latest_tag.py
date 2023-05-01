from re import match
from sys import argv

from packaging import version
import git


def latest_tag(repo_path: str, as_ver=False) -> str:
    repo = git.Repo(repo_path)
    tags_list = [str(tag) for tag in repo.tags]
    ver_tags = [version.parse(m.group(1)) for tag in tags_list if (m := match(r'v(\d+\.\d+\.\d+)$', tag))]
    tag = str(max(ver_tags))
    if as_ver:
        tag = f'v{tag}'
    return tag


if __name__ == '__main__':
    print(latest_tag(*argv[1:]))
