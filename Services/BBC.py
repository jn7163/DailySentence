import re
from threading import Thread

import bs4
from aqt import pyqtSignal
from requests import Session


# from ..Helpers import *


class url_patterns:
    todays_phrase = "http://www.bbc.co.uk/learningenglish/chinese/features/todays-phrase/ep-{date}"  # 170928


today_phrase_index = 'http://www.bbc.co.uk/learningenglish/chinese/features/todays-phrase'


class _phrase_getter(Thread):
    Complete = pyqtSignal(list)

    def __init__(self, date_str):
        super(_phrase_getter, self).__init__()
        self.date_str = date_str
        self.todays_phrase_data = []

    def run(self):
        url = url_patterns.todays_phrase.format(date=self.date_str)

        s = Session()

        rsp = s.get(url, )
        if rsp.status_code == 200:
            soup = bs4.BeautifulSoup(rsp.content.decode('utf-8', 'ignore'), 'html.parser')

            phrase_line = soup.find_all('h3', dir='ltr')[1].text
            first_chinese = re.search('[\u4e00-\u9fa5]', phrase_line).group()

            phrase_eng = phrase_line.split(first_chinese)[0].strip()
            phrase_chn = first_chinese + (phrase_line.split(first_chinese)[1].strip())

            contents = soup.find_all("p", attrs={"class": "NewsReport"})
            jiang_je = contents[0].text

            self.todays_phrase_data.append(phrase_eng)
            self.todays_phrase_data.append(phrase_chn)
            self.todays_phrase_data.append(jiang_je)

            for content in contents[1:]:
                eng, chn = content.text.split(".")
                self.todays_phrase_data.append(eng)
                self.todays_phrase_data.append(chn)

            self.todays_phrase_data.append(url)
