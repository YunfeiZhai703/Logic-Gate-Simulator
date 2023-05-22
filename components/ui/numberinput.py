import wx
from .colors import COLORS


class NumberInput(wx.SpinCtrl):
    def __init__(self, parent, value=0, min=0, max=100, step=1, size=wx.DefaultSize, onChange=None):
        wx.SpinCtrl.__init__(self, parent, id=wx.ID_ANY,
                             value=str(value), size=size, min=min, max=max, style=wx.SP_ARROW_KEYS)
        self.SetRange(min, max)
        self.SetIncrement(step)
        self.SetValue(value)

        self.SetForegroundColour(COLORS.GRAY_100)
        self.SetBackgroundColour(COLORS.GRAY_900)
        self.SetOwnBackgroundColour(COLORS.GRAY_900)

        if onChange:
            self.Bind(wx.EVT_SPINCTRL, onChange)
