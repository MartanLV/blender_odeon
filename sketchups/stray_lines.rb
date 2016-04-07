# Copyright 2004-2006, Todd Burch - Burchwood USA   http://www.burchwoodusa.com 

=begin
Smustard.com(tm) Ruby Script End User License Agreement

This is a License Agreement is between you and Smustard.com.

If you download, acquire or purchase a Ruby Script or any freeware or any other product (collectively "Scripts") from Smustard.com, then you hereby accept and agree to all of the following terms and conditions:

Smustard.com, through its agreements with individual script authors, hereby grants you a permanent, worldwide, non-exclusive, non-transferable, non-sublicensable use license with respect to its rights in the Scripts.

If you are an individual, then you may copy the Scripts onto any computer you own at any location.

If you are an entity, then you may not copy the Scripts onto any other computer unless you purchase a separate license for each computer and you must have a separate license for the use of the Script on each computer.

You may not alter, publish, market, distribute, give, transfer, sell or sublicense the Scripts or any part of the Scripts.

This License Agreement is governed by the laws of the State of Texas and the United States of America.

You agree to submit to the jurisdiction of the Courts in Houston, Harris County, Texas, United States of America, to resolve any dispute, of any kind whatsoever, arising out of, involving or relating to this License Agreement.

THIS SOFTWARE IS PROVIDED "AS IS" AND WITHOUT ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, 
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

This software has not been endorsed or sanctioned by Google.  Any comments, concerns or issues about this software 
or the affects of this software should be not directed to Google, but to Smustard.com.  
=end


# Name :          stray_lines.rb 1.0
# Description :   This script functions against open ended line segments. It will: 
#
#                     1. Label them, 
#                     2. Select them, 
#                     3. Delete them 
#                     4. Hide everything else so you can see them.
#
# Author :        Todd Burch   http://www.smustard.com
# Usage :         1. select the part of a drawing that you want analyzed, or, select nothing 
#                 and the whole drawing will be analyzed. 
#                 2. Click "Stray Lines" from the Plugins menu and then choose a sub option.
# Date :          12.May.2006
# Type :          Plugin. This will typically be used on Imported CAD Drawings 
# History:        1.0 (12.May.2006) - First version. Based on label_stray_lines.rb and 
#                                     select_stray_lines.rb
#                                  
#-----------------------------------------------------------------------------

require 'sketchup.rb' 

class BadDrawing 

def BadDrawing.get_lone_verts(ents) 
  loneverts = Array.new ; 
  ents.each {|e| 
    if  e.class == Sketchup::Edge then   # If this is an edge...  
      e.vertices.each {|v|               # ...loop through its vertices... and 
        loneverts.push(v) if v.edges.length == 1 }  # ...see if there is only 1 connected edge.
      end   # if 
    } 
  loneverts ;      # return the array of vertices that have only 1 edge 
  end ;     

def BadDrawing.labelLines 
  lonepoints = Array.new 
  am = Sketchup.active_model        # Sketchup Active Model. 
  se = am.active_entities           # Sketchup Active Entities - my scope of work 
  ae = am.selection                 # Work with user's selection, if any... 
  if ae.length == 0 then ae = se end     # ...else work with entities within my scope. 

  # Get the point3d's of all the single edged vertices. 
  lonepoints = BadDrawing.get_lone_verts(ae).collect {|e| e.position } 

  if lonepoints.length==0 then 
    UI.messagebox("There were no stray lines\nin the Selection.",0,"Label Stray Lines") ; 
    return false ; 
    end ; 
  am.start_operation "Label Stray Lines"        # Encapsulate into a single UNDO operation.
  i=1 
  lonepoints.each {|p| 
    se.add_text(i.to_s + " of " + lonepoints.length.to_s , p, [0,0,5] )    # Add the Text Label. 
    i+=1  } 
  am.commit_operation          # End of UNDO capsule.   
  true ; 
  end  # def labellines 

def BadDrawing.selectLines 
  add_to_selection = false          # Assume we are removing from the selection.  
  am = Sketchup.active_model        # Sketchup Active Model. 
  se = am.active_entities           # Sketchup active Entities. 
  ae = am.selection                 # Work with selection, if any... 
  if (ae.length == 0) then          # Nothing selected if 0 
    add_to_selection = true         # We are adding to the current selection... 
    ae = se                         # Work with all unselected items. 
    end 
  if add_to_selection then 
    BadDrawing.get_lone_verts(ae).collect {|e| am.selection.add(e.edges[0]) }  
  else 
  (ae.to_a-(BadDrawing.get_lone_verts(ae).collect {|e| e.edges[0]})).collect {|ent| am.selection.remove(ent)} 
    end ; 
  end  # def 

def BadDrawing.deleteLines 
  am = Sketchup.active_model ; 
  BadDrawing.selectLines ;       # Make the Strays the currect selection set 
  if (am.selection.length==0) then 
    UI.messagebox("There were no Stray Lines\nin the Selection to Delete",0, "Delete Stray Lines") ; 
    return false; 
    end ; 
  am.start_operation "Delete Stray Lines" ; 
  am.active_entities.erase_entities(Sketchup.active_model.selection) ; 
  am.commit_operation ; 
  true 
  end 

def BadDrawing.showLines 
  am = Sketchup.active_model ; 
  BadDrawing.selectLines ;       # Make the Strays the currect selection set 
  if (am.selection.length==0) then 
    UI.messagebox("There were no Stray Lines\nin the Selection to Show",0, "Show Stray Lines") ; 
    return false ; 
    end ; 
  am.start_operation("Show Only Stray Lines") ; 
  am.selection.toggle(am.active_entities.to_a)
  am.selection.collect {|ent| ent.hidden=true } ;  
  am.selection.clear ; 
  am.commit_operation ; 
  true 
  end ; 

end # class BadDrawing 

if not file_loaded?("stray_lines.rb") then 
  # Add the function to the Plugins Menu.
  submenu = UI.menu("Plugins").add_submenu("Stray Lines")
  submenu.add_item("Label")     { UI.beep if BadDrawing.labelLines  } 
  submenu.add_item("Select")    { BadDrawing.selectLines ; UI.beep  } 
  submenu.add_item("Delete")    { UI.beep if BadDrawing.deleteLines } 
  submenu.add_item("Show Only") { UI.beep if BadDrawing.showLines   } 
  end 

file_loaded("stray_lines.rb")   # Mark the script loaded.  