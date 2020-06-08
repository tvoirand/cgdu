"""
Define classes to handle directory tree for Curses Google Drive Usage.
"""


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

        super(MyFolder, self).__init__(*args, **kwargs)  # inherit MyFile constructor
        self.children = []  # initiate children list

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
                print("{}".format(child.name.rjust(len(child.name) + indent)))

            # call method again with increase indentation (sublevel) if child is folder
            elif type(child) is MyFolder:
                print("{}".format(child.name.rjust(len(child.name) + indent)))
                child.print_children(indent + 4)


if __name__ == "__main__":

    # prepare dummy tree
    root_folder = MyFolder("root_folder", "root", 0, 1000)
    root_file = MyFile("root_file", root_folder, 1, 100)
    folder_1 = MyFolder("folder_1", root_folder, 1, 500)
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
    folder_1.children.append(folder_1_file_1)
    folder_1.children.append(folder_1_file_2)
    folder_2.children.append(folder_2_file_1)
    folder_2.children.append(folder_2_folder_1)
    folder_2_folder_1.children.append(folder_2_folder_1_file_1)

    indent = 0

    root_folder.print_children(indent)
