import heapq
import re
import sys
from typing import *

T = TypeVar("T")


EntersEvent: TypeAlias = tuple[Literal["ENTERS"], str, float, int]
LeavesEvent: TypeAlias = tuple[Literal["LEAVES"], int]
Event: TypeAlias = Union[EntersEvent, LeavesEvent]


def tokenGenerator(input_buffer: TextIO) -> Generator[str, None, None]:
    for line in input_buffer:
        line = line.strip()
        if not line:
            return
        yield from line.split()


def listenEvents(input_buffer: TextIO) -> Iterable[Event]:
    """
    Given an open file buffer, yield the events on the log, which satisfy the
    following structure:

    ```
    <EVENT> <data1> <data2> ...
    ```

    The possible events are:
    - `ENTERS <name> <priority> <queue_number>`
    - `LEAVES <queue_number>`

    For instance,

    ```
    ENTERS Melissa 42 3
    LEAVES 4
    ```

    Yields
    ------
    The parsed events in the form of tuples, the first element of which is the
    event type, and the rest of which is its data.
    """
    tokens = tokenGenerator(input_buffer)
    for event_type in tokens:  # Read a single element of the text
        if event_type == "ENTERS":
            yield (event_type, next(tokens), float(next(tokens)), int(next(tokens)))
        elif event_type == "LEAVES":
            yield (event_type, int(next(tokens)))


def readHeader(input_buffer: TextIO) -> list[list[str]]:
    """
    Read the initial configuration of the queues. It must follow the structure
    ```
    <num_queues>
    Q1Person1 Q1Person1Priority Q1Person2 Q1Person2Priority ...
    Q2Person1 Q2Person1Priority Q2Person2 Q2Person2Priority ...
    ...
    QNPerson1 ...
    ```

    Returns
    -------
    initial_configuration : list[PriorityQueue[str]]
        The initial configuration of the queues.
    """
    num_queues = int(input_buffer.readline().strip())
    if num_queues is None:
        raise ValueError(f"Could not read num_queues: {num_queues}")
    initial_configuration: list[list[str]] = []
    for _ in range(num_queues):
        line = input_buffer.readline()
        line = line.strip()
        line = re.sub(" +", " ", line)  # This will remove duplicate whitespaces from the line
        if line == "":
            queue_configuration = []
        else:
            queue_configuration = line.split()  # And split the line into tokens
        queue_configuration = list(map(lambda t: (-float(t[1]), t[0]), batched(queue_configuration, 2)))
        # "minus" because we want a max-queue, instead of min-queue
        heapq.heapify(queue_configuration)  # Initialize the queues
        initial_configuration.append(queue_configuration)

    # Before continuing, there's an empty line that we need to skip
    input_buffer.readline()

    return initial_configuration


def batched(iterable: Iterable[T], n: int) -> Generator[Tuple[T, ...], None, None]:
    iterable = iter(iterable)

    if n < 1:
        raise ValueError("N cannot be lower than 1")
    for first in iterable:
        yield tuple([first, *(next(iterable) for _ in range(n - 1))])


class QueueManager:
    def __init__(self, initial_configuration: list[list[str]]):
        self.queues = initial_configuration

    def enqueue(self, name: str, priority: int, queue_number: int) -> None:
        if self._checkQueueNumber(queue_number):
            heapq.heappush(self.queues[queue_number - 1], (-priority, name))  # "minus" because is a max-queue

    def dequeue(self, queue_number: int) -> str:
        if self._checkQueueNumber(queue_number) and len(self.queues[queue_number - 1]) > 0:
            return heapq.heappop(self.queues[queue_number - 1])[1]

    def _checkQueueNumber(self, queue_number: int):
        return 0 < queue_number <= len(self.queues)

    def getContents(self) -> list[list[str]]:
        return list(list(heapq.heappop(q)[1] for _ in range(len(q))) for q in self.queues)


if __name__ == "__main__":
    # input_file = pathlib.Path(__file__).parent / "demo_input.txt"
    # io = input_file.open()
    io = sys.stdin
    queues = readHeader(io)
    manager = QueueManager(queues)
    print("DEPARTS")
    print("-------")
    for event in listenEvents(io):
        if event[0] == "ENTERS":
            manager.enqueue(*event[1:])
        elif event[0] == "LEAVES":
            person = manager.dequeue(*event[1:])
            if person is not None:
                print(person)
        else:
            raise ValueError(f"Unknown event type {event[0]}")

    print("")
    print("FINAL CONTENTS")
    print("--------------")
    for j, queue_content in enumerate(manager.getContents(), start=1):
        if len(queue_content) == 0:
            print(f"queue {j}:")
        else:
            print(f"queue {j}:", " ".join(queue_content))
