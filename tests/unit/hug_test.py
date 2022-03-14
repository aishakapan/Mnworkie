from flaskie_app.mnworkie_todo import verify
import pytest

class TestHugFunctions():

    def test_verify(self):
        result_1 = verify('aisha', 'morkovka.13')
        assert result_1 == (1,)
        result_2 = verify('kapanik', 'sha256$e1x3tFxCnvdHePkf$4309197ba2fd85800c8d56c2eb3ee3714fbf5884dbd7bcf7c719f633e2ef0986')
        assert result_2 == (2,)
        result_3 = verify('mnworkie', 'sha256$FIEsUAaRr1WvISrF$39c7c62888d3360f3aff1f5947cee6e9d68362b5743fa6788e2f0264e2960573')
        assert result_3 == (4,)
        result_4 = verify('mnuck', 'abc13')
        assert result_4 == False










