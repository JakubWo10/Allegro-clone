from typing import Protocol, Dict


class DataProtocol(Protocol):

    def to_dict(self) -> Dict:
        pass
