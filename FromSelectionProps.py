import bpy,bmesh

mesh=bmesh.from_edit_mesh(bpy.context.object.data)

for v in mesh.verts:
    if v.select = True:
        v.co.z = 5.2

[bpy.ops.object.editmode_toggle() for _ in range(2)]#toggle twice to refresh view
