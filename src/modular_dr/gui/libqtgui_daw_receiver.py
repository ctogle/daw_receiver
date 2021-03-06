import modular_core.fundamental as lfu
import modular_core.gui.libqtgui as lqg
lgm = lqg.lgm
lgd = lqg.lgd
lgb = lqg.lgb
import modular_dr.libdawcontrol as ldc

import os
import sys

class application_daw_rec(lqg.application):
    
    gear_icon = lfu.get_resource_path('gear.png')
    _content_ = [ldc.motor_manager()]

    def __init__(self, *args, **kwargs):
        lqg.application.__init__(self, *args, **kwargs)
        lqg.application.setStyle(lgb.create_style('plastique'))
        x, y = lfu.convert_pixel_space(1024, 256)
        x_size, y_size = lfu.convert_pixel_space(512, 768)
        self._standards_ = {
                'title' : 'DAW Receiver', 
                'geometry' : (x, y, x_size, y_size), 
                'window_icon' : self.gear_icon}
        lqg._window_.apply_standards(self._standards_)

def initialize():lqg.initialize_app(application_daw_rec)







