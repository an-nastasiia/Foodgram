def check_for_duplicates(value):
    '''Check if there are duplicates in a list.'''
    value_set = []
    for elem in value:
        if elem in value_set:
            return True
        value_set.append(elem)
    return False
