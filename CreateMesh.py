#----------------------------------------------------------
# File meshes.py
#----------------------------------------------------------
import bpy

bulkverts = (
(

(

(523431.3880/1000,-43990.5470/1000,0),
(518231.3880/1000,-43990.5470/1000,0),
(518231.3880/1000,-47990.5470/1000,0),
(523431.3880/1000,-47990.5470/1000,0),

),(

(523431.3880/1000,-48190.5470/1000,0),
(518231.3880/1000,-48190.5470/1000,0),
(518231.3880/1000,-52190.5470/1000,0),
(523431.3880/1000,-52190.5470/1000,0),
)

)








verts = (
(98694.7732/1000,-53896.0197/1000,0),
(95721.9698/1000,-44491.8007/1000,0),
(99787.4583/1000,-63130.6810/1000,0),
(98694.7732/1000,-53896.0197/1000,0),
(95951.8143/1000,-83906.4107/1000,0),
(99023.0253/1000,-73364.3499/1000,0),
(99023.0253/1000,-73364.3499/1000,0),
(99787.4583/1000,-63130.6810/1000,0),
)
edges = []
for i in range(0, len(verts)):
    ii = i+1
    if ii == len(verts):
        ii = 0
    edges.append(tuple([i, ii]))

edges = tuple(edges)

def createMesh(name, origin, verts, edges, faces):
    # Create mesh and object
    me = bpy.data.meshes.new(name+'Mesh')
    ob = bpy.data.objects.new(name, me)
    ob.location = origin
    ob.show_name = True
    # Link object to scene
    bpy.context.scene.objects.link(ob)

    # Create mesh from given verts, edges, faces. Either edges or
    # faces should be [], or you ask for problems
    me.from_pydata(verts, edges, faces)

    # Update mesh with new data
    me.update(calc_edges=True)
    return ob

def run(origin):
    ob2 = createMesh('Edgy', origin, verts, edges, [])
    return

def run2(origin, bulkverts):
    for verts in bulkverts:
        edges = []
        for i in range(0, len(verts)):
            ii = i+1
            if ii == len(verts):
                ii = 0
            edges.append(tuple([i, ii]))

        edges = tuple(edges)
        ob2 = createMesh('Fresh', origin, verts, edges, [])
    return

if __name__ == "__main__":
    # run((0,0,0))
    run2((0,0,0), bulkverts)
