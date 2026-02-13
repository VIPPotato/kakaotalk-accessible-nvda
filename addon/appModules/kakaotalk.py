import appModuleHandler
import api
import ui
import controlTypes
import speech
import vision
import review
from logHandler import log
import NVDAObjects.window
import NVDAObjects.UIA
import NVDAObjects.IAccessible
import eventHandler
import winUser
from _ctypes import COMError

# Window classes that are known to require UIA for proper accessibility.
# EVA_VH_ListControl_Dblclk: Main list control (contacts, chats, messages).
#   Returning False for this class causes the window to lose focus entirely.
_GOOD_UIA_WINDOW_CLASSES = frozenset({
	"EVA_VH_ListControl_Dblclk",
})


class KakaoUIABase(NVDAObjects.UIA.UIA):
	"""Base overlay for ALL KakaoTalk UIA objects.

	Disables UIA cache prefetching to prevent cross-process COM blocking.

	The core issue: _prefetchUIACacheForPropertyIDs calls
	UIAElement.buildUpdatedCache(), a synchronous cross-process COM call.
	When KakaoTalk's UI thread is busy (context menu modal loop, message
	list scrolling, etc.), this call blocks the NVDA main thread for the
	full COM timeout (~8-22 seconds).

	By applying this to ALL KakaoTalk UIA objects, we ensure no element
	can trigger this freeze, regardless of its role or window class.
	Individual property accesses fall back to getCurrentPropertyValueEx(),
	which are individually cheaper and use per-property timeouts.
	"""

	def _prefetchUIACacheForPropertyIDs(self, IDs):
		"""Skip UIA cache prefetching entirely for KakaoTalk objects."""
		return


class KakaoBrailleSuppressed(KakaoUIABase):
	"""KakaoTalk UIA objects that should not output to braille.

	Used for menu containers and items to prevent braille handler from
	querying 15+ UIA properties via COM (NVDAObjectRegion.update()),
	which can contribute to or worsen freezes during context menu display.

	Speech output is preserved; only braille is suppressed.
	"""

	def getBrailleRegions(self, review=False):
		"""Return empty regions to suppress braille output."""
		return []

	def event_gainFocus(self):
		"""Report focus via speech only, skip braille to reduce UIA queries."""
		self.reportFocus()
		# Skip braille.handler.handleGainFocus(self) and
		# brailleInput.handler.handleGainFocus(self) to avoid
		# triggering UIA COM property queries from braille handler.
		vision.handler.handleGainFocus(self)


class KakaoListItem(KakaoUIABase):
	"""Custom list item to ensure selection events handle focus correctly.

	Applied to LISTITEM and TREEVIEWITEM elements within the
	EVA_VH_ListControl_Dblclk window class.
	"""

	def event_UIA_elementSelected(self):
		# If a menu is currently in the foreground, skip processing.
		# When the user opens a context menu on a message, KakaoTalk
		# may still fire elementSelected on the underlying list item,
		# causing expensive UIA queries on a busy process.
		try:
			focus = api.getFocusObject()
			if focus and focus.role in (
				controlTypes.Role.MENUITEM,
				controlTypes.Role.MENU,
				controlTypes.Role.POPUPMENU,
			):
				return
		except Exception:
			pass
		try:
			super().event_UIA_elementSelected()
		except COMError:
			log.debugWarning("COM error in event_UIA_elementSelected, element may be invalid", exc_info=True)
			return
		try:
			if controlTypes.State.SELECTED in self.states:
				eventHandler.queueEvent("gainFocus", self)
		except COMError:
			log.debugWarning("COM error checking states after elementSelected", exc_info=True)

	def _get_states(self):
		try:
			states = super()._get_states()
		except COMError:
			log.debugWarning("COM error getting states", exc_info=True)
			return set()
		# If the item is selected, fake the FOCUSED state so NVDA treats it as a valid focus.
		if controlTypes.State.SELECTED in states:
			states.add(controlTypes.State.FOCUSED)
		return states

	def _get_name(self):
		try:
			name = super()._get_name()
		except COMError:
			log.debugWarning("COM error getting name", exc_info=True)
			return ""
		if not name and self.value:
			name = str(self.value)
		return name


class KakaoMenuItem(KakaoBrailleSuppressed):
	"""Custom UIA menu item to allow focus events in KakaoTalk context menus.

	KakaoTalk menu items report HasKeyboardFocus as False,
	causing NVDA to drop UIA focus change events.
	See: NVDA UIAHandler/__init__.py:912, NVDAObjects/UIA/__init__.py:1579-1583

	Inherits braille suppression from KakaoBrailleSuppressed.
	"""

	# Allow focus events even when HasKeyboardFocus is False.
	shouldAllowUIAFocusEvent = True


