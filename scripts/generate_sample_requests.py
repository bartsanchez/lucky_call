#!/usr/bin/env python
import argparse
import json
import random


def get_args():
    parser = argparse.ArgumentParser(description='Generate sample requests')
    parser.add_argument('number_of_samples', type=int)
    parser.add_argument('keyword', type=str)

    return parser.parse_args()


def main(args):
    curl_cmd = (
        'curl '
        '--header "Content-Type: application/json" '
        'http://localhost/ -d'
    )
    for i in range(args.number_of_samples):
        user_id = random.randint(0, 999999)
        user_email = 'user{}@example.com'.format(user_id)
        if i % 13 == 0:
            keyword = 'wrong_keyword'
        else:
            keyword = args.keyword
        # 5 users of each 1000 will use a number of two digits
        # in order to generate wrong requests
        number = random.randint(95, 999)
        data = {
            'user_email': user_email,
            'keyword': keyword,
            'number': number,
        }
        json_data = json.dumps(data).replace('"', r'\"')
        line = '{} "{}" &'.format(curl_cmd, json_data)
        if i == args.number_of_samples - 1:
            line = line[:-2]
        print(line)


if __name__ == '__main__':
    main(get_args())
