import bs4 #pip install beautifulsoup4
import requests
import time
import os

url = 'https://xkcd.com'

os.makedirs('xkcd', exist_ok=True)

num_downloads = 0
max_downloads = 10

while not url.endswith('#') and num_downloads < max_downloads:
    print(f'Downloading page {url}')
    response = requests.get(url)
    response.raise_for_status()

    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    # Correct selector
    comic_elem = soup.select('#comic img')

    if comic_elem == []:
        print('Could not find comic image.')
    else:
        comic_url = 'https:' + comic_elem[0].get('src')
        print(f'Downloading image {comic_url}')

        img_res = requests.get(comic_url)
        img_res.raise_for_status()

        image_file = open(os.path.join('xkcd', os.path.basename(comic_url)), 'wb')
        for chunk in img_res.iter_content(1024):
            image_file.write(chunk)
        image_file.close()

    # Correct selector for previous link
    prev_link = soup.select('a[rel="prev"]')[0]
    url = 'https://xkcd.com' + prev_link.get('href')

    num_downloads += 1
    time.sleep(1)

print('Done')
