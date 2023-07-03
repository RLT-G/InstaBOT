def remove_duplicates(lst):
    result = []
    unique_elements = set()

    for item in lst:
        if item not in unique_elements:
            unique_elements.add(item)
            result.append(item)

    return result
