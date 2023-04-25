import tkinter as tk
from logging import getLogger
from pathlib import Path
import customtkinter
from PIL import Image
from dcspy import LCD_TYPES, config
from dcspy.utils import save_cfg

LOG = getLogger(__name__)


class DcspyGui(tk.Frame):
    """Tkinter GUI."""
    def __init__(self, master: customtkinter.CTk) -> None:
        """
        Create basic GUI for dcspy application.

        :param master: Top level widget
        """
        super().__init__(master)
        self.master = master
        self.cfg_file = Path(__file__).resolve().with_name('config.yaml')
        self.status_txt = tk.StringVar()
        self.lcd_type = tk.StringVar()
        self._init_widgets()

    def _init_widgets(self) -> None:
        """Init all GUI widgets."""
        self.master.grid_columnconfigure(index=0, weight=0)
        self.master.grid_columnconfigure(index=1, weight=1)
        self._sidebar()
        tabview = customtkinter.CTkTabview(master=self.master, width=250, height=400, state=tk.ACTIVE)
        tabview.grid(column=1, row=1, padx=30, pady=30, sticky=tk.N + tk.E + tk.S + tk.W)
        tabview.add('Keyboards')
        self._keyboards(tabview)
        status = customtkinter.CTkLabel(master=self.master, textvariable=self.status_txt)
        status.grid(row=4, column=0, columnspan=2, sticky=tk.SE, padx=7)

    def _sidebar(self) -> None:
        """Configure sidebar of GUI."""
        sidebar_frame = customtkinter.CTkFrame(master=self.master, width=70, corner_radius=0)
        sidebar_frame.grid(row=0, column=0, rowspan=4, sticky=tk.N + tk.S + tk.W)
        sidebar_frame.grid_rowconfigure(4, weight=1)
        logo_label = customtkinter.CTkLabel(master=sidebar_frame, text='Settings', font=customtkinter.CTkFont(size=20, weight='bold'))
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        logo_path = Path(__file__).resolve().with_name('dcspy.png')
        logo_icon = customtkinter.CTkImage(Image.open(logo_path), size=(130, 60))
        logo_label = customtkinter.CTkLabel(master=sidebar_frame, text='', image=logo_icon)
        logo_label.grid(row=4, column=0, sticky=tk.W + tk.E)
        close = customtkinter.CTkButton(master=sidebar_frame, text='Close', command=self.master.destroy)
        close.grid(row=7, column=0, padx=20, pady=10)

    def _keyboards(self, tabview: customtkinter.CTkTabview) -> None:
        """Configure keyboard tab GUI."""
        for i, text in enumerate(LCD_TYPES):
            icon_path = Path(__file__).resolve().with_name(LCD_TYPES[text]['icon'])
            icon = customtkinter.CTkImage(Image.open(icon_path), size=(103, 70))
            label = customtkinter.CTkLabel(master=tabview.tab('Keyboards'), text='', image=icon)
            label.grid(row=i, column=0)
            rb_lcd_type = customtkinter.CTkRadioButton(master=tabview.tab('Keyboards'), text=text, variable=self.lcd_type, value=text, command=self._lcd_type_selected)
            rb_lcd_type.grid(row=i, column=1)
            if config.get('keyboard') == text:
                rb_lcd_type.select()

    def _save_cfg(self) -> None:
        """Save configuration from GUI."""
        cfg = {'keyboard': self.lcd_type.get(),}
        save_cfg(cfg_dict=cfg, filename=self.cfg_file)
        self.status_txt.set(f'Saved: {self.cfg_file}')

    def _lcd_type_selected(self) -> None:
        """Handling selected LCD type."""
        keyboard = self.lcd_type.get()
        LOG.debug(f'Logitech {keyboard} selected')
        self.status_txt.set(f'Logitech {keyboard} selected')
        self._save_cfg()
