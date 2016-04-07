#script selects one issue at a time
import bpy,bmesh
print('--=---')
#!!!!!!!!!!! bpy.ops.mesh.dissolve_verts()
#toggle this to not by hand
mesh=bmesh.from_edit_mesh(bpy.context.object.data)
bpy.ops.mesh.reveal()
#bpy.ops.mesh.select_all(action='TOGGLE')
#toggle this after first sycle-thru

#alt+h

ex = False
for face in mesh.faces: #for a face
	a = len(face.verts)
	if a > 4: #allowed count of verts
		print(a)
		ex = True
		print(face);
		face.select = True
		bpy.ops.mesh.split()
		bpy.ops.mesh.hide(unselected=True)
		break

if not ex:
	print('all finish')