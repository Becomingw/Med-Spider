import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tookit import tranlate


# 主程序部分
def main(page, kw, cytoken):
    paper_data = pd.DataFrame(columns=['title', 'journal', 'Date', 'doi', "abstract", "摘要", 'PMID', 'journal_link',
                                       'free_link', 'download'])
    url = 'https://pubmed.ncbi.nlm.nih.gov/'
    fmt = 'abstract'
    for num in range(1, page):
        response = requests.get(url,
                                params={'term': kw,
                                        'page': str(num),
                                        'filter': 'datesearch.y_5',
                                        'format': fmt},
                                headers={"User-Agent": UserAgent().random})
        response.raise_for_status()  # 防止没正确解析出现错误运行
        response.encoding = response.apparent_encoding  # 防止乱码

        soup = BeautifulSoup(response.text, 'html.parser')

        paper_list = soup.find_all('div', attrs={"class": "results-article"})
        paper_record = {}

        for paper in paper_list:
            title = []
            print('正在运行.....')
            # 清空字典
            paper_record.clear()
            article = paper.article
            titles = article.h1.a.strings
            # strip函数用于删除头尾的空白符,包括\n\t等
            for s in titles:
                title.append(s.strip())
            paper_record['title'] = ''.join(title)

            # 获取发表年份
            date_tem = article.find('span', attrs={'class': 'cit'})
            try:
                date = date_tem.text[0:4]
                paper_record['Date'] = date + '年'
            except:
                pass

            # 获取DOI信息
            doi = article.find('span', attrs={"class": "citation-doi"})
            if doi is None:
                paper_record['doi'] = 'No doi'
            else:
                paper_record['doi'] = doi.string.strip()[5:-1]

            # 获取PMID
            try:
                PMID = article.find('strong', attrs={"class": "current-id"})
                pmid = ''.join(filter(str.isdigit, PMID.text))
                paper_record['PMID'] = pmid
            except:
                pass

            # 获取文章地址
            try:
                PMIC_tem = article.find('a', attrs={"class": "id-link"})
                PMIC_link = PMIC_tem.get('href')
                if PMIC_link.startswith('http://www.ncbi.nlm.nih.gov'):
                    paper_record['free_link'] = PMIC_link
                else:
                    paper_record['journal_link'] = PMIC_link
            except:
                print('NOT LINK!')

            # 获取期刊
            journal_temp = article.find('button', attrs={'class': 'journal-actions-trigger trigger'})
            try:
                journal = journal_temp.get('title')
                paper_record['journal'] = journal
            except:
                pass
            # 获取摘要信息
            abstract = []
            abstracte = []
            if article.find_all("em", attrs={"class": "empty-abstract"}):
                abstract.append("No abstract")
            else:
                content = article.find("div", attrs={"class": "abstract-content selected"})
                abstracts = content.find_all('p')

                for item in abstracts:
                    for sub_content in item.strings:
                        if cytoken:
                            sub_contentC = tranlate(sub_content, "auto2zh", cytoken)  # 调用彩云
                            abstract.append(sub_contentC.strip())
                            paper_record['摘要'] = ''.join(abstract)
                        abstracte.append(sub_content.strip())
                paper_record['abstract'] = ''.join(abstracte)
            paper_tem = pd.DataFrame(paper_record, index=[0])
            paper_data = pd.concat([paper_data, paper_tem], ignore_index=True)
    try:
        paper_data.to_excel('./RX.xlsx', index=False)
    except:
        print('不关Excel，保存失败，重新再来一次吧！')
    print(f"查找结束！共计【{len(paper_data['title'])}】篇文献")
