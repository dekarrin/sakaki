import pygame

class Wheel(object):
	"""Hold all wheel data and display the current wheel."""

	def __init__(self, wheel_data, root_wheel_id, size, spacing, font_normal, font_select):
		"""Construct a new Wheel.
		
		
		wheel_data - All data read from the wheels dir.
		
		root_wheel_id - The id of the wheel that should be shown at start.
		
		size - tuple containing width and height.
		
		spacing - number of pixels between each menu item.
		
		font_normal - tuple containing name of font face and size of font for unselected
		menu items.
		
		font_select - same as above, but for the selected font.
		"""
		self._current = None
		self._position = 0
		self._root_wheel_id = root_wheel_id
		self._wheels = {}
		self.group = pygame.sprite.RenderUpdates()
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
		self._recreate_sprites()

	def next(self):
		if self.subitems_count() > 0:
			self._position = (self._position + 1) % len(self._current['items'])
			self._reposition_sprites()

	def prev(self):
		if self.subitems_count() > 0:
			self._position = (self._position - 1) % len(self._current['items'])
			self._reposition_sprites()

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

	def _recreate_sprites(self):
		self.group.empty()
		

class WheelItem(pygame.sprite.DirtySprite):
	"""Display a single item from the wheel."""

	def __init__(self, text, color, font):
		"""Creates a new WheelItem.
		
		text - the text that the item should display.
		color - the color of the text.
		font - tuple that contains name of font face and font size.
		"""
		self.image = pygame.font.Font(font[0], font[1]).render(text, True, color)
		self.rect = self.image.get_rect()
		self._oldx = self.rect.x
		self._oldy = self.rect.y
		self._oldface = font[0]
		self._oldsize = font[1]
		self._oldtext = text
		self._oldcolor = color
		self._is_recooked = False
		self.dirty = 1

	def update(self):
		if self._is_moved() or self._is_recooked:
			self.dirty = 1
			self._oldx = self.rect.x
			self._oldy = self.rect.y
		
	def set_font_face(self, face):
		if self._oldface != face:
			self._oldface = face
			self._cook()

	def set_font_size(self, size):
		if self._oldsize != size:
			self._oldsize = size
			self._cook()

	def set_color(self, color):
		if self._oldcolor != color:
			self._oldcolor = color
			self._cook()

	def set_text(self, text):
		if self._oldtet != text
			self._oldtext = text
			self._cook()

	def _cook(self):
		currx = self.rect.x
		curry = self.rect.y
		self.image = pygame.fong.Font(self._oldface, self._oldsize).render(self._oldtext, True, self._oldcolor)
		self.rect = self.image.get_rect()
		self.rect.x = currx
		self.rect.y = curry
		self._is_recooked = True

	def _is_moved():
		movedy = (self._oldy is not self.rect.y)
		movedx = (self._oldx is not self.rect.x)
		return movedy or moved x

