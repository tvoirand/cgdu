"""
Terminal user interface module using curses for Curses Google Drive Usage.
"""

# standard imports
import curses
import math

# third party imports
import hurry.filesize as hf

# local imports
from directory_tree import MyFile
from directory_tree import MyFolder


def render_folder_contents(folder, win, scrolling, max_lines):
    """
    Render folder's contents using a curses window.
    Input:
        -folder                 MyFolder instance
        -win                    curses window instance
        -scrolling              int
        -max_lines              int
    """

    def create_child_str(child, largest_size):
        """
        Create string to display children sizes.
        Input:
            -child          MyFile or MyFolder instance
            -largest_size   int (bytes)
        """

        # initiate child display string
        child_str = ""

        # add size
        child_str += hf.size(child.size, system=hf.si).rjust(10)

        # add size bar
        size_bar = ""
        nb_characters = math.floor(
            child.size * 10 / largest_size
        )  # compute nb characters
        for i in range(nb_characters):
            size_bar += "#"  # fill size bar with characters
        size_bar = size_bar.ljust(10)  # add trailing whitespaces
        size_bar = "[{}]".format(size_bar)  # add braces
        child_str += size_bar

        # add child name
        if type(child) is MyFolder:
            child_str += "/{}".format(child.name)
        else:
            child_str += " {}".format(child.name)

        return child_str

    # render line for parent directory
    win.addstr(0, 22, "/..", curses.color_pair(1))

    # sort children by size
    folder.children.sort(key=lambda x: x.size, reverse=True)

    # get largest size to compute size bar
    largest_size = folder.children[0].size

    # render line for each children
    for i, child in enumerate(folder.children[scrolling : scrolling + max_lines]):
        child_str = create_child_str(child, largest_size)
        win.addstr(i + 1, 0, child_str, curses.color_pair(1))


def user_interface(stdscr, root_folder):
    """
    Draw Curses Google Drive Usage user interface on terminal using curses.
    Input:
        -stdscr         curses stdscr window object
        -root_folder    MyFolder instance with parent "root"
    """

    # initiate current folder
    current_folder = root_folder

    # initiate key value, cursor location, and scrolling value
    k = 0
    cursor_x = 0
    cursor_y = 0
    scrolling = 0

    # clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # loop where k is the last character pressed
    while k != ord("q"):

        # initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        max_lines = height - 2  # -2 leaves room for status bar

        # changing directory if "enter" key (coded 10 in ASCII) is pressed
        if k == 10:

            # get child currently selected by cursor
            if cursor_y != 0:
                selected_child = current_folder.children[cursor_y - 1 + scrolling]
            else:
                # select parent folder if cursor is on first line, which should contain ".."
                selected_child = current_folder.parent

            # move to selected child if it is a non empty folder
            if type(selected_child) is MyFolder and selected_child.size != 0:
                current_folder = selected_child
                cursor_y = 0  # move cursor to first line
                scrolling = 0  # reinitiate scrolling

        # get new cursor location
        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
            if cursor_y > max_lines:  # scroll down
                scrolling += 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
            if cursor_y < 0 and scrolling > 0:  # scroll up
                scrolling -= 1

        # rendering current folder
        render_folder_contents(current_folder, stdscr, scrolling, max_lines)

        # keep cursor inside the current tree bounds
        cursor_y = max(0, cursor_y)
        cursor_y = min(len(current_folder.children) - scrolling, cursor_y, max_lines)

        # render status bar
        statusbarstr = "Use arrows and 'enter' to navigate, press 'q' to exit"
        statusbarstr += " | Current folder: {}".format(current_folder.name)
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height - 1, 0, statusbarstr)
        stdscr.addstr(
            height - 1, len(statusbarstr), " " * (width - len(statusbarstr) - 1)
        )
        stdscr.attroff(curses.color_pair(3))

        # move cursor
        stdscr.move(cursor_y, cursor_x)

        # refresh the screen
        stdscr.refresh()

        # wait for next input
        k = stdscr.getch()


if __name__ == "__main__":

    # prepare dummy tree
    root_folder = MyFolder("root_folder", "root", 0, 1000)
    root_file = MyFile("root_file", root_folder, 1, 100)
    folder_1 = MyFolder("folder_1", root_folder, 1, 500)
    folder_1_folder_1 = MyFolder("folder_1_folder_1", folder_1, 2, 0)
    folder_1_file_1 = MyFile("folder_1_file_1", folder_1, 2, 400)
    folder_1_file_2 = MyFile("folder_1_file_2", folder_1, 2, 100)
    folder_2 = MyFolder("folder_2", root_folder, 1, 600)
    folder_2_file_1 = MyFile("folder_2_file_1", folder_2, 2, 40)
    folder_2_folder_1 = MyFolder("folder_2_folder_1", folder_2, 2, 460)
    folder_2_folder_1_file_1 = MyFile(
        "folder_2_folder_1_file_1", folder_2_folder_1, 3, 460
    )
    root_folder.children.append(root_file)
    root_folder.children.append(folder_1)
    root_folder.children.append(folder_2)
    folder_1.children.append(folder_1_folder_1)
    folder_1.children.append(folder_1_file_1)
    folder_1.children.append(folder_1_file_2)
    folder_2.children.append(folder_2_file_1)
    folder_2.children.append(folder_2_folder_1)
    folder_2_folder_1.children.append(folder_2_folder_1_file_1)

    curses.wrapper(user_interface, root_folder)
