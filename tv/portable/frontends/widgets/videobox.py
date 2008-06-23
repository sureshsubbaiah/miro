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

"""Contains the videobox (the widget on the bottom of the right side with
video controls).
"""

from miro.frontends.widgets import imagepool
from miro.frontends.widgets import widgetutil
from miro.frontends.widgets import imagebutton
from miro.plat.frontends.widgets import widgetset
from miro.plat import resources

def format_time(time):
    return "%d:%02d" % divmod(int(round(time)), 60)

class PlaybackControls(widgetset.HBox):
    def __init__(self):
        widgetset.HBox.__init__(self, spacing=2)
        self.previous = self.make_button('skip_previous', True)
        self.stop = self.make_button('stop', False)
        self.play = self.make_button('play', False)
        self.forward = self.make_button('skip_forward', True)
        self.pack_start(widgetutil.align_middle(self.previous))
        self.pack_start(widgetutil.align_middle(self.stop))
        self.pack_start(widgetutil.align_middle(self.play))
        self.pack_start(widgetutil.align_middle(self.forward))

    def make_button(self, name, continous):
        if continous:
            button = imagebutton.ContinuousImageButton(name)
            button.set_delays(0.6, 0.3)
        else:
            button = imagebutton.ImageButton(name)
        return button

class ProgressTime(widgetset.DrawingArea):
    def __init__(self):
        widgetset.DrawingArea.__init__(self)
        self.current_time = None

    def size_request(self, layout):
        return (40, 13)

    def set_current_time(self, current_time):
        self.current_time = current_time
        self.queue_redraw()

    def draw(self, context, layout):
        if self.current_time is None:
            return
        layout.set_font(0.85)
        layout.set_text_color(widgetutil.WHITE)
        text = layout.textbox(format_time(self.current_time))
        width, height = text.get_size()
        text.draw(context, context.width-width, 2, width, height)

class ProgressTimeRemaining(widgetset.CustomButton):
    def __init__(self):
        widgetset.CustomButton.__init__(self)
        self.duration = self.current_time = None
        self.display_remaining = True

    def size_request(self, layout):
        return (50, 13)

    def set_current_time(self, current_time):
        self.current_time = current_time
        self.queue_redraw()

    def set_duration(self, duration):
        self.duration = duration
        self.queue_redraw()

    def toggle_display(self):
        self.display_remaining = not self.display_remaining
        self.queue_redraw()

    def draw(self, context, layout):
        if self.current_time is None or self.duration is None:
            return
        if self.display_remaining:
            text = '-' + format_time(self.duration - self.current_time)
        else:
            text = format_time(self.duration)
        layout.set_font(0.85)
        layout.set_text_color(widgetutil.WHITE)
        text = layout.textbox(text)
        width, height = text.get_size()
        text.draw(context, 10, 2, width, height)

    def draw_pressed(self, context, layout):
        # Maybe we should have a different style here for user feed back?
        self.draw(context, layout)

class ProgressSlider(widgetset.CustomSlider):
    def __init__(self):
        widgetset.CustomSlider.__init__(self)
        self.background_surface = \
                widgetutil.ThreeImageSurface('playback_track')
        self.progress_surface = \
                widgetutil.ThreeImageSurface('playback_track_progress')

    def is_horizontal(self):
        return True

    def is_continuous(self):
        return False

    def size_request(self, layout):
        return (60, 13)

    def slider_size(self):
        return 1

    def draw(self, context, layout):
        min, max = self.get_range()
        progress_width = int(round(self.get_value() / max * context.width))
        self.progress_surface.draw(context, 0, 0, progress_width)
        if progress_width == 0:
            self.background_surface.draw(context, 0, 0, context.width)
        else:
            self.background_surface.draw_right(context, progress_width, 0, 
                    context.width - progress_width)

