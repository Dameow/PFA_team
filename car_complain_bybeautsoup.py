import requests
from bs4 import BeautifulSoup
import pandas as pd #不要忘了引用pd
# 请求URL
#url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-1.shtml'
#封装一个函数叫get_page_content():
def get_page_content(request_url):
# 得到页面的内容：
	headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}#？？？？
	html=requests.get(request_url,headers=headers,timeout=10) 
	content = html.text
	# 通过content创建BeautifulSoup文件:
	soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
	return soup 
	#通过以上语句获取了url内容后，return一个soup空文件，在后面再把get_page_content(request_url)赋值给soup

#在写完df后，包装成一个函数analysis()，意思是分析页面的投诉的函数:
def analysis(soup):
# 找到完整的投诉信息框：找div，找到div的class_="tslb_b，tslb——投诉列表
# 然后找到的div，代表了整个信息框，整个一段信息框赋值给一个临时变量temp
	temp = soup.find('div',class_="tslb_b")

	# 创建DataFrame,一个空的pandas数据框（df是dataframe的缩写）：
	df = pd.DataFrame(columns = ['id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status'])

	# 在上面找到的信息框里，找到“tr”开头
	# 创建一个tr标签的列表，叫做tr_list
	tr_list = temp.find_all('tr') #temp.是什么？？？
	for tr in tr_list:
	    # ToDolist：提取汽车投诉信息,从tr里找出所有的td
	    temp={} #字典
	    td_list=tr.find_all('td') #第一个tr没有td，而是th，也就是表头。其余几行都有8个td
	    if len(td_list)>0: #如果检测到td,就开始读每个字段的内容（注意加.text，不然拿的是整个标签)
	    	id, brand, car_model, type, desc, problem, datatime, status = td_list[0].text, td_list[1].text, td_list[2].text, td_list[3].text, td_list[4].text, td_list[5].text, td_list[6].text, td_list[7].text
	    #然后放到DataFrame中的temp变量里
	    	temp['id'], temp['brand'], temp['car_model'], temp[ 'type'], temp[ 'desc'], temp[ 'problem'], temp[ 'datetime'], temp[ 'status'] = id, brand, car_model, type, desc, problem, datatime, status 
	    	df = df.append(temp,ignore_index=True) 
	return df

# df=analysis(soup)
# print(df)

# 如果要抓多页：
Page_num=20 
base_url= 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-1' #从页码的基数开始抓，注意，没有.shtml

	#创建DataFrame：
result = pd.DataFrame(columns=['id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status'])
for i in range(Page_num):
	request_url = base_url + str(i+1) + '.shtml'
	soup = get_page_content(request_url) #把前面的get_page_content(request_url)赋值给soup文件
	df=analysis(soup)
	print(df)
	result= result.append(df)

result.to_csv('result.csv',index=False)			
