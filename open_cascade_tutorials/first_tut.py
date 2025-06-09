from OCP.gp import gp_Pnt, gp_Dir, gp_Ax2
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeEdge
from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCP.gp import gp_Vec
from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCP.IFSelect import IFSelect_RetDone

# 1. Define a simple airfoil-like profile using points
points = [
    gp_Pnt(0, 0, 0),
    gp_Pnt(1.5, 0.2, 0),
    gp_Pnt(3, 0.1, 0),
    gp_Pnt(4, 0, 0),
    gp_Pnt(3, -0.1, 0),
    gp_Pnt(1.5, -0.2, 0),
    gp_Pnt(0, 0, 0)  # close the loop
]

# 2. Build a polygon from points
polygon = BRepBuilderAPI_MakePolygon()
for pt in points:
    polygon.Add(pt)
polygon.Close()
wire = polygon.Wire()

# 3. Create a face from the wire
face = BRepBuilderAPI_MakeFace(wire).Face()

# 4. Extrude the face into 3D
extrusion_vec = gp_Vec(0, 0, 1)  # direction of extrusion
solid = BRepPrimAPI_MakePrism(face, extrusion_vec).Shape()

# 5. Export the result to STEP file
writer = STEPControl_Writer()
writer.Transfer(solid, STEPControl_AsIs)
status = writer.Write("simple_wing.step")

if status == IFSelect_RetDone:
    print("STEP file written successfully.")
else:
    print("Failed to write STEP file.")
