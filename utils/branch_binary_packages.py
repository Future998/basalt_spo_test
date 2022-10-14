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

def get_rez(first_branch: str, second_branch: str) -> dict: 
    fb_packages = get_branch_binary_packages(branch=first_branch)
    sb_packages = get_branch_binary_packages(branch=second_branch)
    all_pkgs = {
        first_branch: generate_branch(fb_packages['packages']),
        second_branch: generate_branch(sb_packages['packages'])
        }
    result = {
        f'in{second_branch.title()}NotIn{first_branch.title()}': comparison_packages(\
            first_branch=all_pkgs[second_branch],\
            sec_branch=all_pkgs[first_branch]),
        f'in{first_branch.title()}NotIn{second_branch.title()}': comparison_packages(\
            first_branch=all_pkgs[first_branch],\
            sec_branch=all_pkgs[second_branch]),
        f'versionMoreIn{first_branch.title()}ThanIn{second_branch.title()}': find_latest_version(\
            first_branch=all_pkgs[first_branch],\
            sec_branch=all_pkgs[second_branch]),
    }  
    return result