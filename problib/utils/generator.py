def exhaust(gen, verbose=True, interval=1):
    '''
    Exhaust given generator, printing items along
    the way (if verbose=True) at specified interval.
    Return final element of the generator.
    '''
    for i, item in enumerate(gen):
        if verbose and i % interval == 0:
            print(item)
    return item
