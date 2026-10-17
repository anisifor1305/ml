from typing import Optional


class TableDataset:
    def __init__(self, features, targets):
        self.features = features
        self.targets = targets
        if len(self.features) != len(self.targets):
            raise ValueError("lens doesn't equal")

    def __len__(self):
        return len(self.targets)

    def __getitem__(self, index: int) -> tuple[list[float], int]:
        return (self.features[index], self.targets[index])

    def __repr__(self):
        return "Число чего то там: " + str(len(self.features))


dataset = TableDataset([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], [0, 1, 0])

print(dataset)
print(len(dataset))
print(dataset[0])

from dataclasses import dataclass


@dataclass
class ExperimentCofnig:
    name: str
    learning_rate: float
    batch_size: int
    epochs: int
    seed: int = 42

    def __post_init__(self):
        if (
            len(self.name) == 0
            or self.learning_rate <= 0
            or self.batch_size <= 0
            or self.epochs <= 0
            or self.seed < 0
        ):
            raise ValueError("Ошибка валидации данных")


config_first = ExperimentCofnig("Artem", 13.0, 21, 43, 11)
config_second = ExperimentCofnig("Artem2", 13.0, 221, 243, 121)
try:
    config_third = ExperimentCofnig("Artem2", -13.0, 221, 243, 121)  # Тут анлак будет
except ValueError as error:
    print(error)


def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags


print(add_tag("alexey"))
print(add_tag("alexey2"))


def add_tag2(tag: str, tags: Optional[list[str]] = None) -> list[str]:
    if tags is None:
        tags = []
    tags.append(tag)
    return tags


print(add_tag2("alexey"))
print(add_tag2("alexey2"))
