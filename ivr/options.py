class Session:
    """
    Session option for call
    """
    WELCOME = 0
    DISPLAY_OPTION = 1
    GET_OPTION = 2
    SESSION_CHOICES = (
        (WELCOME, 'welcome'),
        (DISPLAY_OPTION, 'display_option'),
        (GET_OPTION, 'get_option'),
    )
