from PyQt5.QtWidgets import QDesktopWidget

def center_on_screen(window) -> None:
    """Centra la ventana en la pantalla principal."""
    screen = QDesktopWidget().screenGeometry()
    size = window.geometry()
    x = (screen.width() - size.width()) // 2
    y = (screen.height() - size.height()) // 2
    window.move(x, y)
