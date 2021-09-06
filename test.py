# http://mail.python.org/pipermail/python-win32/2006-March/004340.html
import win32com.client

import win32com
wmi = win32com.client.GetObject('winmgmts:')
pids = [p.ProcessId for p in wmi.InstancesOf('win32_process') if p.Name == 'acad.exe']

acad = win32com.client.Dispatch('AutoCAD.Application')
print(acad)

print(pids)