class KakaoTalkMessageEdit(NVDAObjects.IAccessible.IAccessible):
	"""Overlay for KakaoTalk message input field (RICHEDIT50W).

	Aggressively suppresses braille and most NVDA events to prevent
	focus jumping and character composition breakage during Korean
	IME input.  Speech output is preserved where possible.
	"""

	def initOverlayClass(self):
		self.shouldAllowIAccessibleTextChangeEvent = True
		self.hasIAccessibleTextObject = True
		if hasattr(self, '_accRole'):
			self._accRole = 0
		self.braille_role = None
		self.hasBraille = False
		self.excludeFromBraille = True

	def _get_IAccessibleObject(self):
		obj = super()._get_IAccessibleObject()
		if obj:
			try:
				obj.accRole = 0
				if hasattr(obj, '_accRole'):
					obj._accRole = 0
			except Exception:
				pass
		return obj

	def _get_role(self):
		return 0

	def _get_roleText(self):
		return None

	def _get_IA2Role(self):
		return 0

	def _get_brailleRoleText(self):
		return None

	def _get_roleDescription(self):
		return None

	def _get_states(self):
		states = super()._get_states()
		states.discard(controlTypes.State.MULTILINE)
		return states

	def _get_brailleText(self):
		return ""

	def _get_brailleName(self):
		return ""

	def _get_brailleDescription(self):
		return ""

	def _get_brailleRegions(self):
		return []

	def event_brailleRegionChanged(self):
		pass

	def event_brailleDisplayChanged(self):
		pass

	def event_brailleSettingsChanged(self):
		pass

	def event_brailleViewportChanged(self):
		pass

	def shouldAcceptEvent(self, event):
		if event.eventName.startswith("braille"):
			return False
		return True

	def getBrailleRegions(self, review=False):
		return []

	def routeTo(self, braillePos):
		pass

	def braillePosToScreenPos(self, braillePos):
		return None

	def screenPosToBraillePos(self, screenPos):
		return None

	def event_gainFocus(self):
		"""Report focus via speech only, skip braille."""
		self.reportFocus()
		vision.handler.handleGainFocus(self)

	def event_valueChange(self):
		"""Handle value change with speech only, skip braille."""
		if self is api.getFocusObject():
			speech.speakObjectProperties(
				self, value=True, reason=controlTypes.OutputReason.CHANGE
			)
		vision.handler.handleUpdate(self, property="value")

	def event_caret(self):
		"""Handle caret move without braille update."""
		if self is api.getFocusObject() and not eventHandler.isPendingEvents("gainFocus"):
			vision.handler.handleCaretMove(self)
			review.handleCaretMove(self)


class AppModule(appModuleHandler.AppModule):
	"""
	App Module for KakaoTalk.
	"""

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		# Message input field (IAccessible RICHEDIT50W, controlID 1006).
		# Suppress braille during message composition.
		if (
			isinstance(obj, NVDAObjects.IAccessible.IAccessible)
			and obj.windowClassName == "RICHEDIT50W"
			and obj.windowControlID == 1006
		):
			clsList.insert(0, KakaoTalkMessageEdit)
			return

		# Apply prefetch-disabling overlay to ALL KakaoTalk UIA objects.
		# Without this catch-all, container elements (LIST, TREEVIEW,
		# PANE, WINDOW), menu containers (MENU, POPUPMENU), and any
		# UIA objects from windows where UiaHasServerSideProvider
		# returns True would still use the base class buildUpdatedCache,
		# causing 10-22 second freezes.
		if isinstance(obj, NVDAObjects.UIA.UIA):
			if (
				obj.windowClassName == "EVA_VH_ListControl_Dblclk"
				and obj.role in (controlTypes.Role.LISTITEM, controlTypes.Role.TREEVIEWITEM)
			):
				clsList.insert(0, KakaoListItem)
			elif obj.windowClassName == "EVA_Menu":
				# All EVA_Menu objects get braille suppression.
				# MENUITEM gets additional shouldAllowUIAFocusEvent.
				if obj.role == controlTypes.Role.MENUITEM:
					clsList.insert(0, KakaoMenuItem)
				else:
					clsList.insert(0, KakaoBrailleSuppressed)
			else:
				# For all other UIA objects, apply base class to disable prefetch.
				clsList.insert(0, KakaoUIABase)

	def event_inputComposition(self, obj, nextHandler):
		"""Suppress input composition events for Korean locale.

		Without this, Korean IME composition events can cause additional
		braille updates and focus instability in the message input field.
		"""
		import locale
		if (
			obj.role == controlTypes.Role.EDITABLETEXT
			and (obj.name == "Enter a message" or obj.name is None)
		):
			current_locale, _ = locale.getdefaultlocale()
			if current_locale and current_locale.startswith("ko"):
				return
		nextHandler()

	def isGoodUIAWindow(self, hwnd):
		"""
		Force UIA only for window classes known to require it.

		Previously this returned True unconditionally, which forced UIA on
		EVA_Menu (context menu) windows. KakaoTalk's EVA_Menu provides a
		broken or incomplete UIA provider, causing getNearestWindowHandle
		and buildUpdatedCache to block the main thread with COM errors,
		resulting in 10-20 second freezes.

		By using a whitelist, EVA_Menu and other unknown windows fall back
		to NVDA's core decision logic, which typically selects IAccessible
		for standard Win32 menus -- a far more stable path.
		"""
		windowClassName = winUser.getClassName(hwnd)
		return windowClassName in _GOOD_UIA_WINDOW_CLASSES
