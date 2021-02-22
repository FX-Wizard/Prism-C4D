import os, sys
import c4d
from c4d import gui

PRISM_PLUGIN_ID1 = 1055542
PRISM_PLUGIN_ID2 = 1055543
PRISM_PLUGIN_ID3 = 1055544
PRISM_PLUGIN_ID4 = 1055545
PRISM_PLUGIN_ID5 = 1055546


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

import PrismCore
global pcore


# Save Version
class PC_1055542(c4d.plugins.CommandData):
    def Execute(self, doc):
        print('Saving Version...')
        return True


# Save Comment
class PC_1055543(c4d.plugins.CommandData):
    def Execute(self, doc):
        print('Saving Comment...')
        return True


# Open Project Browser
class PC_1055544(c4d.plugins.CommandData):
    def Execute(self, doc):
        print('Opening Project Browser...')
        pcore.projectBrowser()
        return True


# Open Settings
class PC_1055545(c4d.plugins.CommandData):
    def Execute(self, doc):
        print('Opening Prism Settings...')
        pcore.prismSettings()
        return True


def EnhanceMainMenu():
    mainMenu = gui.GetMenuResource('M_EDITOR') 
    pluginsMenu = gui.SearchPluginMenuResource()

    # Create custom menu
    menu = c4d.BaseContainer()
    menu.InsData(c4d.MENURESOURCE_SUBTITLE, "Prism")

    # Add commands
    menu.InsData(c4d.MENURESOURCE_COMMAND, 'PLUGIN_CMD_1055542')
    menu.InsData(c4d.MENURESOURCE_COMMAND, 'PLUGIN_CMD_1055543')
    menu.InsData(c4d.MENURESOURCE_SEPERATOR, True)
    menu.InsData(c4d.MENURESOURCE_COMMAND, 'PLUGIN_CMD_1055544')
    menu.InsData(c4d.MENURESOURCE_SEPERATOR, True)
    menu.InsData(c4d.MENURESOURCE_COMMAND, 'PLUGIN_CMD_1055545')

    if pluginsMenu:
        # Insert menu after 'Plugins' menu
        mainMenu.InsDataAfter(c4d.MENURESOURCE_STRING, menu, pluginsMenu)
    else:
        # Insert menu after the last existing menu ('Plugins' menu was not found)
        mainMenu.InsData(c4d.MENURESOURCE_STRING, menu)


def PluginMessage(id, data):
    # pcore = prismInit()
    # Refresh menu bar
    if id==c4d.C4DPL_BUILDMENU:
        EnhanceMainMenu()
        gui.UpdateMenus()


def prismInit():
    try:
        return PrismCore.PrismCore(app='Cinema4D')
    except Exception as e:
        print(e)


if __name__ == "__main__":
    c4d.plugins.RegisterCommandPlugin(PRISM_PLUGIN_ID1, 'Save Version', 0, None, '', PC_1055542())
    c4d.plugins.RegisterCommandPlugin(PRISM_PLUGIN_ID2, 'Save Comment', 0, None, '', PC_1055543())
    c4d.plugins.RegisterCommandPlugin(PRISM_PLUGIN_ID3, 'Project Browser', 0, None, '', PC_1055544())
    c4d.plugins.RegisterCommandPlugin(PRISM_PLUGIN_ID4, 'Settings', 0, None, '', PC_1055545())
