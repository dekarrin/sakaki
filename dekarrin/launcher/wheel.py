import pygame

class Wheel(pygame.sprite.DirtySprite):
	"""Hold all wheel data and display the current wheel."""

	def __init__(self, wheel_data, root_wheel_id, size, spacing, font_normal, font_select):
		"""Construct a new Wheel.
		
		
		wheel_data - All data read from the wheels dir.
		
		root_wh
		
		"""
		super(Wheel, self).__init__()
		self.image = pygame.Surface(
		self._current = None
		self._position = 0
		self._root_wheel_id = root_wheel_id
		self._wheels = dict()
		for wheel in wheel_data:
			self._wheels[wheel['id']] = wheel
		self._init_wheels()
		self.change_to_root()

	def _init_wheels(self):
		for id in self._wheels:
			self._assign_subitems(id)
		for id in self._wheels:
			if 'set' in self._wheels[id]:
				del self._wheels[id]['set']
			if 'items' not in self._wheels[id]:
				self._wheels[id]['items'] = list()
				
	def _assign_subitems(self, wheel_id):
		wheel = self._wheels[wheel_id]
		if 'set' in wheel:
				return
		wheel['set'] = True
		parent_id = wheel['parent']
		if parent_id in self._wheels:
			wheel['parent'] = self._wheels[parent_id]
			if wheel_id != self._root_wheel_id:
				if 'items' not in self._wheels[parent_id]:
					self._wheels[parent_id]['items'] = list()
				self._wheels[parent_id]['items'].append(wheel)
				self._assign_subitems(parent_id)
		else:
			print "Warning! Wheel '%s' links to nonexistant parent '%s'. Wheel not linked." % (wheel_id, parent_id)

	def change_to_root(self):
		self.change(self._root_wheel_id)

	def change(self, wheel_id):
		self._current = self._wheels[wheel_id]
		self._position = 0

	def next(self):
		if self.subitems_count() > 0:
			self._position = (self._position + 1) % len(self._current['items'])

	def prev(self):
		if self.subitems_count() > 0:
			self._position = (self._position - 1) % len(self._current['items'])

	def advance(self):
		if self.subitems_count() > 0:
			id = self._current['items'][self._position]['id']
			self.change(id)

	def backtrack(self):
		"""Go to the previous wheel."""
		id = self._current['parent']['id']
		self.change(id)
			
	def subitems_count(self):
		return len(self._current['items'])
			
	def get_item_title(self, position=0):
		"""Get the text of the menu item."""
		if self.subitems_count() > 0:
			pos = (self._position + position) % self.subitems_count()
			return self._current['items'][pos]['title']
		else:
			return None