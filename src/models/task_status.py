from enum import IntEnum


class TaskStatus(IntEnum):
    Backlog = 1
    Todo = 2
    InProgress = 3
    Done = 4
    Closed = 5
