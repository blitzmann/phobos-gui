import cPickle
import os.path
import sys

base_path = unicode(os.path.dirname(os.path.realpath(os.path.abspath(
            sys.argv[0]))), sys.getfilesystemencoding())

class SettingsProvider():
    BASE_PATH = base_path
    settings = {}
    _instance = None
    @classmethod
    def getInstance(cls):
        if cls._instance == None:
            cls._instance = SettingsProvider()

        return cls._instance

    def __init__(self):
        if not os.path.exists(self.BASE_PATH):
            os.mkdir(self.BASE_PATH)

    def getSettings(self, area, defaults=None):

        s = self.settings.get(area)
        if s is None:
            p = os.path.join(self.BASE_PATH, area)

            if not os.path.exists(p):
                info = {}
                if defaults:
                    for item in defaults:
                        info[item] = defaults[item]

            else:
                try:
                    f = open(p, "rb")
                    info = cPickle.load(f)
                    for item in defaults:
                        if item not in info:
                            info[item] = defaults[item]

                except:
                    info = {}
                    if defaults:
                        for item in defaults:
                            info[item] = defaults[item]

            self.settings[area] = s = Settings(p, info)

        return s

    def saveAll(self):
        for settings in self.settings.itervalues():
            settings.save()

class Settings():
    def __init__(self, location, info):
        self.location = location
        self.info = info

    def save(self):
        f = open(self.location, "wb")
        cPickle.dump(self.info, f, cPickle.HIGHEST_PROTOCOL)

    def __getitem__(self, k):
        try:
            return self.info[k]
        except KeyError:
            return None

    def __setitem__(self, k, v):
        self.info[k] = v

    def __iter__(self):
        return self.info.__iter__()

    def iterkeys(self):
        return self.info.iterkeys()

    def itervalues(self):
        return self.info.itervalues()

    def iteritems(self):
        return self.info.iteritems()

    def keys(self):
        return self.info.keys()

    def values(self):
        return self.info.values()

    def items(self):
        return self.info.items()


class PathSettings():
    _instance = None
    @classmethod
    def getInstance(cls):
        if cls._instance == None:
            cls._instance = PathSettings()

        return cls._instance

    def __init__(self):

        servicePathDefaultSettings = {
            "client_path": None,
            "dump_path": None
        }

        self.servicePathSettings = SettingsProvider.getInstance().getSettings("paths.settings", servicePathDefaultSettings)

    def get(self, type):
        return self.servicePathSettings[type]

    def set(self, type, value):
        self.servicePathSettings[type] = value

