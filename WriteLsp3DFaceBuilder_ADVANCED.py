import bpy, bmesh, os

" aist has problem with 'pseudo' carved holes in plane.
class BlendOneLisp():
    faces = 0
    @staticmethod
    def namespace_opts(prefix, name, opts):
        opts["function_call"] = "func_" + prefix + "_" + name
        opts["filepath"] = prefix + "_" + name + ".lsp"
        opts["acad_layer"] = name
        return opts

    @staticmethod
    def preset_aist_opts():
        return {
            "preset": "aist",
            "cad3face": True,
            "cad3dpoly": True,
            "units": 0.001
        }
        
    @staticmethod
    def preset_odeon_opts():
        return {
            "preset": "odeon",
            "cad3dpoly": False,
            "units": 1,
        }

    @staticmethod
    def preset(prefix):
        print("\n\n\n\n #\n # preset_" + prefix + ": \n #")
        opts = getattr(__class__, "preset_" + prefix + "_opts")()
        runner = __class__()
        feedback = []
        scene = bpy.context.scene
        for obj in scene.objects:
            if obj.type == 'MESH':
                opts = __class__.namespace_opts(prefix, obj.name, opts)
                print("Runnin' obj: \"" + obj.name)
                lispLoadStr = runner.run(obj, opts)
                feedback.append(lispLoadStr)
        print("\n\n\n\n #\n # paste this in acad cmd: \n #")
        print("##########################################\n\n")
        print("\n".join(feedback))
        print("\n\n##########################################")
        print("### -- done -- ### Faces: ", BlendOneLisp.faces)

        
    @staticmethod
    def preset_odeon():
        __class__.preset("odeon")

    @staticmethod
    def preset_aist():
        __class__.preset("aist")
    
    def __init__(self, opts = {}):
        self.opts = { # defaults
            "cad3dpoly":True, # use 3d poly command
            "cad3face":True, # use 3d face command
            "_flipZ":False, # flip Zed axis upon export >> not often needed
            "units":1000, #enlarge values if autocad is set in milimeters
            "function_call":'function_call',
            "filepath":'filepath_dated.lsp', #must be lsp for aCad
            "resolution":3,
            "acad_layer": "new_layer",
            "preset": "x"
        }

    def run(self, obj, opts = {}):
        self.opts.update(opts)
        line = '(defun c:'+self.opts["function_call"]+'()'
        line += '(command "DELAY" 500)'
        line += '(command "._layer" "_M" "'+self.opts["acad_layer"]+'" "")'
        line += '(command "DELAY" 500)'

        bm = bmesh.new()
        context = bpy.context
        scene = context.scene
        mesh = obj.to_mesh(scene, False, 'PREVIEW')
        bm.from_mesh(mesh)

        f = 0
        # mesh = bmesh.from_edit_mesh(bpy.context.object.data)
        for p in bm.faces:
            f += 1
            if self.opts["cad3face"] and len(p.verts) > 4 and self.opts["preset"] != "aist":
                s="!!!! got extra verts on face"
                print("---------\n%s\n---------" % s, len(p.verts))
            if len(p.verts) == 4 and self.opts["cad3face"]: #3dface can have 4points MAX ( 3point have different spacings )
                line+='(command "._3dface" '
                for v in p.verts:
                    exp = ','.join(map(str,map(self.multby,self.prep(v.co))))
                    line+='"'+exp+'" '
                line += '"")'
            elif len(p.verts) == 3 and self.opts["cad3face"]: #3dface can have 4points MAX ( 3point have different spacings )
                line+='(command "._3dface" '
                for v in p.verts:
                    exp = ','.join(map(str,map(self.multby,self.prep(v.co))))
                    line+='"'+exp+'" '
                line += '"" "")'
            elif self.opts["cad3dpoly"]: #fallback to 3d polyline
                if self.opts["preset"] == "aist" and len(p.verts) > 28:
                    print("Exceeded 28 vertexes AIST limit: ", len(p.verts))

                line+='(command "._3dpoly" '
                for v in p.verts:
                    exp = ','.join(map(str,map(self.multby,self.prep(v.co))))
                    line+='"'+exp+'" '
                # close polyline on first vert
                exp = ','.join(map(str,map(self.multby,self.prep(p.verts[0].co))))
                line+='"'+exp+'" '
                line += '"")'
            else:
                s="unrendered some data"
                print("---------\n%s\n---------" % s)
        line += ')'
        fo = open(self.opts["filepath"], 'w+')
        fo.write( line )
        
        fo.close()
        print("faces: ", f)
        BlendOneLisp.faces += f
        return '(load "' + os.path.realpath(fo.name) + '")\n' + opts["function_call"]

    def prep(self, elem): #apply transforms
        if self.opts["_flipZ"]:
            elem[2] = 0 - elem[2]
        return elem

    def multby(self, elem): 
        return round(elem * self.opts["units"],self.opts["resolution"])


#BlendOneLisp.preset_odeon()
BlendOneLisp.preset_aist()
