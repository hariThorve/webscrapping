
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(0.5)
driver.maximize_window()

company_list = []
btn_list = []
div_no = 20

for i in range(1, 9):
    div_no = 20

    driver.get(f"https://www.trustpilot.com/categories/music_movies?page={i}")
    html_data = driver.page_source
    soup = BeautifulSoup(html_data, 'lxml')
    all_main_div = soup.find_all('div',class_='paper_paper__29o4A card_card__2F_07 card_noPadding__1tkWv styles_wrapper__2QC-c styles_businessUnitCard__1-z5m')
    btn_count = 1
    if i == 1:
        div_no = 14
    elif i == 8:
        div_no = 12
    driver.execute_script("window.scrollTo(0, window.scrollY + 150)")
    for main_div in all_main_div[:div_no]:
        driver.execute_script("window.scrollTo(0, window.scrollY + 175)")
        if i == 1:
            link = driver.find_element('xpath', f'//*[@id="__next"]/div/main/div/div[2]/section/div[2]/div[2]/div[{btn_count}]/div[2]/div/span/button')
            driver.execute_script("arguments[0].click();", link)
        elif i > 1:
            link = driver.find_element('xpath',
                                        f'//*[@id="__next"]/div/main/div/div[2]/section/div[3]/div[{btn_count}]/div[2]/div/span/button')
            driver.execute_script("arguments[0].click();", link)
        # driver.execute_script("arguments[0].click();", link)

        btn_count = btn_count + 1

        html_data = driver.page_source
        soup = BeautifulSoup(html_data, 'lxml')


        company_name = main_div.find('p', class_='typography_typography__23IQz typography_h4__IhMYK typography_weight-heavy__36UHe typography_fontstyle-normal__1_HQI styles_displayName__1LIcI').text

        try:
            main_tag = main_div.find('p', class_='typography_typography__23IQz typography_bodysmall__24hZa typography_color-gray-7__2eGCj typography_weight-regular__iZYoT typography_fontstyle-normal__1_HQI styles_ratingText__nheL7').text

            reviews = main_tag[15:-8]
            trustscore = main_tag[11:14]
        except AttributeError:
            reviews = "0"
            trustscore = "0"

        tooltip_div = soup.find('div', class_='tooltip_tooltip__3qWEC')
        ul = tooltip_div.find('ul', class_='styles_list__2_BIw')
        tooltip_div_li = ul.find_all('li', class_='styles_item__3UwLI')
        website_name = ""
        location = ""
        count = 1
        for li in tooltip_div_li:
            if count == 1:
                website_name = li.text
                count = count + 1
            elif count == 2:
                location = li.text
        if location == "":
            location = 'None'
        myDict = {
            'Name': company_name,
            'Trust Score': trustscore,
            'Total reviews': reviews,
            'Website name': website_name,
            'Location': location
        }
        company_list.append(myDict)

df = pd.DataFrame(company_list)
df.index += 1
df.to_excel('Music and Movies.xlsx')

print(df.isnull().sum())