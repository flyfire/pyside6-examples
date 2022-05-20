#############################################################################
##
## Copyright (C) 2022 The Qt Company Ltd.
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

from PySide6.QtCore import QObject, Property
from PySide6.QtGui import QColor
from PySide6.QtQml import QmlAnonymous, QmlElement

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "examples.grouped.people"
QML_IMPORT_MAJOR_VERSION = 1


@QmlAnonymous
class ShoeDescription(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._brand = ''
        self._size = 0
        self._price = 0
        self._color = QColor()

    @Property(str)
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, b):
        self._brand = b

    @Property(int)
    def size(self):
        return self._size

    @size.setter
    def size(self, s):
        self._size = s

    @Property(float)
    def price(self):
        return self._price

    @price.setter
    def price(self, p):
        self._price = p

    @Property(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, c):
        self._color = c


@QmlAnonymous
class Person(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._name = ''
        self._shoe = ShoeDescription()

    @Property(str)
    def name(self):
        return self._name

    @name.setter
    def name(self, n):
        self._name = n

    @Property(ShoeDescription)
    def shoe(self):
        return self._shoe


@QmlElement
class Boy(Person):
    def __init__(self, parent=None):
        super().__init__(parent)


@QmlElement
class Girl(Person):
    def __init__(self, parent=None):
        super().__init__(parent)
