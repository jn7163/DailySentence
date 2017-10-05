import datetime

import bs4
from aqt import mw
from requests import Session

daily_sentence_url_pattern = "http://bingdict.chinacloudsites.cn/dailysentence/{year}/{month}/{full_date}.html"


class BingDict(Session):
    def __init__(self):
        super(BingDict, self).__init__()

    def _form_parameters(self, date):
        """

        :param date:
        :type date: datetime.date
        :return:
        """
        rValues = []
        for minus_days in range(mw.addonManager.getConfig(__name__)['DailySentenceMax']):
            _date = date + datetime.timedelta(days=0 - minus_days)
            year = _date.strftime("%Y")
            month = _date.strftime("%m")
            full_date = _date.strftime("%Y%m%d")
            rValues.append([year, month, full_date])
        return rValues

    def DailySentences(self):
        """

        :return: (English Sentence, Chinese Translation)
        :rtype: tuple
        """

        sentences = []
        for year, month, full_date in self._form_parameters(datetime.date.today()):
            url = daily_sentence_url_pattern.format(
                year=year, month=month, full_date=full_date
            )
            rsp = self.request("get", url)
            if rsp.status_code != 200:
                continue
            bs = bs4.BeautifulSoup(rsp.content.decode("utf-8", "ignore"), 'html.parser')
            eng_sentence = bs.find("p", id="Eng_label").text
            chn_sentence = bs.find("p", id="Chn_label").text
            yield full_date, eng_sentence, chn_sentence, url
