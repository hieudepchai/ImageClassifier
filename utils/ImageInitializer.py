from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from fastai.vision import *

chromepath = "/usr/bin/chromedriver"
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--headless")
driver = webdriver.Chrome(chromepath, chrome_options=chromeOptions)
wait = WebDriverWait(driver, 5)



def get_image_urls(driver, wait, image_class):
    driver.get('https://images.google.com/')
    driver.find_element_by_css_selector(
        '#sbtc > div > div.a4bIc > input').send_keys(image_class)
    driver.find_element_by_css_selector(
        '#sbtc > button > div > span > svg').click()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(0.5)
    urls = list(map(lambda x: x.get_attribute('data-src'), driver.find_elements_by_css_selector('.rg_i')))
    urls = [x for x in urls if x is not None]
    print('Image Class: {}, Result: {}'.format(image_class, len(urls)))
    return urls

def exportURLs(img_urls, path, type='csv'):
    for img_class in img_urls:
        print('-- generating {} csv file'.format(img_class))
        urls = img_urls[img_class]
        filename = img_class+'.csv'
        filepath=path/filename
        with open(filepath, 'w') as csvfile:
            # csv_writer = csv.writer(csvfile)
            for url in urls:
                csvfile.write(url)
                csvfile.write('\n')
            csvfile.close()

def input_cmd():
    dataset_name = input('Dataset name: ')
    n = int(input('Number of image classes: '))
    for iclass in range(n):
        img_classes.append(input('Class {}: '.format(iclass+1)))
    return dataset_name, n, img_classes

def input_file():
    with open('input.txt','r') as inputfile:
        dataset_name = inputfile.readline().rstrip()
        print('Dataset name: ', dataset_name)
        n = int(inputfile.readline().rstrip())
        print('Number of image classes: ', n)
        for iclass in range(n):
            img_classes.append(inputfile.readline().rstrip())
            print('Class {}: {}'.format(iclass+1, img_classes[iclass]))
        inputfile.close()
        return dataset_name, n, img_classes 

if __name__ == "__main__":
    #variables
    datast_name = ''
    n = 0
    img_classes = []
    img_urls = {}
    #input
    print('Input section: ')
    dataset_name, n, img_classes = input_file()
    print()
    #create path
    print('Creating a new directory according to classes ...')
    path=Path('dataset/'+dataset_name)
    for img_class in img_classes:
        dest = path/img_class
        dest.mkdir(parents=True, exist_ok=True)
    print('Created directory: ', path.ls())
    print('Complete!\n')
    #get img urls
    print('Getting img urls ...')
    for img_class in img_classes:
        img_urls[img_class] = get_image_urls(driver, wait, img_class)
    print('Complete!\n')
    #generate url csv
    print('Generating url csv files ...')
    exportURLs(img_urls, path)
    print('Complete!\n')

    #download images
    print('Downloading images ...')
    for img_class in img_classes:
        print('-- downloading {} images'.format(img_class))
        dest = path/img_class
        filename = img_class+'.csv'
        filepath= path/filename
        download_images(filepath, dest, max_pics=200, max_workers=3)
    print('Complete!\n')
    #verify images
    print('Verifying images (removing images that cannot be opened) ...')
    for img_class in img_classes:
        print('-- verifying {} images'.format(img_class))
        verify_images(path/img_class, delete=True, max_size=500)
    print('Complete!\n')
    #view data
    print('Displaying data')
    

    driver.close()