# =============================
# Student Names: Hannah Larsen, Nathan Saric
# Group ID: Group 13
# Date: Feb 13, 2022
# =============================
# heuristics.py
# desc: A file containing different heuristic methods that return
# specific variables based on the definition of each heuristic.


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return variables according to the Degree Heuristic 
    Definiton of Degree Heuristic: assigning a value to the variable 
    included in the most constraints on other unassigned variables'''
    
    # Initializingnunassigned variables, a minimum constraint (that will be updated later)
    # and a 'best var' which is the var we will end up returning
    minCons = 0
    bestVar = None

    # Looping through unassigned variables to find var in the most constraints
    for i in csp.vars:
        if (len(csp.get_cons_with_var(i)) > minCons):
            minCons = len(csp.get_cons_with_var(i))
            bestVar = i
                    
    return bestVar


def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic 
    Definition of Minimum Remaining Value Heuristic: choosing the variable 
    with the fewest possible values'''
    
    # Initializing unassigned variables, minimum variable, and minimum domain
    v = csp.get_all_unasgn_vars()
    minVar = v[0]
    minDomain = minVar.cur_domain_size()

    # Looping through unassigned variables to find smallest domain size
    # Updating minVar and minDomain whenever we find a new minimum
    for i in csp.vars:
        if i.cur_domain_size() < minDomain:
            minVar = i
            minDomain = i.cur_domain_size()

    # Once loop terminates, current minVar will be the minimum, which is returned
    return minVar

