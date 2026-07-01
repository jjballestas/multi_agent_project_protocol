import ctypes, sys
from ctypes import wintypes, byref, Structure, c_uint, create_unicode_buffer

rm = ctypes.windll.rstrtmgr
CCH_APP = 255
CCH_SVC = 63

class FILETIME(Structure):
    _fields_ = [("l", wintypes.DWORD), ("h", wintypes.DWORD)]
class RM_UNIQUE_PROCESS(Structure):
    _fields_ = [("dwProcessId", wintypes.DWORD), ("ProcessStartTime", FILETIME)]
class RM_PROCESS_INFO(Structure):
    _fields_ = [
        ("Process", RM_UNIQUE_PROCESS),
        ("strAppName", wintypes.WCHAR * (CCH_APP + 1)),
        ("strServiceShortName", wintypes.WCHAR * (CCH_SVC + 1)),
        ("ApplicationType", c_uint),
        ("AppStatus", wintypes.ULONG),
        ("TSSessionId", wintypes.DWORD),
        ("bRestartable", wintypes.BOOL),
    ]

path = sys.argv[1]
session = wintypes.DWORD()
key = create_unicode_buffer(256)
if rm.RmStartSession(byref(session), 0, key) != 0:
    print("RmStartSession failed"); sys.exit(1)
try:
    arrpaths = (wintypes.LPCWSTR * 1)(path)
    if rm.RmRegisterResources(session, 1, arrpaths, 0, None, 0, None) != 0:
        print("RmRegisterResources failed"); sys.exit(1)
    needed = c_uint(0); count = c_uint(0); reason = c_uint(0)
    rm.RmGetList(session, byref(needed), byref(count), None, byref(reason))
    n = needed.value
    if n == 0:
        print("HOLDERS: none (file is free)"); sys.exit(0)
    arr = (RM_PROCESS_INFO * n)()
    count = c_uint(n)
    rc = rm.RmGetList(session, byref(needed), byref(count), arr, byref(reason))
    if rc != 0:
        print("RmGetList rc", rc); sys.exit(1)
    for i in range(count.value):
        print("HOLDER pid=%d app=%s" % (arr[i].Process.dwProcessId, arr[i].strAppName))
finally:
    rm.RmEndSession(session)
