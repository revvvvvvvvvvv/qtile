# Modernisierte Qtile config.py basierend auf deinem Original

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import time

mod = "mod1"
terminal = guess_terminal()

colors = {
    "bg": "#272822",
    "fg": "#f8f8f2",
    "black": "#1e1f1c",
    "red": "#f92672",
    "green": "#a6e22e",
    "yellow": "#f4bf75",
    "blue": "#66d9ef",
    "magenta": "#ae81ff",
    "cyan": "#38ccd1",
    "white": "#f8f8f2",
    "grey": "#75715e",
    "accent": "#66d9ef",  # z. B. für focused border
}


keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "Tab", lazy.layout.next()),
    Key([mod], "space", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "t", lazy.window.toggle_floating()),
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    Key(["control"], "braceleft", lazy.to_screen(0)),
    Key(["control"], "parenleft", lazy.to_screen(1)),

    Key([mod, "shift"], "Left", lazy.layout.grow_width(-30)),
    Key([mod, "shift"], "Right", lazy.layout.grow_width(30)),
    Key([mod, "shift"], "Up", lazy.layout.grow_height(30)),
    Key([mod, "shift"], "Down", lazy.layout.grow_height(-30)),

    Key([mod, "control"], "Left", lazy.layout.integrate_left()),
    Key([mod, "control"], "Right", lazy.layout.integrate_right()),
    Key([mod, "control"], "Up", lazy.layout.integrate_up()),
    Key([mod, "control"], "Down", lazy.layout.integrate_down()),

    Key([mod, "shift", "control"], "Left", lazy.layout.integrate_left()),
    Key([mod, "shift", "control"], "Right", lazy.layout.integrate_right()),
    Key([mod, "shift", "control"], "Down", lazy.layout.integrate_down()),
    Key([mod, "shift", "control"], "Up", lazy.layout.integrate_up()),
]

groups = []
groups.append(Group("braceleft", label="1"))
groups.append(Group("parenleft", label="2"))
groups.append(Group("bracketleft", label="3"))
groups.append(Group("percent", label="4"))
groups.append(Group("exclam", label="5"))
groups.append(Group("6", label="6"))


for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

layouts = [
    layout.Plasma(border_focus=colors["accent"], border_normal=colors["grey"], border_width=2, margin=8),
    layout.Max(),
]

widget_defaults = dict(
    #font="JetBrainsMono Nerd Font",
    #spacing=1,
    padding=1,
    fontsize=16,
    background=colors["bg"],
    foreground=colors["fg"]
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar([
            widget.GroupBox(
                highlight_method="block",
                this_current_screen_border=colors["blue"],
                inactive=colors["grey"],
                active=colors["accent"],
                rounded=True,
            ),
            widget.Prompt(),
            widget.TextBox("|", foreground=colors["grey"]),
            widget.TaskList(border=colors["accent"], highlight_method="block", urgent_border=colors["yellow"]),
            widget.TextBox("|", foreground=colors["grey"]),
            #widget.WindowName(foreground=colors["blue"]),
            #widget.TextBox("|", foreground=colors["grey"]),
            widget.CPU(update_interval=0.5, foreground=colors["green"]),
            widget.CPUGraph(
                border_color="#1e1e2e",
                graph_color="#a6e3a1",
                fill_color="#a6e3a166",  # halbtransparent
                line_width=2,
                core="all",
                type="line",
                frequency=0.05,
            ),
            widget.TextBox("|", foreground=colors["grey"]),

            widget.Net(
                interface="usb0",  # auto erkennt aktives Interface
                # format="{down:.1f} ↓↑ {up:.1f}",
                update_interval=0.5,
                foreground=colors["blue"],
            ),
            widget.TextBox("|", foreground=colors["grey"]),
            widget.NetGraph(
                interface="usb0",  # auto erkennt aktives Interface
                # format="{down:.1f} ↓↑ {up:.1f}",
                foreground=colors["blue"],
                graph_color="#a6e3a1",
                fill_color="#a6e3a166",  # halbtransparent
                line_width=2,
                core="all",
                type="line",
                frequency=0.05,
            ),


            widget.TextBox("|", foreground=colors["grey"]),
            widget.CurrentLayoutIcon(scale=0.7, foreground=colors["blue"]),
            widget.TextBox("|", foreground=colors["grey"]),
            widget.Systray(),
            widget.Clock(format="%a %d %b %H:%M:%S", foreground=colors["yellow"]),
        ],
        28,
        background=colors["bg"],
        opacity=0.65),
    )
]

@hook.subscribe.startup_once
def autostart():
    qtile.spawn("/home/olli/init.sh")

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class="confirmreset"),
    Match(wm_class="makebranch"),
    Match(wm_class="maketag"),
    Match(wm_class="ssh-askpass"),
    Match(title="branchdialog"),
    Match(title="pinentry"),
])

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = True
wl_xcursor_theme = None
wl_xcursor_size = 12
wmname = "LG3D"
