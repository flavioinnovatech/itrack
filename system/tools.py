from itrack.system.models import System
from collections import Iterable

def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

# Creates the list of childs for the system with id = 'parent'. 
# Returns the id's of the childs
def findChild(parent):
    if (System.objects.filter(parent__id=parent).count() == 0):
		return []
    else:
        u=[]
        for x in System.objects.filter(parent__id=parent):
            n = x.id
            u.append(n)
            el = findChild(n)
            if el != []:
                u.append(el)
        return u
        
#creates the list of childs for the system with id ='parent'
# Returns the instances of childs
def findChildInstance(parent):
    if (System.objects.filter(parent__id=parent).count() == 0):
		return []
    else:
        u=[]
        for x in System.objects.filter(parent__id=parent):
            n = x
            u.append(n)
            el = findChildInstance(n.id)
            if el != []:
                u.append(el)
        return u

#checks if 'system' is a child of the list of childs 'list'        
def isChild(system,childs):
    is_child = False
    for sys in childs:
        if sys == system:
            #found the system in the list
            return True
        elif sys == [] and is_child == False:
            #not found the system yet
                is_child = False
        elif type(sys).__name__ == "list" and is_child == False:
            #if its a list, search recursively inside it
            is_child = isChild(system,sys)
    return is_child
    
def serializeChild(childs,ser_list=[]):
    if childs == []: 
        return []
    for x in childs:
        if  type(x).__name__ == "list":
        #if its a list, execute recursively inside it
            serializeChild(x,ser_list)
        else:
        #if its a number, append it
            ser_list.append(x)           
    return ser_list
    
#creates the list of childs for the system with id = 'parent', for the direct childs of the system
def findDirectChild(parent):
        u=[]
        for x in System.objects.filter(parent__id=parent):
            u.append(x.id)
        return u

#calculates the depth of the system
def systemDepth(system):
    if system.parent is None:
        return 0
    else:
        return systemDepth(system.parent) + 1


#given a system list, return the system with the lowest depth        
def lowestDepth(system_list):
    lowest = systemDepth(system_list[0])
    result = system_list[0]
    for system in system_list[1:]:
        depth = systemDepth(system)
        if depth > lowest:
            lowest = depth
            result = system
    
    return result
 
#find all parents of a system. you can pass initial values to the return list if needed.    
def findParents(child,parents):
    
    while child.parent != None:
        parents.append(child.parent)
        child = child.parent
            
    return parents
