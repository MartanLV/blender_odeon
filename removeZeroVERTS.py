import bpy,bmesh,sys
def deselect():
    for v in mesh.verts:
        if v.select:
            v.select = False
        [bpy.ops.object.editmode_toggle() for _ in range(2)]#toggle twice to refresh view

#SPLIT ALL
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
pp=0
while(splitall()):
    pp+=1
    sys.stdout.write("[-] ")
sys.stdout.flush()
print("%s faces splitted" % pp)

# NO AREA
deselect()
obj = bpy.context.edit_object.data
mesh=bmesh.from_edit_mesh(obj)
rems = [f for f in mesh.faces if f.calc_area() < 0.0001]
bmesh.ops.delete(mesh, geom=rems, context=5)
bmesh.update_edit_mesh(obj, True)
[bpy.ops.object.editmode_toggle() for _ in range(2)]
print(str(len(rems))+' noarea faces removed !')

# FLOATING VERTICES
deselect()
m=bmesh.from_edit_mesh(bpy.context.object.data)
x=0
for v in m.verts:
    if len(v.link_edges) == 0:
        v.select = True
        x+=1
    else:
        v.select = False
bpy.ops.mesh.delete(type='VERT')
print( "%s <- floating verteces deleted" % x) 

#COPLANARS
deselect()
rez = 21 #decimal places|treshold| .21 to .0
mesh=bmesh.from_edit_mesh(bpy.context.object.data)
all = []
allobj = []
seen = set()
ex = True
mesh=bmesh.from_edit_mesh(bpy.context.object.data)
for face in mesh.faces:
    all.append(str(sorted([str(v.co.to_tuple(rez)) for v in face.verts])))
    allobj.append(face)
for i,x in enumerate(all):
    if x not in seen:seen.add(x)
    else:allobj[i].select = True;ex = False;
[bpy.ops.object.editmode_toggle() for _ in range(2)]#toggle twice to refresh view
if ex:
    print('no duplicated faces')
else:
    ct=len(allobj)-len(seen)
    print('%s Duplicated Faces found and removed' % ct)
    bpy.ops.mesh.delete(type='VERT')


#TEST
mesh=bmesh.from_edit_mesh(bpy.context.object.data)
for face in mesh.faces: #for a face
    a = len(face.verts)
    if a > 4: #allowed count„ of verts
        print("--!!! HUSTON MORE THAN 4 VERTS FOUND !!!")
        break

print("<>LOG OUT<>")