import bpy,bmesh
obj = bpy.context.edit_object.data
mesh=bmesh.from_edit_mesh(obj)

rems = [f for f in mesh.faces if f.calc_area() < 0.0001]
bmesh.ops.delete(mesh, geom=rems, context=5)
bmesh.update_edit_mesh(obj, True)

[bpy.ops.object.editmode_toggle() for _ in range(2)]
print(str(len(rems))+' removed !')