class ProgressTimeline(widgetset.Background):
    def __init__(self):
        widgetset.Background.__init__(self)
        self.background = widgetutil.ThreeImageSurface('display')
        self.duration = self.current_time = None
        self.slider = ProgressSlider()
        self.time = ProgressTime()
        self.slider.connect('moved', self.on_slider_moved)
        self.remaining_time = ProgressTimeRemaining()
        self.remaining_time.connect('clicked', self.on_remaining_clicked)
        hbox = widgetset.HBox()
        hbox.pack_start(widgetutil.align_middle(self.time), expand=False, padding=5)
        hbox.pack_start(widgetutil.align_middle(self.slider), expand=True)
        hbox.pack_start(widgetutil.align_middle(self.remaining_time,
            left_pad=20, right_pad=5))
        self.add(widgetutil.align_middle(hbox))

    def on_remaining_clicked(self, widget):
        self.remaining_time.toggle_display()

    def on_slider_moved(self, slider, new_time):
        self.time.set_current_time(new_time)
        self.remaining_time.set_current_time(new_time)

    def set_duration(self, duration):
        self.slider.set_range(0, duration)
        self.slider.set_increments(5, min(20, duration / 20.0))
        self.remaining_time.set_duration(duration)

    def set_current_time(self, current_time):
        self.slider.set_value(current_time)
        self.time.set_current_time(current_time)
        self.remaining_time.set_current_time(current_time)

    def size_request(self, layout):
        return -1, self.background.height

    def draw(self, context, layout):
        self.background.draw(context, 0, 0, context.width)

class VolumeSlider(widgetset.CustomSlider):
    def __init__(self):
        widgetset.CustomSlider.__init__(self)
        self.set_range(0.0, 1.0)
        self.set_increments(0.05, 0.20)
        self.track = widgetutil.make_surface('volume_track')
        self.knob = widgetutil.make_surface('volume_knob')

    def is_horizontal(self):
        return True

    def is_continuous(self):
        return True

    def size_request(self, layout):
        return (self.track.width, self.knob.height)

    def slider_size(self):
        return self.knob.width

    def draw(self, context, layout):
        self.draw_track(context)
        self.draw_knob(context)

    def draw_track(self, context):
        y = (context.height - self.track.height) / 2
        self.track.draw(context, 0, y, self.track.width, self.track.height)

    def draw_knob(self, context):
        x_max = context.width - self.slider_size()
        slider_x = int(round(self.get_value() * x_max))
        slider_y = (context.height - self.knob.height) / 2
        self.knob.draw(context, slider_x, slider_y, self.knob.width,
                self.knob.height)

class VideoBox(widgetset.Background):
    def __init__(self):
        widgetset.Background.__init__(self)
        self.controls = PlaybackControls()
        self.timeline = ProgressTimeline()
        self.volume_slider = VolumeSlider()
        self.time_slider = self.timeline.slider

        self.timeline.set_duration(310)
        self.timeline.set_current_time(50)
        self.volume_slider.set_value(0.4)

        self.image = widgetutil.make_surface('wtexture')
        self.image_inactive = widgetutil.make_surface('wtexture_inactive')

        hbox = widgetset.HBox(spacing=35)
        hbox.pack_start(self.controls, expand=False)
        hbox.pack_start(widgetutil.align_middle(self.timeline), expand=True)
        volume_image = imagepool.get(
                resources.path('wimages/volume_high.png'))
        volume_display = widgetset.ImageDisplay(volume_image)
        volume_hbox = widgetset.HBox(spacing=5)
        volume_hbox.pack_start(widgetutil.align_middle(volume_display))
        volume_hbox.pack_start(widgetutil.align_middle(self.volume_slider))
        hbox.pack_start(volume_hbox)
        self.add(widgetutil.align_middle(hbox, 0, 0, 30, 30))

    def size_request(self, layout):
        return (0, 63)

    def draw(self, context, layout):
        if self.get_window().is_active():
            image = self.image
        else:
            image = self.image_inactive
        image.draw(context, 0, 0, context.width, context.height)

    def is_opaque(self):
        return True
