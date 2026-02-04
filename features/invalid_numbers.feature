@logic @regression
Feature: Calculator - Invalid numbers and syntax

  Background:
    Given the calculator app is open
    And the display shows "0"

  # Risk: invalid numeric formats must fail on calculation.
  @regression
  Scenario Outline: Invalid decimals return Error
    When I input the sequence "<sequence>"
    Then the display should show "Error"

    Examples:
      | sequence |
      | .5=      |
      | 5.=      |
      | 5..2=    |
      | 1.2.3=   |

  # Risk: malformed expressions should error deterministically.
  @regression
  Scenario Outline: Malformed expressions return Error
    When I input the sequence "<sequence>"
    Then the display should show "Error"

    Examples:
      | sequence |
      | +=       |
      | -=       |
      | *=       |
      | /=       |
