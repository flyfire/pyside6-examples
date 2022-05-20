
#############################################################################
##
## Copyright (C) 2016 The Qt Company Ltd.
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

"""PySide6 port of the qml/tutorials/extending-qml/chapter5-listproperties example from Qt v5.x"""

import os
from pathlib import Path
import sys

from PySide6.QtCore import Property, QUrl
from PySide6.QtGui import QGuiApplication, QPen, QPainter, QColor
from PySide6.QtQml import QmlElement, ListProperty
from PySide6.QtQuick import QQuickPaintedItem, QQuickView, QQuickItem

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "Charts"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class PieSlice (QQuickPaintedItem):
    def __init__(self, parent=None):
        QQuickPaintedItem.__init__(self, parent)
        self._color = QColor()
        self._fromAngle = 0
        self._angleSpan = 0

    @Property(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @Property(int)
    def fromAngle(self):
        return self._angle

    @fromAngle.setter
    def fromAngle(self, value):
        self._fromAngle = value

    @Property(int)
    def angleSpan(self):
        return self._angleSpan

    @angleSpan.setter
    def angleSpan(self, value):
        self._angleSpan = value

    def paint(self, painter):
        pen = QPen(self._color, 2)
        painter.setPen(pen)
        painter.setRenderHints(QPainter.Antialiasing, True)
        painter.drawPie(self.boundingRect().adjusted(1, 1, -1, -1), self._fromAngle * 16, self._angleSpan * 16)


@QmlElement
class PieChart (QQuickItem):
    def __init__(self, parent=None):
        QQuickItem.__init__(self, parent)
        self._name = u''
        self._slices = []

    @Property(str)
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def appendSlice(self, _slice):
        _slice.setParentItem(self)
        self._slices.append(_slice)

    slices = ListProperty(PieSlice, appendSlice)


if __name__ == '__main__':
    app = QGuiApplication(sys.argv)

    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    qml_file = os.fspath(Path(__file__).resolve().parent / 'app.qml')
    view.setSource(QUrl.fromLocalFile(qml_file))
    if view.status() == QQuickView.Error:
        sys.exit(-1)
    view.show()
    res = app.exec()
    # Deleting the view before it goes out of scope is required to make sure all child QML instances
    # are destroyed in the correct order.
    del view
    sys.exit(res)
