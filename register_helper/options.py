class HelperStatusOptions:
    """
    Status options available to Helper
    """
    ACTIVE = 1
    BLOCKED = 2
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (BLOCKED, 'Blocked'),
    )


class LoginStatus:
    """
        Login Status options of Helper
    """
    LOGGED_IN = 1
    LOGGED_OUT = 2
    PENDING = 3
    STATUS_CHOICES = (
        (LOGGED_IN, 'LOGGED_IN'),
        (LOGGED_OUT, 'LOGGED_OUT'),
        (PENDING, 'PENDING'),
    )
