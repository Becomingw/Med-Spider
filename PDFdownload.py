import os
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def Pubmed_download(excel):
    print('开始下载.....')
    df = pd.read_excel(excel, engine='openpyxl')
    for index, link in df.iterrows():
        if type(link['free_link']) == type('str'):
            Tl = re.sub(r'[\\/:*?"<>|]', '_', link['title'])
            p_url = link['free_link']
            response = requests.get(p_url, headers={"User-Agent": UserAgent().random})
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, 'html.parser')
            link_tem = soup.find('li', attrs={'class': 'pdf-link other_item'})
            real_link = link_tem.find('a').get('href')
            real_link = 'https://www.ncbi.nlm.nih.gov' + real_link
            response = requests.get(real_link, headers={"User-Agent": UserAgent().random})
            if response.status_code == 200:
                if os.path.exists('pdf'):
                    pass
                else:
                    os.makedirs('pdf')
                with open(f'pdf/{Tl}.pdf', 'wb') as file:
                    file.write(response.content)
                print(f"[{Tl}] has been downloaded!")
                df.at[index, 'download'] = '1'
            else:
                print(f"[{Tl}] failed to be downloaded!")
                df.at[index, 'download'] = '0'
        else:
            df.at[index, 'download'] = '0'
    try:
        df.to_excel('RX.xlsx', engine='openpyxl', index=False)
    except:
        print('请关闭excel文件后重试，本次表格写入失败！')
    print('PubMed Downloaded over!')


def sci_hub(doi=None, folder='pdf', filename=None):
    output_folder = folder
    scihub_url = "https://sci-hub.st/"
    response = requests.post(scihub_url, data={"request": doi})
    soup = BeautifulSoup(response.content, features="html.parser")
    flag = False
    n = 0
    try:
        buttons_div = soup.find('div', {'id': 'buttons'})
        download_button = buttons_div.find('button')
        download_url = download_button['onclick'][15:-1]
        flag = True
        n = 1
    except:
        print(f'[{doi}] has no target')
    while flag:
        if download_url.startswith('//'):
            print(download_url[2:-14])
            pdf_response = requests.get("https://" + download_url[2:-14], stream=True)
        else:
            pdf_url = scihub_url + download_url
            pdf_url = pdf_url[0:-14]
            pdf_response = requests.get(pdf_url, stream=True)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if filename:
            filename = filename
        else:
            filename = doi.replace('/', '_')
        local_filename = os.path.join(output_folder, f"{filename}.pdf")
        with open(local_filename, 'wb') as f:
            for chunk in pdf_response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f'[{filename}] has been downloaded!')
        flag = False
    return n
