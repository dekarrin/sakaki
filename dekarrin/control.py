import pygame, subprocess, os, psutil
from pygame.locals import *
import pprint

class ControlSchemeManager(object):
	"""Handles dynamic key remapping for particular apps"""

	def __init__(self, allSchemes):
		self._current = None
		self._schemes = dict()
		self._translator = AutoHotKeyRemapper()
		self._controls_remapped = False
		for scheme in allSchemes:
			self.add_scheme(scheme['attributes']['name'], scheme['rules'])
		for s in self._schemes:
			self._translator.start(self._schemes[s])

	def add_scheme(self, name, rules):
		self._schemes[name] = []
		for keys, prods in rules:
			rule = {}
			rule['key'] = self._create_sequence_step(keys)
			rule['productions'] = list()
			for p in prods:
				rule['productions'].append(self._create_sequence_step(p))
			self._schemes[name].append(rule)
			
	def remap_controls(self, name):
		if name in self._schemes:
			if self._controls_remapped:
				self.restore_controls()
			self._controls_remapped = True
			self._translator.start(self._schemes[name])
		
	def restore_controls(self):
		if self._controls_remapped:
			self._translator.end()
			self._controls_remapped = False
	
	def _create_sequence_step(self, keys):
		step = {'button': None, 'modifiers': list()}
		for k in keys:
			if k[:2] == "K_":
				if step['button'] is not None:
					print "Warning! More than one normal key found in sequence step. Old key will be overwritten."
				try:
					step['button'] = eval(k)
				except NameError as e:
					print "'%s' is not a valid key code!" % k
					raise e
			elif k[:5] == "KMOD_":
				try:
					step['modifiers'].append(eval(k))
				except NameError as e:
					print "'%s' is not a valid key code!" % k
					raise e
			else:
				raise NameError(k)
		return step
		
class AutoHotKeyRemapper(object):
	def __init__(self):
		self._kill_ahk()
		self._ahk_command = "C:\Program Files\AutoHotkey\AutoHotkey.exe"
		# note: buttons that cannot be reproduced without mod keys are not used
		button_map = {
			K_BACKSPACE:	'Backspace',
			K_TAB:			'Tab',
			K_CLEAR:		'NumpadClear',
			K_RETURN:		'Return',
			K_ESCAPE:		'Esc',
			K_SPACE:		'Space',
			K_QUOTE:		'\'',
			K_COMMA:		',',
			K_MINUS:		'-',
			K_PERIOD:		'.',
			K_SLASH:		'/',
			K_0:			'0',
			K_1:			'1',
			K_2:			'2',
			K_3:			'3',
			K_4:			'4',
			K_5:			'5',
			K_6:			'6',
			K_7:			'7',
			K_8:			'8',
			K_9:			'9',
			K_SEMICOLON:	';',
			K_EQUALS:		'=',
			K_LEFTBRACKET:	'[',
			K_BACKSLASH:	'\\',
			K_RIGHTBRACKET:	']',
			K_BACKQUOTE:	'`',
			K_a:			'a',
			K_b:			'b',
			K_c:			'c',
			K_d:			'd',
			K_e:			'e',
			K_f:			'f',
			K_g:			'g',
			K_h:			'h',
			K_i:			'i',
			K_j:			'j',
			K_l:			'l',
			K_m:			'm',
			K_n:			'n',
			K_o:			'o',
			K_p:			'p',
			K_q:			'q',
			K_r:			'r',
			K_s:			's',
			K_t:			't',
			K_u:			'u',
			K_v:			'v',
			K_w:			'w',
			K_x:			'x',
			K_y:			'y',
			K_z:			'z',
			K_DELETE:		'Del',
			K_KP0:			'Numpad0',
			K_KP1:			'Numpad1',
			K_KP2:			'Numpad2',
			K_KP3:			'Numpad3',
			K_KP4:			'Numpad4',
			K_KP5:			'Numpad5',
			K_KP6:			'Numpad6',
			K_KP7:			'Numpad7',
			K_KP8:			'Numpad8',
			K_KP9:			'Numpad9',
			K_KP_PERIOD:	'NumpadDot',
			K_KP_DIVIDE:	'NumpadDiv',
			K_KP_MULTIPLY:	'NumpadMult',
			K_KP_MINUS:		'NumpadSub',
			K_KP_PLUS:		'NumpadAdd',
			K_KP_ENTER:		'NumpadEnter',
			K_KP_EQUALS:	'NumpadEnter',
			K_UP:			'Up',
			K_DOWN:			'Down',
			K_RIGHT:		'Right',
			K_LEFT:			'Left',
			K_INSERT:		'Ins',
			K_HOME:			'Home',
			K_END:			'End',
			K_PAGEUP:		'PgUp',
			K_PAGEDOWN:		'PgDn',
			K_F1:			'F1',
			K_F2:			'F2',
			K_F3:			'F3',
			K_F4:			'F4',
			K_F5:			'F5',
			K_F6:			'F6',
			K_F7:			'F7',
			K_F8:			'F8',
			K_F9:			'F9',
			K_F10:			'F10',
			K_F11:			'F11',
			K_F12:			'F12',
			K_F13:			'F13',
			K_F14:			'F14',
			K_F15:			'F15',
			K_SCROLLOCK:	'ScrollLock',
			K_CAPSLOCK:		'CapsLock',
			K_RSHIFT:		'RShift',
			K_LSHIFT:		'LShift',
			K_RCTRL:		'RCtrl',
			K_LCTRL:		'LCtrl',
			K_RALT:			'RAlt',
			K_LALT:			'LAlt',
			K_RSUPER:		'RWin',
			K_LSUPER:		'LWin',
			K_HELP:			'Help',
			K_PRINT:		'PrintScreen',
			K_BREAK:		'CtrlBreak',
			K_MENU:			'AppsKey'
		}
		modifier_map = {
			KMOD_LSHIFT:		'<+',
			KMOD_RSHIFT:		'>+',
			KMOD_SHIFT:		'+',
			KMOD_LCTRL:		'<^',
			KMOD_RCTRL:		'>^',
			KMOD_CTRL:		'^',
			KMOD_LALT:		'<!',
			KMOD_RALT:		'>!',
			KMOD_ALT:		'!',
		}
		self._buttons = button_map
		self._modifiers = modifier_map
		
	def start(self, rules):
		with open('remapping.ahk', 'w') as map_file:
			for r in rules:
				map_file.write(self._combo_to_ahk(r['key']) + "::\n")
				for p in r['productions']:
					map_file.write("Send {" + self._combo_to_ahk(p) + "}\n")
				map_file.write("Return\n\n")
		#self._ahk_proc = subprocess.Popen([self._ahk_command, 'remapping.ahk'])
		
	def end(self):
		self._kill_ahk()
		os.remove('remapping.ahk')
				
	def _combo_to_ahk(self, key_combo):
		ahk_str = ''
		for m in key_combo['modifiers']:
			ahk_str += self._modifiers[m]
		ahk_str += self._buttons[key_combo['button']]
		return ahk_str

	def _kill_ahk(self):
		for proc in psutil.process_iter():
			if proc.name() == "AutoHotkey.exe":
				proc.kill()

