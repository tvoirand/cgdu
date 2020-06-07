"""
Curses Google Drive Usage main script.
"""

# standard import
import curses

# third party imports
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# local imports
from user_interface import user_interface
from directory_tree import MyFile
from directory_tree import MyFolder


def scan_google_drive_folder(drive, google_drive_folder, parent="root"):
    """
    Recursively scan google drive folder, computing size of each children.
    Input:
        -drive                  pydrive.drive.GoogleDrive instance
        -google_drive_folder    GoogleDriveFile instance
            mimeType must contain the string "folder"
        -parent                 MyFolder instance or "root"
    Return:
        -folder                 MyFolder instance
    """

    # initiate folder
    total_size = 0
    folder = MyFolder(
        google_drive_folder["title"],
        parent=parent
    )

    # get list of contents
    folder_id = google_drive_folder["id"]
    contents_list = drive.ListFile({"q": "'{}' in parents".format(folder_id)}).GetList()

    # loop through each element
    for element in contents_list:

        # identify files for which the size is known
        if "fileSize" in element.keys():

            # get file size
            file_size = int(element["fileSize"])

            # add size of file to this folder's size
            folder.size += file_size

            # add new file to this folder's children
            folder.children.append(MyFile(element["title"], parent=folder, size=file_size))

        # identify subfolders
        elif "folder" in element["mimeType"]:

            # scan subfolder
            subfolder = scan_google_drive_folder(drive, element, parent=folder)

            # add size of file to this folder's tree_size
            folder.size += subfolder.size

            # add subfolder to this folder's children
            folder.children.append(subfolder)

        # add any other element and affect size of zero bytes
        else:
            folder.children.append(MyFile(element["title"], parent=folder, size=0))

    return folder


def main():
    """
    Curses Google Drive Usage main function.
    """

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    # initiate root folder
    root_folder = MyFolder("root", parent="root", level=0, size=0)

    # iterate through all elements in root folder
    root_elements = drive.ListFile({"q": "'root' in parents"}).GetList()
    for i, element in enumerate(root_elements[:3]):

        # identify files for which the size is known
        if "fileSize" in element.keys():

            # get file size
            file_size = int(element["fileSize"])

            # add size of file to this folder's size
            root_folder.size += file_size

            # add new file to this folder's children
            root_folder.children.append(
                MyFile(element["title"], parent=root_folder, size=file_size)
            )

        # identify subfolders
        elif "folder" in element["mimeType"]:

            # scan subfolder
            subfolder = scan_google_drive_folder(drive, element, parent=root_folder)

            # add size of file to this folder's tree_size
            root_folder.size += subfolder.size

            # add subfolder to this folder's children
            root_folder.children.append(subfolder)

        # add any other element and affect size of zero bytes
        else:
            root_folder.children.append(MyFile(element["title"], parent=root_folder, size=0))

    # root_folder.print_children(0)

    # curses.wrapper(user_interface, root_folder)


if __name__ == "__main__":

    main()
