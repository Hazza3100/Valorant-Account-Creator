import json
import os
import random
import string
import requests
import threading

from colorama import Fore


with open('data/config.json') as f:
    config = json.load(f)

    api_key = config['Capmonster Key']
    logs    = config['Logs'] 



class Hcaptcha:
    def __init__(self, api_key) -> None:
        pass

        self.api_key = api_key
        self.session = requests.Session()

    def getTaskResult(self, taskID):
        json = {
            'clientKey': self.api_key,
            'taskId'   : taskID
            }
        while True:
            r = self.session.post('https://api.capmonster.cloud/getTaskResult', json=json)
            if r.json()['status'] == 'ready':
                captcha_token = r.json()['solution']['gRecaptchaResponse']
                return captcha_token


    def createTask(self):
        json = {
            'clientKey': self.api_key,
                'task': {
                    'type'            : 'HCaptchaTaskProxyless',
                    'websiteURL'      : 'https://auth.riotgames.com',
                    'websiteKey'      : 'a010c060-9eb5-498c-a7b9-9204c881f9dc',
                }
            }
        r = self.session.post('https://api.capmonster.cloud/createTask', json=json)
        try:
            return r.json()['taskId']
        except:
            return r.json()['errorId']


class stat():
    created = 0

class valo:
    def __init__(self) -> None:
        pass
        self.session = requests.Session()

    def Gen(self):
        try:
            capmonster = Hcaptcha(api_key)
            captcha_token = capmonster.getTaskResult(capmonster.createTask())
            proxy = random.choice(open('data/proxies.txt', 'r').read().splitlines())
            proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}

            username = random.choice(open('data/usernames.txt', 'r').read().splitlines()) + ''.join(random.choices(string.ascii_letters, k=2))
            email    = username + ''.join(random.choices(string.ascii_letters + string.ascii_uppercase + string.digits, k=3)) + "@gmail.com"
            password = ''.join(random.choices(string.ascii_letters + string.ascii_uppercase + string.digits, k=10))
            headers  = {'authority': 'signup-api.riotgames.com','accept': '*/*','accept-language': 'en-GB,en;q=0.9','origin': 'https://auth.riotgames.com','referer': 'https://auth.riotgames.com/','sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-site','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',}

            json = {
                'tou_agree'       : True,
                'newsletter'      : False,
                'date_of_birth'   : '2000-02-13',
                'email'           : email,
                'username'        : username,
                'password'        : password,
                'confirm_password': password,
                'client_id'       : 'prod-xsso-playvalorant',
                'redirect_uri'    : 'https://xsso.playvalorant.com/redirect',
                'locale'          : 'en',
                'token'           : f'hcaptcha {captcha_token}',
                }

            response = self.session.post('https://signup-api.riotgames.com/v1/accounts', headers=headers, json=json, proxies=proxies)
            if "token" in response.text:
                stat.created += 1
                token = response.json()['token']
                open('data/results/tokens.txt', 'a').write(f'{token}\n')
                open('data/results/accounts.txt', 'a').write(f'{email}:{username}:{password}\n')
                open('data/results/full_accounts.txt', 'a').write(f'{email}:{username}:{password}:{token}\n')
                print(f"{Fore.BLUE}[ {Fore.GREEN}+ {Fore.BLUE}]{Fore.RESET} Created Account with username {username} ({stat.created})")
            else:
                print(f"{Fore.BLUE}[ {Fore.RED}x {Fore.BLUE}]{Fore.RESET} Error")
        except Exception as e:
            if logs == True:
                print(e)
            else:
                pass


os.system('cls')
threads = int(input(f"{Fore.GREEN}[{Fore.CYAN} ? {Fore.GREEN}] Amount of accounts to create {Fore.CYAN}> {Fore.WHITE}"))
for i in range(threads):
    threading.Thread(target=valo().Gen).start()
