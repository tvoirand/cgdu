"""
Terminal user interface module using curses for Curses Google Drive Usage.
"""

# standard imports
import curses

# local imports
from tree import MyFile
from tree import MyFolder


def user_interface(stdscr, root_folder):
    """
    Draw Curses Google Drive Usage user interface on terminal using curses.
    Input:
        -stdscr         curses stdscr window object
        -root_folder    MyFolder instance with parent "root"
    """

    # initiate current folder
    current_folder = root_folder

    # initiate key value and cursor location
    k = 0
    cursor_x = 0
    cursor_y = 0

    # clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # loop where k is the last character pressed
    while (k != ord('q')):

        # initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # move cursor
        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1

        # keep cursor inside window bounds
        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)
        cursor_y = max(0, cursor_y)
        cursor_y = min(len(current_folder.children), cursor_y)

        # changing folder if enter is pressed
        if k == 10:
            if cursor_y == 0:
                next_folder = current_folder.parent
            else:
                next_folder = current_folder.children[cursor_y-1]
            if type(next_folder) is MyFolder:
                current_folder = next_folder
                cursor_y = 0

        # rendering current folder
        current_folder.render_content(stdscr)

        # render debugging line
        debuggingstr = "Next folder: {}".format(0)
        stdscr.addstr(height-2, 0, debuggingstr)

        # render status bar
        statusbarstr = "Press 'q' to exit | Last key: {} | Current folder: {}".format(k, current_folder.name)
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # move cursor
        stdscr.move(cursor_y, cursor_x)

        # refresh the screen
        stdscr.refresh()

        # wait for next input
        k = stdscr.getch()

def main():

    # prepare dummy tree
    root_folder = MyFolder("root_folder", "root", 0, 10000)
    root_file = MyFile("root_file", root_folder, 1, 1000)
    folder_1 = MyFolder("folder_1", root_folder, 1, 5000)
    folder_1_file_1 = MyFile("folder_1_file_1", folder_1, 2, 4000)
    folder_1_file_2 = MyFile("folder_1_file_2", folder_1, 2, 1000)
    folder_2 = MyFolder("folder_2", root_folder, 1, 6000)
    folder_2_file_1 = MyFile("folder_2_file_1", folder_2, 2, 4000)
    folder_2_folder_1 = MyFolder("folder_2_folder_1", folder_2, 2, 2000)
    folder_2_folder_1_file_1 = MyFile("folder_2_folder_1_file_1", folder_2_folder_1, 3, 2000)
    root_folder.children.append(root_file)
    root_folder.children.append(folder_1)
    root_folder.children.append(folder_2)
    folder_1.children.append(folder_1_file_1)
    folder_1.children.append(folder_1_file_2)
    folder_2.children.append(folder_2_file_1)
    folder_2.children.append(folder_2_folder_1)
    folder_2_folder_1.children.append(folder_2_folder_1_file_1)

    curses.wrapper(user_interface, root_folder)

if __name__ == "__main__":
    main()
