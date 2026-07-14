import time


class PerformanceLogger:

    def __init__(self):

        self.timings = {}

    def start(self, stage):

        self.timings[stage] = {
            "start": time.perf_counter()
        }

    def stop(self, stage):

        if stage not in self.timings:
            return

        end = time.perf_counter()

        self.timings[stage]["time"] = (
            end - self.timings[stage]["start"]
        ) * 1000

    def print_summary(self):

        print("\n")
        print("=" * 70)
        print("PERFORMANCE REPORT")
        print("=" * 70)

        total = 0

        for stage, value in self.timings.items():

            t = value["time"]

            total += t

            print(f"{stage:<30}{t:.2f} ms")

        print("-" * 70)

        print(f"{'TOTAL':<30}{total:.2f} ms")

        print("=" * 70)
        print("\n")