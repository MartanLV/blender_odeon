import bpy,bmesh
mesh=bmesh.from_edit_mesh(bpy.context.object.data)

for v in mesh.edges:
    if v.select == True:
        v.select = False
        break

[bpy.ops.object.editmode_toggle() for _ in range(2)]#toggle twice to refresh view


# select_history