class PermissionsDenied(Exception):
    """
    Raise if `request.user` is not `model.author` but should be.
    """

class ThreadClosed(Exception):
    """
    Raise if attempt to add `forum.Post` to `forum.Thread` model.
    """