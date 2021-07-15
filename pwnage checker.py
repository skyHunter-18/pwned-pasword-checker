import requests
import hashlib
import sys

from requests.models import Response
from getpass import getpass


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f'Error fetching: {res.status_code}. Check & Try again!!')
    return res


def get_passkey_leak_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(passkey):
    sha1_passkey = hashlib.sha1(passkey.encode('utf-8')).hexdigest().upper()
    first5_char, remaining_char = sha1_passkey[:5], sha1_passkey[5:]
    response = request_api_data(first5_char)
    return get_passkey_leak_count(response, remaining_char)


def main():
    # for password in args:
    # password = input('Enter the passowrd u want to check: ')
    print('Input will be hidden to ensure security!')
    password = getpass('Enter your password to check: ')
    count = pwned_api_check(password)
    if count:
        # print(f'The password "{password}" appears {count} times. Please change your password!!')
        print(
            f'Your password appears {count} times. Please change your password!!')
    else:
        # print(f'The password "{password}" doesn\'t appears in any leaks. All Good!!')
        print(f'Your password doesn\'t appears in any leaks. All Good!!')
    return 'Execution completed!!'


if __name__ == '__main__':
    # sys.exit(main(sys.argv[1:]))
    main()
