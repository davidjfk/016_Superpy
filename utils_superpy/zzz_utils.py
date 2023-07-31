

def make_id_for_each_row_in_csv_file(csv_file_name_first_letter, first_nr_in_range):
    ''' 
    e.g. "b" is abbreviation of 'bought.csv'. This 'b' will be part of 
    argparse argument, so needs to be concise for pleasant user 
    experience.    
    '''
    count = first_nr_in_range
    count -= 1 # to start with 1, not 0
    def counter():
        nonlocal count
        '''
        note to self: nonlocal is keyword that allows 
        you to assign to variables in outer 
        (but non-global) scope.  
        jsComp: no kw nonlocal in javascript.      
        '''
        count += 1
        return f"{csv_file_name_first_letter}_{count}"
    return counter


 












