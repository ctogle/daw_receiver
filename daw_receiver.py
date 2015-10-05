import modular_core.fundamental as lfu
#import modular_dr.gui.libqtgui_daw_receiver as praqg

if __name__ == '__main__':
    lfu.using_gui = True
    lfu.set_gui_pack('modular_dr.gui.libqtgui_daw_receiver')
    lfu.gui_pack.initialize()


