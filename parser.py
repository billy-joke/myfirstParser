# -*- coding: utf-8 -*-
import os
import sys
import random
import string
import requests
import argparse
import threading
import cfscrape
import string
import re

# nsia36
start_string = 'nsj8g4'

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--threads', type=int, default=5, help='sets the number of threads')
parser.add_argument('-c', '--charset', default=None,
                    help='sets a character mask for links generating, see README.md for syntax information')
namespace = parser.parse_args()

base_file = 'used.txt'
img_dir = 'img'
charset_values = {'?d': string.digits, '?s': string.ascii_lowercase, '?a': string.digits + string.ascii_lowercase}
scraper = cfscrape.create_scraper()
if not os.path.exists(base_file):
    open(base_file, 'a').close()
if not os.path.exists(img_dir):
    os.mkdir(img_dir)

def main(string):
    #initial_url = get_string(namespace.charset)
    initial_url = get_string(string)
    full_url = 'http://prnt.sc/' + initial_url
    print('[*] processing link {}'.format(full_url))
    image_link = get_img_link(full_url)
    if image_link:
        print('[+] image found {}'.format(image_link))
        save_img(initial_url, image_link)
    else:
        print('[-] bad luck, moving on')
    return initial_url


def get_string(mask):
    basefile = open(base_file, 'r')
    base = [item.strip() for item in basefile]
    basefile.close()
    final_string = generate_string(mask)
    if final_string not in base:
        write_to_base(final_string)
    return final_string


def generate_string(string):
    string_list = []
    for x in string:
        string_list.append(ord(x))
    string_list[5] += 1
    for x in range(len(string_list)):
        #print()
        if string_list[len(string_list) - 1 - x] == 58 or string_list[len(string_list) - 1 - x] == 123:
            if string_list[len(string_list) - 1 - x] == 58:
                string_list[len(string_list) - 1 - x] = 97
            if string_list[len(string_list) - 1 - x] == 123:
                string_list[len(string_list) - 1 - x] = 48
            string_list[len(string_list) - 2 - x] += 1
        else:
            pass
    string_return = []
    for x in string_list:
        string_return.append(chr(x))
    str_ret = ''.join(string_return)
    return str_ret

def write_to_base(link):
    with open('used.txt', 'a') as base_file:
        base_file.write(link + '\n')


def get_img_link(link):
    html_response = scraper.get(link).content
    native_img = re.search('http[s]*://image.prntscr.com/image/\w+.png', str(html_response))
    imgur_img = re.search('http[s]*://i.imgur.com/\w+.png', str(html_response))
    if (native_img or imgur_img):
        return (native_img or imgur_img).group()


def save_img(initial_url, img_link):
    img = requests.get(img_link)
    with open('{0}/{1}.png'.format(img_dir, initial_url), 'wb') as file:
        file.write(img.content)


def loop(start_string):
    while True:
        tmp_string = start_string
        try:
            main()
        except KeyboardInterrupt:
            sys.exit()

while True:
    tmp_string = start_string
    try:
        start_string = main(tmp_string)
    except KeyboardInterrupt:
        sys.exit()
