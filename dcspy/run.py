from logging import getLogger
from pathlib import Path
import customtkinter
from dcspy import config
from dcspy.tk_gui import DcspyGui

LOG = getLogger(__name__)


def run():
    """Function to start DCSpy GUI."""
    if config['show_gui']:
        root = customtkinter.CTk()
        width, height = 770, 500
        root.geometry(f'{width}x{height}')
        root.minsize(width=width, height=height)
        dcspy_ico = Path(__file__).resolve().with_name('dcspy.ico')
        root.iconbitmap(dcspy_ico)
        root.title('DCSpy')
        DcspyGui(master=root)
        root.mainloop()


if __name__ == '__main__':
    run()
