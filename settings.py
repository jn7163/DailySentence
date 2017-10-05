from aqt import mw, os

this_addon_name = os.path.dirname(__file__)


class _settings:
    def _ensure_dir(self, name):
        if not os.path.isdir(name):
            os.makedirs(name)
        return name

    @property
    def profile_folder(self):
        return self._ensure_dir(mw.pm.profileFolder())

    @property
    def addons_folder(self):
        return self._ensure_dir(mw.addonManager.addonsFolder())

    @property
    def media_folder(self):
        return self._ensure_dir(os.path.join(self.profile_folder, "collection.media"))

    @property
    def this_addon_folder(self):
        return self._ensure_dir(mw.addonManager.addonsFolder(this_addon_name))

    @property
    def user_files_folder(self):
        return self._ensure_dir(os.path.join(self.this_addon_folder, "user_files"))

    @property
    def deck_template_file(self):
        return os.path.join(self.this_addon_folder, "Template.apkg")

    @property
    def addon_config(self):
        return mw.addonManager.getConfig(__name__)

    @property
    def config_file(self):
        return os.path.join(self.this_addon_folder, "config.json")


settings = _settings()

