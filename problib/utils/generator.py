def exhaust(gen, func=None, interval=1, verbose=True, last=True):
    '''
    Exhaust given generator, applying given function (func)
    to items along  the way (if verbose=True) at specified 
    interval. Return final element of the generator.
    '''
    for i, item in enumerate(gen):
        if i % interval == 0:
            if func: func(item)
            if verbose: print(item)
    
    # perform same actions for last item
    if last and i % interval != 0:
        if func: func(item)
        if verbose: print(item)

    return item
