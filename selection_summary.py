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
    selectionA: 15-26
    selectionB: 45-79
    sele: 101-259
    
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
    
def selection_summary(offset=0, all_residues="False"):
  offset=int(offset)
  returndic = {}
  for sel in cmd.get_names("selections"):
    s = sets.Set()
    cmd.iterate(sel, 's.add(resi)', space={'s':s})
    l = list(s)
    l.sort()
    resints = map(int, l)
    if resints and not strTrue(all_residues):
      maxresi = max(resints)
      minresi = min(resints)
      print "%s: %i-%i" % (sel, minresi+offset, maxresi+offset)
      returndic[sel] = (minresi+offset, maxresi+offset)
    elif strTrue(all_residues):
      print sel + ": " + ", ".join(l)
      returndic[sel] = resints

  return returndic
    
cmd.extend('selection_summary', selection_summary)

