import json
import click
from utils import branch_binary_packages as bbp


def save_as_json(path: str, info: dict):
    with open(path, 'a') as r:
        json.dump(info, r)

@click.command()
@click.option(
    '--path', '-p',
    help='(Optional) path to the .json file to save the result',
    )
def main(path: str = ''):
    """
    A small CLI utility that:\n
        1) get lists of binary packages of sisyphus and p10 branches\n
        2) makes a comparison of the received package lists and outputs JSON, which will display:\n
            - all packages that are in p10 but not in sisyphus\n
            - all packages that are in sisyphus but not in p10\n
            - all packages whose version is greater in sisyphus than in p10\n
    This is done for all branches of architectures.\n
    The response is in JSON format:\n
    {\n
        'inP10NotInSisyphus': {\n
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
        'inSisyphusNotInP10': {\n
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
        'versionMoreInSisyphusThanInP10': {\n
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
    rez = bbp.get_rez()
    if path != None and path.endswith('.json'): 
        save_as_json(path, rez)
    else:
        print(rez)

if __name__ == '__main__':
    main()