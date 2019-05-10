import bpy
import bmesh

def FILE(*args):
    return list(map(lambda i: str(i), [*args, 0, "EOF"]))

def COMMENT(line):
    return [999, line]

def SECTION(name, *args):
    if name not in [
            # "HEADER",
            # "CLASSES",
            "TABLES",
            # "BLOCKS",
            "ENTITIES",
            # "OBJECTS",
            # "THUMBNAILIMAGE",
    ]: return COMMENT("ERROR: IN SECTION UNRECOGNIZED %s" % name)
    return [0, "SECTION", 2, name, *args, 0, "ENDSEC"]

def TABLE(name, *args):
    if name not in [
            # "APPID",
            # "DIMSTYLE",
            "LAYER",
            # "LTYPE",
            # "STYLE",
            # "UCS",
            # "VIEW",
            # "VPORT",
            # "BLOCK_RECORD",
    ]: return COMMENT("ERROR: IN TABLE UNRECOGNIZED %s" % name)
    return [0, "TABLE", 2, name, *args, 0, "ENDTAB"]

def ENTITY(name, layer, color, *args):
    if name not in [
            # "POLYLINE",
            "3DFACE",
    ]: return COMMENT("ERROR: IN ENTITY UNRECOGNIZED %s" % name)
    return [0, name, 8, layer, 62, color, *args]

def LAYER(name, flags = 64, color = 1):
    return [0, "LAYER", 2, name, 70, flags, 62, color, 6, "CONTINUOUS"]

def A3DFACE_PTS(p1, p2, p3, p4 = None):
    if p4 == None:
        p4 = p3
    return [
        10, p1[0], 20, p1[1], 30, p1[2],
        11, p2[0], 21, p2[1], 31, p2[2],
        12, p3[0], 22, p3[1], 32, p3[2],
        13, p4[0], 23, p4[1], 33, p4[2],
    ]

class DXF:
    def __init__(self, scale = 1, decimal = 2):
        self.facesctn = 0
        self.layers = []
        self.entities = []

        self.layer_state = 'unnamed'
        self.color_state = 1

        self.decimal = decimal
        self.scale = scale

    def add_face(self, verts):
        self.facesctn += 1
        self.entities += ENTITY("3DFACE", self.layer_state, self.color_state, *A3DFACE_PTS(*verts))

    def add_layer(self, name):
        import re
        name = re.sub("[^a-zA-Z0-9]", "", name)
        self.layers += LAYER(name, 64, self.color_state)
        self.layer_state = name
        self.color_state += 1

    def get_entities(self):
        return SECTION("ENTITIES", *self.entities)

    def get_tables(self):
        return SECTION("TABLES", *TABLE("LAYER", *self.layers))

    def get_comment(self):
        return COMMENT("count 3DFACE: %s" % self.facesctn)

    def write(self, path):
        fo = open(path, 'w+')
        fo.write(self.to_string())
        fo.close()

    def to_lines(self):
        return FILE(
            *self.get_comment(),
            *self.get_tables(),
            *self.get_entities(),
        )

    def run(self):
        for i in self.to_lines():
            if len(i) > 256:
                raise Exception("%s \n\nDXF file may not contain a ^line longer than 256 character" % i)
            yield i

    def to_string(self):
        lines = self.run()
        return "\n".join(lines)+"\n"

bpy.ops.object.transform_apply(location = True, scale = True, rotation = True)

dxf = DXF()
dxf_2 = DXF()
for obj in bpy.data.objects:
    if not obj.visible_get(): continue
    if not type(obj.data) == bpy.types.Mesh: continue
    dxf.add_layer(obj.name)
    dxf_2.add_layer(obj.name)

    for f in obj.data.polygons:
        if len(f.vertices) > 4: continue
        verts = []
        verts_2 = []
        for i in f.vertices:
            l = list(obj.data.vertices[i].co.xyz)
            verts_2.append(["%.2f" % i for i in l])
            l = [1000 * i for i in l]
            verts.append(["%.0f" % i for i in l])
        dxf.add_face(verts_2)
        dxf_2.add_face(verts)

variant = ""
fp = bpy.data.filepath
if fp:
    dxf.write(fp + variant + "_unit_meter.dxf")
    dxf_2.write(fp + variant + "_unit_milimeter.dxf")
    print(fp + variant + "_unit_meter.dxf")
    print(fp + variant + "_unit_milimeter.dxf")
else:
    print("Ya gotta save dat file! Error:")
    # print(dxf.to_string())


# origin translate (old style)
# bpy.context.scene.cursor.location = (0.0,0.0,0.0)
# for obj in bpy.data.objects:
#     obj.select_set(True)
# bpy.ops.object.origin_clear()
# bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
# ALL transformations must be applied onto objects
# so undelaying mesh will read global coordinates


# I hate python, what a silly language.

# This script maybe will create ASCII-DXF for ya.
# An object name will serve as layer name.
# Each layer will have different color assigned to it.
# DXF will have only 3DFACE primitive.
