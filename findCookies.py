from selenium import webdriver
from time import sleep
import json

aimUrl = 'https://ieeexplore.ieee.org/document/8009795'
# 使用说明：在运行程序后，在打开的网页界面中找到institutional sign in,选择xx大学并用自己的账号登录，然后等待120秒后程序自动结束，出现cookies保存成功！
# 保存好的cookies在cookies.txt文件中，cookies有时效限制，如果时效需要重复上述操作

if __name__ == '__main__':
    chrome_options = webdriver.ChromeOptions()
    # 设置chrome不加载图片，提高速度
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    # 使用headless无界面浏览器模式(如果在调试时可以注释掉下两行）
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # 注意这里要把executable_path设置成自己的chromedriver在Chrome的位置
    browser = webdriver.Chrome(executable_path=r'/Applications/Google Chrome.app/chromedriver', options=chrome_options)
    browser.get(aimUrl)
    sleep(60)
    dictCookies = browser.get_cookies()  # 获取list的cookies
    jsonCookies = json.dumps(dictCookies)  # 转换成字符串保存
    print(jsonCookies)
    with open('cookies.txt', 'w') as f:
        f.write(jsonCookies)
    print('cookies保存成功！')
    browser.quit()