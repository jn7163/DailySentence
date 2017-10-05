from aqt import mw, os

anki_addons_folder = mw.addonManager.addonsFolder()
anki_media_folder = os.path.join(mw.pm.profileFolder(), "collection.media")
this_addon_folder = mw.addonManager.addonsFolder("DailySentence")
if not os.path.isdir(this_addon_folder):
    this_addon_folder = mw.addonManager.addonsFolder("1004445081")
user_files = os.path.join(this_addon_folder, "user_files")
if not os.path.isdir(user_files):
    os.makedirs(user_files)
TemplatePackage = os.path.join(this_addon_folder, "Template.apkg")
