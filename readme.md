# Curses Google Drive Usage

A terminal application to display google drive usage inspired from ncdu.

<img src="docs/example.png" width="50%" />

## Dependencies

Python 3 with the following packages:

*   pydrive
*   hurry.filesize

## Installation

*   Get google api client secrets
*   Duplicate `example_client_secrets.json` in the `config` folder using `client_secrets.json` as filename and store your client-id and client-secret in the new file
*   Install the dependencies, for example with a conda environement using the `environment.yml` file

    `conda env create -f environment.yml`

## Usage

*   Run the `cgdu.py` script from within the root folder where `settings.yaml` is stored
*   In case of authentication error, remove the file `config/credentials.json` and try again to perform authenticatin workflow in browser
*   Wait until scanning is over
*   Navigate with arrows, press 'q' to exit

## Todo

*   Add header and update footer

## Contribute

Please feel free to contribute by opening issues or pull-requests!
