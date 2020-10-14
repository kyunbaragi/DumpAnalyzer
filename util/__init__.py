import os
import zipfile


def unzip(directory):
    pass


def unzip_all(directory: str):
    filenames = os.listdir(directory)
    for filename in filenames:
        file_path = os.path.join(directory, filename)

        # Extract compressed files
        if filename.endswith('.zip'):
            os.mkdir(file_path)
            with zipfile.ZipFile(file_path, 'r') as zip_f:
                zip_f.extractall(file_path)
        elif filename.endswith('.7z'):
            pass
        elif filename.endswith('.gz'):
            pass

        # DFS with recursive
        if os.path.isdir(file_path):
            unzip_all(file_path)
