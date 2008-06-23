# Miro - an RSS based video player application
# Copyright (C) 2005-2008 Participatory Culture Foundation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
#
# In addition, as a special exception, the copyright holders give
# permission to link the code of portions of this program with the OpenSSL
# library.
#
# You must obey the GNU General Public License in all respects for all of
# the code used other than OpenSSL. If you modify file(s) with this
# exception, you may extend this exception to your version of the file(s),
# but you are not obligated to do so. If you do not wish to do so, delete
# this exception statement from your version. If you delete this exception
# statement from all source files in the program, then also delete it here.

"""GTK Hacks.  GTK Code that can't be done in PyGTK for whatever reason."""

cdef extern from "gtk/gtk.h":
    ctypedef struct GtkWidget
    ctypedef struct GtkTreeView
    ctypedef struct GtkTreePath
    ctypedef struct GObject
    ctypedef int gint
    ctypedef unsigned long gulong
    ctypedef unsigned int guint
    ctypedef char gchar
    ctypedef void * gpointer
    ctypedef void * GCallback
    ctypedef enum GtkTreeViewDropPosition:
            GTK_TREE_VIEW_DROP_BEFORE,
            GTK_TREE_VIEW_DROP_AFTER,
            GTK_TREE_VIEW_DROP_INTO_OR_BEFORE,
            GTK_TREE_VIEW_DROP_INTO_OR_AFTER
    void gtk_tree_view_set_drag_dest_row(GtkTreeView *tree_view,
                                         GtkTreePath *path,
                                         GtkTreeViewDropPosition pos)

cdef extern from "pygobject.h":
    ctypedef struct PyGObject:
        GObject * obj

cdef GtkWidget* get_gtk_widget(object pygtk_widget):
    cdef PyGObject *pygobject
    pygobject = <PyGObject *>pygtk_widget
    return <GtkWidget*>(pygobject.obj)

def unset_tree_view_drag_dest_row(object py_tree_view):
    cdef GtkTreeView* tree_view 
    tree_view = <GtkTreeView*>get_gtk_widget(py_tree_view)
    gtk_tree_view_set_drag_dest_row(tree_view, NULL, GTK_TREE_VIEW_DROP_BEFORE)
