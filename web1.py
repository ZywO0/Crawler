from bs4 import BeautifulSoup #网页解析，获取数据
import re  #正则表达式，进行文字匹配
import urllib.request,urllib.error #指定url，获取网页数据
import pymysql
#正则提取
findLink = re.compile(r'<a href="(.*?)"')
findContent = re.compile(r'<p>(.*?)</p>')
findTitle = re.compile(r'<title>(.*?)</title>')
#爬取网页，解析数据
def getData(baseurl):
    #从第一个网址，获得各个文章的网址（这个是通过解析html一个div获得所有的网址，豆瓣那个是通过url之间的关系，直接用for循环获得各个网页的网址）
    datalist = []
    html = askURL(baseurl)
    bs = BeautifulSoup(html, "html.parser")
    div_list = bs.find_all("div", class_="lmcn")
    div_list = str(div_list)
    res = re.findall(findLink, div_list)#各个菜谱的网址
    for string in res:
        data = []
        string = "http://www.coozhi.com"+string
        html1 = askURL(string)
        bs1 = BeautifulSoup(html1, "html.parser")
        div_list1 = bs1.find_all("div", class_="news cnt")
        div_list1 = str(div_list1)
        res1 = re.findall(findContent, div_list1) #一个菜谱的所有文字，类型为列表
        title = bs1.select("title")#也是tag标签
        title = str(title)
        title = re.findall(findTitle,title)#也是返回一个列表
        data.append(title[0])
        i = 0
        for da in res1:
            i += len(da)
            if i < 5000:
                data.append(da)
        datalist.append(data)
    return datalist

def askURL(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    request = urllib.request.Request(url, headers=header)
    try:
        response = urllib.request.urlopen(request)
        # html = response.read().decode("utf-8")
        html = response.read()
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
    return html
#保存数据
def saveData(datalist):
    print("start saving data")
    conn = pymysql.Connection(host='121.199.173.191', user='Warehouse', password='7Hc5w3L7H8eKmBcs', port=3306,
                              database='Warehouse')
    cursor = conn.cursor()
    j = 1
    for data in datalist:#每个data是一个文章的标题和正文，第一个元素是标题，后面是正文
        sql = '''
            INSERT INTO `12` (ID,title,content,author,tag,platform)
         VALUES('%d','%s','%s','热心网友','美食','酷知网') 
        ''' % (j, data[0], ''.join(data[1:]))
        j += 1
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()
    print("finished saving data")
def main():
    baseurl = "http://www.coozhi.com/meishijiayin/"
    datalist = getData(baseurl)
    saveData(datalist)

if __name__ ==  "__main__":
    main()




