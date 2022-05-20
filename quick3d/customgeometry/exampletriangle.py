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

import numpy as np
from PySide6.QtCore import Property, Signal
from PySide6.QtGui import QVector3D
from PySide6.QtQml import QmlElement
from PySide6.QtQuick3D import QQuick3DGeometry

QML_IMPORT_NAME = "ExampleTriangleGeometry"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class ExampleTriangleGeometry(QQuick3DGeometry):

    normalsChanged = Signal()
    normalXYChanged = Signal()
    uvChanged = Signal()
    uvAdjustChanged = Signal()

    def __init__(self, parent=None):
        QQuick3DGeometry.__init__(self, parent)
        self._hasNormals = False
        self._normalXY = 0.0
        self._hasUV = False
        self._uvAdjust = 0.0

        self.updateData()

    @Property(bool, notify=normalsChanged)
    def normals(self):
        return self._hasNormals

    @normals.setter
    def normals(self, enable):
        if self._hasNormals == enable:
            return

        self._hasNormals = enable
        self.normalsChanged.emit()
        self.updateData()
        self.update()

    @Property(float, notify=normalXYChanged)
    def normalXY(self):
        return self._normalXY

    @normalXY.setter
    def normalXY(self, xy):
        if self._normalXY == xy:
            return

        self._normalXY = xy
        self.normalXYChanged.emit()
        self.updateData()
        self.update()

    @Property(bool, notify=uvChanged)
    def uv(self):
        return self._hasUV

    @uv.setter
    def uv(self, enable):
        if self._hasUV == enable:
            return

        self._hasUV = enable
        self.uvChanged.emit()
        self.updateData()
        self.update()

    @Property(float, notify=uvAdjustChanged)
    def uvAdjust(self):
        return self._uvAdjust

    @uvAdjust.setter
    def uvAdjust(self, f):
        if self._uvAdjust == f:
            return

        self._uvAdjust = f
        self.uvAdjustChanged.emit()
        self.updateData()
        self.update()

    def updateData(self):
        self.clear()

        stride = 3
        if self._hasNormals:
            stride += 3
        if self._hasUV:
            stride += 2

        # We use numpy arrays to handle the vertex data,
        # but still we need to consider the 'sizeof(float)'
        # from C to set the Stride, and Attributes for the
        # underlying Qt methods
        FLOAT_SIZE = 4
        vertexData = np.zeros(3 * stride, dtype=np.float32)

        # a triangle, front face = counter-clockwise
        p = 0
        vertexData[p] = -1.0
        p += 1
        vertexData[p] = -1.0
        p += 1
        vertexData[p] = 0.0
        p += 1

        if self._hasNormals:
            vertexData[p] = self._normalXY
            p += 1
            vertexData[p] = self._normalXY
            p += 1
            vertexData[p] = 1.0
            p += 1

        if self._hasUV:
            vertexData[p] = 0.0 + self._uvAdjust
            p += 1
            vertexData[p] = 0.0 + self._uvAdjust
            p += 1

        vertexData[p] = 1.0
        p += 1
        vertexData[p] = -1.0
        p += 1
        vertexData[p] = 0.0
        p += 1

        if self._hasNormals:
            vertexData[p] = self._normalXY
            p += 1
            vertexData[p] = self._normalXY
            p += 1
            vertexData[p] = 1.0
            p += 1

        if self._hasUV:
            vertexData[p] = 1.0 - self._uvAdjust
            p += 1
            vertexData[p] = 0.0 + self._uvAdjust
            p += 1

        vertexData[p] = 0.0
        p += 1
        vertexData[p] = 1.0
        p += 1
        vertexData[p] = 0.0
        p += 1

        if self._hasNormals:
            vertexData[p] = self._normalXY
            p += 1
            vertexData[p] = self._normalXY
            p += 1
            vertexData[p] = 1.0
            p += 1

        if self._hasUV:
            vertexData[p] = 1.0 - self._uvAdjust
            p += 1
            vertexData[p] = 1.0 - self._uvAdjust
            p += 1

        self.setVertexData(vertexData.tobytes())
        self.setStride(stride * FLOAT_SIZE)
        self.setBounds(QVector3D(-1.0, -1.0, 0.0), QVector3D(+1.0, +1.0, 0.0))
        self.setPrimitiveType(QQuick3DGeometry.PrimitiveType.Triangles)
        self.addAttribute(
            QQuick3DGeometry.Attribute.PositionSemantic, 0, QQuick3DGeometry.Attribute.F32Type
        )

        if self._hasNormals:
            self.addAttribute(
                QQuick3DGeometry.Attribute.NormalSemantic,
                3 * FLOAT_SIZE,
                QQuick3DGeometry.Attribute.F32Type,
            )

        if self._hasUV:
            self.addAttribute(
                QQuick3DGeometry.Attribute.TexCoordSemantic,
                6 * FLOAT_SIZE if self._hasNormals else 3 * FLOAT_SIZE,
                QQuick3DGeometry.Attribute.F32Type,
            )
