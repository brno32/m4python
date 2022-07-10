from logging import getLogger

logger = getLogger(__name__)


class VirtualP4:
    """
    A global, in-memory store for all written data when using tests decorated with @mock_p4
    """

    pass


virtual_p4 = VirtualP4()
