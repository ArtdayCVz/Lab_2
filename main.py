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
        self.assertEqual(self.stats_basic.mean(), 3)

    def test_mean_negative(self):
        self.assertEqual(self.stats_negative.mean(), -2)

    def test_mean_mixed_signs(self):
        self.assertAlmostEqual(self.stats_mixed.mean(), 1)

    def test_mean_floats(self):
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
        self.assertEqual(self.stats_basic.median(), 3)
    
    def test_median_negative_numbers(self):
        self.assertEqual(self.stats_negative.median(), -3)

    def test_median_floats(self):
        self.assertAlmostEqual(self.stats_floats.median(), 2.8)

    def test_median_even_list(self):
        self.assertEqual(self.stats_even.median(), 35)

    def test_median_unsorted_input(self):
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
        self.assertEqual(self.stats_negative.mode(), -2)

    def test_mode_floats(self):
        self.assertEqual(self.stats_floats.mode(), 2.2)

    def test_mode_multiple(self):
        self.assertEqual(set(self.stats_multiple.mode()), {1, 3, 4, 5})

    def test_mode_unsorted_input(self):
        self.assertEqual(set(self.stats_unsorted.mode()), {1, 3})

    def test_mode_unrepeated(self):
        self.assertIsNone(self.stats_unique.mode())
    
    def test_mode_all_same(self):
        self.assertEqual(self.stats_same.mode(), 7)
    
    def test_mode_empty_list(self):
        with self.assertRaises(ValueError):
            Statistics([]).mode()


class TestVarianceAndStdDev(unittest.TestCase):
    """!
    @brief Tests for variance() and std_deviation().
    @details Covers sample vs. population, integer, float, large and small numbers.
    """

    def assertVarianceAndStd(self, data, sample_var, pop_var, delta=1e-4):
        stats = Statistics(data)

        self.assertAlmostEqual(stats.variance(sample=True), sample_var, delta=delta)
        self.assertAlmostEqual(stats.variance(sample=False), pop_var, delta=delta)
        self.assertAlmostEqual(stats.std_deviation(sample=True),
                               math.sqrt(sample_var), delta=delta)
        self.assertAlmostEqual(stats.std_deviation(sample=False),
                               math.sqrt(pop_var), delta=delta)

    def test_basic(self):
        self.assertVarianceAndStd([1, 2, 3, 4, 5], 2.5, 2)

    def test_same_numbers(self):
        self.assertVarianceAndStd([5, 5, 5, 5], 0, 0)

    def test_negative_numbers(self):
        self.assertVarianceAndStd([-2, -4, -4, -6], 2.6666666, 2)

    def test_floats(self):
        self.assertVarianceAndStd([1.5, 2.5, 3.5, 4.5], 1.6666666, 1.25)

    def test_dataset(self):
        self.assertVarianceAndStd(list(range(100)), 841.6666667, 833.25)

    def test_with_large_numbers(self):
        self.assertVarianceAndStd([1e10, 1e10 + 1, 1e10 + 2], 1, 2/3)

    def test_with_small_numbers(self):
        self.assertVarianceAndStd([1e-10, 1e-10 - 1, 1e-10 - 2], 1, 2/3)

    def test_single_element_population(self):
        stats = Statistics([42])
        self.assertEqual(stats.variance(sample=False), 0)
        self.assertEqual(stats.std_deviation(sample=False), 0)

    def test_single_element_sample_error(self):
        with self.assertRaises(ValueError):
            Statistics([42]).variance(sample=True)
            Statistics([42]).std_deviation(sample=True)


class TestValidationAndErrors(unittest.TestCase):
    """!
    @brief Unit tests for error handling and data validation.
    @details Ensures proper exceptions (TypeError, ValueError) are raised for invalid inputs.
    """
    def test_empty_list(self):
        with self.assertRaises(ValueError):
            Statistics([])

    def test_non_numeric(self):
        with self.assertRaises(TypeError):
            Statistics([1, "a", 3])

    def test_non_list_input(self):
        with self.assertRaises(TypeError):
            Statistics("12345")

    def test_none_input(self):
        with self.assertRaises(TypeError):
            Statistics(None)

    def test_nested_list_input(self):
        with self.assertRaises(TypeError):
            Statistics([[1, 2], [3, 4]])


class TestIntegrationStatistics(unittest.TestCase):
    """!
    @brief Integration tests for the Statistics class.
    @details verifies that the summary() method correctly aggregates all metrics.
    """

    def test_summary_returns_correct_structure(self):
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