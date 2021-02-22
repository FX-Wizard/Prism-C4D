import os, sys
import c4d

try:
    PRISMROOT
except:
    PRISMROOT = r'C:\Prism'
    # sys.path.insert(0, PRISMROOT)

sys.path.insert(0, os.path.join(PRISMROOT, 'Scripts'))

Dir = os.path.join(PRISMROOT, 'Scripts')

if Dir not in sys.path:
    sys.path.append(Dir)

PySidePath = os.path.join(PRISMROOT, 'PythonLibs', 'Python27', 'PySide')

if PySidePath not in sys.path:
    sys.path.append(PySidePath)

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *
    # from PySide.QtWidgets import *


def prismInit():
    try:
        import PrismCore
        global pcore
        pcore = PrismCore.PrismCore(app='Cinema4D')
        print('LOADED PRISM CORE', pcore)
        return pcore
    except Exception as e:
        print(e)


if __name__ == '__main__':
    pcore = prismInit()