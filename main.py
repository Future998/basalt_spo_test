import json
import click
from utils import branch_binary_packages as bbp


def save_as_json(path: str, info: dict):
    with open(path, 'a') as r:
        json.dump(info, r)

@click.command()
@click.argument(
    'first_branch',
    type=str,
    )
@click.argument(
    'second_branch',
    type=str,
    )
@click.option(
    '--path', '-p',
    help='(Optional) path to the .json file to save the result',
    )
def main(first_branch: str, second_branch: str ,path: str = ''):
    """
    A small CLI utility that:\n
        1) get lists of binary packages of first_branch and second_branch branches\n
        2) makes a comparison of the received package lists and outputs JSON, which will display:\n
            - all packages that are in second_branch but not in first_branch\n
            - all packages that are in first_branch but not in second_branch\n
            - all packages whose version is greater in first_branch than in second_branch\n
    This is done for all branches of architectures.\n
    The response is in JSON format:\n
    {\n
        'inSecond_branchNotInFirst_branch': {\n
            "arch": {\n
            "package_name": {\n
                "name": "string",\n
                "epoch": 0,\n
                "version": "string",\n
                "release": "string",\n
                "arch": "string",\n
                "disttag": "string",\n
                "buildtime": 0,\n
                "source": "string"\n
                }\n
            }\n
        },\n
        'inFirst_branchNotInSecond_branch': {\n
            "arch": {\n
            "package_name": {\n
                "name": "string",\n
                "epoch": 0,\n
                "version": "string",\n
                "release": "string",\n
                "arch": "string",\n
                "disttag": "string",\n
                "buildtime": 0,\n
                "source": "string"\n
                }\n
            }\n
        },\n
        'versionMoreInFirst_branchThanInSecond_branch': {\n
            "arch": {\n
            "package_name": {\n
                "name": "string",\n
                "epoch": 0,\n
                "version": "string",\n
                "release": "string",\n
                "arch": "string",\n
                "disttag": "string",\n
                "buildtime": 0,\n
                "source": "string"\n
                }\n
            }\n
        },\n
    }\n
    """
    rez = bbp.get_rez(first_branch, second_branch)
    if path != None and path.endswith('.json'): 
        save_as_json(path, rez)
    else:
        print(rez)