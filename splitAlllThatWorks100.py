# best face SplitAll "one by one"
print("---off")
import bpy,bmesh
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
                    print("# we got manifold")
                    f.select = True
                    stble = True
                    bpy.ops.mesh.split()
                    break

splitall()


### or il noop verion
# best face SplitAll "one by one"
print("---off")
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
print("this many")