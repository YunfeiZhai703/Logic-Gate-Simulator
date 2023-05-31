"""Implement the graphical user interface for the Logic Simulator.

Used in the Logic Simulator project to enable the user to run the simulation
or adjust the network properties.

Classes:
--------
MyGLCanvas - handles all canvas drawing operations.
Gui - configures the main window and all the widgets.
"""
import math
import random
from typing import List
import wx


from names import Names
from devices import Device, Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
from parse import Parser
from components.ui import Button, Text, NumberInput, TextBox, COLORS
from components import Canvas, FileButton, Box, ScrollBox
from errors import Error


class Notebook(wx.Notebook):
    def __init__(self, parent, devices, monitors):
        super().__init__(parent, style=wx.NB_FIXEDWIDTH)
        self.canvas = Canvas(self, devices, monitors)
        self.file_path = ""
        self.uploaded_code = ""
        self.SetBackgroundColour(COLORS.GRAY_400)


class Gui(wx.Frame):
    # notebook

    def __init__(self, title, path, names, devices, network, monitors):
        super().__init__(parent=None, title=title, size=(800, 600))

        nb = Notebook(self, devices, monitors)
        self.nb = nb

        nb.file_path = path
        nb.uploaded_code = self._read_file(nb.file_path)
        nb.AddPage(MainPage(devices,
                   network, monitors, notebook=nb), "Main")

        nb.AddPage(nb.canvas, "Graphs")
        nb.AddPage(CodePage(nb), "Code")

        self.setup_menu()

        self.Show()

    def _read_file(self, path):
        """Read the file specified by path."""
        try:
            with open(path, "r") as file:
                return file.read()
        except FileNotFoundError:
            return "No Code Uploded"

    def setup_menu(self):
        fileMenu = wx.Menu()
        menuBar = wx.MenuBar()
        fileMenu.Append(wx.ID_EXIT, "&Exit")
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.on_menu)

    def print_code(self, event):
        print(self.nb.uploaded_code)

    def on_menu(self, event):
        """Handle the event when the user selects a menu item."""
        Id = event.GetId()
        if Id == wx.ID_EXIT:
            self.Close(True)


class ErrorsGui(wx.Frame):
    def __init__(self, errors: List[Error]):
        super().__init__(parent=None, title="Errors", size=(800, 600))
        self.SetBackgroundColour(COLORS.RED_900)
        self.setup_menu()
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        scroll_box = ScrollBox(
            self,
            bg_color=COLORS.RED_900,
            dir="col")

        main_sizer.Add(
            Button(
                self,
                "Close",
                size="md",
                color=COLORS.RED_700,
                onClick=lambda event: self.Close(True)), 0, wx.ALIGN_CENTER, 20

        )

        for error in errors[0:5]:  # only show first 5 errors
            scroll_box.Add(
                Text(
                    scroll_box,
                    str(error),
                    font_family="modern",
                    style=wx.ALIGN_LEFT),
                0,
                wx.EXPAND,
                5)

        scroll_box.Attach(
            main_sizer,
            1,
            wx.EXPAND,
            20)

        self.SetSizer(main_sizer)

        self.Show()

    def setup_menu(self):
        fileMenu = wx.Menu()
        menuBar = wx.MenuBar()
        fileMenu.Append(wx.ID_EXIT, "&Exit")
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.on_menu)

    def on_menu(self, event):
        """Handle the event when the user selects a menu item."""
        Id = event.GetId()
        if Id == wx.ID_EXIT:
            self.Close(True)


