import bpy,bmesh
from mathutils import geometry

obj = bpy.context.object
me = obj.data
bm = bmesh.from_edit_mesh(me)

fedges = [] #face edges
sedges = [] #splittable edges
isEdgeOfFace = lambda e, f: True in [fe == e for fe in f]

for f in bm.faces:
    if f.select == True:
        face = f
        fedges = f.edges

if not fedges: print('no face')
else:
    for e in bm.edges:
        if e.select == True and not isEdgeOfFace(e, fedges):
            sedges.append(e)
    if not sedges: print('no edge')
    else:
        # <HEART>
        for sedge in sedges:
            iv = geometry.intersect_line_plane(
                sedge.verts[0].co,
                sedge.verts[1].co,
                face.verts[0].co,
                face.normal,
                False
            )
            if iv == None: print('coplanar edge is selected')
            else:
                sedge.select = False
                bm.verts.new(iv).select = True
        face.select = False
        bmesh.update_edit_mesh(me)
        # vert mode highligts created verts
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
# -------------------------------------------
# select a face plus some other mesh edges
# run script, VERTICES PLACED where that plane crossed an edge
# .. face edges considered to be planar
# -------------------------------------------
### MIT licence