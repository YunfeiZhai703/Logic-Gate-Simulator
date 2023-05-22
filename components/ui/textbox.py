import wx


class TextBox(wx.TextCtrl):
    def __init__(self, parent, value="", placeholder="", onChange=None,
                 onEnter=None,
                 size=wx.DefaultSize
                 ):
        wx.TextCtrl.__init__(self, parent, id=wx.ID_ANY,
                             value=value, size=size, style=wx.TE_PROCESS_ENTER)

        if onChange:
            self.Bind(wx.EVT_TEXT, onChange)
        if onEnter:
            self.Bind(wx.EVT_TEXT_ENTER, onEnter)

    def SetHint(self, placeholder):
        self.SetHint(placeholder)
