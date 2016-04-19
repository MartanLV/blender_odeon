#http://www.blender.org/api/blender_python_api_2_67_release/bmesh.types.html
# 4 DEVMODE true
# bpy.app.debug_wm = True

# script selects one issue at a time
import bpy,bmesh,mathutils,math

print('--=---')
bpy.ops.mesh.dissolve_verts()
#toggle this to not by hand
mesh=bmesh.from_edit_mesh(bpy.context.object.data)
bpy.ops.mesh.reveal()
bpy.ops.mesh.select_all(action='TOGGLE')
#toggle this after first sycle-thru

#alt+h
aiSelected=[]
ex = False
for face in mesh.faces: #for a face
	a = len(face.verts)
	if a > 4: #allowed count of verts
		print(a)
		ex = True
		face.select = True
		bpy.ops.mesh.hide(unselected=True)
		for i in range(a):
			v1=face.verts[i].co
			if i == a-1:
				v2=face.verts[0].co
				v3=face.verts[1].co
			elif i == a-2:
				v2=face.verts[1].co
				v3=face.verts[2].co
			else:
				v2=face.verts[i+1].co
				v3=face.verts[i+2].co
			# FIND OUT HOW TO FIND IF THESE TREE ARE LINEAR, TAKE MIDDLE ONE FOR SELCTION
			# the wrong way is below...
			e=mathutils.geometry.area_tri(v1,v2,v3)
			print('loop: %s area %s' % (i, e))
			if math.ceil(e) == 0 and len(aiSelected) != a-4:
				aiSelected.append(face.verts[1-i])
		break
if not ex:
	print('all finish')

# zoom cameras/views
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        ctx = bpy.context.copy()
        ctx['area'] = area
        ctx['region'] = area.regions[-1]
        bpy.ops.view3d.view_selected(ctx)            # points view
        # bpy.ops.view3d.camera_to_view_selected(ctx)   # points camera

bpy.ops.mesh.select_all(action='TOGGLE')

# select chosen
for v in aiSelected:
	v.select = True
most=0
for face in mesh.faces: #for a face
	a = len(face.verts)
	if a > 4: #allowed count of verts
		most+=1

print('%s to go' % most)