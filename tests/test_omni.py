import numpy as np
import pytest
from numpy import allclose, array_equal
from numpy.linalg import norm
from numpy.testing import assert_allclose

from graspy.embed.omni import OmnibusEmbed, _get_omni_matrix
from graspy.simulations.simulations import er_nm, er_np
from graspy.utils.utils import is_symmetric, symmetrize


def generate_data(n, seed=1):
    """Generate data form dirichelet distribution with 
    n numbers of points
    """
    np.random.seed(seed)

    parameters = [1, 1, 1]

    # Generate latent positions
    X = np.random.dirichlet(parameters, size=n)

    # Generate probability matrix
    P = np.dot(X, X.T)

    # Generate two adjacencies
    A1 = symmetrize(np.random.binomial(1, P))
    A2 = symmetrize(np.random.binomial(1, P))

    return (X, A1, A2)


# Below tests omni matrix generation code
def test_omni_matrix_ones_zeros():
    # Should get all ones
    n_graphs = [2, 5, 10]  # Test for different number of graphs

    for n in n_graphs:
        ones = [np.ones((10, 10)) for _ in range(n)]
        expected_output = np.ones((10 * n, 10 * n))
        output = _get_omni_matrix(ones)
        assert array_equal(output, expected_output)

        zeros = [np.zeros((10, 10)) for _ in range(n)]
        expected_output = np.zeros((10 * n, 10 * n))
        output = _get_omni_matrix(zeros)
        assert array_equal(output, expected_output)


def test_omni_matrix_random():
    expected_output = np.array(
        [
            [0.0, 1.0, 1.0, 0.0, 0.5, 0.5],
            [1.0, 0.0, 1.0, 0.5, 0.0, 1.0],
            [1.0, 1.0, 0.0, 0.5, 1.0, 0.0],
            [0.0, 0.5, 0.5, 0.0, 0.0, 0.0],
            [0.5, 0.0, 1.0, 0.0, 0.0, 1.0],
            [0.5, 1.0, 0.0, 0.0, 1.0, 0.0],
        ]
    )

    np.random.seed(4)
    dat_list = (
        [[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]],
        [[0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]],
    )
    graphs = np.array(dat_list)
    A = _get_omni_matrix(graphs)
    assert_allclose(A, expected_output)


def test_invalid_inputs():
    with pytest.raises(TypeError):
        wrong_diag_aug = "True"
        omni = OmnibusEmbed(diag_aug=wrong_diag_aug)

    with pytest.raises(ValueError):
        empty_list = []
        omni = OmnibusEmbed(n_components=2)
        omni.fit(empty_list)

    with pytest.raises(ValueError):
        wrong_shapes = [np.ones((10, 10)), np.ones((20, 20))]
        omni = OmnibusEmbed(n_components=2)
        omni.fit(wrong_shapes)

    with pytest.raises(TypeError):
        wrong_dtypes = [1, 2, 3]
        omni = OmnibusEmbed(n_components=2)
        omni.fit(wrong_dtypes)


def test_omni_matrix_symmetric():
    np.random.seed(3)
    n = 15
    p = 0.4

    n_graphs = [2, 5, 10]
    for n in n_graphs:
        graphs = [er_np(n, p) for _ in range(n)]
        output = _get_omni_matrix(graphs)
        assert is_symmetric(output)


def test_omni_unconnected():
    np.random.seed(4)
    n = 100
    m = 50

    graphs = [er_nm(n, m) for _ in range(2)]
    omni = OmnibusEmbed()

    with pytest.warns(UserWarning):
        omni.fit(graphs)


def test_omni_embed():
    """
    We compare the difference of norms of OmniBar and ABar.
    ABar is the lowest variance estimate of the latent positions X.
    OmniBar should be reasonablly close to ABar when n_vertices is high. 
    """

    def compute_bar(arr):
        n = arr.shape[0] // 2
        return (arr[:n] + arr[n:]) / 2

    def run(diag_aug):
        X, A1, A2 = generate_data(1000, seed=2)
        Abar = (A1 + A2) / 2

        omni = OmnibusEmbed(n_components=3, diag_aug=diag_aug)
        OmniBar = compute_bar(omni.fit_transform([A1, A2]))

        omni = OmnibusEmbed(n_components=3, diag_aug=diag_aug)
        ABar = compute_bar(omni.fit_transform([Abar, Abar]))

        tol = 1.0e-2
        assert allclose(norm(OmniBar, axis=1), norm(ABar, axis=1), rtol=tol, atol=tol)

    run(diag_aug=True)
    run(diag_aug=False)
