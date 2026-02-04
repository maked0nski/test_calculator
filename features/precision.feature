@logic @precision
Feature: Calculator - Display and precision rules

  Background:
    Given the calculator app is open
    And the display shows "0"

  # Risk: integers must not show a decimal part.
  @regression
  Scenario Outline: Integer display formatting
    When I input the sequence "<sequence>"
    Then the display should show "<result>"

    Examples:
      | sequence | result |
      | 2/1=     | 2      |
      | 10/5=    | 2      |
      | 6/3=     | 2      |

  # Risk: decimals must be rounded to max 8 places.
  @precision
  Scenario Outline: Decimal rounding to 8 places
    When I input the sequence "<sequence>"
    Then the display should show "<result>"

    Examples:
      | sequence                | result     |
      | 1/3=                    | 0.33333333 |
      | 2/3=                    | 0.66666667 |
      | 0.123456789+0=          | 0.12345679 |
      | 123456789.123456789+0=  | 123456789.12345679 |
