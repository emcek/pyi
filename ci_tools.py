from os import environ
from re import match
from sys import argv
from typing import Sequence

import git
from PyInstaller.utils.win32 import versioninfo
from packaging import version


def _generate(major: int, minor: int, patch: int, build: int, git_sha: str) -> versioninfo.VSVersionInfo:
    """
    Generate version information object.

    :param major: version major part
    :param minor: version minor part
    :param patch: version patch part
    :param build: GitHub build number
    :param git_sha: Git SHA hash
    :return: VSVersionInfo object
    """
    ver_info = versioninfo.VSVersionInfo(
        ffi=versioninfo.FixedFileInfo(
            filevers=(major, minor, patch, build),
            prodvers=(major, minor, patch, build),
            mask=0x3f,
            flags=0x0,
            OS=0x40004,
            fileType=0x1,
            subtype=0x0,
            date=(0, 0)),
        kids=[versioninfo.StringFileInfo([versioninfo.StringTable('040904B0', [
              versioninfo.StringStruct('CompanyName', 'Michał Plichta'),
              versioninfo.StringStruct('FileDescription', 'Integrating DCS Planes with Logitech keyboards with LCD'),
              versioninfo.StringStruct('FileVersion', f'{major}.{minor}.{patch}'),
              versioninfo.StringStruct('InternalName', 'dcs_py'),
              versioninfo.StringStruct('LegalCopyright', '© Michał Plichta. All rights reserved.'),
              versioninfo.StringStruct('OriginalFilename', 'dcs_py.exe'),
              versioninfo.StringStruct('ProductName', 'DCSpy'),
              versioninfo.StringStruct('ProductVersion', f'{major}.{minor}.{patch} ({git_sha})')])]),
              versioninfo.VarFileInfo([versioninfo.VarStruct('Translation', [1033, 1200])])])
    return ver_info


def _latest_version(repo_path: str, as_tag: bool) -> str:
    """
    Get latest version number form repository.

    :param repo_path: path to repository
    :param as_tag: if True return full tag name
    :return: return version or tag name as string
    """
    repo = git.Repo(repo_path)
    tags_list = [str(tag) for tag in repo.tags]
    ver_tags = [version.parse(m.group(1)) for tag in tags_list if (m := match(r'v(\d+\.\d+\.\d+)$', tag))]
    ver = str(max(ver_tags))
    if as_tag:
        ver = f'v{ver}'
    return ver


def _save_ver_file(ver=environ.get('GITHUB_REF_NAME'), bld=environ.get('GITHUB_RUN_NUMBER'),
                   sha=environ.get('GITHUB_SHA'), ver_f='file_version_info.txt') -> Sequence[str]:
    """
    Save generated version file based on list of strings.

    Example of params: v1.9.5 40 6bbd8808 file_version_info.txt

    :param ver: version name or tag name
    :param bld: GitHub build number
    :param sha: Git SHA hash
    :param ver_f: file name of version file
    :return: input parameters
    """
    if all([ver, bld, sha, ver_f]):
        if ver.startswith('v'):
            ver = ver[1:]
        info_ver = _generate(*[int(i) for i in ver.split('.')], build=int(bld), git_sha=sha)
        with open(ver_f, mode='w+', encoding='utf-8') as f:
            f.write(str(info_ver))
    else:
        print("Use: v1.9.5 40 6bbd8808 file_version_info.txt")
    return ver, bld, sha, ver_f


if __name__ == '__main__':
    if argv[1] == 'ver_file':
        print(_save_ver_file(*argv[2:]))
    elif argv[1] == 'ver':
        print(_latest_version(argv[2], False))
    elif argv[1] == 'tag':
        print(_latest_version(argv[2], True))
    else:
        print(' ver_file v1.9.5 40 6bbd8808 file_version_info.txt\n', 'ver <repo_path>\n', 'tag <repo_path>\n')
