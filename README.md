# LAB2

This project implements a Python class, `Statistics`, designed to perform descriptive statistical analysis on numerical datasets. It includes methods for calculating measures of central tendency and statistical variability, fully covered by unit tests.

This repository is part of **Laboratory Work #2**, focusing on code documentation, CI/CD pipelines, and automatic documentation publication.

## Features

The `Statistics` class supports the following operations:

* **Central Tendency:**
    * `mean()`: Arithmetic mean.
    * `median()`: Middle value (handles both odd and even dataset sizes).
    * `mode()`: Most frequent value(s). Handles unimodal, multimodal, and no-mode scenarios.
* **Variability:**
    * `variance(sample=True/False)`: Calculates sample or population variance.
    * `std_deviation(sample=True/False)`: Calculates standard deviation.
* **Utilities:**
    * `summary()`: Returns a dictionary containing all the above metrics.
    * **Validation**: Ensures input data is a non-empty list of numeric values.

## Documentation

**Format**: The source code is documented using Doxygen style comments (using @brief, @param, @return tags).

**Generation**: HTML documentation is generated automatically using a CI/CD pipeline.

**Hosting**: The documentation is deployed to GitHub Pages.

## Prerequisites
* Python 3.x
* Standard libraries: `math`, `unittest`
