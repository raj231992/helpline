class Session:
    """
    Session option for call
    """
    WELCOME = 0
    DISPLAY_LANGUAGE = 1
    GET_LANGUAGE = 2
    DISPLAY_OPTION = 3
    GET_OPTION = 4
    CALL_EXIT = 5
    CALL_FORWARD = 6
    SESSION_CHOICES = (
        (WELCOME, 'welcome'),
        (DISPLAY_LANGUAGE, 'display_language'),
        (GET_LANGUAGE, 'get_language'),
        (DISPLAY_OPTION, 'display_option'),
        (GET_OPTION, 'get_option'),
        (CALL_EXIT,'call_exit'),
        (CALL_FORWARD,'call_forward'),
    )


