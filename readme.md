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
*   Run the `cgdu.py` script from within the root folder where `settings.yaml` is stored
