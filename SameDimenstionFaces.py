#select mesh elems by same:
# * [1]AREA
# * [2]POSITION [xyz]

TRESHOLD=11 #11max decimals
# AXES=['z','y'] #for edges and verts choose axes to collide
AXES=[0,2] #for edges and verts choose axes to collide
import bpy, bmesh

mesh=bmesh.from_edit_mesh(bpy.context.object.data)
etalon = 0
# INTELLIGENT SELECTION
for face in mesh.faces:
    if face.select:
        etalonOp = 'faces'
        etalonUp = mesh.faces
        etalon = face
        break
if not etalon:
    for edge in mesh.edges:
        if edge.select:
            etalonOp = 'edges'
            etalonUp = mesh.edges
            etalon = edge
            break
if not etalon:
    for vert in mesh.verts:
        if vert.select:
            etalonOp = 'verts'
            etalonUp = mesh.verts
            etalon = vert
            break

#SELECT
et = etalon
for el in etalonUp:
    if el != et:
        if etalonOp == 'faces': # same area faces
            e0=round(el.calc_area(),TRESHOLD)
            e1=round(et.calc_area(),TRESHOLD)
            if e0 == e1:
                el.select = True
        elif etalonOp == 'edges':
            det = 0
            for axe in AXES:
                if TRESHOLD:
                    e0 = round(el.verts[0].co[axe],TRESHOLD)
                    e1 = round(el.verts[1].co[axe],TRESHOLD)
                    e2 = round(et.verts[0].co[axe],TRESHOLD)
                    e3 = round(et.verts[1].co[axe],TRESHOLD)
                else:
                    e0 = el.verts[0].co[axe]
                    e1 = el.verts[1].co[axe]
                    e2 = et.verts[0].co[axe]
                    e3 = et.verts[1].co[axe]
                    
                if e0 == e1 and e2 == e3:
                    det += 1
            if det == len(AXES):
                el.select = True

        elif etalonOp == 'verts':
            pass
#toggle twice to refresh view
[bpy.ops.object.editmode_toggle() for _ in range(2)]

