class MainPage(wx.Panel):

    def __init__(
            self,
            devices: Devices,
            network: Network,
            monitors: Monitors,
            notebook: Notebook):
        """Initialise widgets and layout."""
        super().__init__(parent=notebook)

        self.network = network
        self.monitors = monitors

        self.SetBackgroundColour(COLORS.GRAY_950)
        self.number_of_cycles = 5
        self.cycles_completed = 0

        # Configure sizers for layout
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer = Box(self, dir="col")

        self.canvas = Canvas(right_sizer, devices, monitors)
        self.canvas2 = notebook.canvas

        Heading(self, notebook).Attach(left_sizer, 0, wx.EXPAND, 5)

        DevicesPanel(self, devices).Attach(
            left_sizer, 5, wx.EXPAND | wx.ALL, 5)
        SwitchesPanel(self, devices).Attach(
            left_sizer, 3, wx.EXPAND | wx.ALL, 5)

        right_sizer.Add(self.canvas,
                        3, wx.EXPAND | wx.ALL, 5)

        right_bottom_block = Box(
            right_sizer, dir="row")

        right_sizer.Add(right_bottom_block, 1, wx.EXPAND, 5)

        MonitorsPanel(
            right_bottom_block,
            devices,
            monitors,
            [self.canvas, self.canvas2],
            self.cycles_completed).Attach(
            right_bottom_block,
            1,
            wx.ALL,
            5)

        ConfigurationPanel(
            right_bottom_block,
            self.on_run,
            self.on_reset,
            self.on_number_input).Attach(
            right_bottom_block,
            1,
            wx.EXPAND,
            5)

        main_sizer.Add(left_sizer, 2, wx.ALL, 5)
        main_sizer.Add(right_sizer, 5, wx.EXPAND | wx.ALL, 5)

        self.SetSizeHints(600, 600)
        self.SetSizer(main_sizer)

    def on_run(self, event):

        for _ in range(self.number_of_cycles):
            self.network.execute_network()
            self.monitors.record_signals()

        monitors_dict = self.monitors.monitors_dictionary
        signal_names = self.monitors.get_signal_names()[0]

        # get a list of montiors_dict values
        monitored_signals = list(monitors_dict.values())

        for i, signal in enumerate(monitored_signals):
            self.canvas.add_signal(
                signal, signal_names[i], self.cycles_completed)
            self.canvas2.add_signal(
                signal, signal_names[i], self.cycles_completed)

        self.canvas.Refresh()
        self.canvas2.Refresh()
        self.cycles_completed += self.number_of_cycles

    def on_reset(self, event):
        self.canvas.reset()
        self.canvas2.reset()

        self.canvas.Refresh()
        self.canvas2.Refresh()

        self.cycles_completed = 0

    def on_number_input(self, event):
        """Handle the event when the user changes the spin control value."""
        self.number_of_cycles = event.GetInt()


class Heading(wx.BoxSizer):
    def __init__(self, parent, notebook: wx.Notebook):
        """Initialise the heading."""
        super().__init__(wx.HORIZONTAL)

        self.Add(
            Button(parent, "Logic Simulator", size="md",
                   color=wx.RED,
                   onClick=self.on_click
                   ), 1, wx.ALL, 5)

        self.Add(FileButton(parent, notebook), 1, wx.ALL, 5)

    def Attach(self, parent: wx.BoxSizer, proportion, flag, border):
        """Attach the heading to the parent."""
        parent.Add(self, proportion, flag, border)

    def on_click(self, event):
        wx.MessageBox(
            "Logic Simulator\nTeam 19 - Lakee, Dhillon, Yunfei\n2023",
            "About Logsim",
            wx.ICON_INFORMATION | wx.OK)


class DevicesPanel(ScrollBox):
    def __init__(self, parent, devices: Devices):
        """Initialise the devices panel."""
        super().__init__(parent, dir="col")
        self.Add(Text(self, "Devices"), 0, wx.ALL, 5)
        self.parent = parent
        self.device_list: List[Device] = devices.devices_list

        cols = 2
        rows = math.ceil(len(self.device_list) / cols)

        grid = wx.GridSizer(rows, cols, 10, 10)

        for device in self.device_list:
            grid.Add(
                Button(
                    self,
                    device.name,
                    onClick=self.on_click),
                0,
                wx.EXPAND,
                5)

        self.Add(grid, 5, wx.EXPAND, 5)

        self.SetSizeHints(200, 200)

    def on_click(self, event):
        device_name = event.GetEventObject().GetLabel()
        device = [dev for dev in self.device_list if dev.name == device_name][0]
        wx.MessageBox(
            str(device),
            device_name,
            wx.ICON_INFORMATION | wx.OK)


class SwitchesPanel(ScrollBox):
    def __init__(self, parent, devices: Devices):
        """Initialise the devices panel."""
        super().__init__(parent, dir="col")
        self.Add(Text(self, "Switches"), 0, wx.ALL, 5)
        self.parent = parent
        self.device_list: List[Device] = devices.devices_list
        self.switches: List[Device] = []

        for device in self.device_list:
            if device.device_kind == devices.SWITCH:
                self.switches.append(device)

        cols = 2
        rows = math.ceil(len(self.switches) / cols)

        grid = wx.GridSizer(rows, cols, 10, 10)

        for i, switch in enumerate(self.switches):
            switch_id = switch.device_id
            output_value = switch.switch_state

            color = COLORS.GREEN_900 if output_value == 1 else COLORS.RED

            button = Button(
                self,
                str(switch.name).split(":")[1],
                color=color,
                onClick=lambda event: self.on_switch_toggle(event, devices)
            )

            grid.Add(button, 0, wx.EXPAND, 5)

        self.Add(grid, 5, wx.EXPAND, 5)

        self.SetSizeHints(200, 200)

    def on_switch_toggle(
            self,
            event,
            devices: Devices):

        switch_name = "SWITCH:" + event.GetEventObject().GetLabel()

        switch_id = [
            switch.device_id for switch in self.switches if switch.name == switch_name][0]

        switch = devices.get_device(switch_id)

        if switch is None:
            return
        output_value = switch.switch_state
        new_output_value = 0 if output_value == 1 else 1
        devices.set_switch(switch_id, new_output_value)

        switch = devices.get_device(switch_id)

        event.GetEventObject().SetColor(
            COLORS.GREEN_900 if new_output_value == 1 else COLORS.RED)


