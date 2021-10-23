# -*- encoding: utf-8 -*-
"""Módulo common.logging

Contém a classe de log.

Autor: Rogers Reiche de Mendonça <rogers.rj@gmail.com>
Data: Outubro/2021
"""
from datetime import datetime


def now(fmt_time: str = '%d/%m/%Y %H:%M:%S'):
    return datetime.now().strftime(fmt_time)


def log(message: str, end: str = '\n', log_file: str = None, with_timestamp: bool = True):
    log_message = f"[{now()}] {message}" if with_timestamp else message
    print(log_message, end)

    if bool(log_file and log_file.strip()):
        try:
            with open(log_file, 'a') as f:
                f.write(log_message + end)
        except Exception as ex:
            log_error = f"{log_file}.{now('%Y.%m.%d.%H.%M.%S.%f')}.err"
            with open(log_error, 'a') as f_err:
                f_err.write(ex.__str__() + end)
                f_err.write(log_message + end)
