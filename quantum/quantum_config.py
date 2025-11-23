import os
from getpass import getpass

def setup_token():
    print('IBM Quantum Token Setup')
    print('='*40)
    print('Obtenha seu token em: https://quantum.ibm.com/account')
    
    token = getpass('Digite seu token: ')
    
    with open('.env', 'w') as f:
        f.write(f'IBMQ_TOKEN={token}\n')
    
    print('Token salvo em arquivo .env')
    print('Adicione .env ao .gitignore!')

if __name__ == '__main__':
    setup_token()
