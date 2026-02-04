@logic @regression
Feature: Calculator - Core arithmetic
  The calculator supports +, -, *, / with integers and decimals.

  Background:
    Given the calculator app is open
    And the display shows "0"

  # Risk: verifies basic arithmetic with integers.
  @smoke
  Scenario Outline: Basic operations with integers
    When I input the sequence "<sequence>"
    Then the display should show "<result>"

    Examples:
      | sequence | result |
      | 2+2=     | 4      |
      | 7-5=     | 2      |
      | 6*3=     | 18     |
      | 8/4=     | 2      |

  # Risk: verifies arithmetic with decimals.
  @regression
  Scenario Outline: Basic operations with decimals
    When I input the sequence "<sequence>"
    Then the display should show "<result>"

    Examples:
      | sequence    | result |
      | 2.5+1.25=   | 3.75   |
      | 5.5-2=      | 3.5    |
      | 2.5*2=      | 5      |
      | 7.5/2.5=    | 3      |
