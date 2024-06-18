from project.consts import *
import os


def get_file_content(file_path: str) -> bytes:
    """
    gets the content of a file
    :param file_path: file path
    :return: content
    """
    with open(file_path, 'rb') as file:
        contents = file.read()
    os.remove(file_path)
    return contents


def create_new_file(file_path: str, content: bytes) -> None:
    """
    creates a new file
    :param file_path: new path
    :param content: file contents
    :return:
    """
    file_name = os.path.basename(file_path)
    new_file_path = f"{QUARANTINE_PATH}\\{file_name}"
    with open(new_file_path, 'ab') as new_file:
        old_path_bytes = file_path.encode()
        new_file.write(old_path_bytes + b"\n" + content)


def move_to_quarantine(file_path: str):
    """
    moves the specified file to quarantine
    :param file_path: file path
    """
    file_content = get_file_content(file_path)
    create_new_file(file_path, file_content)


def restore_file(file_name: str):
    """
    restores the file from the quarantine folder to its original location
    :param file_name: file name
    """
    file_path = f"{QUARANTINE_PATH}\\{file_name}"
    with open(f"{QUARANTINE_PATH}\\{file_name}", 'rb') as file:
        old_file_path = file.readline().decode().rstrip()
        file_content = file.read()
    os.remove(file_path)

    with open(f"{old_file_path}", 'ab') as new_file:
        new_file.write(file_content)

