import requests
import time
import random
from lxml import etree
from setting import json_data,num_list,adress_list


headers = {
    "Cookie": "cy=6; cye=suzhou; __guid=169583271.1192118947553049600.1548259899249.8318; _lxsdk_cuid=1687b7b3906c8-0bbb4f91871844-454c092b-1fa400-1687b7b39069f; _lxsdk=1687b7b3906c8-0bbb4f91871844-454c092b-1fa400-1687b7b39069f; _hc.v=f881bf49-e5cb-7108-4360-018d19f00345.1548259900; s_ViewType=10; _lx_utm=utm_source%3Dbaidu%26utm_medium%3Dorganic%26utm_term%3D%25E7%25BE%258E%25E5%259B%25",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}
item={}

def get_html(url):
    response=requests.get(url,headers=headers).text
    html=etree.HTML(response)
    contents = html.xpath('//div[@id="shop-all-list"]/ul/li')
    for content in contents:
        url_list = content.xpath('.//div[@class="tit"]/a/@href')[0]
        print("正在弄抓取：{}".format(url_list))
        get_value_list(url_list)
        print(item)
        time.sleep(0.5+random.random())
        # break


#获取属性值列表
def get_value_list(url_list):
    response = requests.get(url_list, headers=headers).text
    html=etree.HTML(response)
    shop_name=html.xpath('//h1[@class="shop-name"]/text()')
    comments_value_list=html.xpath('//span[@id="reviewCount"]/text()|//span[@id="reviewCount"]/d/@class')[:-1]
    price_value_list = html.xpath('//span[@id="avgPriceTitle"]/text()|//span[@id="avgPriceTitle"]/d/@class')
    tasty_value_list = html.xpath('//span[@id="comment_score"]/span[1]/text()|//span[@id="comment_score"]/span[1]/d/@class')[1:]
    environment_value_list = html.xpath('//span[@id="comment_score"]/span[2]/text()|//span[@id="comment_score"]/span[2]/d/@class')[1:-1]
    service_value_list = html.xpath('//span[@id="comment_score"]/span[3]/text()|//span[@id="comment_score"]/span[3]/d/@class')[1:-1]
    telephone_value_list = html.xpath('//p[@class="expand-info tel"]/text()|//p[@class="expand-info tel"]/d/@class')
    address_value_list = html.xpath(
        '//span[@id="address"]/text()|//span[@id="address"]/d/@class|//span[@id="address"]/e/@class')

    item['店名'] =("".join(shop_name)).strip()
    item['店铺链接'] = url_list
    item['口味'] = get_info(tasty_value_list)
    item['环境'] = get_info(environment_value_list)
    item['服务'] = get_info(service_value_list)
    item['评论数']=get_info(comments_value_list).strip()
    price =get_info(price_value_list)
    item['人均']=price.replace('人均:','').replace('元','').strip()
    item['电话'] = get_info(telephone_value_list).strip()
    address = get_info(address_value_list)
    item['地址'] =address.replace(' \xa0',';').strip()


def get_info(value_list):
    # print(value_list)   #[' 1', 'woota', 'wok3b', 'wonh2'] 解析数据
    comment_value=[]
    for comment in value_list:  #1没有加密直接解析
        if comment.strip() in ['1','.']:
            comment_value.append(comment)
        elif comment.strip() == '-':  # 提取小数点
            comment_value.append(comment)
        elif comment.strip() == '':  #属性中没有text()
            pass
        elif comment.startswith('op'):
            # print(comment)
            value = json_data[str(comment)]
            offset = value[0]  / 14  # css属性offset
            position = value[1]  # css属性position
            # print(offset,position)
            comments = adress_list[str(position)][int(offset)]
            comment_value.append(comments)
        elif comment.startswith('wo'):
            value=json_data[str(comment)]
            offset=(value[0]+6)/14  #css属性offset
            position =value[1] #css属性position
            # print(offset,position) (18,132)
            comments=num_list[str(position)][int(offset)-1]
            # print(comments) 0, 8 ,2
            comment_value.append(comments)
        else:
            comment_value.append(comment)
        # print(comment_value)
    result="".join(comment_value)
    return result
    # print(item)



if __name__ == '__main__':
    urls=['http://www.dianping.com/suzhou/ch10/p%d'%i for i in range(1,51)]
    for url in urls:
        page=int(url.split('/')[-1].replace('p',''))
        print("正在爬取第{}页".format(page),url)
        get_html(url)
        time.sleep(random.randint(1,5))





