# =============================
# Student Names: Hannah Larsen, Nathan Saric
# Group ID: Group 13
# Date: Feb 13, 2022
# =============================
# propagators.py
# desc: A file containing various different propagator methods used
# to solve CSP problems as outlined in the test.py file.


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []



def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
    
    # Initializing empty list to keep track of pruned variable/value pairs
    prunedVars = []

    if not newVar:  
        # Do forward checking ALL constraints
        queue = csp.get_all_cons()
    else:
        # Do forward checking but only with constraints containing newVar
        queue = csp.get_cons_with_var(newVar)

    # After constraints are obtained based on newVar, iterate through constraints list
    for x in queue:
        # If there's only 1 var in scope of x's constraints, get the variables the constraint is over
        if x.get_n_unasgn() == 1:
            varScope = x.get_scope()

            for v in varScope:

                # Looking for unassigned variables and making the current domain 
                # the domain of the unassigned var
                if v.is_assigned() == False:
                    currentDom = v.cur_domain()
                    unasgn = v

            # Looping through current domain of unassigned var
            for val in currentDom:
                # Initializing an empty list for values
                valList = []
                # Assigning val to unassigned variable
                unasgn.assign(val)

                # Looping through list of vars in the scope of x and appending assigned values
                for v in varScope:
                    valList.append(v.get_assigned_value())

                # If assignment doesnt satisfy constaints [as per 'check' function in cspbase]
                if x.check(valList) == False:

                    # Pruning values that dont satisfy requirements
                    if unasgn.in_cur_domain(val):
                        unasgn.prune_value(val)
                        prunedVars.append((unasgn, val))

                    # If domain size reaches 0, return False & pruned var list
                    if unasgn.cur_domain_size == 0:
                        # Unassigning the val we previously assigned above
                        unasgn.unassign()
                        return (False, prunedVars)

                # Unassigning the val we previously assigned above
                unasgn.unassign()

# Returning True and pruned var list
    return (True, prunedVars)



# *THIS ALGORITHM WAS INFLUENCED BY WEEK 3 LECTURE NOTES ON GAC*
def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
    processing all constraints. Otherwise we do GAC enforce with
    constraints containing newVar on GAC Queue'''

    # Initializing empty list to keep track of pruned variable/value pairs
    prunedVars = []

    if not newVar:  
        # Do forward checking ALL constraints
        queue = csp.get_all_cons()
    else:
        # Do forward checking but only with constraints containing newVar
        queue = csp.get_cons_with_var(newVar)

    # While queue is NOT empty
    while len(queue) != 0:
        # Remove the first item off the queue
        x = queue.pop(0)

        # Looping through the list of variables the constraint is over (from queue)
        for y in x.get_scope():

            # Looping through remaining values of current domain
            for z in y.cur_domain():

                # Seeing if (Variable, Value) pair has supporting tuple [see cspbase]
                # If it is NOT a supporting tuple, prune it!
                if x.has_support(y, z) == False:

                    # Pruning the unsupported value and adding (Variable, Value) pair to prunedVars
                    if y.in_cur_domain(z):
                        y.prune_value(z)
                        prunedVars.append((y, z))

                    # If the current domain is eventually empty, False & pruned vars are returned
                    if y.cur_domain_size() == 0:
                        return (False, prunedVars)

                    # Constraints containing variable y are pushed back onto the queue after pruning
                    else:
                        for i in csp.get_cons_with_var(y):
                            if i not in queue:
                                queue.append(i)

    # Nothing was triggered in the nested for loops, so
    # True and prunedVars can be returned
    return (True, prunedVars)
