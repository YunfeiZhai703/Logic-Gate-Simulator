import wx


class NumberInput(wx.SpinCtrl):
    def __init__(self, parent, value=0, min=0, max=100, step=1, size=wx.DefaultSize, onChange=None):
        wx.SpinCtrl.__init__(self, parent, id=wx.ID_ANY,
                             value=str(value), size=size, min=min, max=max)
        self.SetRange(min, max)
        self.SetIncrement(step)
        self.SetValue(value)

        if onChange:
            self.Bind(wx.EVT_SPINCTRL, onChange)
