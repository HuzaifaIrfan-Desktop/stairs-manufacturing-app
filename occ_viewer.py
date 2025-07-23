from OCC.Display.backend import get_qt_modules, load_backend
from pyparsing import Path
load_backend("pyside6")
from OCC.Display.qtDisplay import qtViewer3d
from OCC import VERSION
from typing import Any, Optional, Tuple
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMainWindow , QStyleFactory

from PySide6.QtCore import Qt


from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace
from OCC.Core.TopoDS import TopoDS_Compound, TopoDS_Face, TopoDS_Shape
from OCC.Core.BRep import BRep_Builder
import numpy as np

import pathlib
import os

def stl_to_shape(stl_file_path: str) -> TopoDS_Shape:
    shape = TopoDS_Shape()
    reader = StlAPI_Reader()
    reader.Read(shape, stl_file_path)
    return shape

def obj_to_shape(obj_file_path, triangulate=True):
    """
    Convert an OBJ file to a PythonOCC TopoDS_Shape.
    
    Args:
        obj_file_path (str): Path to the OBJ file
        triangulate (bool): Whether to triangulate non-triangular faces (recommended)
    
    Returns:
        TopoDS_Compound: The resulting shape containing all faces
    """
    # Parse OBJ file manually (lightweight alternative to pywavefront)
    vertices = []
    faces = []
    
    with open(obj_file_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                # Vertex definition
                parts = line.strip().split()
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif line.startswith('f '):
                # Face definition (can be triangle, quad, or n-gon)
                parts = line.strip().split()
                face_vertex_indices = []
                for part in parts[1:]:
                    # Handle formats like "f v1/vt1/vn1 v2/vt2/vn2 ..."
                    vertex_part = part.split('/')[0]
                    if vertex_part:
                        face_vertex_indices.append(int(vertex_part) - 1)  # OBJ uses 1-based indexing
                faces.append(face_vertex_indices)
    
    # Create a compound to hold all faces
    builder = BRep_Builder()
    compound = TopoDS_Compound()
    builder.MakeCompound(compound)
    
    # Convert each face to a TopoDS_Face
    for face_indices in faces:
        if len(face_indices) < 3:
            continue  # Skip invalid faces
            
        if triangulate and len(face_indices) > 3:
            # Triangulate polygon by creating triangle fans
            triangles = []
            for i in range(1, len(face_indices) - 1):
                triangles.append([face_indices[0], face_indices[i], face_indices[i+1]])
        else:
            triangles = [face_indices]
        
        # Create each triangle face
        for tri in triangles:
            polygon = BRepBuilderAPI_MakePolygon()
            for idx in tri:
                if idx < 0 or idx >= len(vertices):
                    continue  # Skip invalid indices
                x, y, z = vertices[idx]
                polygon.Add(gp_Pnt(x, y, z))
            polygon.Close()
            
            # Try to create a face from the polygon
            face = BRepBuilderAPI_MakeFace(polygon.Wire()).Face()
            if not face.IsNull():
                builder.Add(compound, face)
    
    return compound


def get_shape_from_file(file_path: str) -> TopoDS_Shape:
    path = pathlib.Path(file_path)
    filename = path.name # e.g., "file.pdf"
    extension = path.suffix  # e.g., ".pdf"
    filename_without_extension = path.stem  # e.g., "file"

    if not path.exists():
        print(f"File does not exist: {file_path}. Displaying default shape.")
        shape = BRepPrimAPI_MakeBox(10, 20, 30).Shape()
    else:
        try:
            if extension == ".stl":
                # file_path = "output/Crestmont/Landing.stl"
                shape = stl_to_shape(file_path)
            elif extension == ".obj":
                # file_path = "output/Crestmont/Landing.obj"
                shape = obj_to_shape(file_path, triangulate=False)
            else:
                shape = BRepPrimAPI_MakeBox(10, 20, 30).Shape()
        except Exception as e:
            print(f"Error loading shape from {file_path}: {e}")
            shape = BRepPrimAPI_MakeBox(10, 20, 30).Shape()
        
    return shape

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy
)
class OCCViewerWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None, size: Optional[Tuple[int, int]] = (1024, 768)):
        super().__init__(parent)
        self._size = size
        self._display = None
        self._viewer = None
        self.init_ui()
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
    def init_ui(self):
        """Initialize the user interface."""
        # Get Qt modules

        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        # Create the OCC viewer
        self._viewer = qtViewer3d(self)
        layout.addWidget(self._viewer)
        
        # Initialize the viewer
        self._viewer.InitDriver()
        self._display = self._viewer._display
        
        
        # Set initial size
        if self._size:
            self._viewer.resize(self._size[0], self._size[1])
            self.resize(self._size[0], self._size[1])
            
    
    @property
    def display(self):
        """Get the OCC display instance."""
        return self._display
    
    def get_viewer(self):
        """Get the underlying qtViewer3d instance."""
        return self._viewer
    
    # def minimumSizeHint(self):
    #     """Provide a reasonable minimum size hint."""
    #     return self._size or super().minimumSizeHint()
    
    # def sizeHint(self):
    #     """Provide a reasonable size hint."""
    #     return self._size or super().sizeHint()


from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from PySide6.QtWidgets import QPushButton
from OCC.Core.StlAPI import StlAPI_Reader
from OCC.Core.TopoDS import TopoDS_Shape

class OCCViewerWindow(QMainWindow):
    def __init__(self, file_path: str = "output/test.stl", parent: Optional[QWidget] = None):

        self.file_path = file_path 

        super().__init__()
        self.setWindowTitle(f"OCC Viewer ({self.file_path})")
        self.resize(500, 500)



        # Setup central widget
        central_widget = QWidget()
        layout = QVBoxLayout()

        # header_layout = QHBoxLayout()
        # title_label = QLabel("OCC Viewer Window")
        # title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Equivalent to anchors.horizontalCenter
        # title_label.setStyleSheet("font-size: 20px;")  # Equivalent to font.pixelSize: 20
        # header_layout.addWidget(title_label)
        # layout.addLayout(header_layout)


        # Create OCC viewer widget
        main_layout = QHBoxLayout()
        self.occ_viewer = OCCViewerWidget()
        main_layout.addWidget(self.occ_viewer)
        layout.addLayout(main_layout)

        footer_layout = QHBoxLayout()
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Equivalent to anchors.horizontalCenter
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        footer_layout.addWidget(close_button)
        layout.addLayout(footer_layout)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        


        shape=get_shape_from_file(self.file_path)
        
        self.occ_viewer.display.EraseAll()
        self.occ_viewer.display.DisplayShape(shape, update=True)
        self.occ_viewer.display.FitAll()


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    occ_viewer_window = OCCViewerWindow(file_path="output\example_part.stl")
    occ_viewer_window.show()
    sys.exit(app.exec())