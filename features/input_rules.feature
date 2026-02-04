@logic @regression
Feature: Calculator - Input rules and operator handling

  Background:
    Given the calculator app is open
    And the display shows "0"

  # Risk: ensures leading operators are ignored until a number is entered.
  @regression
  Scenario Outline: Leading operators are ignored
    When I input the sequence "<sequence>"
    Then the display should show "<result>"

    Examples:
      | sequence | result |
      | +5=      | 5      |
      | -5=      | 5      |
      | *5=      | 5      |
      | /5=      | 5      |

  # Risk: ensures consecutive operators replace the previous one.
  @smoke
  Scenario Outline: Consecutive operators replace the previous operator
    When I input the sequence "<sequence>"
    Then the display should show "<result>"

    Examples:
      | sequence | result |
      | 5++5=    | 10     |
      | 5+-5=    | 0      |
      | 5*-5=    | 0      |
      | 5//5=    | 1      |

  # Risk: equals on incomplete expression must error.
  @regression
  Scenario Outline: Equals on incomplete expression returns Error
    When I input the sequence "<sequence>"
    Then the display should show "Error"

    Examples:
      | sequence |
      | 5+=      |
      | 5-=      |
      | 5*=      |
      | 5/=      |
