from typing import Protocol
from dataclasses import dataclass, field


@dataclass(frozen=True)
class RequiredEdges:
    alive_edges: set[int] = field(default_factory=set)
    failed_edges: set[int] = field(default_factory=set)


class State(Protocol):
    @staticmethod
    def parse_state(current_state: str):
        raise NotImplementedError


@dataclass(frozen=True)
class SkippingRoutingState:
    in_edge: int | None
    current_node: str

    @staticmethod
    def parse_state(current_state: str):
        try:
            state = current_state.split(",")
            return SkippingRoutingState(int(state[0]), state[1])
        except Exception as e:
            raise Exception(f"Error during parsing of current state: {e}")

@dataclass(frozen=True)
class CombinatorialRoutingState:
    pass
