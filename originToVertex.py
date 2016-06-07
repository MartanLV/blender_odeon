# http://blender.stackexchange.com/a/1302/13906
def execute(self, context):
    saved_location = bpy.context.scene.cursor_location.copy()
    bpy.ops.view3d.snap_cursor_to_selected()

    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.context.scene.cursor_location = saved_location

    bpy.ops.object.mode_set(mode = 'EDIT')
    return {'FINISHED'}
