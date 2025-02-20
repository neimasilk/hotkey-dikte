"""User interface components for Hotkey Dikte application.

This module handles the system tray icon and menu functionality.
"""

from typing import Callable, Dict
from PIL import Image, ImageDraw
import pystray
from threading import Event, Thread

class TrayIcon:
    """System tray icon manager."""
    def __init__(self, hotkey: str):
        self.icon: pystray.Icon = None
        self.status = "idle"
        self.hotkey = hotkey
        self.update_event = Event()
        
        # Generate icon images
        self.images = {
            "idle": self._create_image("green"),
            "recording": self._create_image("red"),
            "processing": self._create_image("yellow")
        }
        
        self._init_menu()
        
    def _create_image(self, color: str) -> Image.Image:
        """Create tray icon image.

        Args:
            color: Color of the microphone icon.

        Returns:
            PIL Image object with the icon.
        """
        image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        dc = ImageDraw.Draw(image)
        
        # Draw microphone
        dc.rectangle((28, 40, 36, 48), fill=color)
        dc.ellipse((26, 38, 38, 42), fill=color)
        dc.rectangle((24, 16, 40, 40), fill=color)
        dc.ellipse((24, 14, 40, 18), fill=color)
        dc.ellipse((24, 38, 40, 42), fill=color)
        
        if color == "red":  # Recording state
            for i in range(3):
                offset = (i + 1) * 6
                dc.arc((20-offset, 12-offset, 44+offset, 36+offset), 
                      -60, 60, fill=color, width=2)
        
        return image
        
    def _init_menu(self) -> None:
        """Initialize the tray icon menu."""
        self.menu = pystray.Menu(
            pystray.MenuItem(
                "Hotkey Dikte",
                lambda: None,
                enabled=False
            ),
            pystray.MenuItem(
                f"Hotkey: {self.hotkey}",
                lambda: None,
                enabled=False
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Status: " + self.status.capitalize(),
                lambda: None,
                enabled=False
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Keluar",
                self.exit_program
            )
        )
    
    def set_exit_callback(self, callback: Callable[[], None]) -> None:
        """Set callback for exit menu item.

        Args:
            callback: Function to call when exit is selected.
        """
        self._exit_callback = callback
            
    def update_status(self, status: str) -> None:
        """Update tray icon status.

        Args:
            status: New status to display ('idle', 'recording', or 'processing').
        """
        self.status = status
        if self.icon:
            self.icon.icon = self.images[status]
            self.icon.title = f"Hotkey Dikte - {status.capitalize()}"
            
    def exit_program(self, _=None) -> None:
        """Handle exit menu selection."""
        if hasattr(self, '_exit_callback'):
            self._exit_callback()
        self.icon.stop()
        
    def run(self) -> None:
        """Start the system tray icon."""
        self.icon = pystray.Icon(
            "hotkey_dikte",
            icon=self.images["idle"],
            menu=self.menu,
            title="Hotkey Dikte - Ready"
        )
        self.icon.run()

    def start(self) -> None:
        """Start the tray icon in a separate thread."""
        tray_thread = Thread(target=self.run, daemon=True)
        tray_thread.start()