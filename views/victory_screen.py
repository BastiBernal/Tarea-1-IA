from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PySide6.QtGui import QShowEvent, QMovie
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QSoundEffect
from pathlib import Path


class VictoryScreen(QWidget):
	"""Pantalla de victoria, similar a DeadScreen pero sin animación (aparición instantánea)."""

	def __init__(self, parent=None):
		super().__init__(parent)

		self.sfx = QSoundEffect(self)
		wav_path = (Path(__file__).resolve().parents[1] / 'assets' / 'sounds' / 'victory.wav')
		if wav_path.exists():
			self.sfx.setSource(QUrl.fromLocalFile(str(wav_path)))
		self.sfx.setVolume(1.0)

		layout = QVBoxLayout(self)
		layout.setContentsMargins(0, 0, 0, 0)

		self.label = QLabel(self)
		self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

		self._movie = None
		self._orig_pixmap = None
		gif_path = Path(__file__).resolve().parents[1] / 'assets' / 'img' / 'confetti.gif'
		if gif_path.exists():
			try:
				self._movie = QMovie(str(gif_path))
				self.label.setMovie(self._movie)
			except Exception:
				self._movie = None

		if self._movie is None and self._orig_pixmap is not None:
			self.label.setPixmap(
				self._orig_pixmap.scaled(600, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
			)
		elif self._movie is None and self._orig_pixmap is None:
			self.label.setText("VICTORY!")
			self.label.setStyleSheet("font: bold 36px; color: #00ff88;")

		layout.addWidget(self.label)

	def showEvent(self, event: QShowEvent) -> None:
		super().showEvent(event)
		try:
			self.sfx.stop()
			self.sfx.play()
		except Exception:
			pass
		try:
			if self._movie is not None:
				self._movie.setScaledSize(self.size())
				self._movie.start()
		except Exception:
			pass

	def resizeEvent(self, event):
		super().resizeEvent(event)
		if self._movie is not None:
			try:
				self._movie.setScaledSize(self.size())
			except Exception:
				pass
		elif self._orig_pixmap is not None:
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
	w = VictoryScreen()
	w.resize(600, 400)
	w.show()
	sys.exit(app.exec())

