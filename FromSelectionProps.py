import bpy,bmesh

mesh=bmesh.from_edit_mesh(bpy.context.object.data)

for v in mesh.verts:
    if v.select == True:
        print(v)

[bpy.ops.object.editmode_toggle() for _ in range(2)]#toggle twice to refresh view






# console FN
import bpy,bmesh
A=[0,0,0]
def cp():
    global A
    m=bmesh.from_edit_mesh(bpy.context.object.data)
    for v in m.verts:
        if v.select == True:
            A=list(v.co)

def appl(ax, v):
    global A
    print("%s -> %s" % (v.co[ax], A[ax]))
    v.co[ax]=A[ax]

def mv(axe):
    global A
    m=bmesh.from_edit_mesh(bpy.context.object.data)
    for v in m.verts:
        if v.select == True:
            if type(axe) != list:
                axe=[axe]
            for ax in axe:
                appl(ax, v)
    [bpy.ops.object.editmode_toggle() for _ in range(2)]#toggle twice to refresh view

def cpmv(axe):
    cp()
    bpy.ops.ed.undo()
    mv(axe)


