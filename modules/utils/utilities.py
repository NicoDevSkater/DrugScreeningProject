

def strip_path(path, n) -> str:

    arr = path.split('/')
    
    #remove last element which is the fila name
    for _ in range(n):    
        
        arr.pop()

    to_string = '/'.join(arr)

    return to_string