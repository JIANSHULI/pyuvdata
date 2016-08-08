import os
import warnings
import collections
import sys


def setup_package():
    testdir = '../data/test/'
    if not os.path.exists(testdir):
        print('making test directory')
        os.mkdir(testdir)


# Functions that are useful for testing:
def get_iterable(x):
    if isinstance(x, collections.Iterable):
        return x
    else:
        return (x,)


def clearWarnings():
    # Quick code to make warnings reproducible
    for name, mod in list(sys.modules.items()):
        try:
            reg = getattr(mod, "__warningregistry__", None)
        except ImportError:
            continue
        if reg:
            reg.clear()


def checkWarnings(func, func_args=[], func_kwargs={},
                  category=UserWarning,
                  nwarnings=1, message=None, known_warning=None):

    if known_warning == 'miriad':
        # The default warnings for known telescopes when reading miriad files
        category = [UserWarning]
        message = ['Altitude is not present in Miriad file, using known '
                   'location values for PAPER.']
        nwarnings = 1
    elif known_warning == 'paper_uvfits':
        # The default warnings for known telescopes when reading uvfits files
        category = [UserWarning] * 2
        message = ['Required Antenna frame keyword', 'telescope_location is not set']
        nwarnings = 2

    category = get_iterable(category)
    message = get_iterable(message)

    clearWarnings()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")  # All warnings triggered
        output = func(*func_args, **func_kwargs)  # Run function
        # Verify
        status = True
        if len(w) != nwarnings:
            print('wrong number of warnings')
            for idx, wi in enumerate(w):
                print('warning {i} is: {w}'.format(i=idx, w=wi))
            status = False
        else:
            for i, w_i in enumerate(w):
                if w_i.category is not category[i]:
                    status = False
                if message[i] is not None:
                    if message[i] not in str(w_i.message):
                        status = False
    return output, status