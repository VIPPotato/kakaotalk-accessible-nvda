import appModuleHandler
import api
import ui
import controlTypes
from logHandler import log
import NVDAObjects.window
import NVDAObjects.UIA
import eventHandler

class KakaoListItem(NVDAObjects.UIA.UIA):
	"""
	Custom list item to ensure selection events handle focus correctly.
	"""
	def event_UIA_elementSelected(self):
		super().event_UIA_elementSelected()
		if controlTypes.State.SELECTED in self.states:
			eventHandler.queueEvent("gainFocus", self)

	def _get_states(self):
		states = super()._get_states()
		# If the item is selected, fake the FOCUSED state so NVDA treats it as a valid focus.
		if controlTypes.State.SELECTED in states:
			states.add(controlTypes.State.FOCUSED)
		return states

	def _get_name(self):
		name = super()._get_name()
		if not name and self.value:
			name = str(self.value)
		return name

class AppModule(appModuleHandler.AppModule):
	"""
	App Module for KakaoTalk.
	"""
	
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		# Apply our custom list item class to list items in the KakaoTalk specific list control.
		if obj.windowClassName == "EVA_VH_ListControl_Dblclk" and obj.role in [controlTypes.Role.LISTITEM, controlTypes.Role.TREEVIEWITEM]:
			clsList.insert(0, KakaoListItem)

	def isGoodUIAWindow(self, hwnd):
		"""
		Tells NVDA whether to use UIA for a specific window.
		"""
		# Returning False for EVA_VH_ListControl_Dblclk causes the window to lose focus entirely.
		# We must use UIA (return True) and find another way to handle the list items.
		return True