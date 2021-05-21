class PermissionsDenied(Exception):
    """
    Raise if `request.user` is not `model.author` but should be.
    """