"""
Benchmark of the program using different data structures.
"""
import time
import random
import pprint
import sys
from src.DataStructures.Trie import Trie
from src.DataStructures.PrefixHashTree import PrefixHashTree
from src.AutoComplete import AutoComplete


class AttemptingToCompareResultsOfIllegalNumberOfDataStructuresToTest(Exception):
    """
    There is an attempt to compare the results of data structures that is not of count 2.
    """


class ResultsKeysDiffer(Exception):
    """
    The keys do not match from the two dicts being compared.
    """


class ResultsDifferForKey(Exception):
    """
    The results for a key/query do not match.
    """


class Benchmark:
    """
    Class was created to benchmark Autocomplete for Trie and PrefixHashTree.
    """

    def __init__(self, data_structures_to_test, file_to_test, number_of_lines_to_test):
        """
        Defines the vars needed to run the bench marks, namely the data structures that need to be compared. The file
        that should be read and inserted into the data structures and the prefixes that should be queried.

        :param data_structures_to_test:
        :param file_to_test:
        :return:
        """
        self.prefixes = []
        self.lines = []

        self.data_structures_to_test = data_structures_to_test
        self.__read_file_generate_lines(file_to_test, number_of_lines_to_test)

    def benchmark(self, number_of_times, number_of_prefixes_to_benchmark=1000):
        """
        Runs all the benchmarks in this class. Returns a dict with all the results.
        :return:
        """
        self.__generate_prefixes_to_test(number_of_prefixes_to_benchmark)

        returned_autocompletes = []
        returned_results = []

        timed_runs = {}

        for ds in self.data_structures_to_test:
            print("benchmarking data structures: " + ds[0])
            start_time = time.perf_counter()
            returned_autocompletes.append(
                self.__run_benchmark_multiple_times(
                    Benchmark.__insertions_from_file,
                    number_of_times,
                    ds[1]
                )
            )

            end_time = time.perf_counter()
            timed_runs[ds[0]] = {}
            timed_runs[ds[0]]["insertions"] = {
                "runs": number_of_times,
                "total_time": end_time - start_time,
                "time_per_run": (end_time - start_time) / number_of_times
            }

            start_time = time.perf_counter()
            returned_results.append(
                self.__run_benchmark_multiple_times(
                    Benchmark.__queries,
                    number_of_times,
                    returned_autocompletes[-1]
                )
            )
            end_time = time.perf_counter()
            timed_runs[ds[0]]["queries"] = {
                "runs": number_of_times,
                "total_time": end_time - start_time,
                "time_per_run": (end_time - start_time) / number_of_times
            }

        if len(self.data_structures_to_test) == 2:
            self.compare_query_results(returned_results)

        return timed_runs

    def __read_file_generate_lines(self, file_to_test, number_of_lines_to_test):
        """
        Read the file, get all the lines to add to the autocomplete and generate the prefixes to test.

        :param file_to_test:
        :return:
        """
        f = open(file_to_test, 'r')
        self.lines = f.readlines()
        self.lines = random.sample(self.lines, number_of_lines_to_test)

    def __generate_prefixes_to_test(self, number_to_generate):
        """
        Generates the prefixes to test specified by number_to_generate.

        :param number_to_generate:
        :return:
        """
        self.prefixes = []

        for _ in range(number_to_generate):
            line = self.lines[random.randint(0, len(self.lines) - 1)]
            prefix = line[0: max(1, random.randint(0, len(line) - 1))]
            self.prefixes.append(prefix.lower())

    def __run_benchmark_multiple_times(self, benchmark_to_run, times_to_run, *args):
        """
        Runs the benchmark, times_to_run is the number of times the benchmark is run with the args passed in. Returns
        the results of the last run of the benchmark and the time it took to run the tests

        :param times_to_run:
        :param data_structure:
        :return:
        """

        # So the results can be saved
        results = None
        for i in range(times_to_run):
            sys.stdout.write(
                '\r' + "running iteration {0} of {1}, of {2}".format(i + 1, times_to_run, benchmark_to_run))
            results = benchmark_to_run(self, args[0])

        print("\nfinished benchmarking: {0}".format(benchmark_to_run))
        return results

    def __insertions_from_file(self, data_structure):
        """
        Inserts all the phrases into autocomplete from the file and returns the data structure.

        :param data_structure:
        :return:
        """
        autocomplete = AutoComplete(data_structure)
        autocomplete.insert(self.lines)
        return autocomplete

    def __queries(self, autocomplete):
        """
        Queries the autocomplete for the prefixes and returns all the values returns in a dict.

        :param autocomplete:
        :return:
        """
        results = {}

        for prefix in self.prefixes:
            results[prefix] = autocomplete.query(prefix)

        return results

    def compare_query_results(self, results):
        """
        Compares the query results returned by __benchmark_query if the number of data_structures_to_test == 2. Expects
        an array with two dicts.

        :param results:
        :return:
        """
        if len(results) != 2:
            raise AttemptingToCompareResultsOfIllegalNumberOfDataStructuresToTest('data_structures_to_test '
                                                                                  'does not have two structures '
                                                                                  'to test')

        # Just convert the keys to to sets, makes them easier to compares
        key_sets = [set(results[0].keys()), set(results[1].keys())]

        # If the keys differ, then the same queries were not run on both the result, return an error
        if len(key_sets[0]) != len(key_sets[1]) or len(key_sets[0]) != len(key_sets[0].intersection(key_sets[1])):
            raise ResultsKeysDiffer("Benchmark::compare_query_results: The keys of the passed in results passed in "
                                    "differ")

        # Iterate through the keys, if the results differ, then throw and error cause one of the structures is not
        # returning the expected data
        for key in key_sets[0]:
            # Conversion to sets makes the comparison easier
            result_sets = [set(results[0][key]), set(results[1][key])]

            if len(result_sets[0]) != len(result_sets[0].intersection(result_sets[1])):
                raise ResultsDifferForKey("Benchmark::compare_query_results: results do not match for key: " + key)

        # No error were thrown, so every ran fine
        print("compare_query_results...success")


if __name__ == "__main__":
    # Compare the two data structures
    benchmark = Benchmark([("Trie", Trie), ("PrefixHashTree", PrefixHashTree)], "rand_words.txt", 10000)
    # benchmark = Benchmark([("PrefixHashTree", PrefixHashTree)], "rand_words.txt")
    times = benchmark.benchmark(1000)

    pprint.pprint(times)
    print("Category: Trie vs. PrefixHashTree")

    print("Total Insertion Time: {0} vs. {1}".format(
        times["Trie"]["insertions"]["total_time"],
        times["PrefixHashTree"]["insertions"]["total_time"]))

    print("Total Query Time: {0} vs. {1}".format(
        times["Trie"]["queries"]["total_time"],
        times["PrefixHashTree"]["queries"]["total_time"]))

    print("Insertion Time Per Run: {0} vs. {1}".format(
        times["Trie"]["insertions"]["time_per_run"],
        times["PrefixHashTree"]["insertions"]["time_per_run"]))

    print("Query Time Per Run: {0} vs. {1}".format(
        times["Trie"]["queries"]["time_per_run"],
        times["PrefixHashTree"]["queries"]["time_per_run"]))
