import requests
import lxml.html as html
import os
import datetime
import string

HOME_URL = "https://www.larepublica.pe"

XPATH_LINK_TO_ARTICLE = '//h2[@class="discover__headline"]/a/@href'
XPATH_TITLE = '//h1[@class="DefaultTitle"]/text()'
XPATH_SUMMARY = '//h2[@class="DefaultSubtitle"]/text()'
XPATH_BODY = '//section[@class="section-visibility"]/p/text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code ==200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                new_title = ''.join(filter(str.isalnum, title))
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
                print(new_title)
            except IndexError:
                return

            with open(f'{today}/{new_title}.txt', 'w', encoding = 'utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
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
            # print(links_to_notices)

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