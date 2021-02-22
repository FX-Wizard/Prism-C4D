# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2019 Richard Frangenberg
#
# Licensed under GNU GPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.

import c4d

try:
	from PySide2.QtCore import *
	from PySide2.QtGui import *
	from PySide2.QtWidgets import *
	psVersion = 2
except:
	from PySide.QtCore import *
	from PySide.QtGui import *
	psVersion = 1

import os, sys
import traceback, time, platform, shutil, socket
from functools import wraps
if platform.system() == "Windows":
	if sys.version[0] == "3":
		import winreg as _winreg
	else:
		import _winreg

class Prism_Cinema4D_Integration(object):
	def __init__(self, core, plugin):
		print('CALLING C4D INTERGRATION')
		self.core = core
		self.plugin = plugin
		c4dVersion = str(c4d.GetC4DVersion())[:2]
		if platform.system() == "Windows":
			self.examplePath = os.environ["programfiles"] + "\\Maxon Cinema 4D %s\\" % c4dVersion
		elif platform.system() == "Darwin":
			userName = os.environ['SUDO_USER'] if 'SUDO_USER' in os.environ else os.environ['USER']
			self.examplePath = "/Users/%s/Library/Preferences/Autodesk/Cinema4D%s/" % userName, c4dVersion


	def err_decorator(func):
		@wraps(func)
		def func_wrapper(*args, **kwargs):
			exc_info = sys.exc_info()
			try:
				return func(*args, **kwargs)
			except Exception as e:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				erStr = ("%s ERROR - Prism_Plugin_Cinema4D_Integration %s:\n%s\n\n%s" % (time.strftime("%d/%m/%y %X"), args[0].plugin.version, ''.join(traceback.format_stack()), traceback.format_exc()))
				if hasattr(args[0].core, "writeErrorLog"):
					args[0].core.writeErrorLog(erStr)
				else:
					QMessageBox.warning(args[0].core.messageParent, "Prism Integration", erStr)

		return func_wrapper


	# @err_decorator
	# def getExecutable(self):
	# 	execPath = ""
	# 	if platform.system() == "Windows":
	# 		defaultpath = os.path.join(self.getCinema4DPath(), "Cinema 4D.exe")
	# 		if os.path.exists(defaultpath):
	# 			execPath = defaultpath

	# 	return execPath


	# @err_decorator
	# def getCinema4DPath(self):
	# 	# get executable path
	# 	return os.path.join(self.examplePath, 'cinema4d.exe')


	# @err_decorator
	# def integrationAdd(self, origin):
	# 	path = QFileDialog.getExistingDirectory(self.core.messageParent, "Select Cinema4D folder", os.path.dirname(self.examplePath))

	# 	if path == "":
	# 		return False

	# 	result = self.writeCinema4DFiles(path)

	# 	if result:
	# 		QMessageBox.information(self.core.messageParent, "Prism Integration", "Prism integration was added successfully")
	# 		return path

	# 	return result


	# @err_decorator
	# def integrationRemove(self, origin, installPath):
	# 	result = self.removeIntegration(installPath)

	# 	if result:
	# 		QMessageBox.information(self.core.messageParent, "Prism Integration", "Prism integration was removed successfully")

	# 	return result


	# def writeCinema4DFiles(self, pluginPath):
	# 	try:
	# 		integrationBase = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Integration")
	# 		addedFiles = []

	# 		initpath = os.path.join(pluginPath, "scripts", "PrismInit.py")

	# 		if os.path.exists(initpath):
	# 			os.remove(initpath)

	# 		if os.path.exists(initpath + "c"):
	# 			os.remove(initpath + "c")

	# 		origInitFile = os.path.join(integrationBase, "PrismInit.py")
	# 		shutil.copy2(origInitFile, initpath)
	# 		addedFiles.append(initpath)

	# 		with open(initpath, "r") as init:
	# 			initStr = init.read()

	# 		with open(initpath, "w") as init:
	# 			initStr = initStr.replace("PRISMROOT", "\"%s\"" % self.core.prismRoot.replace("\\", "/"))
	# 			init.write(initStr)

	# 		if platform.system() in ["Linux", "Darwin"]:
	# 			for i in addedFiles:
	# 				os.chmod(i, 0o777)

	# 		return True

	# 	except Exception as e:
	# 		exc_type, exc_obj, exc_tb = sys.exc_info()

	# 		msgStr = "Errors occurred during the installation of the Cinema4D integration.\nThe installation is possibly incomplete.\n\n%s\n%s\n%s" % (str(e), exc_type, exc_tb.tb_lineno)
	# 		msgStr += "\n\nRunning this application as administrator could solve this problem eventually."

	# 		QMessageBox.warning(self.core.messageParent, "Prism Integration", msgStr)
	# 		return False


	# def removeIntegration(self, installPath):
	# 	try:
	# 		initPy = os.path.join(installPath, "scripts", "PrismInit.py")
	# 		initPyc = os.path.join(installPath, "scripts", "PrismInit.pyc")
	# 		shelfpath = os.path.join(installPath, "prefs", "shelves", "shelf_Prism.mel")

	# 		for i in [initPy, initPyc, shelfpath]:
	# 			if os.path.exists(i):
	# 				os.remove(i)

	# 		userSetup = os.path.join(installPath, "scripts", "userSetup.py")

	# 		if os.path.exists(userSetup):
	# 			with open(userSetup, "r") as usFile:
	# 				text = usFile.read()

	# 			if "#>>>PrismStart" in text and "#<<<PrismEnd" in text:
	# 				text = text[:text.find("#>>>PrismStart")] + text[text.find("#<<<PrismEnd")+len("#<<<PrismEnd"):]

	# 				otherChars = [x for x in text if x != " "]
	# 				if len(otherChars) == 0:
	# 					os.remove(userSetup)
	# 				else:
	# 					with open(userSetup, "w") as usFile:
	# 						usFile.write(text)

	# 		return True

	# 	except Exception as e:
	# 		exc_type, exc_obj, exc_tb = sys.exc_info()

	# 		msgStr = "Errors occurred during the removal of the Cinema4D integration.\n\n%s\n%s\n%s" % (str(e), exc_type, exc_tb.tb_lineno)
	# 		msgStr += "\n\nRunning this application as administrator could solve this problem eventually."

	# 		QMessageBox.warning(self.core.messageParent, "Prism Integration", msgStr)
	# 		return False


	# def updateInstallerUI(self, userFolders, pItem):
	# 	try:
	# 		pluginItem = QTreeWidgetItem(["Houdini"])
	# 		pItem.addChild(pluginItem)

	# 		pluginPath = self.examplePath

	# 		if pluginPath != None and os.path.exists(pluginPath):
	# 			pluginItem.setCheckState(0, Qt.Checked)
	# 			pluginItem.setText(1, pluginPath)
	# 			pluginItem.setToolTip(0, pluginPath)
	# 		else:
	# 			pluginItem.setCheckState(0, Qt.Unchecked)
	# 	except Exception as e:
	# 		exc_type, exc_obj, exc_tb = sys.exc_info()
	# 		msg = QMessageBox.warning(self.core.messageParent, "Prism Installation", "Errors occurred during the installation.\n The installation is possibly incomplete.\n\n%s\n%s\n%s\n%s" % (__file__, str(e), exc_type, exc_tb.tb_lineno))
	# 		return False


	# def installerExecute(self, pluginItem, result, locFile):
	# 	try:
	# 		pluginPaths = []
	# 		installLocs = []

	# 		if pluginItem.checkState(0) != Qt.Checked:
	# 			return installLocs

	# 		for i in range(pluginItem.childCount()):
	# 			item = pluginItem.child(i)
	# 			if item.checkState(0) == Qt.Checked and os.path.exists(item.text(1)):
	# 				pluginPaths.append(item.text(1))

	# 		for i in pluginPaths:
	# 			result["Cinema4D integration"] = self.writeCinema4DFiles(i)
	# 			if result["Cinema4D integration"]:
	# 				installLocs.append(i)

	# 		return installLocs
	# 	except Exception as e:
	# 		exc_type, exc_obj, exc_tb = sys.exc_info()
	# 		msg = QMessageBox.warning(self.core.messageParent, "Prism Installation", "Errors occurred during the installation.\n The installation is possibly incomplete.\n\n%s\n%s\n%s\n%s" % (__file__, str(e), exc_type, exc_tb.tb_lineno))
	# 		return False