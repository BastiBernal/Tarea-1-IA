from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QGraphicsOpacityEffect
from PySide6.QtGui import QPixmap, QShowEvent
from PySide6.QtCore import QPropertyAnimation, Qt, QEasingCurve
from pathlib import Path
import os

class DeadScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 180);")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        assets_path = os.path.join(Path(__file__).parent.parent, 'assets', 'img', 'you_died.jpg')
        pixmap = QPixmap(str(assets_path))
        self._orig_pixmap = pixmap if not pixmap.isNull() else None

        if self._orig_pixmap is not None:
            self.label.setPixmap(self._orig_pixmap.scaled(600, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.label.setText("YOU DIED")
            self.label.setStyleSheet("font: bold 36px; color: red;")

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)

        layout.addWidget(self.label)

        self._animation_started = False
        self.animation = None

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        if not self._animation_started:
            self._animation_started = True
            self.start_fade_in_animation()

    def start_fade_in_animation(self):
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity", self)
        self.animation.setDuration(4000)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.start()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._orig_pixmap is not None:
            self.label.setPixmap(
                self._orig_pixmap.scaled(
                    self.width(),
                    self.height(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

# Test
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = DeadScreen()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())