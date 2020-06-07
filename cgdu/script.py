"""
My drive python script to handle my google drive account.
"""

# third party imports
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def get_size_of_file(google_drive_file):
    """
    Get size of google drive file in bytes.
    Input:
        -google_drive_file  GoogleDriveFile instance
    Output:
        -                   int
    """
    return float(google_drive_file["fileSize"])


def get_size_of_folder(drive, google_drive_folder):
    """
    Recursively compute size of google drive folder.
    Input:
        -drive                  pydrive.drive.GoogleDrive instance
        -google_drive_folder    GoogleDriveFile instance
            mimeType must contain the string "folder"
    Return:
        -tree_size              dict
            contains:
                "total_size": int
            and for each element, either the size or another tree_size sub-dictionary:
                str (name): int
                OR str (name): {"total_size": float, {str (name): int}, {...},  }
    """

    # initiate output dictionary
    total_size = 0
    tree_size = {}

    # get list of contents
    folder_id = google_drive_folder["id"]
    contents_list = drive.ListFile({"q": "'{}' in parents".format(folder_id)}).GetList()

    # loop through each element
    for element in contents_list:

        # identify files for which the size is known
        if "fileSize" in element.keys():

            # get size and name of file
            file_size = get_size_of_file(element)
            file_name = element["title"]

            # add size of file to this folder's tree_size
            total_size += file_size
            tree_size[file_name]= file_size

        # identify subfolders
        if "folder" in element["mimeType"]:

            # get size and name of folder
            folder_size = get_size_of_folder(drive, element)
            folder_name = element["title"]

            # add size of file to this folder's tree_size
            total_size += folder_size["total_size"]
            tree_size[folder_name]= folder_size

    # compute this folder total size and add it in tree_size items
    tree_size["total_size"] = total_size

    return tree_size


def my_drive():
    """
    Handle my google drive account
    """

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    # Auto-iterate through all files that matches this query
    file_list = drive.ListFile({"q": "'root' in parents"}).GetList()
    for i, f in enumerate(file_list):

        print("Processing file {} of {}".format(i+1, len(file_list)))

        size = get_size_of_folder(drive, f)["total_size"]
        print("Size of {} (bytes): {}".format(f["title"], size))


if __name__ == "__main__":

    my_drive()
