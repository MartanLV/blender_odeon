#script selects one issue at a time
import bpy,bmesh
print('--=---')
#!!!!!!!!!!! bpy.ops.mesh.dissolve_verts()
#toggle this to not by hand
mesh=bmesh.from_edit_mesh(bpy.context.object.data)
#bpy.ops.mesh.reveal()
#bpy.ops.mesh.select_all(action='TOGGLE')
#toggle this after first sycle-thru

#alt+h

ex = False
for face in mesh.faces: #for a face
	a = len(face.verts)
	if face.select and a != 4: #allowed count of verts
		print(a)
		bpy.ops.mesh.hide(unselected=True)
		bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
	else:
		bpy.ops.mesh.dissolve_verts()
		bpy.ops.mesh.reveal()
		bpy.ops.mesh.select_all(action='TOGGLE')
		bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')

