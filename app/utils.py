import os


def shorten_path(path, levels=3):
    """
    Shortens a file path to only display the last few directories.
    
    Args:
        path (str): The full path to shorten.
        levels (int): The number of directory levels to display.
    
    Returns:
        str: The shortened path.
    """
    path_parts = path.split(os.sep)
    if len(path_parts) > levels:
        return os.sep.join(path_parts[-levels:])
    return path
