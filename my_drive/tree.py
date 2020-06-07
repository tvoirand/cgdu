"""
Define classes to handle directory tree.
"""

# standard imports
import curses


class MyFile:
    """
    Defines a file.
    """

    def __init__(self, name, parent, level, size=0):
        """
        MyFile constructor.
        Input:
            -name       str
            -parent     MyFolder or MyTree instance
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
        super(MyFolder, self).__init__(*args, **kwargs)
        self.children = []

    def print_children(self, indent):
        """
        Input:
            -indent     int
        """

        for child in self.children:

            if type(child) is MyFile:
                print("{}".format(child.name.rjust(len(child.name)+indent)))

            elif type(child) is MyFolder:
                print("{}".format(child.name.rjust(len(child.name)+indent)))
                child.print_children(indent+4)

    def render_content(self, win):
        """
        Render directory contents using a curses window.
        Input:
            -win    curses window instance
        """

        win.addstr(0, 0, "..", curses.color_pair(1))
        for i, child in enumerate(self.children):
            win.addstr(i+1, 0, child.name, curses.color_pair(1))


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
