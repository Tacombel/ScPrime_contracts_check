import os
import sys
from config import Config
from urllib.request import Request, urlopen
from urllib.error import URLError


def check_contracts(host):

    first_line = True
    host_contracts = os.popen(Config.base_cmd + ' ' + host + ' spc host contracts').readlines()

    print(f'Hay {len(host_contracts) - 1} contratos')
    unresolved = 0
    locked = 0
    not_found = 0
    for e in host_contracts:
        if first_line:
            first_line = False
            continue
        e = e.split()
        if e[1] == 'Unresolved':
            unresolved += 1
            SCP = 0
            url = 'https://scprime.info/navigator-api/hash/' + e[0]
            req = Request(url)
            try:
                response = urlopen(req)
            except URLError as e:
                if hasattr(e, 'reason'):
                    print('We failed to reach a server.')
                    print('Reason: ', e.reason)
                elif hasattr(e, 'code'):
                    print('The server couldn\'t fulfill the request.')
                    print('Error code: ', e.code)
                sys.exit()

            data = response.read()
            data = data.decode("utf-8")
            if len(data) < 3:
                not_found += 1
                continue
            if e[5] == 'SCP':
                SCP = float(e[4])
            if e[5] == 'mS':
                SCP = float(e[4]) / 1000
            if e[5] == 'uS':
                SCP == float(e[4]) / 1000000
            print(f'{e[0]}: {SCP} SCP')
            locked += SCP

    print(f'Unresolved: {unresolved}')
    print(f'Not found: {not_found}')
    print(f'Ongoing: {unresolved - not_found}')
    print(f'Locked: {locked} SCP')
    wallet = os.popen(Config.base_cmd + ' ' + host + ' spc wallet').readlines()
    exact = wallet[5]
    exact = exact.split()
    print(f'Exact: {exact[1]} H')



def main():
    for e in Config.hosts:
        print(f'{e}')
        check_contracts(e)
        print('----------------------------------------')

if __name__ == "__main__":
    main()
