# IEEE_spider_bynum.py

# 本脚本用来读取ieee论文链接并获取全部信息，然后存入csv文件
# 平均爬取一篇文章的时间如果大于10秒，请挂梯子


# Anaconda搭建chorme环境教程： https://www.jianshu.com/p/99b55b2834e6
# 服务器配置chorme环境教程： https://www.jb51.net/article/183899.htm
import time
import requests
from time import sleep
import json
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

durl = 'https://ieeexplore.ieee.org/document/'
apiurl = 'http://ieeexploreapi.ieee.org/api/v1/search/articles?apikey=gqk6ss8wkj3zd4khxqtntwfe&format=json' \
         '&max_records=2&start_record=1&sort_order=asc&sort_field=article_number&article_number='
# df = []

# 输入csv文件路径：
oricsv = '/Users/dengyunlong/PycharmProjects/IEEE_spider_bynum/Pat_Hanrahan_1_Allcitation_Link.csv'
# 输出到csv路径：
aimcsv = 'IEEE_PatHarahan_1_Article.csv'


def get_otherinf(url):
    print(url)
    r = requests.get(url)
    inf_list = json.loads(r.text)
    print(inf_list)
    art = inf_list['articles'][0]
    global pubtime
    pubtime = art['publication_date']
    global abstract
    abstract = art['abstract']
    global tit
    tit = art['title']
    global doi
    doi = art['doi']
    global aulist
    aulist = art['authors']['authors']
    global auname_list
    auname_list = []
    global auid_list
    auid_list = []
    global auurl_list
    auurl_list = []
    global affiliation_list
    affiliation_list = []
    global publication_title
    publication_title = art['publication_title']
    for i in range(0, len(aulist)):
        auname_list.append(aulist[i]['full_name'])
        auid_list.append(aulist[i]['id'])
        auurl_list.append(aulist[i]['authorUrl'])
        try:
            affiliation_list.append(aulist[i]['affiliation'])
        except Exception as e:
            print(repr(e))
            affiliation_list.append('nan')


