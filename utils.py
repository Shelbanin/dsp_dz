# coding: utf-8

from __future__ import unicode_literals

from datetime import datetime


def log_execution_time(debug_mode):

    def outer_decor(func):
        def wrapper(*args, **kwargs):

            start_time = datetime.now()
            result = func(*args, **kwargs)
            delta = datetime.now() - start_time

            print('Total time: {}'.format(delta.total_seconds()))

            return result

        return wrapper if debug_mode else func

    return outer_decor
