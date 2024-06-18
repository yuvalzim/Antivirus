import win32api as wapi
import win32con as wcon
import win32security as wsec

# List of privilege names that we want to enable
PRIV_NAMES = (
    wsec.SE_BACKUP_NAME,
    wsec.SE_DEBUG_NAME,
    wsec.SE_SECURITY_NAME,
)


def enable_privs(remote_server=None, priv_names=PRIV_NAMES):
    """
    Enables specific privileges for the current process.

    Parameters:
    remote_server (str): The name of the remote server on which to enable privileges. Defaults to None.
    priv_names (tuple): A tuple of privilege names to be enabled. Defaults to PRIV_NAMES.
    """

    # Lookup the LUID (Locally Unique Identifier) for each privilege name
    priv_ids = sorted(wsec.LookupPrivilegeValue(remote_server, e) for e in priv_names)
    print("Privileges to be enabled IDs:", priv_ids)

    # Open the access token associated with the current process
    tok = wsec.OpenProcessToken(wapi.GetCurrentProcess(), wcon.TOKEN_ADJUST_PRIVILEGES | wcon.TOKEN_QUERY)

    # Get the current token privileges
    proc_privs = wsec.GetTokenInformation(tok, wsec.TokenPrivileges)
    print("Existing process privileges:", proc_privs)

    # List to store the new privileges
    new_proc_privs = []
    need_change = False

    # Iterate over the current process privileges
    for proc_priv in proc_privs:
        if proc_priv[0] in priv_ids:
            print("Checking privilege " + str(proc_priv[0]))
            if proc_priv[1] != wcon.SE_PRIVILEGE_ENABLED:
                need_change = True
            # Append the privilege with enabled state
            new_proc_privs.append((proc_priv[0], wcon.SE_PRIVILEGE_ENABLED))
        else:
            # Keep the current privilege state
            new_proc_privs.append(proc_priv)

    print("New process privileges:", new_proc_privs)

    # Adjust token privileges only if changes are needed
    if need_change:
        modif_privs = wsec.AdjustTokenPrivileges(tok, False, new_proc_privs)
        res = wapi.GetLastError()
        print("Changed privileges:", modif_privs)  # Output the changed privileges
        if res != 0:
            print("Error (partial) setting privileges:", res)
    else:
        print("Already set")

    # Close the token handle
    wapi.CloseHandle(tok)

