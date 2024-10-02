from _utils import get_samples, plot_live_ecg
import numpy as np

PLOT_WIDTH_NS = int(4e9)


class LiveECGPlotter:

    samples: list[tuple[int, int]]

    def __init__(self, buffer: list[tuple[int, int]]):
        """
        :param buffer: Buffer of ECG samples (nanosecond timestamp, sample value)
                       The buffer is sorted by timestamp.
                       Note that the timestamps do not start at 0!
        """
        self.buffer = np.array(buffer)

    def display_slice(self, timestamp: int) -> list[tuple[int, int]]:
        """
        Prepare ecg samples from a buffer for display in a chart.
        The provided slice should function according to the provided demo video,
        specifically the overlapping behaviour.

        This function should be performant enough to be called 40 times per second.

        :param timestamp: Timestamp (ns) to display ecg for.
                          Only samples between [timestamp - PLOT_WIDTH_NS, timestamp] should be selected.
        :return: list of x, y tuples, where the x coordinates are in the range [0, PLOT_WIDTH_NS].
                 Note that points outside of this range will not be displayed.
        """

        start_time = timestamp - PLOT_WIDTH_NS
        # print(self.buffer)
        time_column = self.buffer[:, 0]
        isDisplayable = (time_column >= start_time) & (time_column <= timestamp)
        samples = self.buffer[isDisplayable]
        samples[:, 0] = samples[:, 0] - start_time
        print(samples)
        # for time, value in self.buffer:
        #   if start_time <= time <= timestamp:
        #     samples.append((time, value))
        # # print(samples)
        # showable_samples = []
        # for time, value in samples:
        #   showable_samples.append((time - start_time, value))
        # print(showable_samples)

        # result = []
        # for time, value in showable_samples:
        #   result.append(())

        return samples.tolist()

if __name__ == '__main__':
    samples = get_samples()
    ecg = LiveECGPlotter(samples)
    plot_live_ecg(ecg, samples, PLOT_WIDTH_NS)
