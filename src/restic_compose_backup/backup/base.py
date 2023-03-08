

class BackupBase:
    """
    Base class for specific backup types such as various databases.

    A backup type is responsible for processing all actions defined
    on a service. This includes pre-run and post-run actions.

    All backup objects are instantiated before all the backup
    execution begins to sanity check the configuration and
    report the current parsed configuration to the user.
    """
    def __init__(self, *args, **kwargs):
        # Possibly pass in the service object here?
        # Grab labels from service.
        pass

    def pre_run(self):
        """
        Pre-run raw command.
        Pre-run execution in a container.
        """
        pass

    def run(self):
        """
        Run the backup
        """
        raise NotImplementedError

    def post_run(self):
        """
        Post-run raw command.
        Post-run execution in a container.
        """
        pass
