import sys
import os
sys.path.insert(0, 'Phobos.zip')

if not hasattr(sys, 'frozen'):
    if sys.version_info < (2,6) or sys.version_info > (3,0):
        print("Requires python 2.x branch ( >= 2.6 )\nExiting.")
        sys.exit(1)

    try:
        import wxversion
    except ImportError:
        print("Cannot find wxPython\nYou can download wxPython (2.8) from http://www.wxpython.org/")
        sys.exit(1)
    try:
        wxversion.select('2.8')
    except wxversion.VersionError:
        try:
            wxversion.ensureMinimal('2.8')
        except wxversion.VersionError:
            print("Installed wxPython version doesn't meet requirements.\nYou can download wxPython (2.8) from http://www.wxpython.org/")
            sys.exit(1)
        else:
            print("wxPython 2.8 not found; attempting to use newer version, expect errors")

    try:
        import reverence
    except ImportError:
        print("Cannot find reverence\nYou can download it from https://github.com/ntt/reverence")
        sys.exit(1)

if __name__ == "__main__":
    # Import everything
    import wx
    import mainframe
    import reverence
    gui = wx.App(False)
    mainframe.MainFrame()
    gui.MainLoop()
