import os.path
import argparse
import datetime
import requests
import whois


def load_urls4check(path):
    if not os.path.exists(path):
        return None
    with open(path) as file_handler:
        urls = []
        for line in file_handler.readlines():
            urls.append(line.rstrip())
        return urls


def is_server_respond_with_200(url):
    return requests.get(url).status_code == requests.codes.ok


def get_domain_expiration_date(domain_name):
    return whois.whois(domain_name).expiration_date


def get_file_name_with_urls():
    parser = argparse.ArgumentParser(description='Программа проверяет работоспособность сайта')
    parser.add_argument('file', default='urls.txt', type=str,
                        help='файл, содержащий урлы сайтов для проверки')
    return parser.parse_args().file


def check_urls(urls):
    today = datetime.datetime.today()
    days_in_month = 30
    urls_ok = []
    for url in urls:
        is_code_200 = is_server_respond_with_200(url)
        expiration_date = get_domain_expiration_date(url)
        days_to_expiration = (expiration_date - today).days
        if is_code_200 and days_to_expiration > days_in_month:
            urls_ok.append(url)
    return urls_ok


def print_urls_ok(urls):
    for url in urls:
        print('%s в порядке!' % url)


if __name__ == '__main__':
    path = get_file_name_with_urls()
    urls = load_urls4check(path)
    if not urls:
        print('файл %s не найден\n' % path)
    else:
        urls = check_urls(urls)
        print_urls_ok(urls)
