class Patterns:
    USERNAME_PATTERN = "^([A-z0-9@_\-\.]{4,20})"
    YOUTUBE_PATTERN = "(https:\/\/)?(www.)?youtube.(com)\/watch\?v=[a-zA-Z0-9\-\_]{11}"
    PASSWORD_PATTERN = (
        "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$"
    )
