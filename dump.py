import wx
import sys
import thread_utils
from flow import FlowManager
from miner import *
from translator import Translator
from writer import *


class RedirectText(object):
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        self.out.WriteText(string)


class PhobosThread(thread_utils.ThreadWithExc):
    def __init__(self, rvr, dump_path):
        thread_utils.ThreadWithExc.__init__(self)
        self.rvr = rvr
        self.dump_path = dump_path

    def run(self):
        pickle_miner = ResourcePickleMiner(self.rvr)
        trans = Translator(pickle_miner)
        bulkdata_miner = BulkdataMiner(self.rvr, trans)
        staticcache_miner = StaticdataCacheMiner(self.rvr.paths.root, trans)

        miners = (
            MetadataMiner(self.rvr.paths.root),
            bulkdata_miner,
            TraitMiner(staticcache_miner, bulkdata_miner, trans),
            SqliteMiner(self.rvr.paths.root, trans),
            staticcache_miner,
            #CachedCallsMiner(self.rvr, trans),  # doesn't work?
            pickle_miner)

        writers = (
            JsonWriter(self.dump_path, indent=2),)

        try:
            FlowManager(miners, writers).run("", "multi")
        except KeyboardInterrupt:
            pass

        print "\n== Done! =="


class PhobosDump(wx.Frame):
    def __init__(self, parent, rvr, dump_path):
        wx.Frame.__init__(self, parent, wx.ID_ANY, "Dumping...", size=wx.Size(400, 400))
        self.rvr = rvr
        self.dump_path = dump_path

        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        log = wx.TextCtrl(panel, wx.ID_ANY, size=(300, 200),
                          style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)

        # Add widgets to a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(log, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.Centre(wx.BOTH)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # redirect text here
        redir = RedirectText(log)
        self.old_stdout = sys.stdout
        sys.stdout = redir

        self.thread = PhobosThread(self.rvr, self.dump_path)
        self.thread.daemon = True
        self.thread.start()

    def OnClose(self, event):
        # We pass KeyboardInterrupt as Phobos is specifically designed to
        # kill itself in this case. A regular Exception, or any subclass,
        # will simply tell Phobos to log the particular iteration as failed
        # and continue with the next iteration
        self.thread.raiseExc(KeyboardInterrupt)
        sys.stdout = self.old_stdout
        self.Destroy()
