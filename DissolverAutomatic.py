#script selects one issue at a time
import bpy,bmesh
print('--=---')
bpy.ops.mesh.dissolve_verts()
#toggle this to not by hand
mesh=bmesh.from_edit_mesh(bpy.context.object.data)
bpy.ops.mesh.reveal()
bpy.ops.mesh.select_all(action='TOGGLE')
#toggle this after first sycle-thru

#alt+h

ex = False
for face in mesh.faces: #for a face
	a = len(face.verts)
	if a > 4: #allowed count of verts
		print(a)
		ex = True
		face.select = True
		bpy.ops.mesh.hide(unselected=True)
		for a in face.verts:
			print(a.link_edges)
			i = 0
			print("---")
			for t in a.link_edges:
				i += 1
				print(t)
				if i != 2:
					bpy.ops.mesh.select_all(action='TOGGLE')
					a.select = True
					break

		break

if not ex:
	print('all finish')