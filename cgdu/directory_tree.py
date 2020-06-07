"""
Define classes to handle directory tree for Curses Google Drive Usage.
"""

# standard imports
import curses
import math

# third party imports
import hurry.filesize as hf


class MyFile:
    """
    Defines a file.
    """

    def __init__(self, name, parent="root", level=0, size=0):
        """
        MyFile constructor.
        Input:
            -name       str
            -parent     MyFolder instance or "root"
            -level      int
            -size       int (bytes)
        """

        self.name = name
        self.parent = parent
        self.level = level
        self.size = size


class MyFolder(MyFile):
    """
    Defines a folder. Subclass of MyFile.
    """

    def __init__(self, *args, **kwargs):
        """
        MyFolder constructor.
        """

        super(MyFolder, self).__init__(*args, **kwargs) # inherit MyFile constructor
        self.children = [] # initiate children list

    def print_children(self, indent):
        """
        Print this folder's children to terminal
        Input:
            -indent     int
        """

        # loop through children
        for child in self.children:

            # print directly if child is file
            if type(child) is MyFile:
                print("{}".format(child.name.rjust(len(child.name)+indent)))

            # call method again with increase indentation (sublevel) if child is folder
            elif type(child) is MyFolder:
                print("{}".format(child.name.rjust(len(child.name)+indent)))
                child.print_children(indent + 4)

    def render_contents(self, win):
        """
        Render directory contents using a curses window.
        Input:
            -win    curses window instance
        """

        def create_child_str(child, largest_size):
            """
            Create string to display children sizes.
            Input:
                -child          MyFile or MyFolder instance
                -largest_size   int (bytes)
            """

            # initiate child display string
            child_str = "  "

            # add size
            child_str += hf.size(child.size, system=hf.si).rjust(len(hf.size(largest_size, system=hf.si)))

            # add size bar
            size_bar = ""
            nb_characters = math.floor(child.size * 10 / largest_size) # compute nb characters
            for i in range(nb_characters): size_bar += "#" # fill size bar with characters
            size_bar = size_bar.ljust(10) # add trailing whitespaces
            size_bar = "[{}]".format(size_bar) # add braces
            child_str += size_bar

            # add child name
            if type(child) is MyFolder:
                child_str += "/{}".format(child.name)
            else:
                child_str += " {}".format(child.name)

            return child_str

        # render line for parent directory
        win.addstr(0, 18, "/..", curses.color_pair(1))

        # sort children by size
        self.children.sort(key=lambda x: x.size, reverse=True)

        # get largest size to compute size string length and size bar
        largest_size = self.children[0].size # in bytes

        # render line for each children
        for i, child in enumerate(self.children):
            child_str = create_child_str(child, largest_size)
            win.addstr(i+1, 0, child_str, curses.color_pair(1))


if __name__ == "__main__":

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

    indent = 0

    root_folder.print_children(indent)
