import wx


class Text(wx.StaticText):
    def __init__(self, parent, label, size=wx.DefaultSize, style=wx.ALIGN_CENTER):
        super().__init__(parent, label=label, size=size, style=style)
