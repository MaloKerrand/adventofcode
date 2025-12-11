from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class DataType(Enum):
    NO_FFT_OR_DAC = "no_fft_or_dac"
    ONLY_FFT = "only_fft"
    ONLY_DAC = "only_dac"
    BOTH_FFT_AND_DAC = "both_fft_and_dac"


@dataclass(frozen=True)
class Data:
    data_type: DataType
    point: str


def main() -> None:
    current_file: Path = Path(__file__)
    content: str = (current_file.parent / "input").read_text(encoding="utf-8")
    point_to_neighbors: dict[str, list[str]] = {}
    for line in content.splitlines():
        vertex, neighbors = line.split(sep=":")
        point_to_neighbors[vertex] = neighbors.strip().split(sep=" ")

    point_to_data_type_to_nb_point: dict[str, dict[DataType, int]] = defaultdict(lambda: defaultdict(int))
    data_to_visit: list[Data] = [Data(data_type=DataType.NO_FFT_OR_DAC, point="svr")]
    while data_to_visit:
        data = data_to_visit.pop()
        for neighbor in point_to_neighbors.get(data.point, []):
            current_type = data.data_type
            match neighbor, current_type:
                case "fft", DataType.ONLY_FFT:
                    raise ValueError("Data is looping")
                case "dac", DataType.ONLY_DAC:
                    raise ValueError("Data is looping")
                case "fft", DataType.NO_FFT_OR_DAC:
                    current_type = DataType.ONLY_FFT
                case "dac", DataType.NO_FFT_OR_DAC:
                    current_type = DataType.ONLY_DAC
                case "fft", DataType.ONLY_DAC:
                    current_type = DataType.BOTH_FFT_AND_DAC
                case "dac", DataType.ONLY_FFT:
                    current_type = DataType.BOTH_FFT_AND_DAC
            point_to_data_type_to_nb_point[neighbor][current_type] += 1
            data_to_visit.append(Data(data_type=current_type, point=neighbor))
    print(point_to_data_type_to_nb_point["out"][DataType.BOTH_FFT_AND_DAC])


if __name__ == "__main__":
    # import timeit

    # print(timeit.timeit("main()", number=1000, globals=locals()))
    main()
