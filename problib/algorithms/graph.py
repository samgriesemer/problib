class Graph():
    '''
    Base graph object. Maintains a collection of nodes and their edge connections
    '''
    def __init__(self, nodes, edges):
        pass

    @classmethod
    def from_adj_mat(cls, matrix):
        '''
        Adjacency matrix as an NxN NumPy array 
        '''
        pass

    @classmethod
    def from_adj_list(cls, lst):
        '''
        Adjacency list structure as a dictionary of lists, indexed by vertex
        numbers ("ids") and values as the vertices to which they're connected
        {
            0: [1, 5, 6],
            ...,
            N: [9, 5]
        }
        '''
        pass
