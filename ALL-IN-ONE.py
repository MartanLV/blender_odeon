import bpy,bmesh
print("<>LOG IN<>")
# splitt
# splitt
# splitt
import bpy,bmesh,sys
def splitall():
    import bpy,bmesh
    stble=False
    m=bmesh.from_edit_mesh(bpy.context.object.data)
    for f in m.faces:
        f.select = False
    for f in m.faces:
        if stble:
            break
        else:
            for v in f.verts:
                if len(v.link_edges) != 2:
                    f.select = True
                    stble = True
                    bpy.ops.mesh.split()
                    break
    return stble

while(splitall()):
    sys.stdout.write("[-] ")
sys.stdout.flush()
print("this many face splits")

# zero area remove
# zero area remove
# zero area remove
obj = bpy.context.edit_object.data
mesh=bmesh.from_edit_mesh(obj)

rems = [f for f in mesh.faces if f.calc_area() < 0.0001]
bmesh.ops.delete(mesh, geom=rems, context=5)
bmesh.update_edit_mesh(obj, True)
print(str(len(rems))+' noarea faces removed !')

# zero verts remoe
# zero verts remoe
# zero verts remoe
# import bpy,bmesh

m=bmesh.from_edit_mesh(bpy.context.object.data)
x=0
for v in m.verts:
    if len(v.link_edges) == 0:
        v.select = True
        x+=1
    else:
        v.select = False

bpy.ops.mesh.delete(type='VERT')
print( "%s <- floating vertexses deleted" % x)

# zero edges remoe
# zero edges remoe
# zero edges remoe
import bpy,bmesh
m1=bmesh.from_edit_mesh(bpy.context.object.data)
xx=0
for ed in m1.edges:
    if len(ed.link_faces) == 0:
        ed.select = True
        xx+=1
    else:
        ed.select = False

bpy.ops.mesh.delete(type='VERT')
print( "%s <- floating edges deleted" % xx)

# zero faces remove
# zero faces remove
# zero faces remove
import bpy,bmesh
rez = 21 #decimal places|treshold| .21 to .0
mesh2=bmesh.from_edit_mesh(bpy.context.object.data)
all = []
allobj = []
seen = set()
ex = True
for face in mesh2.faces:
    for vrt in face.verts:
        face.select = False
mesh=bmesh.from_edit_mesh(bpy.context.object.data)

for face in mesh.faces:
    all.append(str(sorted([str(v.co.to_tuple(rez)) for v in face.verts])))
    allobj.append(face)

for i,x in enumerate(all):
    if x not in seen:seen.add(x)
    else:allobj[i].select = True;ex = False;


if ex:
    print('no duplicated faces')
else:
    ct=len(allobj)-len(seen)
    print('%s Duplicated Faces found and removed' % ct)
    bpy.ops.mesh.delete(type='VERT')


# TEST
import bpy,bmesh
print('--=---')
mesh=bmesh.from_edit_mesh(bpy.context.object.data)
for face in mesh.faces: #for a face
    a = len(face.verts)
    if a > 4: #allowed count„ of verts
        print("--!!! HUSTON MORE THAN 4 VERTS !!!")
        break

print("<>LOG OUT<>")
[bpy.ops.object.editmode_toggle() for _ in range(2)]#toggle twice to refresh view
