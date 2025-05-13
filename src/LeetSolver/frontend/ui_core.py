import curses

MINIMAL_HEIGHT = 24
MINIMAL_WIDTH = 80

# what my ui core needs
# METHODS   
# 1. update parts of screens
# 2. 



class UICore:
    
    def __init__(self):
        self.stdscr = self.__setup_terminal()
        
    def __setup_terminal(self) -> "curses.window":
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)
        curses.start_color()
        return screen
    
    def resize_windows(self):
        h, w = self.stdscr.getmaxyx()
        if h < MINIMAL_HEIGHT or w < MINIMAL_WIDTH:
            return False

        # Clear old windows if they exist
        if self.menu_win:
            del self.menu_win
        if self.main_win:
            del self.main_win

        # Example: reserve top 3 rows for menu
        menu_height = 3
        self.menu_win = curses.newwin(menu_height, w, 0, 0)
        self.main_win = curses.newwin(h - menu_height, w, menu_height, 0)

        # Optional: box the windows
        self.menu_win.box()
        self.main_win.box()

        return True

    def draw(self):
        """Draw your UI"""
        self.menu_win.addstr(1, 2, "Menu Window")
        self.main_win.addstr(1, 2, "Main Window")
        self.menu_win.refresh()
        self.main_win.refresh()

    def run(self):
        try:
            while True:
                if not self.resize_windows():
                    self.stdscr.clear()
                    self.stdscr.addstr(0, 0, "Terminal too small.")
                    self.stdscr.refresh()
                    curses.napms(500)
                    continue

                self.draw()
                key = self.stdscr.getch()
                if key == ord('q'):
                    break
        finally:
            self.__teardown_terminal()


    def __teardown_terminal(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()