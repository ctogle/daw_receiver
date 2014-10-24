import modular_core.libfundamental as lfu
lfu.USING_GUI = True
import modular_dr.gui.libqtgui_daw_receiver as praqg

if __name__ == '__main__':
  params = {'application':praqg._application_}
  lfu.initialize_gui(params)


