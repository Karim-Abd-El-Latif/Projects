import diarex
import sys

def test_get_argument():
    # name of the first argument of sys.argv does not matter as it is not checked
    # the argument is not checked for validity yet, so it can be anything
    sys.argv = ['test']
    assert diarex.get_argument() == None
    sys.argv = ['test','3']
    assert diarex.get_argument() == '3'
    sys.argv = ['test', '!7oe']
    assert diarex.get_argument() == '!7oe'
    # no test case for 3+ argvs as I could not manage to make sys.exit() work with pytest

def test_get_mode():
    assert diarex.get_mode(None) == 'gui'
    assert diarex.get_mode('-g') == 'gui'
    assert diarex.get_mode('-t') == 'text'
    # no test case for sys.exit for same reason as above!

