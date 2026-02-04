from behave import given, when, then

from calculator import CalculatorGUI, CalculatorLogic


class CalculatorState:
    def __init__(self):
        self.expression = ""
        self.display = "0"
        self.error_state = False
        self.leading_operator_ignored = False

    def _update_display(self, value):
        self.display = str(value)

    def _process_input(self, char):
        if char not in "0123456789+-*/.C=←":
            return
        if self.error_state and char != "C":
            return
        if char == "C":
            self.expression = ""
            self.error_state = False
            self.leading_operator_ignored = False
            self._update_display("0")
        elif char == "←":
            self.expression = self.expression[:-1]
            self._update_display(self.expression if self.expression else "0")
        elif char == "=":
            if not self.expression and self.leading_operator_ignored:
                self._update_display("Error")
                self.error_state = True
                self.leading_operator_ignored = False
                return
            result = CalculatorLogic.calculate(self.expression)
            self._update_display(result)
            if result == "Error":
                self.expression = ""
                self.error_state = True
            else:
                self.expression = str(result)
        else:
            if char in "+-*/":
                if not self.expression:
                    self.leading_operator_ignored = True
                    return
                elif self.expression[-1] in "+-*/":
                    self.expression = self.expression[:-1] + char
                else:
                    self.expression += char
            else:
                self.expression += str(char)
                self.leading_operator_ignored = False
            self._update_display(self.expression)

    def input_sequence(self, sequence):
        for char in sequence:
            self._process_input(char)


def _input_sequence(context, sequence):
    seq = _normalize_sequence(sequence)
    if hasattr(context, "calculator_gui") and context.calculator_gui:
        for char in seq:
            context.calculator_gui.process_input(char)
    else:
        context.calculator.input_sequence(seq)


def _get_display_value(context):
    if hasattr(context, "calculator_gui") and context.calculator_gui:
        return context.calculator_gui.display.get()
    return context.calculator.display


def _normalize_sequence(sequence):
    result = []
    i = 0
    while i < len(sequence):
        if sequence.startswith("BACK", i):
            result.append("←")
            i += 4
            continue
        result.append(sequence[i])
        i += 1
    return result


@given("the calculator app is open")
def step_open_calculator(context):
    context.calculator_gui = None
    context.calculator = CalculatorState()


@given("the GUI calculator app is open")
def step_open_gui_calculator(context):
    context.calculator = None
    root = context.tk_root
    context.calculator_gui = CalculatorGUI(root)
    root.update_idletasks()


@given('the display shows "{value}"')
def step_display_shows_value(context, value):
    assert _get_display_value(context) == value


@when('I input the sequence "{sequence}"')
def step_input_sequence(context, sequence):
    _input_sequence(context, sequence)


@when('I press "{char}"')
def step_press_single(context, char):
    _input_sequence(context, char)


@then('the display should show "{value}"')
def step_display_should_show(context, value):
    assert _get_display_value(context) == value


@then('the internal expression should be "{value}"')
def step_internal_expression_should_be(context, value):
    if hasattr(context, "calculator_gui") and context.calculator_gui:
        current = context.calculator_gui.expression
    else:
        current = context.calculator.expression
    assert current == value


@then('the internal expression should be ""')
def step_internal_expression_should_be_empty(context):
    if hasattr(context, "calculator_gui") and context.calculator_gui:
        current = context.calculator_gui.expression
    else:
        current = context.calculator.expression
    assert current == ""


@then('the window title should be "{title}"')
def step_window_title_should_be(context, title):
    assert context.calculator_gui is not None
    assert context.calculator_gui.master.title() == title
