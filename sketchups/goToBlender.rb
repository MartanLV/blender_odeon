def unfoldLoop(anyLoop, outerLoop)
    # if anyLoop == outerLoop
    #     puts "<<"
    # end
    verts = []
    anyLoop.vertices.each do |v|
        verts << v.position.to_a
    end
    return [
        verts,
        (0..anyLoop.vertices.length-1).to_a,
    ]
end

def blend(m)
    m.each do |e|
        if e.typename == 'Group'
            blend(e.entities)
        elsif e.typename == 'Face'
            ol = e.outer_loop # apply boolean later
            e.loops.each do |l|
                $facesInVects << unfoldLoop(l, ol)
            end
        end
    end
end

def wrap(filename)
    $facesInVects = []
    m=Sketchup.active_model.selection
    blend(m)
    # index='fasades-002'
    index=filename
    IO.write('/tmp/lastExport.txt', index)
    IO.write('/Users/dacetiruma/oo-MARTINS-oo/260316-Rimi/BlenderTXT/%s.txt' % index, $facesInVects)
end

# wrap('fasades-001')