class MonitorsPanel(ScrollBox):
    def __init__(
            self,
            parent,
            devices: Devices,
            monitors: Monitors,
            canvases: List[Canvas],
            cycles_completed):
        """Initialise the devices panel."""
        super().__init__(parent, dir="col")
        self.Add(Text(self, "Montiors"), 0, wx.ALL, 5)
        self.parent = parent
        self.device_list: List[Device] = devices.devices_list
        self.signal_names = monitors.get_signal_names()

        cols = 2
        rows = math.ceil(
            len(self.signal_names[0]) + len(self.signal_names[1]) / cols)

        grid = wx.GridSizer(rows, cols, 10, 10)

        for i, output in enumerate(self.signal_names[0]):

            button = Button(
                self,
                str(output),
                color=COLORS.GREEN_900,
                onClick=lambda event: self.on_switch_toggle(
                    event,
                    monitors,
                    canvases,
                    cycles_completed))

            grid.Add(button, 0, wx.EXPAND, 5)

        for i, output in enumerate(self.signal_names[1]):

            button = Button(
                self,
                str(output),
                color=COLORS.RED,
                onClick=lambda event: self.on_switch_toggle(
                    event,
                    monitors,
                    canvases,
                    cycles_completed))

            grid.Add(button, 0, wx.EXPAND, 5)

        self.Add(grid, 5, wx.EXPAND, 5)

        self.SetSizeHints(200, 200)

    def on_switch_toggle(
            self,
            event,
            monitors: Monitors, canvases: List[Canvas], cycles_completed):

        port_name = event.GetEventObject().GetLabel()
        monitors.toggle_monitor(port_name, cycles_completed)

        self.signal_names = monitors.get_signal_names()

        is_monitored = port_name in self.signal_names[0]

        if not is_monitored:
            for canvas in canvases:
                canvas.remove_signal(port_name)

        event.GetEventObject().SetColor(
            COLORS.GREEN_900 if is_monitored else COLORS.RED)


class ConfigurationPanel(Box):
    def __init__(
        self,
        parent,
        on_run,
        on_reset, on_number_input
    ):
        """Initialise the devices panel."""
        super().__init__(parent, dir="col")
        self.parent = parent

        self.Add(Text(self, "Configuration"), 0, wx.ALL, 5)

        cycles_input = Box(self, dir="row")
        cycles_input.Add(Text(cycles_input, "Number of Cycles",
                         style=wx.ALIGN_LEFT), 2, wx.ALL, 20)

        cycles_input.Add(NumberInput(
            cycles_input, value=5, onChange=on_number_input), 2, wx.ALL, 20)

        self.Add(cycles_input, 0, wx.CENTER, 10)

        buttons = Box(self, dir="row")

        buttons.Add(Button(buttons, "Run",
                           onClick=on_run,
                           color=COLORS.GREEN_950,
                           size="md"), 0, wx.ALL, 5)
        buttons.Add(Button(buttons, "Reset",
                           onClick=on_reset,
                           color=COLORS.RED,
                           size="md"), 0, wx.ALL, 5)

        self.Add(buttons, 0, wx.CENTER, 20)


class CodePage(ScrollBox):
    def __init__(self, parent: Notebook):
        super().__init__(parent, dir="col")
        self.parent = parent
        self.code = parent.uploaded_code

        self.Add(Text(self, self.code, style=wx.ALIGN_LEFT,
                 font_family="modern"), 0, wx.ALL, 5)

        # update the text when the parent's uploaded code changes
        parent.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_page_changed)

    def on_page_changed(self, event):
        """Handle the event when the user changes the page."""
        self.code = self.parent.uploaded_code
        self.GetChildren()[0].SetLabel(self.code)
