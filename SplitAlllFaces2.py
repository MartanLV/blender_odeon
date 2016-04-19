import bpy,bmesh
def splitface():
    mesh=bmesh.from_edit_mesh(bpy.context.object.data)
    bpy.ops.mesh.select_all(action='TOGGLE')
    sels = False
    for f in mesh.faces:
        f.select = False
        for e in f.edges:
            if e.is_contiguous:
                # print(f)
                f.select = True
                sels = True
                bpy.ops.mesh.split()
                return sels
                break
        else:
            bpy.ops.mesh.split()
            continue  # executed if the loop ended normally (no break)
        bpy.ops.mesh.split()
        return sels
        break  # executed if 'continue' was skipped (break)

while(splitface()): 
    print('face split')

print('nothing more to split')
    
[bpy.ops.object.editmode_toggle() for _ in range(2)]#toggle twice to refresh view

