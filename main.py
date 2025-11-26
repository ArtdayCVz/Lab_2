import math
import unittest


class Statistics:
    """!
    @brief A class for performing descriptive statistics on numerical datasets.

    @details This class provides methods to compute measures of central tendency
    (mean, median, mode) and measures of statistical variability
    (variance, standard deviation). It validates the input data before applying
    mathematical operations.

    @par Example usage:
    @code
        stats = Statistics([1, 2, 3])
        print(stats.mean())
    @endcode
    """

    def __init__(self, data):
        """!
        @brief Constructor for the Statistics class.

        @param data A list of integer or floating-point numbers.
        @return None
        @throws TypeError If data is not a list or contains invalid elements.
        @throws ValueError If the list is empty.

        @note Validation is automatically performed via the private method `_validate_data()`.
        """
        self.data = self._validate_data(data)

    def _validate_data(self, data):
        """!
        @brief Validates the raw input data.

        @details This method ensures the provided dataset is suitable for all statistical
        operations performed by the class. It checks for correct type, non-emptiness,
        and ensures that all elements are numeric.

        @param data The input dataset to validate.
        @return A validated list of numbers.
        @throws TypeError If data is not a list or contains non-numeric elements.
        @throws ValueError If data is an empty list.
        """
        if not isinstance(data, list):
            raise TypeError("Data must be a list.")
        if len(data) == 0:
            raise ValueError("Data list cannot be empty.")
        for x in data:
            if not isinstance(x, (int, float)):
                raise TypeError(f"Invalid element type: {x}")
        return data

    def mean(self):
        """!
        @brief Computes the arithmetic mean.

        @details The mean is determined by summing all values and dividing the
        result by the number of elements in the dataset.

        @return The arithmetic mean (float).
        
        @par Example:
        @code
            stats = Statistics([1, 2, 3])
            result = stats.mean() 
            # result is 2.0
        @endcode
        """
        return sum(self.data) / len(self.data)

    def median(self):
        """!
        @brief Computes the median of the dataset.

        @details If the number of elements is odd, the middle number is returned.
        If the number is even, the median is the average of the two central numbers.

        @return The median value.
        
        @par Example:
        @code
            # Odd number of elements
            Statistics([1, 3, 5]).median() 
            # Returns 3

            # Even number of elements
            Statistics([1, 3, 5, 7]).median() 
            # Returns 4.0
        @endcode
        """
        sorted_data = sorted(self.data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2
        else:
            return sorted_data[mid]

    def mode(self):
        """!
        @brief Computes the statistical mode.

        @details The mode is the most frequently occurring value in the dataset.
        - If a single value is most frequent, that value is returned.
        - If multiple values share the same highest frequency, a list is returned.
        - If all values appear only once, the method returns None.

        @return int | float | list | None The mode or list of modes.
        
        @par Example:
        @code
            # Single mode
            Statistics([1, 2, 2, 3]).mode() # Returns 2
            
            # Multiple modes
            Statistics([1, 1, 2, 2]).mode() # Returns [1, 2]
            
            # No mode (all unique)
            Statistics([1, 2, 3]).mode()    # Returns None
        @endcode
        """
        freq = {}
        for x in self.data:
            freq[x] = freq.get(x, 0) + 1
        max_count = max(freq.values())
        modes = [x for x, count in freq.items() if count == max_count]
        if len(modes) == 1:
            return modes[0]
        if len(modes) == len(freq):
            return None
        return modes

    def variance(self, sample=True):
        """!
        @brief Computes the statistical variance.

        @param sample If True, computes **sample variance** (divisor N-1).
                      If False, computes **population variance** (divisor N).
        @return The variance (float).
        @throws ValueError If sample variance is requested for a dataset with fewer than 2 elements.

        @note Variance measures the average squared deviation from the mean.
        
        @par Example:
        @code
            stats = Statistics([2, 4, 4, 4, 5, 5, 7, 9])
            
            # Sample variance (default)
            stats.variance()             # Returns 4.571...
            
            # Population variance
            stats.variance(sample=False) # Returns 4.0
        @endcode
        """
        n = len(self.data)
        if n < 2 and sample:
            raise ValueError("At least two elements are required for sample variance.")
        mean_value = self.mean()
        squared_diffs = [(x - mean_value) ** 2 for x in self.data]
        denominator = n - 1 if sample else n
        return sum(squared_diffs) / denominator

    def std_deviation(self, sample=True):
        """!
        @brief Computes the standard deviation of the dataset.

        @details Standard deviation is the square root of variance.

        @param sample Boolean specifying sample or population variant.
        @return The standard deviation (float).
        
        @par Example:
        @code
            stats = Statistics([2, 4, 4, 4, 5, 5, 7, 9])
            stats.std_deviation() # Returns 2.138...
        @endcode
        """
        return math.sqrt(self.variance(sample))

    def summary(self):
        """!
        @brief Produces a summary of statistical metrics.

        @return A dictionary with keys: mean, median, mode, variance, std_dev.
        
        @par Example:
        @code
            stats = Statistics([1, 2, 2, 3])
            stats.summary()
            # Returns:
            # {
            #     'mean': 2.0, 
            #     'median': 2, 
            #     'mode': 2, 
            #     'variance': 0.667, 
            #     'std_dev': 0.816
            # }
        @endcode
        """
        return {
            "mean": round(self.mean(), 3),
            "median": self.median(),
            "mode": self.mode(),
            "variance": round(self.variance(), 3),
            "std_dev": round(self.std_deviation(), 3)
        }

class TestMean(unittest.TestCase):
    """!
    @brief Tests for mean() method.
    @details Covers several datasets: basic, negative, mixed values, floating point.
    """

    def setUp(self):
        self.stats_basic = Statistics([1, 2, 3, 4, 5])
        self.stats_negative = Statistics([-1, -2, -3])
        self.stats_mixed = Statistics([-2, 0, 5])
        self.stats_floats = Statistics([1.2, 2.3, 3.4])

    def test_mean_basic(self):
        """!
        @brief Verifies mean() for a basic sequential dataset.

        @details Ensures the arithmetic mean of [1,2,3,4,5] equals 3.
        @test Expected result: 3
        """
        self.assertEqual(self.stats_basic.mean(), 3)

    def test_mean_negative(self):
        """!
        @brief Verifies mean() for a dataset of negative integers.

        @details Ensures the arithmetic mean of [-1,-2,-3] equals -2.
        @test Expected result: -2
        """
        self.assertEqual(self.stats_negative.mean(), -2)

    def test_mean_mixed_signs(self):
        """!
        @brief Verifies mean() for a mixed-sign dataset.

        @details Checks that mean of [-2,0,5] is approximately 1.
        @test Expected result: ~1
        """
        self.assertAlmostEqual(self.stats_mixed.mean(), 1)

    def test_mean_floats(self):
        """!
        @brief Verifies mean() for floating-point values.

        @details Ensures mean of [1.2,2.3,3.4] is approximately 2.3.
        @test Expected result: ~2.3
        """
        self.assertAlmostEqual(self.stats_floats.mean(), 2.3)


class TestMedian(unittest.TestCase):
    """!
    @brief Tests for median() method.
    @details Includes tests for sorted, unsorted, odd, even, negative and float datasets.
    """

    def setUp(self):
        self.stats_basic = Statistics([1, 2, 3, 4, 5])
        self.stats_negative = Statistics([-5, -1, -3])
        self.stats_floats = Statistics([1.5, 3.2, 2.8])
        self.stats_even = Statistics([10, 20, 30, 40, 50, 60])
        self.stats_unsorted = Statistics([100, 1, 50, 10])

    def test_median_basic(self):
        """!
        @brief Verifies median() for an odd-length sorted dataset.

        @details Ensures median of [1,2,3,4,5] is 3.
        @test Expected result: 3
        """
        self.assertEqual(self.stats_basic.median(), 3)
    
    def test_median_negative_numbers(self):
        """!
        @brief Verifies median() with negative numbers.

        @details Ensures median of [-5,-1,-3] (unsorted input) returns -3.
        @test Expected result: -3
        """
        self.assertEqual(self.stats_negative.median(), -3)

    def test_median_floats(self):
        """!
        @brief Verifies median() for floating-point dataset.

        @details Ensures median of [1.5,3.2,2.8] is approximately 2.8.
        @test Expected result: ~2.8
        """
        self.assertAlmostEqual(self.stats_floats.median(), 2.8)

    def test_median_even_list(self):
        """!
        @brief Verifies median() for an even-length dataset.

        @details Ensures median of [10,20,30,40,50,60] is the average of the two
        central values (35).
        @test Expected result: 35
        """
        self.assertEqual(self.stats_even.median(), 35)

    def test_median_unsorted_input(self):
        """!
        @brief Verifies median() correctly handles unsorted input.

        @details Ensures median of [100,1,50,10] (unsorted) is 30.
        @test Expected result: 30
        """
        self.assertEqual(self.stats_unsorted.median(), 30)


class TestMode(unittest.TestCase):
    """!
    @brief Tests for mode() method.
    @details Verifies unimodal, multimodal, unique, and repeated-value datasets.
    """

    def setUp(self):
        self.stats_negative = Statistics([-1, -2, -2, -3])
        self.stats_floats = Statistics([1.1, 2.2, 2.2, 3.3])
        self.stats_multiple = Statistics([1, 1, 2, 3, 3, 4, 4, 5, 5])
        self.stats_unsorted = Statistics([3, 1, 3, 2, 1])
        self.stats_unique = Statistics([10, 20, 30, 40])
        self.stats_same = Statistics([7, 7, 7])

    def test_mode_negative_numbers(self):
        """!
        @brief Verifies mode() for negative integers.

        @details Ensures mode of [-1,-2,-2,-3] is -2.
        @test Expected result: -2
        """
        self.assertEqual(self.stats_negative.mode(), -2)

    def test_mode_floats(self):
        """!
        @brief Verifies mode() for floating-point values.

        @details Ensures mode of [1.1,2.2,2.2,3.3] is 2.2.
        @test Expected result: 2.2
        """
        self.assertEqual(self.stats_floats.mode(), 2.2)

    def test_mode_multiple(self):
        """!
        @brief Verifies mode() returns multiple modes when present.

        @details Ensures multi-modal dataset returns the set of modes.
        @test Expected result: {1,3,4,5}
        """
        self.assertEqual(set(self.stats_multiple.mode()), {1, 3, 4, 5})

    def test_mode_unsorted_input(self):
        """!
        @brief Verifies mode() on unsorted input returns correct modes.

        @details Ensures output is independent of input ordering.
        @test Expected result: {1,3}
        """
        self.assertEqual(set(self.stats_unsorted.mode()), {1, 3})

    def test_mode_unrepeated(self):
        """!
        @brief Verifies mode() returns None when all values are unique.

        @details Ensures dataset with all unique values returns None.
        @test Expected result: None
        """
        self.assertIsNone(self.stats_unique.mode())
    
    def test_mode_all_same(self):
        """!
        @brief Verifies mode() when all elements are identical.

        @details Ensures a uniform dataset returns that single value as mode.
        @test Expected result: 7
        """
        self.assertEqual(self.stats_same.mode(), 7)
    
    def test_mode_empty_list(self):
        """!
        @brief Verifies mode() raises on empty dataset creation.

        @details Constructing Statistics with an empty list should raise ValueError
        before mode() is called.
        @test Expected result: ValueError
        """
        with self.assertRaises(ValueError):
            Statistics([]).mode()


class TestVarianceAndStdDev(unittest.TestCase):
    """!
    @brief Tests for variance() and std_deviation().
    @details Covers sample vs. population, integer, float, large and small numbers.
    """

    def assertVarianceAndStd(self, data, sample_var, pop_var, delta=1e-4):
        """!
        @brief Helper that asserts variance and standard deviation values.

        @param data The input dataset to evaluate.
        @param sample_var Expected sample variance value.
        @param pop_var Expected population variance value.
        @param delta Acceptable tolerance for floating comparisons.
        @details Creates a `Statistics` instance and checks both sample and
                 population variance and their square-rooted std deviations.
        """
        stats = Statistics(data)

        self.assertAlmostEqual(stats.variance(sample=True), sample_var, delta=delta)
        self.assertAlmostEqual(stats.variance(sample=False), pop_var, delta=delta)
        self.assertAlmostEqual(stats.std_deviation(sample=True),
                               math.sqrt(sample_var), delta=delta)
        self.assertAlmostEqual(stats.std_deviation(sample=False),
                               math.sqrt(pop_var), delta=delta)

    def test_basic(self):
        """!
        @brief Validates variance and std deviation for a basic integer range.

        @details Checks both sample and population results for [1..5].
        @test Expected sample variance: 2.5, population variance: 2
        """
        self.assertVarianceAndStd([1, 2, 3, 4, 5], 2.5, 2)

    def test_same_numbers(self):
        """!
        @brief Ensures zero variance for a uniform dataset.

        @details All identical values should yield zero variance and std deviation.
        @test Expected sample and population variance: 0
        """
        self.assertVarianceAndStd([5, 5, 5, 5], 0, 0)

    def test_negative_numbers(self):
        """!
        @brief Validates variance/std for negative integer dataset.

        @details Confirms correctness with negative values present.
        @test Expected sample variance: ~2.6666666, population variance: 2
        """
        self.assertVarianceAndStd([-2, -4, -4, -6], 2.6666666, 2)

    def test_floats(self):
        """!
        @brief Validates variance/std for floating-point inputs.

        @details Uses floats to ensure numeric stability and rounding tolerances.
        @test Expected sample variance: ~1.6666666, population variance: 1.25
        """
        self.assertVarianceAndStd([1.5, 2.5, 3.5, 4.5], 1.6666666, 1.25)

    def test_dataset(self):
        """!
        @brief Validates variance/std for a larger sequential dataset.

        @details Tests correctness and numerical stability for 0..99.
        @test Expected sample variance: ~841.6666667, population variance: 833.25
        """
        self.assertVarianceAndStd(list(range(100)), 841.6666667, 833.25)

    def test_with_large_numbers(self):
        """!
        @brief Ensures correctness with very large numbers to check scale handling.

        @test Expected sample variance: 1, population variance: 2/3
        """
        self.assertVarianceAndStd([1e10, 1e10 + 1, 1e10 + 2], 1, 2/3)

    def test_with_small_numbers(self):
        """!
        @brief Ensures correctness with very small numbers (close to zero).

        @test Expected sample variance: 1, population variance: 2/3
        """
        self.assertVarianceAndStd([1e-10, 1e-10 - 1, 1e-10 - 2], 1, 2/3)

    def test_single_element_population(self):
        """!
        @brief Verifies population variance/std for single-element dataset.

        @details Population formulas should yield zero for a single value.
        @test Expected population variance/std: 0
        """
        stats = Statistics([42])
        self.assertEqual(stats.variance(sample=False), 0)
        self.assertEqual(stats.std_deviation(sample=False), 0)

    def test_single_element_sample_error(self):
        """!
        @brief Ensures sample variance/std raise on single-element datasets.

        @details Sample variance requires at least two elements; requesting it
                 with a single element should raise ValueError.
        @test Expected: ValueError
        """
        with self.assertRaises(ValueError):
            Statistics([42]).variance(sample=True)
            Statistics([42]).std_deviation(sample=True)


class TestValidationAndErrors(unittest.TestCase):
    """!
    @brief Unit tests for error handling and data validation.
    @details Ensures proper exceptions (TypeError, ValueError) are raised for invalid inputs.
    """
    def test_empty_list(self):
        """!
        @brief Verifies constructing Statistics with an empty list raises ValueError.

        @test Expected: ValueError on empty dataset
        """
        with self.assertRaises(ValueError):
            Statistics([])

    def test_non_numeric(self):
        """!
        @brief Verifies non-numeric elements cause a TypeError.

        @test Expected: TypeError when list contains non-numeric types
        """
        with self.assertRaises(TypeError):
            Statistics([1, "a", 3])

    def test_non_list_input(self):
        """!
        @brief Verifies non-list inputs raise a TypeError.

        @test Expected: TypeError when input is not a list
        """
        with self.assertRaises(TypeError):
            Statistics("12345")

    def test_none_input(self):
        """!
        @brief Verifies passing None as data raises TypeError.

        @test Expected: TypeError for None input
        """
        with self.assertRaises(TypeError):
            Statistics(None)

    def test_nested_list_input(self):
        """!
        @brief Verifies nested lists are rejected as invalid elements.

        @test Expected: TypeError for nested list elements
        """
        with self.assertRaises(TypeError):
            Statistics([[1, 2], [3, 4]])


class TestIntegrationStatistics(unittest.TestCase):
    """!
    @brief Integration tests for the Statistics class.
    @details verifies that the summary() method correctly aggregates all metrics.
    """

    def test_summary_returns_correct_structure(self):
        """!
        @brief Integration test verifying `summary()` aggregates metrics.

        @details Confirms `summary()` contains expected keys and values for
                 a small dataset and that each metric is computed correctly.
        @test Expected: keys mean, median, mode, variance, std_dev with matching values
        """
        stats = Statistics([1, 2, 2, 3])
        summary = stats.summary()
        expected_keys = {"mean", "median", "mode", "variance", "std_dev"}
        self.assertTrue(expected_keys.issubset(summary.keys()))
        self.assertAlmostEqual(summary["mean"], 2.0)
        self.assertEqual(summary["median"], 2)
        self.assertEqual(summary["mode"], 2)
        self.assertAlmostEqual(summary["variance"], 0.667)
        self.assertAlmostEqual(summary["std_dev"], 0.816)

if __name__ == "__main__":
    data:list =  [1, 2, 3, 3, 3, 4, 5, 5, 8, 8, 9]
    stats = Statistics(data)

    print("Data:", data)
    print("Mean:", stats.mean())
    print("Median:", stats.median())
    print("Mode:", stats.mode())
    print("Variance:", stats.variance())
    print("Standard deviation:", stats.std_deviation())
    print("\nSummary:", stats.summary())


    unittest.main()