import re
import sys
from collections import deque
from typing import Iterable, Literal, TextIO, TypeAlias, Union

import yogi

EntersEvent: TypeAlias = tuple[Literal["ENTERS"], str, int]
LeavesEvent: TypeAlias = tuple[Literal["LEAVES"], int]
Event: TypeAlias = Union[EntersEvent, LeavesEvent]


def tokenGenerator(input_buffer: TextIO) -> Iterable[str]:
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

    For instance,

    ```
    ENTERS Melissa 3
    LEAVES 4
    ```

    Yields
    ------
    The parsed events in the form of tuples, the first element of which is the
    event type, and the rest of which is its data.
    """
    generator = tokenGenerator(input_buffer)
    for event_type in generator:  # Read a single element of the text
        if event_type == "ENTERS":
            yield (event_type, next(generator), int(next(generator)))
        elif event_type == "LEAVES":
            yield (event_type, int(next(generator)))


def readHeader(input_buffer: TextIO) -> list[deque[str]]:
    """
    Read the initial configuration of the queues. It must follow the structure
    ```
    <num_queues>
    Q1Person1 Q1Person2 ...
    Q2Person1 Q2Person2 ...
    ...
    QNPerson1 ...
    ```

    Returns
    -------
    initial_configuration : list[deque[str]]
        The initial configuration of the queues.
    """
    num_queues = yogi.Yogi(input_buffer).scan(int)
    if num_queues is None:
        raise ValueError(f"Could not read num_queues: {num_queues}")
    initial_configuration: list[deque[str]] = []
    for _ in range(num_queues):
        line = input_buffer.readline()
        line = line.strip(" \n\r")
        line = re.sub(" +", " ", line)  # This will remove duplicate whitespaces from the line
        if line == "":
            queue_configuration = []
        else:
            queue_configuration = line.split(" ")  # And split the line into tokens
        initial_configuration.append(deque(queue_configuration))

    return initial_configuration


class QueueManager:
    def __init__(self, initial_configuration: list[deque[str]]):
        self.queues = initial_configuration

    def enqueue(self, name: str, queue_number: int) -> None:
        if self._checkQueueNumber(queue_number):
            self.queues[queue_number - 1].append(name)

    def dequeue(self, queue_number: int) -> str:
        if self._checkQueueNumber(queue_number) and len(self.queues[queue_number - 1]) > 0:
            return self.queues[queue_number - 1].popleft()

    def _checkQueueNumber(self, queue_number: int):
        return 0 < queue_number <= len(self.queues)

    def getContents(self) -> list[list[str]]:
        return list(list(q) for q in self.queues)


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
        print(f"queue {j}: {' '.join(queue_content)}")
