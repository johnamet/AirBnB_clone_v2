#!/usr/bin/python3
from datetime import datetime
from fabric.api import local


def do_pack():
    """Generates a .tgz archive of the web_static directory.

  Returns:
      str: The path to the generated archive or None on failure.
  """
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_name = f"web_static_{timestamp}.tgz"
    archive_path = f"versions/{archive_name}"

    # Create versions directory if it doesn't exist
    local("mkdir -p versions")

    # Create archive using tar
    try:
        local(f"tar -czf {archive_path} web_static")
        return archive_path
    except Exception:
        print("Error creating archive. Please check permissions.")
        return None

# Example usage (uncomment to run locally)
# archive_path = do_pack()
# if archive_path:
#   print(f"Archive created successfully: {archive_path}")
