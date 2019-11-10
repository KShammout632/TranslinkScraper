import requests
import shutil
from bs4 import BeautifulSoup
import upload_to_s3
import time

def scrapeLink(page_link):
    page = requests.get(page_link)
    soup = BeautifulSoup(page.content, 'html.parser')

    im_list = soup.find_all(class_='camera')
    list_of_links = []

    for im in im_list:
        container = im.find('img')
        linkap = container['src']
        file_name = container['alt'].replace(' ', '')
        pair = ["https://trafficcams.vancouver.ca/" + linkap, file_name]
        list_of_links.append(pair)

    saveImg(list_of_links)


def saveImg(list_of_links):
    for link in list_of_links:
        resp = requests.get(link[0], stream=True)
        print(link[1])
        ts = int(time.time())
        local_file = open('images/' + link[1] + str(ts) + '.jpg', 'wb')
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        resp.raw.decode_content = True
        # Copy the response stream raw data to local image file.
        shutil.copyfileobj(resp.raw, local_file)
        # Remove the image url response object.
        del resp
        upload_to_s3.upload_image('images/' + link[1] + str(ts) + '.jpg')

lineList = [line.rstrip('\n') for line in open('links.txt')]

for line in lineList:
    scrapeLink(line)
    print(line + " has been saved")
