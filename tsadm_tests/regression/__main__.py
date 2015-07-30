
import sys
from . import RegressionTestManager

if __name__ == '__main__':
    rtman= RegressionTestManager(sys.argv)
    rtman.bootstrap()
    if not rtman.load_tests():
        print(rtman.err_msg, file=sys.stderr)
        sys.exit(1)
    rtman.run_all()
    rtman.end()
    if rtman.failed():
        sys.exit(2)
    else:
        sys.exit(0)
