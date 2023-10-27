import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://github.com/"
load_more = "https://github.com/topics/machine-learning?page="

url_list = []
for i in range(1,8):
    url_list.append(load_more+str(i))

counter = 30
information_list = []
for values in url_list:
    html_data = requests.get("https://github.com/topics/machine-learning").text
    soup = BeautifulSoup(html_data , 'lxml')
    main_div = soup.find_all('div' , 'd-flex flex-justify-between my-3')
    if(values == url_list[6]):
        counter = 20
    for data in main_div[:counter]:
        repository_name = data.find('a' , "text-bold wb-break-word").text
        username = data.find('a').text
        stars = data.find('span' , id = "repo-stars-counter-star").text
        first_link = data.find('a' , "text-bold wb-break-word")['href']
        repos_link = base_url+first_link

        information_dict = {
            "Repository Name ":repository_name.strip(),
            "Username ":username.strip(),
            "Stars ":stars,
            "URL ":repos_link
        }
        information_list.append(information_dict)
    
df = pd.DataFrame(information_list)
df.to_excel("Machine Learning Information.xlsx")

