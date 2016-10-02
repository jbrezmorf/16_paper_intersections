import json
import numpy as np

'''
def get_frame(data, addr):
    frame=data
    for (level,idx) in enumerate(addr):        
        if "children" in frame:
            childs=frame["children"]
            if idx >= len(childs):
                print "Error: idx {} greater then number of child {} at level {}".format(idx, len(childs), level)
                return None
            else:
                frame=childs[idx]
        else:
            print "No childs at level {}".format(level)
            return None
    return frame    
'''

def get_frame_tag(data, tag):
    if (data["tag"] == tag):
        return data   
    for child in data.get("children", []):        
        frame = get_frame_tag(child, tag)
        if (frame != None):
            return frame 
    return None

def get_frame_tags(data, tags):
    frame =data
    for tag in tags:
        frame = get_frame_tag(frame, tag)        
        if frame == None:
            return None
    return frame    

class ProfilerTable:
    def __init__(self, n_tests):
        self.table = {}
        self.n_tests = n_tests
        
    
    def append(self, i_test, frame, item):        
        if frame == None:
            return
        if not frame["tag"] in self.table:
            self.table[frame["tag"]]=[0]*self.n_tests
            
        self.table[frame["tag"]][i_test] = frame[item]
        #print self.table
        
    def save(self, f_name):
        with open(f_name, "w") as out_file:    
            for (tag, values) in self.table.iteritems():
                row='"' + tag + '"'
                for value in values:
                    row+=", {}".format(value)
                out_file.write(row+"\n")
    
    def statistics(self, f_name):
        

def algorithm_variant(f_base, subdata):
    table = ProfilerTable(7)
    for i_test in range(0, 7):    
        f_name=f_base + "{}.msh.log".format(i_test)
        with open(f_name) as data_file:    
            data = json.load(data_file)
            frame_0  = data["children"][0]
            table.append(i_test, get_frame_tag(frame_0, "MESH - setup topology"), "cumul-time-min")
            table.append(i_test, get_frame_tag(frame_0, "Intersections 2D-3D"), "cumul-time-min")        
            table.append(i_test, get_frame_tag(frame_0, "Intersection initialization"), "cumul-time-min")
            table.append(i_test, get_frame_tag(frame_0, "BIHTree"), "cumul-time-min")
            table.append(i_test, get_frame_tag(frame_0, "Element iteration"), "cumul-time-min")
            table.append(i_test, get_frame_tag(frame_0, "Compute intersection"), "call-count-min") # initial intersection, number of components?
            table.append(i_test, get_frame_tags(frame_0, [subdata, "Compute intersection"]), "call-count-min") # "Compute intersection" second
            table.append(i_test, get_frame_tags(frame_0, [subdata, "CI trace opt"]), "call-count-min") # 
            table.append(i_test, get_frame_tags(frame_0, [subdata, "CI trace convex hull"]), "call-count-min") # "CI trace convex hull"
            table.append(i_test, get_frame_tag(frame_0, "intersection_exists"), "call-count-min")  # initial pairs excluded          
    table.save(f_base+"_summary.csv")
    table.statistics(f_base)
    
algorithm_variant("prof_BIHtree_test1_cube", subdata="Bounding box element iteration")            
algorithm_variant("prof_test1_cube", subdata = "Prolongation algorithm")
algorithm_variant("prof_BB_test1_cube", subdata = "Prolongation algorithm")