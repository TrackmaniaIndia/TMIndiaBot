from __future__ import annotations

from typing import TYPE_CHECKING, Hashable

if TYPE_CHECKING:
    pass


class LockedResourceError(RuntimeError):
    """
    Exception raised when an operation is attempted on a locked resource.
    Attributes:
        `type` -- name of the locked resource's type
        `id` -- ID of the locked resource
    """

    def __init__(self, resource_type: str, resource_id: Hashable):
        self.type = resource_type
        self.id = resource_id

        super().__init__(
            f"Cannot operate on {self.type.lower()} `{self.id}`; "
            "it is currently locked and in use by another operation."
        )
