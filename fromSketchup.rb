#NOTE: all layers must be set to visible before running exploderVerbose_fn
#or you will get million of annoying messages like:
#Your recent operation has caused visible geometry to merge with existing geometry on a hidden layer
#[ok] ?

def exploderVerbose(l)
    puts "==========PASS %s" % [l]
    groups=[]
    # Sketchup.active_model.selection.each do |e|
    Sketchup.active_model.selection.each do |e|
        if e.is_a? Sketchup::Group
            groups << e
        end
    end
    puts "+++++++++++GROUPS LENGTH %s" % [groups.length]
    if groups.length != 0
        return nil if UI.messagebox("Proceed?", MB_YESNO) == 7
        groups.each do |g|
            g.explode
        end
        exploderVerbose(l+=1)
    end
end
exploderVerbose(1)

def exploderVerboseComponents(l)
    if l < 80
        puts "==========PASS %s" % [l]
        Sketchup.active_model.entities.to_a.each do |c|
            if c.is_a? Sketchup::ComponentInstance
                c.explode
                exploderVerboseComponents(l+=1)
                break
            end
        end
    else
        ll = []
        Sketchup.active_model.entities.to_a.each do |c2|
            if c2.is_a? Sketchup::ComponentInstance
                ll << c2
            end
        end
        puts "%s MORE TO GO" % ll.length
        if ll.length
            return nil if UI.messagebox("Proceed?", MB_YESNO) == 7
            exploderVerboseComponents(1)
        else
            puts "ALL DONE!!"
        end
    end
end
exploderVerboseComponents(1)

$facesInVects = []
m=Sketchup.active_model.selection

def blend(m)
    m.each do |e|
        if e.typename == 'Group'
            blend(e.entities)
            break
            return
        end
        desc = [[],[],[]] # 0-verts;1-edges;2-faces
        if e.is_a? Sketchup::Face
            descverts = []
            descedges = []
            e.vertices.each do |vertice|
                rondedPoints = []
                vertice.position.to_a.each do |point|
                    point = point/10
                    rondedPoints << point.round(2)
                end
                descverts << rondedPoints
            end
            desc[0] = descverts
            if e.vertices.length < 5
                desc[2] = (0..e.vertices.length-1).to_a
            else
                e.edges.each do |edge|
                    rondededgV=[]
                    edge.vertices.each do |edgV|
                        edgV2=[]
                        edgV.position.to_a.each do |a|
                            a=a/10
                            a=a.round(2)
                            edgV2 << a
                        end
                    rondededgV << desc[0].index(edgV2)
                    end
                   descedges << rondededgV
                end
                desc[1] = descedges
            end
            $facesInVects << desc
        end
    end
end
blend(m)
IO.write('/tmp/goToBlender.txt', $facesInVects)




## Hide components
m=Sketchup.active_model.selection
def hideComponents(group)
    group.each do |e|
        if e.typename == 'ComponentInstance'
            e.hidden = 1
        elsif e.typename == 'Group'
            hideComponents(e.entities)
        end
    end
end
hideComponents(m)


## Delete free edges
m=Sketchup.active_model.selection
def deleteFreeEdges(group)
    group.each do |e|
        if e.typename == 'Edge'
            if e.faces.length == 0
                e.erase!
            end
        elsif e.typename == 'Group'
            deleteFreeEdges(e.entities)
        elsif e.typename == 'Face'
            if e.deleted?
                puts "yee"
            end
            deleteFreeEdges(e.edges)
        end
    end
end
deleteFreeEdges(m)




## PYTHONS DIR ##
class Object
  def local_methods
    (methods - Object.instance_methods).sort
  end
end