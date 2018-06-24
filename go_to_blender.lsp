; workflow #1
; create layer named GO_TO_BLENDER (window>layers)
; set point visible (format>point style)
; .. then  this output:
(defun c:gotoblender()
    (setq ss (ssget "x" '((0 . "POINT")(8 . "GO_TO_BLENDER"))))
    (setq count 0)
    (setq len (sslength ss))
    (princ "\n---- [")
    (while (< count len)
        (setq entity (ssname ss count))
        (setq entitycoords (assoc 10 (entget entity)))
        (princ "(")
        (princ (nth 1 entitycoords))
        (princ ",")
        (princ (nth 2 entitycoords))
        (princ ",")
        (princ (nth 3 entitycoords))
        (princ "),")
        (setq count (1+ count))
    )
    (princ "]")
    (princ)
)
; # goes here
; import bpy,bmesh,mathutils,math
; 
; def create_vertices (name, verts):
;    # Create mesh and object
;    me = bpy.data.meshes.new(name+'Mesh')
;    ob = bpy.data.objects.new(name, me)
;    ob.show_name = True
;    # Link object to scene
;    bpy.context.scene.objects.link(ob)
;    me.from_pydata(verts, [], [])
;    # Update mesh with new data
;    me.update()
;    return ob

