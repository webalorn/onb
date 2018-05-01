import onb, os

_settingsFile = os.path.join(os.path.dirname(__file__), 'settings.yml')
onb.OnbSettings.loadFrom(_settingsFile)