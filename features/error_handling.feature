@logic @regression
Feature: Calculator - Error handling and state

  Background:
    Given the calculator app is open
    And the display shows "0"

  # Risk: division by zero must always return Error.
  @smoke
  Scenario Outline: Division by zero returns Error
    When I input the sequence "<sequence>"
    Then the display should show "Error"

    Examples:
      | sequence |
      | 5/0=     |
      | 0/0=     |
      | 10/0=    |

  # Risk: after Error, only C can recover.
  @regression
  Scenario Outline: Error state blocks input until C
    When I input the sequence "<sequence>"
    Then the display should show "Error"
    When I input the sequence "<recovery>"
    Then the display should show "<result>"

    Examples:
      | sequence | recovery | result |
      | 5/0=     | 1        | Error  |
      | 5/0=     | 12+3=    | Error  |
      | 5/0=     | C        | 0      |

  # Risk: equals with empty expression should not crash and stays at 0.
  @regression
  Scenario: Equals with empty expression
    When I input the sequence "="
    Then the display should show "0"
