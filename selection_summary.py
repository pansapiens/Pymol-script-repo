"""
--- selection_summary : summarize selections by residue ---
Authors : Andrew Perry
Program : selection_summary
Date    : May 2012
"""

"""
   selection_summary --
    Print a summary of the highest and lowest residue id in every selection.
    
    eg,
    
    PyMoL> selection_summary offset=10
    
    Outputs:
    # selectionA: 15-26
    # selectionB: 45-79
    # sele: 101-259
    
    Useful when you have manually selected a set of named sequence ranges 
    (loopA, loopB, etc) and want to document them outside of Pymol.

    PARAMS

        offset (int)
            If set, adds this value to all output residue ids.
            Useful to shift values to native sequence numbering in some
            situations.
            DEFAULT: 0
        
        all_residues (boolean)
            If all_residues=True, return every residue in the selection, not
            just the lowest and highest residue number.
            DEFAULT: False
        
        as_script (boolean)
            Outputs selection commands that could recreate the selections 
            by residue. Assumes each selection encompasses only one object/model.

    RETURNS
        A dictionary of the format { selection_name : (i_resi, j_resi) }, 
        or if all_residues=True, 
        { selection_name : (i_resi, j_resi, k_resi .. etc) }

    SIDE-EFFECTS
        Modifies the B-factor columns in your original structures.
"""
import sets

def strTrue(p):
  return p[0].upper() == "T"
    
def selection_summary(offset=0, all_residues="False", as_script="False"):
  offset=int(offset)
  returndic = {}
  for sel in cmd.get_names("selections"):
    s = sets.Set()
    # get the residue numbers for this selection
    cmd.iterate(sel, 's.add(resi)', space={'s':s})
    
    # hack to get the model name. there must be a better way
    mod = []
    cmd.iterate(sel, 'mod.append(model)', space={'mod':mod})
    try:
      mod = mod[0] + " and"
    except IndexError:
      mod = ""
    ##
    
    l = list(s)
    l.sort()
    resints = map(int, l)
    # TODO: (this logic would be better as a 
    #        switch/case now that it's more complex)
    if resints and not strTrue(all_residues) and not strTrue(as_script):
      maxresi = max(resints)
      minresi = min(resints)
      print "# %s: %i-%i" % (sel, minresi+offset, maxresi+offset)
      returndic[sel] = (minresi+offset, maxresi+offset)
    elif strTrue(all_residues) and not strTrue(as_script):
      print "# " + sel + ": " + ", ".join(l)
      returndic[sel] = resints
    elif strTrue(as_script):
      if strTrue(all_residues):
        print "select %s, %s " % (sel, mod) + "i. " + " i. ".join(l)
        returndic[sel] = resints
      elif resints:
        maxresi = max(resints)
        minresi = min(resints)
        print "select %s, %s i. %i-%i" % (sel, mod, minresi, maxresi)
        returndic[sel] = (minresi+offset, maxresi+offset)
      
  return returndic
    
cmd.extend('selection_summary', selection_summary)

