import requests
import re
import json

url='http://www.dianping.com/shop/83589283'
headers = {
    "Cookie": "cy=6; cye=suzhou; __guid=169583271.1192118947553049600.1548259899249.8318; _lxsdk_cuid=1687b7b3906c8-0bbb4f91871844-454c092b-1fa400-1687b7b39069f; _lxsdk=1687b7b3906c8-0bbb4f91871844-454c092b-1fa400-1687b7b39069f; _hc.v=f881bf49-e5cb-7108-4360-018d19f00345.1548259900; s_ViewType=10; _lx_utm=utm_source%3Dbaidu%26utm_medium%3Dorganic%26utm_term%3D%25E7%25BE%258E%25E5%259B%25",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}

#网页源码
def get_html():
    html=requests.get(url,headers=headers).text
    return html

#svg_css网址,解析html
def get_svg_css():
    svg = re.search(r'([^"]+svgtextcss[^"]+)',get_html()).group()
    svg_css = "https:"+svg
    svg_css_html=requests.get(svg_css, headers=headers).text
    return svg_css_html

#svg数字图片url，解析html
def get_svg_url():
    print(get_svg_css())
    num_svg_url = "https:"+re.search(r'd\[class\^="wo"\].*?background\-image: url\((.*?)\);',get_svg_css()).group(1)
    num_svg_html = requests.get(num_svg_url, headers=headers).text
    num_list=re.findall(r'>(\d+)<',num_svg_html,re.S)
    # return num_list

    # address_svg_url = "https:" + re.search(r'd\[class\^="op"\].*?background\-image: url\((.*?)\);', get_svg_css()).group(1)
    # address_svg_html = requests.get(address_svg_url, headers=headers).text
    # adress_list = re.findall(r'>(.+)<', address_svg_html, re.S)
    return num_list
    # print(num_list)

#获取偏移量
def get_position():
    data={}
    positions=re.findall(r'\.([a-z0-9A-Z]+)\{background:\-(\d+)\.0px \-(\d+)\.0px',get_svg_css(),re.S)
    for position in positions:
        lists = list(position)
        css_name = lists[0]
        x = int(lists[1])
        y = int(lists[2])
        data[css_name] = [x, y]
    return data



def save_to_json():
    data=get_position()
    with open("num_data.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)



if __name__ == '__main__':
    save_to_json()

    # get_svg_url()



