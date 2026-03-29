from typing import Dict, Protocol


class DataProtocol(Protocol):

    def to_dict(self) -> Dict:
        pass
