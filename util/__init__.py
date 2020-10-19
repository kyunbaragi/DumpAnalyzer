import os
import re
import zipfile


def extract(path):
    name, ext = os.path.splitext(path)
    extract_dir = name
    extension = ext[1:].strip().lower()
    if extension == 'zip':
        if zipfile.is_zipfile(path):
            if not os.path.exists(extract_dir):
                os.mkdir(extract_dir)
            with zipfile.ZipFile(path, 'r') as f:
                f.extractall(extract_dir)
            return True
    elif extension == '7z':
        return False
    elif extension == 'gz':
        return False
    return False


def extract_all(directory):
    for root, dirs, files in os.walk(directory):
        for f in files:
            if extract(os.path.join(root, f)):
                name, ext = os.path.splitext(f)
                extract_dir = os.path.join(root, name)
                extract_all(extract_dir)


def match(directory, patterns, flags=0):
    if isinstance(patterns, str):
        patterns = [patterns]
    matches = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            for pattern in patterns:
                if re.match(pattern, f, flags):
                    matches.append(os.path.join(root, f))
    return matches


def search(directory, patterns, flags=0):
    if isinstance(patterns, str):
        patterns = [patterns]
    matches = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            for pattern in patterns:
                if re.search(pattern, f, flags):
                    matches.append(os.path.join(root, f))
    return matches
