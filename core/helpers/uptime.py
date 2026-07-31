from django.utils import timezone

_start_time = None


def set_start_time():
    global _start_time
    _start_time = timezone.localtime()


def get_uptime():
    if _start_time is None:
        return 0.0
    return (timezone.localtime() - _start_time).total_seconds()
