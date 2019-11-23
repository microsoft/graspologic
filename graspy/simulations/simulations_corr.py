# Copyright 2019 NeuroData (http://neurodata.io)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
from graspy.simulations import sample_edges, er_np, sbm


def sample_edges_corr(P, R, directed, loops):
    """
    Generate a pair of correlated graphs with Bernoulli distribution.
    Both G1 and G2 are binary matrices. 

    Parameters
    ----------
    P: np.ndarray, shape (n_vertices, n_vertices)
        Matrix of probabilities (between 0 and 1) for a random graph.
        
    R: np.ndarray, shape (n_vertices, n_vertices)
        Matrix of correlation (between 0 and 1) between graph pairs.

    directed: boolean, optional (default=False)
        If False, output adjacency matrix will be symmetric. Otherwise, output adjacency
        matrix will be asymmetric.

    loops: boolean, optional (default=False)
        If False, no edges will be sampled in the diagonal. Otherwise, edges
        are sampled in the diagonal.

    References
    ----------
    .. [1] Vince Lyzinski, et al. "Seeded Graph Matching for Correlated Erdos-Renyi Graphs", 
       Journal of Machine Learning Research 15, 2014
        
    Returns
    -------
    G1: ndarray (n_vertices, n_vertices)
        Adjacency matrix the same size as P representing a random graph.

    G2: ndarray (n_vertices, n_vertices)
        Adjacency matrix the same size as P representing a random graph.

    Examples
    --------
    >>> np.random.seed(1)
    >>> p = 0.5
    >>> r = 0.3
    >>> R = r * np.ones((5, 5))
    >>> P = p * np.ones((5, 5))

    To sample a correlated graph pair based on P and Rho matrices:

    >>> sample_edges_corr(P, R, directed = False, loops = False)
    (array([[0., 1., 0., 0., 0.],
            [1., 0., 0., 0., 0.],
            [0., 0., 0., 0., 1.],
            [0., 0., 0., 0., 1.],
            [0., 0., 1., 1., 0.]]), array([[0., 1., 0., 0., 0.],
            [1., 0., 1., 0., 1.],
            [0., 1., 0., 1., 1.],
            [0., 0., 1., 0., 1.],
            [0., 1., 1., 1., 0.]]))
    """
    # test input
    # check P
    if type(P) is not np.ndarray:
        raise TypeError("P must be numpy.ndarray")
    if len(P.shape) != 2:
        raise ValueError("P must have dimension 2 (n_vertices, n_dimensions)")
    if P.shape[0] != P.shape[1]:
        raise ValueError("P must be a square matrix")

    # check R
    if type(R) is not np.ndarray:
        raise TypeError("R must be numpy.ndarray")
    if len(R.shape) != 2:
        raise ValueError("R must have dimension 2 (n_vertices, n_dimensions)")
    if R.shape[0] != P.shape[1]:
        raise ValueError("R must be a square matrix")

    # check directed and loops
    if type(directed) is not bool:
        raise TypeError("directed is not of type bool.")
    if type(loops) is not bool:
        raise TypeError("loops is not of type bool.")

    G1 = sample_edges(P, directed=directed, loops=loops)
    P2 = G1.copy()
    P2 = np.where(P2 == 1, P + R * (1 - P), P * (1 - R))
    G2 = sample_edges(P2, directed=directed, loops=loops)
    return G1, G2


def er_corr(n, p, r, directed, loops):
    """
    Generate a pair of correlated graphs with specified edge probability
    Both G1 and G2 are binary matrices. 

    Parameters
    ----------
    n: int
       Number of vertices

    p: float
        Probability of an edge existing between two vertices, between 0 and 1.
    
    r: float
        The value of the correlation between the same vertices in two graphs.
    
    directed: boolean, optional (default=False)
        If False, output adjacency matrix will be symmetric. Otherwise, output adjacency
        matrix will be asymmetric.
    
    loops: boolean, optional (default=False)
        If False, no edges will be sampled in the diagonal. Otherwise, edges
        are sampled in the diagonal.
    
    Returns
    -------
    G1: ndarray (n_vertices, n_vertices)
        Adjacency matrix the same size as P representing a random graph.

    G2: ndarray (n_vertices, n_vertices)
        Adjacency matrix the same size as P representing a random graph.
    
    Examples
    --------
    >>> np.random.seed(2)
    >>> p = 0.5
    >>> r = 0.3
    >>> n = 5

    To sample a correlated ER graph pair based on n, p and R matrices:

    >>> er_corr(n, p, r, directed=False, loops=False)
    (array([[0., 0., 1., 0., 0.],
        [0., 0., 0., 1., 0.],
        [1., 0., 0., 1., 1.],
        [0., 1., 1., 0., 1.],
        [0., 0., 1., 1., 0.]]), array([[0., 1., 1., 1., 0.],
        [1., 0., 0., 1., 0.],
        [1., 0., 0., 1., 1.],
        [1., 1., 1., 0., 1.],
        [0., 0., 1., 1., 0.]]))
    """
    # test input
    # check n
    if not np.issubdtype(type(n), np.integer):
        raise TypeError("n is not of type int.")
    elif n <= 0:
        msg = "n must be > 0."
        raise ValueError(msg)

    # check p
    if not np.issubdtype(type(p), np.floating):
        raise TypeError("r is not of type float.")
    elif p < 0 or p > 1:
        msg = "p must between 0 and 1."
        raise ValueError(msg)

    # check r
    if not np.issubdtype(type(r), np.floating):
        raise TypeError("r is not of type float.")
    elif r < 0 or r > 1:
        msg = "r must between 0 and 1."
        raise ValueError(msg)

    # check directed and loops
    if type(directed) is not bool:
        raise TypeError("directed is not of type bool.")
    if type(loops) is not bool:
        raise TypeError("loops is not of type bool.")

    P = p * np.ones((n, n))
    R = r * np.ones((n, n))
    G1, G2 = sample_edges_corr(P, R, directed=directed, loops=loops)
    return G1, G2


