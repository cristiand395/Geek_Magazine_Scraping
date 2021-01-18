import requests
import lxml.html as html
import os
import datetime


HOME_URL = 'https://www.xataka.com/'
XPATH_LINK_TO_ARTICLE = '//h2[@class="abstract-title"]/a/@href'
XPATH_TITLE = '//div[@class="article-header article-normal-header"]/header/h1/span/text()'
XPATH_BODY = '//div[@class="blob js-post-images-container"]/p[not(@class)]/text()'

def get_title(link):
    #Separate by "/" and get the last part 
    url = link.split('/')[-1]
    #Separate by "-" and delete last part
    title_list=url.split('-')[:-1]
    #Join the above
    title = " ".join(title_list)

    return(title)

def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = get_title(link)
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                print("as")
                return
            
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
            
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_notices:
                parse_notice(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()
    

if __name__ == "__main__":
    run()