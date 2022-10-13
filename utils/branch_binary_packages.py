import requests 
from packaging import version

def first_is_max_version(first_version: str, sec_version: str) -> bool:
    return version.parse(first_version) > version.parse(sec_version)

def find_latest_version(first_branch: dict, sec_branch: dict) -> dict:
    result: dict = {}
    for arch in first_branch:
        for pkg in first_branch[arch]:
            if arch in sec_branch and pkg in sec_branch[arch]:
                first_version = first_branch[arch][pkg]['version']
                sec_version = sec_branch[arch][pkg]['version']
                if first_is_max_version(first_version, sec_version):
                    if arch not in result:
                        result[arch] = {}
                    result[arch][pkg] = first_branch[arch][pkg]
    return result

def comparison_packages(first_branch: dict, sec_branch: dict) -> dict:
    """returns dict format like: {
    'arch': {
      package_name': {
         "name": "string",
          "epoch": 0,
          "version": "string",
          "release": "string",
          "arch": "string",
          "disttag": "string",
          "buildtime": 0,
          "source": "string"
          }
       }
    }"""
    result = {}
    for arch in first_branch:
        for pkg in first_branch[arch]:
            if arch not in sec_branch:
                result[arch] = first_branch[arch]
            else:
                if pkg not in sec_branch[arch]:
                    if arch not in result:
                        result[arch] = {}
                    result[arch][pkg] = first_branch[arch][pkg]
    return result

def generate_branch(packages: list) -> dict:
    """returns dict format like: {
    'arch': {
      package_name': {
         "name": "string",
          "epoch": 0,
          "version": "string",
          "release": "string",
          "arch": "string",
          "disttag": "string",
          "buildtime": 0,
          "source": "string"
          }
       }
    }"""
    pkgs: dict = {}
    for pkg in packages:
        if pkg['arch'] not in pkgs:
            pkgs[pkg['arch']] = {}
        pkgs[pkg['arch']][pkg['name']] = pkg
    return pkgs

def get_branch_binary_packages(branch: str) -> dict:
    url = f'https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}'
    r = requests.get(url)
    return r.json()

def get_rez() -> dict: 
    sisyphus_packages = get_branch_binary_packages(branch='sisyphus')
    p10_packages = get_branch_binary_packages(branch='p10')
    all_pkgs = {
        'sisyphus': generate_branch(sisyphus_packages['packages']),
        'p10': generate_branch(p10_packages['packages'])
        }
    result = {
        'inP10NotInSisyphus': comparison_packages(\
            first_branch=all_pkgs['p10'],\
            sec_branch=all_pkgs['sisyphus']),
        'inSisyphusNotInP10': comparison_packages(\
            first_branch=all_pkgs['sisyphus'],\
            sec_branch=all_pkgs['p10']),
        'versionMoreInSisyphusThanInP10': find_latest_version(\
            first_branch=all_pkgs['sisyphus'],\
            sec_branch=all_pkgs['p10']),
    }  
    return result