def sbm_corr(n, p, r, directed, loops):
    """
    Generate a pair of correlated graphs with specified edge probability
    Both G1 and G2 are binary matrices. 

    Parameters
    ----------
    n: list of int, shape (n_communities)
        Number of vertices in each community. Communities are assigned n[0], n[1], ...

    p: array-like, shape (n_communities, n_communities)
        Probability of an edge between each of the communities, where p[i, j] indicates 
        the probability of a connection between edges in communities [i, j]. 
        0 < p[i, j] < 1 for all i, j. 

    r: float
        Probability of the correlation between the same vertices in two graphs.
    
    directed: boolean, optional (default=False)
        If False, output adjacency matrix will be symmetric. Otherwise, output adjacency
        matrix will be asymmetric.
    
    loops: boolean, optional (default=False)
        If False, no edges will be sampled in the diagonal. Otherwise, edges
        are sampled in the diagonal.
    
    Returns
    -------
    G1: ndarray (n_vertices, n_vertices)
        Adjacency matrix the same size as P representing a random graph.

    G2: ndarray (n_vertices, n_vertices)
        Adjacency matrix the same size as P representing a random graph.

    Examples
    --------
    >>> np.random.seed(3)
    >>> n = [3, 3]
    >>> p = [[0.5, 0.1], [0.1, 0.5]]
    >>> r = 0.3

    To sample a correlated SBM graph pair based on n, p and R matrices:

    >>> sbm_corr(n, p, r, directed=False, loops=False)
    (array([[0., 1., 0., 0., 0., 0.],
        [1., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 1.],
        [0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 1., 0., 0.]]), array([[0., 1., 0., 0., 0., 0.],
        [1., 0., 0., 1., 1., 0.],
        [0., 0., 0., 0., 0., 0.],
        [0., 1., 0., 0., 0., 1.],
        [0., 1., 0., 0., 0., 0.],
        [0., 0., 0., 1., 0., 0.]]))
    """
    # test input
    # Check n
    if not isinstance(n, (list, np.ndarray)):
        msg = "n must be a list or np.array, not {}.".format(type(n))
        raise TypeError(msg)
    else:
        n = np.array(n)
        if not np.issubdtype(n.dtype, np.integer):
            msg = "There are non-integer elements in n"
            raise ValueError(msg)

    # Check p
    if not isinstance(p, (list, np.ndarray)):
        msg = "p must be a list or np.array, not {}.".format(type(p))
        raise TypeError(msg)
    else:
        p = np.array(p)
        if not np.issubdtype(p.dtype, np.number):
            msg = "There are non-numeric elements in p"
            raise ValueError(msg)
        elif p.shape != (n.size, n.size):
            msg = "p is must have shape len(n) x len(n), not {}".format(p.shape)
            raise ValueError(msg)
        elif np.any(p < 0) or np.any(p > 1):
            msg = "Values in p must be in between 0 and 1."
            raise ValueError(msg)

    # check r
    if not np.issubdtype(type(r), np.floating):
        raise TypeError("r is not of type float.")
    elif r < 0 or r > 1:
        msg = "r must between 0 and 1."
        raise ValueError(msg)

    # check directed and loops
    if type(directed) is not bool:
        raise TypeError("directed is not of type bool.")
    if type(loops) is not bool:
        raise TypeError("loops is not of type bool.")

    P = np.zeros((np.sum(n), np.sum(n)))
    block_indices = np.insert(np.cumsum(np.array(n)), 0, 0)
    p = np.mat(p)
    for i in range(p.shape[0]):  # for each row
        for j in range(p.shape[1]):  # for each column
            P[
                block_indices[i] : block_indices[i + 1],
                block_indices[j] : block_indices[j + 1],
            ] = p[i, j]
    R = r * np.ones((np.sum(n), np.sum(n)))
    G1, G2 = sample_edges_corr(P, R, directed=False, loops=False)
    return G1, G2
