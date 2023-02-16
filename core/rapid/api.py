import requests
import re


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}


def get_email(url):
    domain = url.split('//')[-1].replace('www.', '').split('/')[0]
    url_gen = f'http://www.skymem.info/srch?q={domain}'
    response = requests.get(url_gen, headers=headers)
    email_list = re.findall(r"href=\"\/srch\?q=(.*?@.*)\">", response.text)
    emails_dict = {}
    emails = [line for line in email_list if domain in line]
    emails_dict[domain.split("@")[0]] = emails
    return emails_dict
