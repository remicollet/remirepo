pref("app.update.enabled", false);
pref("app.update.autoInstallEnabled", false);
# Allow users to set custom colors
# pref("browser.display.use_system_colors",   true);
pref("general.useragent.vendor", "Fedora");
pref("general.useragent.vendorSub", "THUNDERBIRD_RPM_VR");
pref("intl.locale.matchOS", true);
pref("mail.shell.checkDefaultClient", false);
pref("toolkit.networkmanager.disable", false);

# Make hyperlinks work
pref("network.protocol-handler.app.http", "COMMAND");
pref("network.protocol-handler.app.https", "COMMAND");
pref("network.protocol-handler.app.ftp", "COMMAND");

# Disable global indexing by default
pref("mailnews.database.global.indexer.enabled", false);

# Do not switch to Smart Folders after upgrade to 3.0b4
pref("mail.folder.views.version", "1")
