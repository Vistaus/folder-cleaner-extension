# Folder Cleaner Extension
#
# Based on Folder Color extension by Marcos Alvarez Costales
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
        f = nautilus_file.pop()
        path = f.get_location().get_path()
        self.sort_files(path)
        
    def sort_by_ext(self, menu_item, nautilus_file):
        f = nautilus_file.pop()
        path = f.get_location().get_path()
        self.sort_files(path, by_extension=True)
        
    def sort_files(self, path, by_extension=False):
    
        dirs, files = get_files_and_folders(path, absolute_folders_paths=False)
        
        for f in files:
            content_type, val = Gio.content_type_guess(f)
            simple_file = Gio.File.new_for_path(f)
            name, ext = simple_file.get_basename().rsplit('.', 1)

            if not by_extension:
                destination_folder = Gio.File.new_for_path(path + '/' + content_type.split('/')[0].capitalize())
                ext = content_type.split('/')[0].capitalize()
            else:
                destination_folder = Gio.File.new_for_path(path + '/' + ext)

            destination_path = destination_folder.get_path() + '/' + simple_file.get_basename()
            destination_for_files = Gio.File.new_for_path(destination_path)

            if ext not in dirs:
                Gio.File.make_directory(destination_folder)
                simple_file.move(destination_for_files, Gio.FileCopyFlags.NONE)
                dirs.append(ext)
            else:
                simple_file.move(destination_for_files, Gio.FileCopyFlags.NONE)
    
def get_files_and_folders(folder, absolute_folders_paths=True):
    folder_list = []
    files_list = []

    path = Gio.File.new_for_path(folder)
    enumerator = path.enumerate_children(Gio.FILE_ATTRIBUTE_STANDARD_NAME, Gio.FileQueryInfoFlags.NONE)
    info = enumerator.next_file()
    while info is not None:
        if info.get_file_type() == Gio.FileType.DIRECTORY:
            if absolute_folders_paths:
                folder_path = path.get_path() + '/' + info.get_name()
            else:
                folder_path = info.get_name()
            folder_list.append(folder_path)
            info = enumerator.next_file()
        else:
            abs_path = path.get_path() + '/' + info.get_name()
            files_list.append(abs_path)
            info = enumerator.next_file()
     
    return folder_list, files_list


