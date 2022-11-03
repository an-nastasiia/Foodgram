def check_for_duplicates(value):
    '''Проверка на наличие повторяющихся элементов в списке.'''
    value_set = []
    for elem in value:
        if elem in value_set:
            return True
        else:
            value_set.append(elem)
    return False
