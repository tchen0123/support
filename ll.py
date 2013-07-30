"""
Low-Level Logging

A module to allow a ton of data (e.g. all SSL unencrypted and encrypted IO) to
be logged but not actually slow the server down unless the thing is being traced
or the whole server is logging super verbose.

Use like:

import ll

ml = ll.LLogger()

....

ml.la("format string {0} {1}", var0, var1)  # always log

ml.ld("format string 2 {0}", var0)  # log most often
ml.ld("format string 3 {0}", var0)  # log most often
ml.ld2("format string 4 {0}", var0)  # log less often
ml.ld3("format string 5 {0}", var0)  # log only at highest verbosity

For best efficiency, use !r in format string, rather than calling str() or repr() on
arguments.

caustinlane@paypal.com for details.

"""

import inspect
from collections import defaultdict
from datetime import datetime
import time

log_msgs = defaultdict(int)


LOG_LEVELS = {'NONE':   0,
              'DEBUG':  1,
              'DEBUG2': 2,
              'DEBUG3': 3
              }


_log_level = LOG_LEVELS['NONE']


def get_log_level():
    """Set global low lovel log level"""
    return _log_level


def set_log_level(level):
    """Set global low lovel log level"""
    global _log_level
    level = max(level, LOG_LEVELS['NONE'])
    level = min(level, LOG_LEVELS['DEBUG3'])
    _log_level = level


class LLogger(object):
    """Instantiate this to get the logger object; it grabs module data"""

    def __init__(self):
        self.caller_mod = inspect.getmodule(inspect.stack()[1][0]).__file__.split(".")[-2].upper()
        self.la = self.log_always
        self.ld = self.log_debug
        self.ld2 = self.log_debug2
        self.ld3 = self.log_debug3

    def log_always(self, *args, **kw):
        """Unconditionally log"""
        log_msgs[args[0]] += 1
        msg = apply(args[0].format, tuple(args[1:]))
        print "%s %s A:" % (datetime.now().strftime("%d/%H:%M:%S.%f"),
                            self.caller_mod), msg

    def log_debug(self, *args, **kw):
        """Log only with -v"""
        log_msgs[args[0]] += 1
        if _log_level >= 1:
            msg = apply(args[0].format, tuple(args[1:]))
            print "%s %s D:" % (datetime.now().strftime("%d/%H:%M:%S.%f"),
                                self.caller_mod), msg

    def log_debug2(self, *args, **kw):
        """Log only with -vv"""
        log_msgs[args[0]] += 1
        if _log_level >= 2:
            msg = apply(args[0].format, tuple(args[1:]))
            print "%s %s D2:" % (datetime.now().strftime("%d/%H:%M:%S.%f"),
                                 self.caller_mod), msg

    def log_debug3(self, *args, **kw):
        """Log only with -vvv"""
        log_msgs[args[0]] += 1
        if _log_level >= 3:
            msg = apply(args[0].format, tuple(args[1:]))
            print "%s %s D3:" % (datetime.now().strftime("%d/%H:%M:%S.%f"),
                                 self.caller_mod), msg


if __name__ == "__main__":
    ll = LLogger()
    ll.log_debug("{0}", "some stuff")