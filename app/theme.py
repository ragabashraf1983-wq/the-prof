from __future__ import annotations

DARK_STYLESHEET = """
QWidget {
    background-color: #11151c;
    color: #e6e8ee;
    font-size: 13px;
}
QMainWindow, QFrame#Sidebar {
    background-color: #0d1117;
}
QPushButton {
    background-color: #1f2a36;
    border: 1px solid #314154;
    border-radius: 6px;
    padding: 6px 10px;
}
QPushButton:hover {
    background-color: #273544;
}
QPushButton:checked {
    background-color: #35506b;
}
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QListWidget, QTreeWidget, QTableWidget {
    background-color: #161b22;
    border: 1px solid #2f3945;
    border-radius: 6px;
    padding: 5px;
    selection-background-color: #35506b;
}
QTabWidget::pane {
    border: 1px solid #2f3945;
}
QTabBar::tab {
    background: #161b22;
    border: 1px solid #2f3945;
    padding: 8px 12px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background: #273544;
}
QHeaderView::section {
    background-color: #1a2029;
    padding: 6px;
    border: 1px solid #2f3945;
}
QStatusBar {
    background: #0d1117;
}
QScrollArea {
    border: none;
}
QLabel#TitleLabel {
    font-size: 20px;
    font-weight: bold;
}
QLabel#SubtitleLabel {
    color: #9fb0c3;
}
"""
