import requests
from bs4 import BeautifulSoup
import pandas as pd


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
base_url = "https://www.themoviedb.org"
html_data = requests.get("https://www.themoviedb.org/movie" , headers= header).text

soup = BeautifulSoup(html_data , 'lxml')

div_tag = soup.find('div', "card style_1")
h2_tag = div_tag.find('h2')
movie_link = base_url + h2_tag.find('a')["href"]
movie_url = movie_link+h2_tag.text
# print(movie_url)
# print(movie_name.text)
movie_page = requests.get(movie_url , headers= header).text
movie_soup = BeautifulSoup(movie_page , 'lxml')
movie_div = movie_soup.find('div' , "single_column")
movie_content = movie_div.find('div' , 'title ott_false')
movie_name = movie_content.find('h2').a.text
movie_rating = movie_div.find('div' , 'user_score_chart')["data-percent"]
movie_genres_base = movie_content.find("span" , "genres")

movie_genres_list = []
for movie_genres in movie_genres_base.find_all('a'):
   movie_genres_list.append(movie_genres.text)

release_date = movie_content.find('span' , 'release').text.strip()
try:
    runtime = movie_content.find('span' , 'runtime').text.strip()
except AttributeError:
    runtime = "None"


def find_director(movie_div_0):
    try:
        people = movie_div_0.find('ol' , 'people no_image')
        li_tag = people.find_all('li')
        for li in li_tag:
            character = li.find('p' , 'character').text
            if "Director" in character:
                return li.p.a.text
    except AttributeError:
        return "No Director Available"
        
director = find_director(movie_div)



def find_director(f_poster_div):
    try:
        ppl_div = f_poster_div.find('ol', class_='people no_image')
        li_tags = ppl_div.find_all('li')
        for li in li_tags:
            character = li.find('p', class_='character').text
            if "Director" in character:
                return li.p.a.text
    except AttributeError:
        return 'None'


def find_genres(f_poster_div):
    f_genres_span = f_poster_div.find('span', class_='genres')
    f_html_movie_genres = f_genres_span.find_all('a')
    f_movie_genres = ""
    f_count = 0
    for f_a_tag in f_html_movie_genres:
        f_count = f_count + 1
        if f_count == len(f_html_movie_genres):
            f_movie_genres = f_movie_genres + f_a_tag.text
        else:
            f_movie_genres = f_movie_genres + f_a_tag.text + ", "
    return f_movie_genres


def get_runtime(f_poster_div):
    try:
        f_movie_runtime = f_poster_div.find('span', class_='runtime').text
        return f_movie_runtime.strip()
    except AttributeError:
        return 'None'


movie_info_list = []
for page_no in range(1, 16):
    base_url = 'https://www.themoviedb.org'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    primary_page = requests.get(base_url+f'/movie?page={page_no}', headers=header).text

    primary_page_soup = BeautifulSoup(primary_page, 'lxml')

    common_div_list = primary_page_soup.find_all('div', class_='card style_1')

    for common_div in common_div_list:
        h2_tag = common_div.find('h2')
        movie_page_link = base_url + h2_tag.find('a')['href']
        movie_html_data = requests.get(movie_page_link, headers=header).text
        movie_page_soup = BeautifulSoup(movie_html_data, 'lxml')
        poster_div = movie_page_soup.find('div', class_='header large border first')
        movie_n_div = poster_div.find('div', class_='title ott_false')
        movie_name = poster_div.find('h2').a.text
        movie_rating = poster_div.find('div', class_='user_score_chart')['data-percent']

        movie_genres = find_genres(poster_div)
        movie_release_date = poster_div.find('span', class_='release').text.strip()

        movie_runtime = get_runtime(poster_div)
        movie_director = find_director(poster_div)
        My_Dict = {
            'Name': movie_name,
            'Rating': movie_rating,
            'Genre': movie_genres,
            'Release date': movie_release_date[:-4],
            'Runtime': movie_runtime,
            'Director': movie_director,
            'URL': movie_page_link
        }
        movie_info_list.append(My_Dict)

table = pd.DataFrame(movie_info_list)
table.to_excel('Movie Data.xlsx')
