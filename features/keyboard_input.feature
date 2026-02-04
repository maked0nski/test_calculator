@logic @regression
Feature: Calculator - Keyboard and invalid character handling

  Background:
    Given the calculator app is open
    And the display shows "0"

  # Risk: non-allowed characters must be ignored.
  Scenario Outline: Invalid characters are ignored
    When I input the sequence "<sequence>"
    Then the display should show "<result>"

    Examples:
      | sequence | result |
      | a        | 0      |
      | ?        | 0      |
      | 1a2=     | 12     |
      | 5@+3=    | 8      |
