"""
Terminal user interface module using curses for Curses Google Drive Usage.
"""

# standard imports
import curses

# local imports
from directory_tree import MyFile
from directory_tree import MyFolder


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

        # keep cursor inside the current tree bounds
        cursor_y = max(0, cursor_y)
        cursor_y = min(len(current_folder.children), cursor_y)

        # changing directory if "enter" key (coded 10 in ASCII) is pressed
        if k == 10:

            # get child currently selected by cursor
            if cursor_y != 0:
                selected_child = current_folder.children[cursor_y-1]
            else:
                # select parent folder if cursor is on first line, which should contain ".."
                selected_child = current_folder.parent

            # move to selected child if it is a folder
            if type(selected_child) is MyFolder:
                current_folder = selected_child
                cursor_y = 0 # move cursor to first line

        # rendering current folder
        current_folder.render_contents(stdscr)

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
    root_folder = MyFolder("root_folder", "root", 0, 1000)
    root_file = MyFile("root_file", root_folder, 1, 100)
    folder_1 = MyFolder("folder_1", root_folder, 1, 500)
    folder_1_file_1 = MyFile("folder_1_file_1", folder_1, 2, 400)
    folder_1_file_2 = MyFile("folder_1_file_2", folder_1, 2, 100)
    folder_2 = MyFolder("folder_2", root_folder, 1, 600)
    folder_2_file_1 = MyFile("folder_2_file_1", folder_2, 2, 40)
    folder_2_folder_1 = MyFolder("folder_2_folder_1", folder_2, 2, 460)
    folder_2_folder_1_file_1 = MyFile("folder_2_folder_1_file_1", folder_2_folder_1, 3, 460)
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
