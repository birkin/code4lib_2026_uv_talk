# /// script
# requires-python = ">=3.12, <3.13"
# dependencies = [
#     "httpx==0.28.1",
# ]
# ///

import httpx


def main():
    url = 'https://repository.library.brown.edu/api/items/bdr:80246/'

    response = httpx.get(url)

    data = response.json()
    primary_title = data.get('primary_title')

    print(f'Primary Title: {primary_title}')


if __name__ == '__main__':
    main()
