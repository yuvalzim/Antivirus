import psutil
import os
from project.consts import *


def get_disk_names():
    """
    gets the computer's disk names
    :return: list(str(disc_names))
    """
    disk_names = set()
    for partition in psutil.disk_partitions(all=True):
        disk_names.add(partition.device)
    return list(disk_names)


def create_quarantine_folder():
    """
    creates the quarantine folder if it doesn't exist
    """
    if not os.path.exists(QUARANTINE_PATH):
        os.mkdir(QUARANTINE_PATH)


def get_quarantined_files():
    """
    gets the content of the quarantined files
    :return: list(files)
    """
    files = os.listdir(QUARANTINE_PATH)
    return files


def delete_file(path):
    """
    deletes the specified file
    :param path: file path
    """
    os.remove(path)
