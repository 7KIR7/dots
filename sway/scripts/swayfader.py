from i3ipc import Connection, Event
from threading import Thread
from time import sleep


FRAME_T = 0.01  # time taken between each frame of fade

# transparency values
CON_AC     = 1     # active window
CON_INAC   = 0.5   # inactive window
FLOAT_AC   = 1     # active floating window
FLOAT_INAC = 0.5  # inactive floating window
BOT_INAC   = 0.9   # bottom window


# fade durations
FADE_TIME      = 0.2
ALT_FADE_TIME  = 0.1

CON_OUT        = FADE_TIME      # window fading out
CON_IN         = 0.15           # window fading in
FLOAT_OUT      = ALT_FADE_TIME  # floating window fading out
FLOAT_IN       = ALT_FADE_TIME  # floating window fading in
BOT_OUT        = ALT_FADE_TIME  # bottom window fading out
BOT_IN         = ALT_FADE_TIME  # bottom window fading in
BOT_SWITCH_IN  = FADE_TIME      # window becoming bottom window
BOT_SWITCH_OUT = FADE_TIME      # bottom window becoming window
FLOAT_BOT_OUT  = FADE_TIME      # floating window fading out from bottom
FLOAT_BOT_IN   = FADE_TIME      # floating window fading in from bottom


class Fader:
    def __init__(self):
        self.floating_windows = []
        self.fader_running    = False
        self.fade_queue       = []
        self.fade_data        = {}
        self.bottom_win       = None
        self.old_win          = None
        self.active_win       = None

        ipc = Connection()
        ipc.on(Event.WINDOW_FOCUS,    self.on_window_focus)
        ipc.on(Event.WINDOW_NEW,      self.on_window_new)
        ipc.on(Event.WINDOW_FLOATING, self.on_window_floating)

        for win in ipc.get_tree():
            if win.type == "floating_con":
                self.floating_windows.append(win.id)
                if win.focused:
                    change_opacity(win, FLOAT_AC)
                    self.active_win = win
                else:
                    change_opacity(win, FLOAT_INAC)
            elif win.type == "con":
                if win.focused:
                    self.active_win = win
                    change_opacity(win, CON_AC)
                else:
                    change_opacity(win, CON_INAC)

        ipc.main()

    def add_fade(self, win, start, target, duration):
        if not duration:
            if win.id in self.fade_queue:
                self.fade_queue.remove(win.id)
                del self.fade_data[win.id]
            change_opacity(win, target)
            return

        if win.id in self.fade_queue:
            f = self.fade_data[win.id]
            change = (FRAME_T / duration) * (target - f["opacity"])
            f["change"] = change
            f["target"] = target
            return

        change_opacity(win, start)
        change = (FRAME_T / duration) * (target - start)
        fade_data = {"opacity": start, "change": change, "target": target, "win": win}
        self.fade_queue.append(win.id)
        self.fade_data[win.id] = fade_data

    def start_fader(self):
        if not self.fader_running:
            self.fader_running = True
            Thread(target=self.fader).start()

    def fader(self):
        while self.fade_queue:
            for win_id in self.fade_queue.copy():
                try:
                    f = self.fade_data[win_id]
                except KeyError:
                    continue
                f["opacity"] += f["change"]

                finished = False
                if f["change"] > 0:
                    if f["opacity"] >= f["target"]:
                        finished = True
                elif f["opacity"] <= f["target"]:
                    finished = True

                if finished:
                    change_opacity(f["win"], f["target"])
                    try:
                        self.fade_queue.remove(win_id)
                        del self.fade_data[win_id]
                    except (KeyError, ValueError):
                        continue
                else:
                    change_opacity(f["win"], f["opacity"])

            sleep(FRAME_T)
        self.fader_running = False

    def on_window_focus(self, ipc, e):
        if self.active_win.id == e.container.id:
            return

        if self.active_win.type == "con":
            if e.container.type == "con":
                self.add_fade(
                    e.container, CON_INAC,
                    CON_AC, CON_IN)
                self.add_fade(
                    self.active_win, CON_AC,
                    CON_INAC, CON_OUT)

            else:
                self.add_fade(
                    e.container, FLOAT_INAC,
                    FLOAT_AC, FLOAT_IN)
                self.add_fade(
                    self.active_win, CON_AC,
                    BOT_INAC, BOT_OUT)
                self.bottom_win = self.active_win

        else:
            if e.container.type == "con":
                self.add_fade(
                    self.active_win, FLOAT_AC,
                    FLOAT_INAC, FLOAT_BOT_OUT)

                if not self.bottom_win:
                    self.add_fade(
                        e.container, CON_INAC,
                        CON_AC, CON_IN)

                elif e.container.id != self.bottom_win.id:
                    self.add_fade(
                        self.bottom_win, BOT_INAC,
                        CON_INAC, BOT_SWITCH_OUT)
                    self.add_fade(
                        e.container, CON_INAC,
                        CON_AC, BOT_SWITCH_IN)
                    self.bottom_win = e.container

                else:
                    self.add_fade(
                        self.bottom_win, BOT_INAC,
                        CON_AC, BOT_IN)

            else:
                self.add_fade(
                    self.active_win, FLOAT_AC,
                    FLOAT_INAC, FLOAT_OUT)
                self.add_fade(
                    e.container, FLOAT_INAC,
                    FLOAT_AC, FLOAT_IN)

        self.start_fader()
        self.active_win = e.container

    def on_window_new(self, ipc, e):
        if self.active_win:
            if self.active_win.type == "con":
                change_opacity(self.active_win, CON_INAC)
            else:
                change_opacity(self.active_win, FLOAT_INAC)

        if self.bottom_win:
            change_opacity(self.bottom_win, CON_INAC)

        elif self.active_win and self.active_win.type == "con":
            self.bottom_win = self.active_win
            change_opacity(self.bottom_win, CON_INAC)

        change_opacity(e.container, CON_AC)
        self.old_win = self.active_win
        self.active_win = e.container

    def on_window_floating(self, ipc, e):
        c_id = e.container.id
        if c_id not in self.floating_windows:
            self.floating_windows.append(c_id)

            if self.active_win.id != e.container.id:
                change_opacity(e.container, FLOAT_INAC)

            else:
                if self.old_win and self.bottom_win:
                    if self.old_win.type == "con":
                        self.bottom_win = self.old_win
                    change_opacity(self.bottom_win, BOT_INAC)
                change_opacity(e.container, FLOAT_AC)

        else:
            self.floating_windows.remove(c_id)
            if self.active_win.id != e.container.id:
                change_opacity(e.container, CON_INAC)

            else:
                if self.old_win and self.old_win.type == "con":
                    change_opacity(self.old_win, CON_INAC)
                change_opacity(self.active_win, CON_AC)

        self.active_win = e.container


def change_opacity(win, trans):
    win.command("opacity " + str(trans))


if __name__ == "__main__":
    Fader()

