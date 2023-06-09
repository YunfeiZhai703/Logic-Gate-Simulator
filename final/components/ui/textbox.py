import wx


class TextBox(wx.TextCtrl):
    """TextBox is a component that allows the user to input text."""

    def __init__(self, parent, value="", placeholder="", onChange=None,
                 onEnter=None,
                 size=wx.DefaultSize
                 ):
        """Initializes the TextBox component

        Args:
            parent (wiget): The parent widget
            value (str, optional): Inital value. Defaults to "".
            placeholder (str, optional): Placeholder text. Defaults to "".
            onChange (function, optional): Function to handle on change event. Defaults to None.
            onEnter (function, optional): Function to handle on enter event. Defaults to None.
            size (wxSize, optional): Size of component. Defaults to wx.DefaultSize.
        """
        wx.TextCtrl.__init__(self, parent, id=wx.ID_ANY,
                             value=value, size=size, style=wx.TE_PROCESS_ENTER)

        if onChange:
            self.Bind(wx.EVT_TEXT, onChange)
        if onEnter:
            self.Bind(wx.EVT_TEXT_ENTER, onEnter)

    def SetHint(self, placeholder):
        self.SetHint(placeholder)
