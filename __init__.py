import shutil
import warnings

from PyQt5.QtWidgets import QAction, QMenu
from aqt import mw, QMessageBox, os



class ActionMenu(QMenu):
    def __init__(self):
        super(ActionMenu, self).__init__(mw)
        self.setTitle("获取每日一句")

        # create actions
        self.action_bbc_today_phrase = QAction("BBC - 今日短语", self)
        self.action_bing_daily_sentence = QAction("Bing - 每日一句", self)
        self.action_clear_cache = QAction("重置", self)

        # add to menu
        self.addAction(self.action_bbc_today_phrase)
        self.addAction(self.action_bing_daily_sentence)
        self.addSeparator()
        self.addAction(self.action_clear_cache)

        # connect
        self.action_bbc_today_phrase.triggered.connect(self.on_get_bbc_todays_phrase)
        self.action_bing_daily_sentence.triggered.connect(self.on_get_bing_daily_sentence)
        self.action_clear_cache.triggered.connect(self.on_reset_all)

    def _clear_user_files(self):
        from .Helpers import user_files
        shutil.rmtree(user_files, True)

    def on_get_bbc_todays_phrase(self):
        from .Services import Service
        self._clear_user_files()
        Service(mw).ImportBBCTodaysPhrases()

    def on_get_bing_daily_sentence(self):
        self._clear_user_files()
        from .Services import Service
        Service(mw).ImportBingSentence()

    def on_reset_all(self):
        mw.pm.profile['FirstTimeRun'] = True
        self._clear_user_files()
        QMessageBox.information(mw, "重置", "建议重启Anki.")

warnings.simplefilter("ignore")
mw.form.menuTools.addMenu(ActionMenu())
