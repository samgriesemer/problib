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

def chunk(gen, n, last=True):
    '''
    map generator <gen> to "chunked" generator,
    yeilding lists of <n> elements of the original
    generator. Last chunk not guaranteed to be size
    <n>, can specific last=False if partial chunks 
    shouldn't be returned.

    TODO: consider adding a time parameter as well, 
    such that if <n> items have not arrived from the
    original generator in <t> seconds, return the 
    current chunk. Could protect against long running,
    async generator processes (and may be useful for
    time dependent physics sims)
    '''
    chunk = []
    for item in gen:
        chunk.append(item)
        if len(chunk) == n:
            yield chunk
            chunk = []

    if last and chunk:
        yield chunk
