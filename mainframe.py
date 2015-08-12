import os
import wx
import sys
import settings
import reverence.blue
from dump import PhobosDump

class MainFrame(wx.Frame):
    __instance = None

    @classmethod
    def getInstance(cls):
        return cls.__instance if cls.__instance is not None else MainFrame()

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Phobos-GUI", size=wx.Size(550, 400))

        MainFrame.__instance = self
        self.settings = settings.PathSettings.getInstance()

        #Fix for msw (have the frame background color match panel color
        if 'wxMSW' in wx.PlatformInfo:
            self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        server_radio_boxChoices = [u"Tranquility", u"Singularity", u"Duality", u"Serenity"]
        self.server_radio_box = wx.RadioBox(self, wx.ID_ANY, u"Server", wx.DefaultPosition, wx.DefaultSize, server_radio_boxChoices, 4, wx.RA_SPECIFY_COLS)
        self.server_radio_box.SetSelection(0)
        main_sizer.Add(self.server_radio_box, 0, wx.ALL, 5)

        self.st_client = wx.StaticText(self, wx.ID_ANY, u"EVE Client Directory", wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_client.Wrap(-1)
        main_sizer.Add(self.st_client, 0, wx.ALL, 5)

        self.client_picker = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select EVE Client Directory", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST)
        main_sizer.Add(self.client_picker, 0, wx.ALL | wx.EXPAND, 5)

        self.st_cache = wx.StaticText(self, wx.ID_ANY, u"Cache Directory", wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_cache.Wrap(-1)
        main_sizer.Add(self.st_cache, 0, wx.ALL, 5)

        self.cache_picker = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select Cache Directort", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST)
        main_sizer.Add(self.cache_picker, 0, wx.ALL | wx.EXPAND, 5)

        self.st_res = wx.StaticText(self, wx.ID_ANY, u"Shared Resource Directory", wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_res.Wrap(-1)
        main_sizer.Add(self.st_res, 0, wx.ALL, 5)

        self.res_picker = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select Shared Resource Directory", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST)
        main_sizer.Add(self.res_picker, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticline2 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        main_sizer.Add(self.m_staticline2, 0, wx.EXPAND | wx.ALL, 5)

        self.st_dump = wx.StaticText(self, wx.ID_ANY, u"Phobos Dump Directory", wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_dump.Wrap(-1)
        main_sizer.Add(self.st_dump, 0, wx.ALL, 5)

        self.dump_picker = wx.DirPickerCtrl(self, wx.ID_ANY, self.settings.get('dump_path') or wx.EmptyString, u"Select Phobos Dump Directory", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE)
        main_sizer.Add(self.dump_picker, 0, wx.ALL | wx.EXPAND, 5)

        m_sdbSizer1 = wx.StdDialogButtonSizer()
        self.m_sdbSizer1OK = wx.Button(self, wx.ID_OK, "Start Dump")
        m_sdbSizer1.AddButton(self.m_sdbSizer1OK)
        m_sdbSizer1.Realize()

        main_sizer.Add(m_sdbSizer1, 0, wx.EXPAND, 5)

        self.SetSizer(main_sizer)
        self.Layout()

        self.set_eve_paths()
        self.check_btn()

        self.Centre(wx.BOTH)
        self.Show()
        # Connect Events
        self.server_radio_box.Bind(wx.EVT_RADIOBOX, self.server_changed)
        self.client_picker.Bind(wx.EVT_DIRPICKER_CHANGED, self.set_eve_paths)
        self.dump_picker.Bind(wx.EVT_DIRPICKER_CHANGED, self.set_dump_path)
        self.m_sdbSizer1OK.Bind(wx.EVT_BUTTON, self.process_dump)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def check_btn(self):
        if self.settings.get('dump_path') and self.settings.get('client_path'):
            self.m_sdbSizer1OK.Enable()
        else:
            self.m_sdbSizer1OK.Disable()

    def restrict(self, bool):
        if bool:
            self.cache_picker.SetPath("")
            self.cache_picker.Disable()
            self.res_picker.SetPath("")
            self.res_picker.Disable()
            self.m_sdbSizer1OK.Disable()
        else:
            self.client_picker.SetPath(self.rvr.paths.root)
            self.cache_picker.SetPath(self.rvr.paths.cache)
            self.cache_picker.Enable()
            self.res_picker.SetPath(self.rvr.paths.sharedcache)
            self.res_picker.Enable()
            self.check_btn()

    def set_eve_paths(self, event=None):
        """
        Sets paths based on EVE client path (either through user selection
        or from settings)
        """
        path = event.Path if event else self.settings.get('client_path')
        try:
            self.rvr = reverence.blue.EVE(path, server=self.server_radio_box.GetStringSelection().lower())
            self.restrict(False)
            self.settings.set('client_path', path)
        except:
            # exception is raise if we don't have a correct path
            if event:
                event.EventObject.SetPath("Invalid EVE Installation")
            self.restrict(True)

    def set_dump_path(self, event):
        """ Sets dump path """
        if os.access(event.Path, os.W_OK | os.X_OK):
            self.settings.set('dump_path', event.Path)
        else:
            self.dump_picker.SetPath("Can't access directory")
        self.check_btn()

    def server_changed(self, event):
        """ When user changes server, reset paths """
        self.set_eve_paths()

    def process_dump(self, event):
        PhobosDump(self, self.rvr, self.settings.get('dump_path')).Show()

    def OnClose(self, event):
        settings.SettingsProvider.getInstance().saveAll()
        event.Skip()
