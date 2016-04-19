# in edit mode 
# make some primitive mesh, remove it's vetrices
# populate sketchup data
# objects merge : ctrl+j

import bpy,bmesh,json
mesh=bmesh.from_edit_mesh(bpy.context.object.data)
e=open('/tmp/lastExport.txt','r')
tmpName=e.read()
jFile=open('/Users/x/oo-MARTINS-oo/260316-Rimi/BlenderTXT/%s.txt' % tmpName,'r')
points=json.load(jFile)

# 1in = 2.54cm a.k.a 127/50
inchesK = lambda x: x*2.54/100

# obj = bpy.context.object

# bm = bmesh.from_edit_mesh(obj.data)
# bm.faces.ensure_lookup_table()

def quickMesh(verts=[], face=[]):
    bm = bmesh.new()

    for vert in verts:
        vert = [inchesK(x) for x in vert]
        bm.verts.new(vert)
    
    bm.verts.ensure_lookup_table()
    if face:
        try:
            bm.faces.new(tuple(bm.verts[i] for i in face))
            bm.faces.ensure_lookup_table()
            # print("success")
        except:
            print("error-1")
    
    bm.faces.ensure_lookup_table()
    me = bpy.data.meshes.new("Mesh")
    bm.to_mesh(me)
    bm.free()
    scene = bpy.context.scene
    obj = bpy.data.objects.new(tmpName, me)
    scene.objects.link(obj)

for pointSet in points:
    # bm.faces.ensure_lookup_table()
    quickMesh(pointSet[0],pointSet[1])


# bpy.ops.object.editmode_toggle()
# bpy.ops.object.editmode_toggle()
print("--- --- ---")