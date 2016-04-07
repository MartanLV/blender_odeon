# THIS FILE MUST BE SOURCED VIA CONSOLE .. select all
#
# hack here is to select even number of edges in specific manner:
# 1)the one to align 2)the one it'll be aligned in .. so on
# give X Y or Z
import bpy,bmesh,time

def align(AXIS): # AXIS=[0,1,2] //x,y,z
    m=bmesh.from_edit_mesh(bpy.context.object.data)
    print('- - x - -')
    SEQ=[]
    SELS=[e.index for e in m.edges if e.select]
    for S in SELS:
        bpy.ops.ed.undo()
        m=bmesh.from_edit_mesh(bpy.context.object.data)
        SELS2=[e.index for e in m.edges if e.select]
        SEQ+=[x for x in SELS if x not in SELS2]
        SELS=SELS2
    print(SEQ)
    if len(SEQ) % 2 != 0:
        print('wrong selection')
    bus=[]
    talon=[]
    for sq in SEQ:
        if len(bus) == len(talon):
            bus.append(sq)
        else:
            talon.append(sq)
    print(bus)
    print(talon)
    m=bmesh.from_edit_mesh(bpy.context.object.data)
    for E in m.edges:
        if E.index in bus:
            m2=bmesh.from_edit_mesh(bpy.context.object.data)
            for E2 in m2.edges:
                if E2.index in talon:
                    for axe in AXIS:
                        E.verts[1].co[axe] = E2.verts[0].co[axe]
                        E.verts[0].co[axe] = E2.verts[0].co[axe]
    [bpy.ops.object.editmode_toggle() for _ in range(2)]


print('SOURCED - use: align([axisIndices])')
