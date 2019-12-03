import pytest
import numpy as np
import math
from graspy.match import FastApproximateQAP as FAQ


class TestMatch:
    @classmethod
    def setup_class(cls):
        cls.barycenter = FAQ()
        cls.rand = FAQ(n_init=100, init_method="rand")

    def test_FAQ_inputs(self):
        with pytest.raises(TypeError):
            FAQ(n_init=-1.5)
        with pytest.raises(ValueError):
            FAQ(init_method="random")
        with pytest.raises(TypeError):
            FAQ(max_iter=-1.5)
        with pytest.raises(TypeError):
            FAQ(shuffle_input="hey")
        with pytest.raises(TypeError):
            FAQ(eps=-1)

    def __get_AB(self, qap_prob):
        with open("tests/match/qapdata/" + qap_prob + ".dat") as f:
            f = [int(elem) for elem in f.read().split()]

            # adjusting
        f = np.array(f[1:])
        n = int(math.sqrt(len(f) / 2))
        f = f.reshape(2 * n, n)
        A = f[:n, :]
        B = f[n:, :]
        return A, B

    def test_barycenter(self):
        A, B = self.__get_AB("lipa20a")
        lipa20a = self.barycenter.fit(A, B)
        score = lipa20a.score_
        assert 3683 <= score < 3900

        A, B = self.__get_AB("lipa20b")
        lipa20b = self.barycenter.fit(A, B)
        score = lipa20b.score_
        assert score == 27076

        A, B = self.__get_AB("lipa30a")
        lipa30a = self.barycenter.fit(A, B)
        score = lipa30a.score_
        assert 13178 <= score < 13650

        A, B = self.__get_AB("lipa30b")
        lipa30b = self.barycenter.fit(A, B)
        score = lipa30b.score_
        assert score == 151426

        A, B = self.__get_AB("lipa40a")
        lipa40a = self.barycenter.fit(A, B)
        score = lipa40a.score_
        assert 31538 <= score < 32300

        A, B = self.__get_AB("lipa40b")
        lipa40b = self.barycenter.fit(A, B)
        score = lipa40b.score_
        assert score == 476581

        A, B = self.__get_AB("lipa50a")
        lipa50a = self.barycenter.fit(A, B)
        score = lipa50a.score_
        assert 62093 <= score < 63300

        A, B = self.__get_AB("lipa50b")
        lipa50b = self.barycenter.fit(A, B)
        score = lipa50b.score_
        assert score == 1210244

    def test_rand(self):
        A, B = self.__get_AB("chr12c")
        chr12c = self.rand.fit(A, B)
        score = chr12c.score_
        assert 11156 <= score < 13500

        A, B = self.__get_AB("chr15a")
        chr15a = self.rand.fit(A, B)
        score = chr15a.score_
        assert 9896 <= score < 11500
