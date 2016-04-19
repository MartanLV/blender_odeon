import bpy,bmesh
#http://www.blender.org/api/blender_python_api_2_67_release/bmesh.types.html

#this requires to keep pushing alt+p until console says its all

#checks a face edges, if edge belongs to more faces, current face is splitted
#then script exits

#http://www.blender.org/api/blender_python_api_2_67_release/bmesh.types.html
mesh=bmesh.from_edit_mesh(bpy.context.object.data)
sels = False

for f in mesh.faces:
    f.select = False
    for e in f.edges:
        if e.is_contiguous:
            print(f.index)
            f.select = True
            sels = True
            break
    else:
        continue  # executed if the loop ended normally (no break)
    break  # executed if 'continue' was skipped (break)

bpy.ops.mesh.split()

if sels == True:
    bpy.ops.mesh.select_all(action='TOGGLE')
    print('face split')
else:
    print('nothing more to split')
    
[bpy.ops.object.editmode_toggle() for _ in range(2)]#toggle twice to refresh view

