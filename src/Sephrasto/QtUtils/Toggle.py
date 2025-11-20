from PySide6.QtCore import Qt, QRectF, QPointF, QSize, Property, Signal, QPropertyAnimation, QEasingCurve, QEvent
from PySide6.QtGui import QColor, QPainter, QBrush, QPen, QPalette
from PySide6.QtWidgets import QWidget, QSizePolicy, QApplication

class Toggle(QWidget):
    toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Default colors
        pal = QApplication.palette()

        # Default colors from palette
        self._handle_border_pen = QPen(pal.color(QPalette.Dark))
        self._handle_border_pen.setWidthF(1.0)

        self._bar_color = pal.color(QPalette.Midlight)
        self._handle_color = pal.color(QPalette.Base)
        self._checked_color = pal.color(QPalette.Highlight)
        self._shadow_color = pal.color(QPalette.Mid)

        self._checked = False
        self._handle_pos = 0.0
        self._hovered = False
        self._pressed = False

        self._preferred_height = 28
        self._handle_radius_frac = 0.24
        self._bar_height_frac = 0.40

        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFocusPolicy(Qt.StrongFocus)

        self._transparent_pen = QPen(Qt.transparent)

        self._anim = QPropertyAnimation(self, b"handlePos")
        self._anim.setDuration(140)
        self._anim.setEasingCurve(QEasingCurve.InOutQuad)

    def changeEvent(self, event):
        if event.type() == QEvent.EnabledChange:
            self.update()
        super().changeEvent(event)

    # ---------------------------
    # Hover / pressed
    # ---------------------------
    def enterEvent(self, event):
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self._pressed = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._pressed = True
            self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self._pressed:
                self.toggle()
            self._pressed = False
            self.update()
        super().mouseReleaseEvent(event)

    # ---------------------------
    # QSS properties
    # ---------------------------
    def getBarColor(self): return self._bar_color
    def setBarColor(self, c):
        col = QColor(c)
        if col.isValid():
            self._bar_color = col
            self.update()
    barColor = Property(QColor, getBarColor, setBarColor)

    def getHandleColor(self): return self._handle_color
    def setHandleColor(self, c):
        col = QColor(c)
        if col.isValid():
            self._handle_color = col
            self.update()
    handleColor = Property(QColor, getHandleColor, setHandleColor)

    def getCheckedColor(self): return self._checked_color
    def setCheckedColor(self, c):
        col = QColor(c)
        if col.isValid():
            self._checked_color = col
            self.update()
    checkedColor = Property(QColor, getCheckedColor, setCheckedColor)

    # ---------------------------
    # Public API
    # ---------------------------
    def isChecked(self): return self._checked

    def setCheckedInstant(self, on):
        on = bool(on)
        if self._checked == on:
            return
        self._checked = on
        self._handle_pos = 1.0 if on else 0.0
        self.toggled.emit(on)
        self.update()

    def setChecked(self, on):
        on = bool(on)
        if self._checked == on:
            return

        self._checked = on

        # animated slide:
        self._anim.stop()
        self._anim.setStartValue(self._handle_pos)
        self._anim.setEndValue(1.0 if on else 0.0)
        self._anim.start()

        self.toggled.emit(on)

    def toggle(self): self.setChecked(not self._checked)

    # ---------------------------
    # Size hints
    # ---------------------------
    def sizeHint(self):
        h = self._preferred_height
        r = self._handle_radius_frac * h
        width = int(2 * r + 2.4 * r)
        return QSize(width, h)

    def minimumSizeHint(self):
        h = max(16, int(self._preferred_height * 0.6))
        r = self._handle_radius_frac * h
        width = int(2 * r + 2.4 * r)
        return QSize(width, h)

    # ---------------------------
    # Painting
    # ---------------------------
    def paintEvent(self, event):
        rect = QRectF(self.contentsRect())
        H = rect.height()
        if H <= 0: return

        handle_r = self._handle_radius_frac * H
        bar_h = self._bar_height_frac * H
        trail = max(0.0, rect.width() - 2 * handle_r)
        bar_w = max(1.0, trail + handle_r)

        barRect = QRectF(0, 0, bar_w, bar_h)
        barRect.moveCenter(rect.center())
        rounding = barRect.height() / 2.0

        x_start = rect.left() + handle_r
        xPos = x_start + trail * self._handle_pos

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # hover effect: adjust bar color
        hovered = self._hovered and self.isEnabled()
        if self._checked:
            bar_color = self._checked_color  # default on-state
            if hovered:
                bar_color = self._checked_color.lighter(120)  # hover effect
        else:
            bar_color = self._bar_color
            if hovered:
                bar_color = self._bar_color.lighter(110)

        if not self.isEnabled():
            bar_color = bar_color.lighter(80)

        # Draw glow behind the bar
        glow_radius = 1.0  # how far the glow extends
        glow_color = bar_color.lighter(120)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(glow_color))

        glow_rect = QRectF(barRect)
        glow_rect.adjust(-glow_radius, -glow_radius, glow_radius, glow_radius)  # slightly bigger
        p.drawRoundedRect(glow_rect, rounding + glow_radius, rounding + glow_radius)

        # Draw bar
        p.setPen(self._transparent_pen)
        p.setBrush(QBrush(bar_color))
        p.drawRoundedRect(barRect, rounding, rounding)

        # Draw handle with border
        handle_color = self._handle_color
        if not self.isEnabled():
            handle_color = handle_color.lighter(80)
        p.setBrush(QBrush(handle_color))
        p.setPen(self._handle_border_pen)
        p.drawEllipse(QPointF(xPos, barRect.center().y()), handle_r, handle_r)

        p.end()

    # ---------------------------
    # Animation-ready property
    # ---------------------------
    def getHandlePos(self): return self._handle_pos
    def setHandlePos(self, v):
        self._handle_pos = max(0.0, min(1.0, float(v)))
        self.update()
    handlePos = Property(float, getHandlePos, setHandlePos)