if __name__ == '__main__':

    # 以下部分是用来读取从google scholar上爬到的论文PDF链接并且筛选出ieee里的论文链接的
    # anotherdf = pd.read_csv(oricsv)
    # anotherlist = anotherdf['tit'].values.tolist()
    # mylist = []
    # print(anotherlist)
    # print("******")
    # for li in anotherlist:
    #     if str(li)[8:33] == 'ieeexplore.ieee.org/iel7/':
    #         mylist.append(li[-11:-4])
    # print(mylist)
    # *******************************

    # 以下部分是读取csv文件中含有论文的一列并根据此爬取论文的
    # 只需要改变下面的csv文件地址，并保证csv文件中有'link'列即可
    mylist = []
    mydf = pd.read_csv(oricsv)
    orilist = mydf['link'].values.tolist()
    # orilist = mydf['html_url'].values.tolist()
    # print(len(orilist))
    # for i in range(1, len(orilist)):
    #     mylist.append(str(orilist[i])[-8:-1])
    # print(mylist)
    # orilist = mydf['0'].values.tolist()
    print(len(orilist))
    for i in range(1, len(orilist)):
        mylist.append(str(orilist[i])[-7:])
    print(mylist)
    # *******************************************

    chrome_options = webdriver.ChromeOptions()
    # 设置chrome不加载图片，提高速度
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    # 使用headless无界面浏览器模式(如果在调试时可以注释掉下两行）
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')

    # 注意这里要把executable_path设置成自己的chromedriver在Chrome的位置
    browser = webdriver.Chrome(executable_path=r'/Applications/Google Chrome.app/chromedriver', options=chrome_options)
    browser.get('https://ieeexplore.ieee.org/Xplore/home.jsp')
    with open('cookies.txt', 'r', encoding='utf8') as f:
        listCookies = json.loads(f.read())

    # 往browser里添加cookies
    for cookie in listCookies:
        try:
            cookie_dict = {
                'domain': '.ieee.org',
                'expiry': '',
                'httpOnly': cookie.get('httpOnly'),
                'name': cookie.get('name'),
                'path': '/',
                'secure': cookie.get('secure'),
                'value': cookie.get('value')
            }
            browser.add_cookie(cookie_dict)
        except:
            cookie_dict = {
                'domain': '.ieee.org',
                'httpOnly': cookie.get('httpOnly'),
                'name': cookie.get('name'),
                'path': '/',
                'secure': cookie.get('secure'),
                'value': cookie.get('value')
            }
            browser.add_cookie(cookie_dict)

    errortime = 0
    for i in range(283, len(mylist) - 1):
        try:

            apiurl1 = apiurl + str(mylist[i])
            get_otherinf(apiurl1)
            durl1 = durl + str(mylist[i])
            st = time.time()
            try:
                browser.get(durl1)
                WebDriverWait(browser, 20, 0.5).until(EC.presence_of_all_elements_located((By.ID, "article")))

            except Exception as e:
                print("抓到异常，页面停止加载，但是程序不停止。")
                errortime += 1
                sleep(2)
                if errortime >= 5:
                    print("当前爬取位置")
                    print(i - errortime + 1)
                    break
            # browser.execute_script(js)
            # print(f"browser text = {browser.page_source}")
            try:
                browser.execute_script("document.documentElement.scrollTop=20000")
                WebDriverWait(browser, 20, 0.5).until(EC.presence_of_all_elements_located((By.ID, "article")))
                sleep(4)
                s = browser.find_element_by_id('article')
                print(s)
                print(s.text)
                stext = str(s.text)
                print(stext)
                # try:
                #     but = browser.find_elements_by_class_name("accordion-chevron")
                #     print(but)
                #     # 点击"references"按钮
                #     but2 = but[2]
                #     but2.click()
                #     sleep(10)
                # except Exception as e:
                #     print("but2 x")
                #     but = browser.find_elements_by_class_name("accordion-chevron")
                #     but3 = but[1]
                #     but3.click()
                #     sleep(10)
                #     print("but1 clicked")
                # print("Clicked")

                durl2 = durl1 + '/references#references'
                browser.get(durl2)

                WebDriverWait(browser, 20, 0.5).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "reference-container")))
                ref = browser.find_elements_by_class_name('reference-container')
                print(len(ref))
                reference = []
                for j in range(0, len(ref)):
                    reference.append(ref[j].get_attribute('textContent'))

                # try:
                #     but = browser.find_elements_by_class_name("accordion-chevron")
                #     print(len(but))
                #     # try:
                #     #     but[3].click()
                #     #
                #     #     sleep(10)
                #     # except Exception as e:
                #     #     print("but3 x")
                #     try:
                #         but[3].click()
                #         sleep(10)
                #     except Exception as e:
                #         print("but3 x")
                #
                #     WebDriverWait(browser, 20, 0.5).until(
                #         EC.presence_of_all_elements_located((By.CLASS_NAME, "doc-keywords-list-item")))
                #     keys = browser.find_elements_by_class_name('doc-keywords-list-item')
                #     print(keys)
                #     print(len(keys))
                #     keywords = keys[0].get_attribute('textContent')
                #     print(str(keywords)[13:])
                #     key = str(keywords)[13:]
                # except Exception as e:
                #     print("but xx")
                #     key = " "
                try:
                    df = []  ####ZXR
                    df.append(
                        [tit, doi, pubtime, str(mylist[i]), auname_list, auid_list, auurl_list, affiliation_list,
                         stext,
                         reference, abstract, publication_title])
                except Exception as e:
                    print(e)

            except Exception as e:

                print('WWW')

            et = time.time()
            print(st - et)
            aimdf = pd.DataFrame(df,
                                 columns=['tit', 'doi', 'pubtime', 'aid', 'auname_list', 'auid_list', 'auurl_list',
                                          'affiliation_list',
                                          's.text', 'ref.text', 'abstract', 'publication_title'])

            # aimdf.to_csv(
            #     aimcsv,
            #     index=False, header=None)  #######ZXR

            # 追加方式写入(注意如果接着上一次爬取的话注意从当前已写入论文的下一篇论文开始爬）
            aimdf.to_csv(aimcsv, mode='a', header=False, index=False)
            print(f'第{i}篇论文已写入')
        except Exception as e:
            print(repr(e))
    browser.quit()

    print(df)
