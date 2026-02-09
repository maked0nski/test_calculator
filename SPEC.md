## Calculator Application — Functional Specification

### Version

* **Product version:** v0.1
* **Document version:** 1.0
* **Last updated:** 2026-02-04

---

## 1. Overview

This document describes the functional and non-functional requirements for a **basic calculator application** with a graphical user interface (GUI).

The calculator supports **basic arithmetic operations only** and intentionally **does NOT support a sign toggle (± / SIGN)** or unary minus as a standalone operator.

The goal of this specification is to:

* remove ambiguity from user input handling,
* clearly define calculator behaviour for edge cases,
* provide a solid basis for testing (manual & BDD automation).

---

## 2. Scope

### In scope

* GUI calculator
* Basic arithmetic operations
* Keyboard and button input
* Error handling
* Deterministic behaviour for malformed input

### Out of scope

* Sign toggle (± / SIGN)
* Scientific functions
* Parentheses
* Memory buttons (M+, M-, MR, etc.)
* Percentage
* Power operations
* Localization

---

## 3. Supported Operations

| Operator | Description      |
|----------|------------------|
| `+`      | Addition         |
| `-`      | Subtraction      |
| `*`      | Multiplication   |
| `/`      | Division         |
| `=`      | Calculate result |
| `C`      | Clear input      |
| `←`      | Backspace        |

---

## 4. Input Model

### 4.1 Input sources

* Calculator buttons (primary)
* Keyboard input (secondary, mapped)

### 4.2 Allowed characters

```
0–9
+
-
*
/
.
=
C
←
```

Any other input MUST be ignored or rejected.

---

## 5. Core Behaviour Rules (Critical Section)

### 5.1 Numbers

* Integers and decimals are supported.
* Decimal separator is `.` (dot).
* Multiple dots in a single number are invalid.

**Valid**

* `5`
* `12.5`
* `0.75`

**Invalid**

* `5..2`
* `.5`
* `5.`
* `1.2.3`

Invalid numeric formats result in `Error` upon calculation.

---

### 5.2 Operators

#### 5.2.1 Operator as first input

| Input | Result |
|-------|--------|
| `+5=` | `5`    |
| `-5=` | `5`    |
| `*5=` | `5`    |
| `/5=` | `5`    |

**Rule:**
Leading operators are ignored until the first number is entered.

---

#### 5.2.2 Consecutive operators (KEY RULE)

If an operator is entered immediately after another operator,
**the previous operator MUST be replaced**.

| Input   | Interpreted as | Result |
|---------|----------------|--------|
| `5++5=` | `5+5`          | `10`   |
| `5+-5=` | `5-5`          | `0`    |
| `5*-5=` | `5-5`          | `0`    |
| `5//5=` | `5/5`          | `1`    |

✅ **No unary minus exists in this calculator.**
❌ `+-` is NOT treated as `+(-x)`.

---

### 5.3 Equals (`=`)

#### 5.3.1 Valid usage

* Calculates the current expression.
* Displays result.
* Result replaces the expression.

Example:

```
2+2= → 4
```

---

#### 5.3.2 Equals on incomplete expression

If the expression ends with an operator, calculation MUST fail.

| Input | Result |
|-------|--------|
| `5+=` | Error  |
| `5-=` | Error  |
| `5*=` | Error  |
| `5/=` | Error  |

---

### 5.4 Division by zero

Any division by zero MUST result in:

```
Error
```

Examples:

* `5/0=`
* `10/(5-5)=` (if supported internally)

---

## 6. Backspace (`←`) Behaviour

| State | Action | Result |
|-------|--------|--------|
| `9`   | `←`    | `0`    |
| `99`  | `←`    | `9`    |
| `5+`  | `←`    | `5`    |
| `0`   | `←`    | `0`    |

* Backspace removes the last character.
* If expression becomes empty → display `0`.

---

## 7. Clear (`C`) Behaviour

* Clears the entire expression.
* Resets display to `0`.
* Clears any error state.

| Before  | After |
|---------|-------|
| `123`   | `0`   |
| `Error` | `0`   |

---

## 8. Error Handling

### 8.1 Error state

* Display text: `Error`
* No automatic recovery
* User MUST press `C` to reset

### 8.2 Error triggers

* Invalid syntax
* Incomplete expression
* Division by zero
* Invalid decimal format

---

## 9. Display Rules

* Default display value: `0`
* Display is right-aligned
* Integer results must NOT show `.0`

  * `4.0` → `4`
* Decimal results rounded to **max 8 decimal places**

---

## 10. State Transitions (Simplified)

```
[Start]
  ↓
[Input numbers/operators]
  ↓
[= pressed]
  ├── valid → [Result]
  └── invalid → [Error]
                     ↓
                   [C]
                     ↓
                  [Start]
```

---

## 11. Non-Functional Requirements

### Performance

* Calculation must complete instantly (<100ms).

### Stability

* Application must not crash on malformed input.

### Security

* Only calculator-allowed characters may be evaluated.
* Arbitrary code execution MUST be prevented.

---

## 12. Test Coverage Expectations

### Mandatory test areas

* Basic arithmetic
* Consecutive operators
* Incomplete expressions
* Division by zero
* Backspace
* Clear
* UI smoke tests

### BDD recommendation

* Given / When / Then scenarios
* Edge cases MUST be explicitly covered

---

## 13. Explicitly Unsupported Features

| Feature         | Reason             |
|-----------------|--------------------|
| SIGN / ±        | Out of scope       |
| Unary minus     | Simplifies parsing |
| Parentheses     | Out of scope       |
| Scientific mode | Out of scope       |

---

## 14. Acceptance Criteria (Summary)

The calculator is considered **DONE** when:

* All rules in this specification are met
* All defined edge cases behave deterministically
* All BDD scenarios pass
* Behaviour matches this document exactly

---

### ✅ Final note 

> **This specification intentionally removes ambiguity.**
> All unclear behaviours from the original task (e.g. `5++5`, `5-=`, `+-`) are resolved **by explicit design decisions**, not assumptions.

---

