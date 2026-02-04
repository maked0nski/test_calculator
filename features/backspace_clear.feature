@logic @regression
Feature: Calculator - Backspace and clear

  Background:
    Given the calculator app is open
    And the display shows "0"

  # Risk: backspace removes last character and shows 0 when empty.
  @smoke
  Scenario Outline: Backspace behavior
    When I input the sequence "<sequence>"
    Then the display should show "<result>"

    Examples:
      | sequence | result |
      | 9BACK    | 0      |
      | 99BACK   | 9      |
      | 5+BACK   | 5      |
      | 0BACK    | 0      |

  # Risk: clear resets expression and display.
  @regression
  Scenario Outline: Clear resets to zero
    When I input the sequence "<sequence>"
    Then the display should show "0"
    And the internal expression should be ""

    Examples:
      | sequence |
      | 123C     |
      | 9+1C     |
      | 0C       |

  # Risk: clear after Error resets state.
  @regression
  Scenario: Clear after Error
    When I input the sequence "5/0="
    Then the display should show "Error"
    When I input the sequence "C"
    Then the display should show "0"
    And the internal expression should be ""
