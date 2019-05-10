import bpy
def threshold_move_pos(i, n, k = 0.09):
    bpy.ops.object.mode_set(mode='OBJECT')
    for obj in bpy.data.objects:
        obj.select_set(False)
        if not obj.visible_get(): continue
        obj.select_set(True)
        for v in obj.data.vertices:
            if v.co[i] > n - k and v.co[i] < n + k:
                v.co[i] = n
                v.select = True
            else:
                v.select = False
def threshold_move_x(n, k = 0.09):
    threshold_move_pos(0, n, k)
def threshold_move_y(n, k = 0.09):
    threshold_move_pos(1, n, k)
def threshold_move_z(n, k = 0.09):
    threshold_move_pos(2, n, k)

def did_normalize(v):
    did = False
    if v.co.x != round(v.co.x, 2):
        threshold_move_x(round(v.co.x, 2))
        did = True
    if v.co.y != round(v.co.y, 2):
        threshold_move_y(round(v.co.y, 2))
        did = True
    if v.co.z != round(v.co.z, 2):
        threshold_move_z(round(v.co.z, 2))
        did = True
    return did

def crazy_normalize():
    for obj in bpy.data.objects:
        obj.select_set(False)
        if not obj.visible_get(): continue
        for v in obj.data.vertices:
            # v.select = False
            if did_normalize(v):
                v.select = True

crazy_normalize()
# threshold_move_x(3.27)

# threshold_move_y(3.14)
# threshold_move_z(3.1)
# threshold_move_z(2.4)
# threshold_move_z(2.8)
# threshold_move_z(2.5)
# threshold_move_z(2.1)
# threshold_move_z(3.27)
# threshold_move_z(3.57)
# threshold_move_z(5.71)
# threshold_move_z(0)
# threshold_move_z(9.5, 1)
# threshold_move_x(0)
# threshold_move_x(0.45)
# threshold_move_x(1.55)
# threshold_move_x(2)
# threshold_move_x(1.9)
# threshold_move_x(3)
# threshold_move_x(4)
# threshold_move_x(5.1)
# threshold_move_x(5.5)
# threshold_move_x(7.7)
# threshold_move_x(9.3)
# threshold_move_x(9.8)
# threshold_move_x(10.2)
