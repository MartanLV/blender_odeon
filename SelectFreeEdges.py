import bpy,bmesh
#http://www.blender.org/api/blender_python_api_2_67_release/bmesh.types.html

mesh=bmesh.from_edit_mesh(bpy.context.object.data)
sels = 0
for v in mesh.edges:
# ___True when this edge is manifold
# between two faces with the same winding (read-only).
	if not v.is_contiguous:
		pass #v.select = True;sels+=1

# ___True when this edge joins 2 convex faces
# depends on a valid face normal
	if not v.is_convex:
		pass #v.select = True;sels+=1

# ___True when this edge joins 2 convex faces
# depends on a valid face normal
	if v.is_wire:
		v.select = True;sels+=1

# print('is_convex')
# print(v.is_manifold)
# print('is_manifold')
# print(v.is_valid)
# print('is_valid')
# print(v.link_faces)
# print('link_faces')
# print(v.link_loops)
# print('link_loops')
# print(v.normal_update)
# print('normal_update')
# print(v.other_vert)
# print('other_vert')
# print(v.seam)
# print('seam')
# print(v.select)
# print('select')
# print(v.select_set)
# print('select_set')
# print(v.smooth)
# print('smooth')
# print(v.tag)
# print('tag')
# print(v.verts)
# print('verts')
print(sels)
[bpy.ops.object.editmode_toggle() for _ in range(2)]#toggle twice


