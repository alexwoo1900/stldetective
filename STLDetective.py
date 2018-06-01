#-*- coding:utf-8 -*-

from sys import argv
import os
import struct
import numpy
import scipy.spatial
from typing import Optional
from copy import deepcopy


class STLDetective:

    _vertex_count = 0
    _vertices = None
    _convex_hull_vertices = None
    _convex_hull = None

    def load_file(self, file_name):
        f = open(file_name, "rb")
        if not self._loadBinary(f):
            f.close()
            f = open(file_name, "rt")
            try:
                self._loadAscii(f)
            except UnicodeDecodeError:
                return None
            f.close()	


    def _loadAscii(self, f):
        num_verts = 0
        for lines in f:
            for line in lines.split("\r"):
                if "vertex" in line:
                    num_verts += 1

        f.seek(0, os.SEEK_SET)
        vertex = 0
        face = [None, None, None]
        for lines in f:
            for line in lines.split("\r"):
                if "vertex" in line:
                    face[vertex] = line.split()[1:]
                    vertex += 1
                    if vertex == 3:
                        self._addVertex(float(face[0][0]), float(face[0][2]), -float(face[0][1]))
                        self._addVertex(float(face[1][0]), float(face[1][2]), -float(face[1][1]))
                        self._addVertex(float(face[2][0]), float(face[2][2]), -float(face[2][1]))
                        vertex = 0

    def _loadBinary(self, f):
        f.read(80)

        num_faces = struct.unpack("<I", f.read(4))[0]
        if num_faces < 1 or num_faces > 1000000000:
            return False
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        f.seek(84, os.SEEK_SET)
        if file_size < num_faces * 50 + 84:
            return False

        for idx in range(0, num_faces):
            data = struct.unpack(b"<ffffffffffffH", f.read(50))
            self._addVertex(data[3], data[5], -data[4])
            self._addVertex(data[6], data[8], -data[7])
            self._addVertex(data[9], data[11], -data[10])

        return True

    def _addVertex(self, x, y, z):
        if self._vertices is None:
            self._vertices = numpy.zeros((10, 3), dtype=numpy.float32)

        if len(self._vertices) == self._vertex_count:
            self._vertices.resize((self._vertex_count * 2, 3))

        self._vertices[self._vertex_count, 0] = x
        self._vertices[self._vertex_count, 1] = y
        self._vertices[self._vertex_count, 2] = z
        self._vertex_count += 1

    def getModelBBox(self):
        self._newVertices = self._immutableNDArray(self._vertices[0: self._vertex_count])
        if self._newVertices is None:
            return None

        data = numpy.pad(self._getConvexHullVertices(), ((0, 0), (0, 1)), "constant", constant_values=(0.0, 1.0))

        minPoint = data.min(axis=0)
        maxPoint = data.max(axis=0)

        width = maxPoint[0] - minPoint[0]
        height = maxPoint[1] - minPoint[1]
        depth = maxPoint[2] - minPoint[2]

        print("%.1f %.1f %.1f" % (width, depth, height))

    def _immutableNDArray(self, nda):
        if nda is None:
            return None

        if type(nda) is list:
            nda = numpy.array(nda, numpy.float32)
            nda.flags.writeable = False

        if not nda.flags.writeable:
            return nda
        copy = deepcopy(nda)
        copy.flags.writeable = False
        return copy

    def _getConvexHullVertices(self) -> numpy.ndarray:
        if self._convex_hull_vertices is None:
            convex_hull = self._getConvexHull()
            self._convex_hull_vertices = numpy.take(convex_hull.points, convex_hull.vertices, axis=0)
        return self._convex_hull_vertices

    def _getConvexHull(self) -> Optional[scipy.spatial.ConvexHull]:
        if self._convex_hull is None:
            self._computeConvexHull()
        return self._convex_hull

    def _computeConvexHull(self):
        points = self._getVertices()
        if points is None:
            return
        self._convex_hull = self._approximateConvexHull(points, 1024)
	
    def _getVertices(self) -> numpy.ndarray:
        return self._newVertices

    def _approximateConvexHull(self, vertex_data: numpy.ndarray, target_count: int) -> Optional[scipy.spatial.ConvexHull]:
        input_max = target_count * 50   
        unit_size = 0.0125           
        max_unit_size = 0.01

        while len(vertex_data) > input_max and unit_size <= max_unit_size:
            new_vertex_data = _uniqueVertices(_roundVertexArray(vertex_data, unit_size))
          
            if numpy.amin(new_vertex_data[:, 1]) != numpy.amax(new_vertex_data[:, 1]):
                vertex_data = new_vertex_data
            else:     
                break
            unit_size *= 2

        if len(vertex_data) < 4:
            return None

   
        hull_result = scipy.spatial.ConvexHull(vertex_data)
        vertex_data = numpy.take(hull_result.points, hull_result.vertices, axis=0)

        while len(vertex_data) > target_count and unit_size <= max_unit_size:
            vertex_data = _uniqueVertices(_roundVertexArray(vertex_data, unit_size))
            hull_result = scipy.spatial.ConvexHull(vertex_data)
            vertex_data = numpy.take(hull_result.points, hull_result.vertices, axis=0)
            unit_size *= 2

        return hull_result


    def _uniqueVertices(vertices: numpy.ndarray) -> numpy.ndarray:
        vertex_byte_view = numpy.ascontiguousarray(vertices).view(numpy.dtype(numpy.void, vertices.dtype.itemsize * vertices.shape[1]))
        _, idx = numpy.unique(vertex_byte_view, return_index=True)
        return vertices[idx]

    def _roundVertexArray(vertices: numpy.ndarray, unit: float) -> numpy.ndarray:
        expanded = vertices / unit
        rounded = expanded.round(0)
        return rounded * unit

if __name__ == "__main__":
    scriptName, stlFullPath = argv
    detective = STLDetective()
    detective.load_file(stlFullPath)
    detective.getModelBBox()
