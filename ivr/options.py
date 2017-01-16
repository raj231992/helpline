class Session:
    """
    Session option for call
    """
    WELCOME = 0
    DISPLAY_LANGUAGE = 1
    GET_LANGUAGE = 2
    DISPLAY_OPTION = 3
    GET_OPTION = 4
    DISPLAY_TERMS = 5
    GET_TERMS = 6
    CALL_EXIT = 7
    CALL_FORWARD = 8
    SESSION_CHOICES = (
        (WELCOME, 'welcome'),
        (DISPLAY_LANGUAGE, 'display_language'),
        (GET_LANGUAGE, 'get_language'),
        (DISPLAY_OPTION, 'display_option'),
        (GET_OPTION, 'get_option'),
        (DISPLAY_TERMS, 'display_terms'),
        (GET_TERMS, 'get_terms'),
        (CALL_EXIT,'call_exit'),
        (CALL_FORWARD,'call_forward'),
    )


