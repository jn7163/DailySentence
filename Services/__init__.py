import datetime
from uuid import uuid4

from aqt import mw, os, QEventLoop, QObject, QMessageBox
from aqt.importing import importFile
from aqt.studydeck import StudyDeck

from ..Helpers.Importer import ImportToAnki
from .BBC import _phrase_getter
from .Bing import BingDict
from ..settings import settings

class Service(QObject):
    def __init__(self, parent):
        super(Service, self).__init__(parent)
        self.today_phrase_file = os.path.join(settings.user_files_folder, "{}.txt".format(uuid4().hex))
        self.check_first_time_run()

    def _ensureExists(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def check_first_time_run(self):
        is_first_time_run = mw.pm.profile.get('FirstTimeRun', True)
        if is_first_time_run:
            importFile(mw, settings.deck_template_file)
            mw.pm.profile['FirstTimeRun'] = False

    def start_progress(self, label=''):
        mw.progress.start(immediate=True)
        mw.app.processEvents(QEventLoop.ExcludeUserInputEvents)
        self.update_progress(label)

    def update_progress(self, label):
        mw.progress.update(label=label)

    def finish_progress(self):
        mw.progress.finish()

    def ImportBingSentence(self):
        bing = BingDict()

        text_file = os.path.join(self._ensureExists(settings.user_files_folder), "{}.txt".format(uuid4().hex))
        empty = True

        self.start_progress("获取Bing每日一句数据 ...")
        with open(text_file, "w", encoding='utf-8') as f:
            for _ in bing.DailySentences():
                (full_date, eng_sentence, chn_sentence, url) = _
                self.update_progress("{} ...".format(eng_sentence[:15]))
                f.write("\t".join(_) + "\n")
                empty = False
        self.finish_progress()
        if not empty:
            mw.progress.finish()
            ImportToAnki("Bing - 每日一句", self.import_deck_name, file=text_file)
            # importFile(mw, text_file)
        else:
            QMessageBox.information(mw, 'Bing每日一句', "没有数据.")

    def ImportBBCTodaysPhrases(self):
        today_date = datetime.date.today()
        thrs = []
        for minus_days in range(mw.addonManager.getConfig(__name__)['TodaysPhraseRecentDays']):
            _date = today_date + datetime.timedelta(days=0 - minus_days)
            thrs.append(_phrase_getter(_date.strftime("%y%m%d")))

        self.start_progress("正在从BBC获取数据...")

        for thr_index, thr in enumerate(thrs, 1):
            self.update_progress("正在获取今日短语 {}%".format(round((thr_index / thrs.__len__()) * 100, 2)))
            thr.run()

        self.finish_progress()

        # write to text

        phrase_file = os.path.join(self._ensureExists(settings.user_files_folder), "{}.txt".format(uuid4().hex))
        empty = True
        with open(phrase_file, "w", encoding='utf-8') as f:
            for thr in thrs:
                if thr.todays_phrase_data:
                    f.write("\t".join(thr.todays_phrase_data) + "\n")
                    empty = False
        if not empty:
            mw.progress.finish()
            ImportToAnki("BBC - 今日短语", self.import_deck_name, file=phrase_file)
        else:
            QMessageBox.information(mw, 'BBC每日短语', "没有数据.")

    @property
    def import_deck_name(self):

        ret = StudyDeck(
            mw, accept=_("Choose"),
            title=_("Choose Deck"), help="addingnotes",
            cancel=False, parent=mw, geomKey="selectDeck")

        if not ret.Accepted:
            return
        return ret.name
