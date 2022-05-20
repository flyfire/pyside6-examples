#############################################################################
##
## Copyright (C) 2021 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of the Qt for Python examples of the Qt Toolkit.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of The Qt Company Ltd nor the names of its
##     contributors may be used to endorse or promote products derived
##     from this software without specific prior written permission.
##
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
## $QT_END_LICENSE$
##
#############################################################################

from pathlib import Path
import sys

from PySide6.QtCore import (QItemSelection, QLibraryInfo, QLocale, QTranslator,
                            Qt, Slot)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QListWidget,
                               QMainWindow, QWidget)


import linguist_rc


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        file_menu = self.menuBar().addMenu(self.tr("&File"))
        quit_action = file_menu.addAction(self.tr("Quit"))
        quit_action.setShortcut(self.tr("CTRL+Q"))
        quit_action.triggered.connect(self.close)
        help_menu = self.menuBar().addMenu(self.tr("&Help"))
        about_qt_action = help_menu.addAction(self.tr("About Qt"))
        about_qt_action.triggered.connect(qApp.aboutQt)

        self._list_widget = QListWidget()
        self._list_widget.setSelectionMode(QAbstractItemView.MultiSelection)
        self._list_widget.selectionModel().selectionChanged.connect(self.selection_changed)
        self._list_widget.addItem("C++")
        self._list_widget.addItem("Java")
        self._list_widget.addItem("Python")
        self.setCentralWidget(self._list_widget)

    @Slot(QItemSelection, QItemSelection)
    def selection_changed(self, selected, deselected):
        count = len(self._list_widget.selectionModel().selectedRows())
        message = self.tr("%n language(s) selected", "", count)
        self.statusBar().showMessage(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    translator = QTranslator(app)
    if translator.load(QLocale.system(), 'qtbase', '_', path):
        app.installTranslator(translator)
    translator = QTranslator(app)
    path = ':/translations'
    if translator.load(QLocale.system(), 'example', '_', path):
        app.installTranslator(translator)

    window = Window()
    window.show()
    sys.exit(app.exec())
