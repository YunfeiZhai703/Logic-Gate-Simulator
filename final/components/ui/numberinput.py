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
        self.SetForegroundColour(COLORS.GREEN_600)

        if onChange:
            self.Bind(wx.EVT_SPINCTRL, onChange)
