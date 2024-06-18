import ctypes
import sys
import enable_py_privs
import faulthandler
from project.consts import *


# Define a structure representing a process with its name and ID
class Proc(ctypes.Structure):
    _fields_ = [
        ('name', ctypes.c_char_p),  # Process name (char pointer)
        ('id', ctypes.c_int)  # Process ID (integer)
    ]


# Define a structure representing a list of processes and a count of these processes
class ListProc(ctypes.Structure):
    _fields_ = [
        ('procs', ctypes.POINTER(Proc)),  # Pointer to an array of Proc structures
        ('countP', ctypes.c_int)  # Number of processes (integer)
    ]


def get_proc_dict():
    """
    Retrieves a dictionary of running processes with their names and IDs.
    Enables necessary privileges, handles faults, and loads process data using a DLL.

    Returns:
        proc_dict (dict): A dictionary with process names as keys and their IDs as values.
    """
    # Enable necessary privileges for the process
    enable_py_privs.enable_privs()
    # Enable fault handler for better error reporting
    faulthandler.enable()
    # Initialize an empty dictionary to store process data
    proc_dict = {}
    # Load the shared C library for process checking
    lib = ctypes.CDLL(PROCESS_CHECK_PATH)

    # Define the return type of the getProcData function in the library
    lib.getProcData.restype = ctypes.POINTER(ListProc)
    try:
        # Call the getProcData function to get the list of processes
        list_proc = lib.getProcData()
        res = list_proc[0].procs  # Pointer to the array of Proc structures
        p_count = list_proc[0].countP  # Number of processes
        # Iterate through the processes and add them to the dictionary
        for i in range(p_count):
            if res[i].name:
                proc_dict[res[i].id] = res[i].name.decode()
    except BaseException as e:
        print(e)  # Print any exceptions that occur
    return proc_dict


def disable_privs(pid):
    """
    Disables all privileges for a process with the given process ID using a DLL.

    Args:
        pid (int): The process ID of the process to disable privileges for.
    """
    # Load the shared C library for process checking
    lib = ctypes.CDLL(PROCESS_CHECK_PATH)
    # Define the return type of the DisableAllPrivs function in the library
    lib.DisableAllPrivs.restypes = ctypes.c_int
    # Call the DisableAllPrivs function to disable privileges for the specified process
    lib.DisableAllPrivs(pid)


def close_proc(pid):
    """
    Closes a process with the given process ID using a DLL.

    Args:
        pid (int): The process ID of the process to close.
    """
    # Load the shared C library for process checking
    lib = ctypes.CDLL(PROCESS_CHECK_PATH)
    # Define the return type of the closeProc function in the library
    lib.closeProc.restypes = ctypes.c_int
    # Call the closeProc function to close the specified process
    lib.closeProc(pid)
