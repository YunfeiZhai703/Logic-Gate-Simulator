import wx
from .colors import COLORS


class NumberInput(wx.SpinCtrl):
    """NumberInput is a component that allows the user to input a number."""

    def __init__(
            self,
            parent,
            value=0,
            min=0,
            max=100,
            step=1,
            size=wx.DefaultSize,
            onChange=None):
        wx.SpinCtrl.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            value=str(value),
            size=size,
            min=min,
            max=max,
            style=wx.SP_ARROW_KEYS)
        self.SetRange(min, max)
        # self.SetIncrement(step) TODO: check if this is works on Linux
        self.SetValue(value)
        dark = wx.SystemSettings.sys_appearance.IsDark()
        text_color = COLORS.WHITE if dark else COLORS.BLACK
        bg_color = COLORS.GRAY_400 if dark else COLORS.WHITE
        self.SetForegroundColour(text_color)
        self.SetBackgroundColour(bg_color)
        self.SetOwnBackgroundColour(bg_color)

        if onChange:
            self.Bind(wx.EVT_SPINCTRL, onChange)
