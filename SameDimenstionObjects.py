# select an object
# script will select objects same width & height
# give treshold if not happy
import bpy

etalon = bpy.context.active_object
flakes = bpy.context.visible_objects
# TRSHLD = {  # might be used to compensate rotated objs
# 	width: {lo:0,hi:0}, # lowest & highest tolerances
# 	height: {lo:0,hi:0}
# }

# tlr = lambda dm, p: [dm-=TRSHLD[p].lo, dm+=TRSHLD[p].hi]

# aW = tlr(etalon.dimensions.y, 'width')
# aH = tlr(etalon.dimensions.z, 'height')

# print(aW)
# print(aH)
for flake in flakes:
	if flake.dimensions.x == etalon.dimensions.x and flake.dimensions.z == etalon.dimensions.z:
		flake.select = True
