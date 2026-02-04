# Calculator BDD Runbook

## About the calculator

This is a basic GUI calculator built with Tkinter.

Capabilities:
- Basic arithmetic: `+`, `-`, `*`, `/`
- Integers and decimals (dot as separator)
- Clear: `C`
- Backspace: `←`
- Result rounding to max 8 decimal places
- Integer results show without `.0`

Limitations:
- No sign toggle (±), no unary minus
- No parentheses
- No scientific functions
- No memory buttons
- No percentage

Input rules (per SPEC):
- Only characters `0–9 + - * / . = C ←` are accepted
- Leading operators are ignored until a number is entered
- Consecutive operators replace the previous operator
- Incomplete expressions (e.g. `5+=`) return `Error`
- Invalid decimals (e.g. `.5`, `5.`, `1.2.3`) return `Error`
- Division by zero returns `Error`
- After `Error`, only `C` clears the state

## Setup

```powershell
pip install -r requirements.txt
```

## Run the calculator

```powershell
python calculator.py
```

## Run tests

```powershell
behave
```

## Quick start

```powershell
behave
```

## Tagged runs (PowerShell)

PowerShell treats `@` specially, so wrap tags in quotes.

```powershell
behave --tags "@smoke"
behave --tags "@regression"
behave --tags "@precision"
behave --tags "@gui"
```

## Test coverage

The BDD suite covers:
- Basic arithmetic (integers and decimals)
- Operator handling (leading operators, consecutive operators)
- Invalid formats and malformed expressions
- Division by zero and error state handling
- Backspace and clear behavior
- Display formatting and precision
- GUI smoke checks
