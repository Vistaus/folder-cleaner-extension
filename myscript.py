# Folder Cleaner Extension
#
# Folder Cleaner Extension is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# Folder Cleaner Extension is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Folder Color; if not, see http://www.gnu.org/licenses
# for more information.

import os, gettext
import gi
gi.require_version('Nautilus', '3.0')
from gi.repository import Nautilus, GObject, Gio

# i18n
gettext.textdomain('folder-color-common')
_ = gettext.gettext

class MyScriptMenu(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        GObject.Object.__init__(self)
        self.all_are_directories = True
        self.all_are_files = True
    
    def get_file_items(self, window, items):
        if not self._check_generate_menu(items):
            return
        
        return self._generate_menu(items)
    
    def _check_generate_menu(self, items):
        if not len(items):
            return False
        
        self.all_are_directories = True
        self.all_are_files = True
        for item in items:
            if item.get_uri_scheme() != 'file':
                return False
            
            if item.is_directory():
                #print('is dir')
                self.all_are_files = False
            else:
                #print('is file')
                return False
        
        return True
    
    def _generate_menu(self, items):
        if self.all_are_directories:
            if len(items) > 1:
                return
            
            top_menuitem = Nautilus.MenuItem(name='MyScriptMenu::Top', label=_("Sort files"))
            submenu = Nautilus.Menu()
            top_menuitem.set_submenu(submenu)
            
            item = Nautilus.MenuItem(name="name", label="By type")
            item.connect('activate', self.sort_by_type, items)
            submenu.append_item(item)
            
            item2 = Nautilus.MenuItem(name="name", label="By extension")
            item2.connect('activate', self.sort_by_ext, items)
            submenu.append_item(item2)
            
            return top_menuitem,
            
        else:
            print("files don't support")
            return 
        
    def sort_by_type(self, menu_item, nautilus_file):
        self.sort_files()
        
    def sort_by_ext(self, menu_item, nautilus_file):
        self.sort_files(by_extension=True)
        
    def sort_files(self, by_extension=False):
        if by_extension:
            print('by_ext')
        else:
            print('by_type')

