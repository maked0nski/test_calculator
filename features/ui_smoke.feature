@gui @smoke
Feature: Calculator - GUI smoke tests

  # Risk: verifies GUI launches and default display.
  Scenario: App opens with default display and title
    Given the GUI calculator app is open
    Then the display should show "0"
    And the window title should be "Calculator"

  # Risk: basic GUI flow for input and equals.
  Scenario Outline: GUI basic operations
    Given the GUI calculator app is open
    When I input the sequence "<sequence>"
    Then the display should show "<result>"

    Examples:
      | sequence | result |
      | 2+2=     | 4      |
      | 7-5=     | 2      |
      | 6*3=     | 18     |
      | 8/4=     | 2      |
