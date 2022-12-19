# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401from typing import List  # noqa: F401

mod = "mod4"              # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"      # My terminal of choice
myBrowser = "firefox" # My terminal of choice

keys = [
         ### The essentials
         Key([mod], "Return",
             lazy.spawn(myTerm+" -e fish"),
             desc='Launches My Terminal'
             ),
         Key([mod], "space",
             lazy.spawn("dmenu_run -p 'Run: '"),
             desc='Run Launcher'
             ),
         Key([mod], "b",
             lazy.spawn(myBrowser),
             desc='Qutebrowser'
             ),
         Key([mod], "Tab",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod, "shift"], "c",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "r",
             lazy.restart(),
             desc='Restart Qtile'
             ),
         Key([mod, "shift"], "q",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         Key(["control", "shift"], "e",
             lazy.spawn("emacsclient -c -a emacs"),
             desc='Doom Emacs'
             ),
         ### Switch focus to specific monitor (out of three)
         Key([mod], "w",
             lazy.to_screen(0),
             desc='Keyboard focus to monitor 1'
             ),
         Key([mod], "e",
             lazy.to_screen(1),
             desc='Keyboard focus to monitor 2'
             ),
         Key([mod], "r",
             lazy.to_screen(2),
             desc='Keyboard focus to monitor 3'
             ),
         ### Switch focus of monitors
         Key([mod], "period",
             lazy.next_screen(),
             desc='Move focus to next monitor'
             ),
         Key([mod], "comma",
             lazy.prev_screen(),
             desc='Move focus to prev monitor'
             ),
         ### Treetab controls
          Key([mod, "shift"], "h",
             lazy.layout.move_left(),
             desc='Move up a section in treetab'
             ),
         Key([mod, "shift"], "l",
             lazy.layout.move_right(),
             desc='Move down a section in treetab'
             ),
         ### Window controls
         Key([mod], "j",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "k",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod, "shift"], "j",
             lazy.layout.shuffle_down(),
             lazy.layout.section_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "k",
             lazy.layout.shuffle_up(),
             lazy.layout.section_up(),
             desc='Move windows up in current stack'
             ),
         Key([mod], "h",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key([mod], "l",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
         Key([mod], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),
         Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
         Key([mod, "shift"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
         Key([mod], "f",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),
         ### Stack controls
         Key([mod, "shift"], "Tab",
             lazy.layout.rotate(),
             lazy.layout.flip(),
             desc='Switch which side main pane occupies (XmonadTall)'
             ),
          Key([mod, "shift"], "space",
             lazy.layout.next(),
             desc='Switch window focus to other pane(s) of stack'
             ),
 #        Key([mod, "shift"], "space",
 #            lazy.layout.toggle_split(),
 #            desc='Toggle between split and unsplit sides of stack'
 #            ),
         # Dmenu scripts launched using the key chord SUPER+p followed by 'key'
]


groups = [Group("DEV", layout='monadtall'),
          Group("WWW", layout='monadtall'),
          Group("SYS", layout='monadtall'),
          Group("SYS", layout='monadtall'),
          Group("DOC", layout='monadtall'),
          Group("VBOX", layout='monadtall'),
          Group("CHAT", layout='monadtall'),
          Group("MUS", layout='monadtall'),
          Group("VID", layout='monadtall'),
          Group("GFX", layout='floating')]

# Allow MODKEY+[0 through 9] to bind to groups, see https://docs.qtile.org/en/stable/manual/config/groups.html
# MOD4 + index Number : Switch to Group[index]
# MOD4 + shift + index Number : Send active window to another Group
from libqtile.dgroups import simple_key_binder
dgroups_key_binder = simple_key_binder("mod4")

layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": "#0066ff",
                "border_normal": "#222222"
                }

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    layout.Floating(**layout_theme)
]

#color scheme dict for widget list
c = {
    "bg": "#000000",
    "fg": "d0d0d0",
    "black": "#000000",
    "gray": "#808080",
    "red": "#ff0000",
    "green": "33ff00",
    "pink": "ff0099",
    "blue": "#0066ff",
    "purple": "#cc00ff",
    "cyan": "#00ffff",
    "light gray": "#d0d0d0",
    "white": "#ffffff",
    "bpgrad": ["#444444", "#222222"]
}

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font=" Ubuntu Bold ",
    fontsize = 14,
    padding = 2,
    background=c["bpgrad"]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = c["white"],
                       background = c['bpgrad']
                       ),
              widget.TextBox(
                       text = '',
                       font = "Go Mono Nerd Font",
                       background = c["bpgrad"],
                       foreground = c['cyan'],
                       padding = 6,
                       fontsize = 18
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = c["white"],
                       background = c["bpgrad"]
                       ),
              widget.GroupBox(
                       font = "Ubuntu Bold",
                       fontsize = 12,
                       margin_y = 4,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = c["red"],
                       inactive = c["cyan"],
                       rounded = True,
                       highlight_color = c["gray"],
                       highlight_method = "line",
                       this_current_screen_border = c['cyan'],
                       this_screen_border = c['black'],
                       other_current_screen_border = c['cyan'],
                       other_screen_border = c['black'],
                       foreground = c["white"],
                       background = c["bpgrad"]
                       ),
             widget.TextBox(
                       text = '|',
                       font = "Ubuntu Mono",
                       background = c["bpgrad"],
                       foreground = c['pink'],
                       padding = 2,
                       fontsize = 18
                       ),
              widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = c['blue'],
                       background = c["bpgrad"],
                       padding = 0,
                       scale = 0.7
                       ),
              widget.CurrentLayout(
                       foreground = c['blue'],
                       background = c["bpgrad"],
                       padding = 5
                       ),
             widget.TextBox(
                       text = '|',
                       font = "Ubuntu Mono",
                       background = c["bpgrad"],
                       foreground = c['pink'],
                       padding = 2,
                       fontsize = 18
                       ),
              widget.WindowName(
                       foreground = c['blue'],
                       background = c["bpgrad"],
                       padding = 0
                       ),
              widget.Systray(
                       background = c["bpgrad"],
                       padding = 5
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = c["bpgrad"],
                       background = c["bpgrad"]
                       ),
              widget.TextBox(
                       text = ' ',
                       font = "Nerd Font",
                       background = c["bpgrad"],
                       foreground = c['pink'],
                       padding = -12,
                       fontsize = 33
                       ),
             widget.Net(
                       interface = "enp7s0",
                       prefix = 'M',
                       use_bits = 'True',
                       format = ' {down} ↓↑ {up}',
                       foreground = c['black'],
                       background = c['pink'],
                       padding = 5
                       ),
              widget.TextBox(
                       text = ' ',
                       font = "Nerd Font",
                       background = c['pink'],
                       foreground = c['blue'],
                       padding = -12,
                       fontsize = 33
                       ),
                widget.TextBox(
                        text = '',
                        font = "Nerd Font",
                        background = c['blue'],
                        foreground = c['black'],
                        fontsize = 20
                        ),
              widget.CPU(
                      foreground = c['black'],
                      background = c['blue'],
                      format = '{load_percent}%'
                      ),
              widget.ThermalSensor(
                       foreground = c['black'],
                       background = c['blue'],
                       threshold = 90,
                       fmt = ' {}',
                       padding = 5
                       ),
           
              widget.TextBox(
                       text = ' ',
                       font = "Nerd Font",
                       background = c['blue'],
                       foreground = c['pink'],
                       padding = -12,
                       fontsize = 33
                       ),
                
              widget.Memory(
                       foreground = c['black'],
                       background = c['pink'],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                       measure_mem = 'G',
                       format = ' {MemUsed: .3f}{mm}',
                       padding = 5,
                       ),
                widget.TextBox(
                        text = ' ',
                        font = "Nerd Font",
                        background = c['pink'],
                        foreground = c['blue'],
                        padding = -12,
                        fontsize = 33
                        ),
                widget.CheckUpdates(
                        background = c['blue'],
                        foreground = c['black'],
                        distro = 'Arch',
                        colour_no_updates = c['black'],
                        colour_have_updates = c['pink'],
                        display_format = 'ﮮ {updates}',
                        no_update_string = ' No Updates'
                        ),
              widget.TextBox(
                       text = ' ',
                       font = "Nerd Font",
                       background = c['blue'],
                       foreground = c['pink'],
                       padding = -12,
                       fontsize = 33
                       ),
              widget.Clock(
                       foreground = c['black'],
                       background = c['pink'],
                       format = "%A, %B %d - %H:%M "
                       ),
              ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    del widgets_screen1[9:10]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2                 # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=20))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3DDD"
