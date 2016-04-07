import bmesh
import bpy
from mathutils import geometry

def add_vertex_to_intersection():

    obj = bpy.context.object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    edges = [e for e in bm.edges if e.select]

    if len(edges) == 2:
        [[v1, v2], [v3, v4]] = [[v.co for v in e.verts] for e in edges]

        iv = geometry.intersect_line_line(v1, v2, v3, v4)
        iv = (iv[0] + iv[1]) / 2
        bm.verts.new(iv)
        bmesh.update_edit_mesh(me)

add_vertex_to_intersection()

# this application
# will find
# intersection point on two selected edges
# place a vector there and print coordinates
# for reference