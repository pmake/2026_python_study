---
name: playwright-locator-generator
description: Generate optimal Playwright Python locator code based on HTML snippets copied from Chrome DevTools ("Copy element").
disable-model-invocation: true
---

# Playwright Locator Generator

Generate robust, maintenance-friendly Playwright Python locator code from HTML element snippets copied via Chrome DevTools ("Copy element").

Before determining locators, inspect [playwright_locators_guide.md](playwright_locators_guide.md) for priority rules and anti-pattern guardrails.

---

## Evaluation Workflow

Follow these steps in sequence to analyze the HTML input and generate the recommended locator:

### Step 1: Parse HTML Attributes & Visibility
Inspect the input HTML for key features:
- **ARIA & Accessibility attributes**: `role`, `aria-label`, `aria-labelledby`, `aria-hidden`
- **Native tag & type**: `<button>`, `<input type="checkbox">`, `<input type="file">`, `<textarea>`, `<a>`, `<h2>`
- **Text content**: Visible text inside tags or nested `<span>`
- **Form attributes**: `placeholder`, `name`, `label`
- **Hidden / CSS state**: `style="display: none;"`, `opacity: 0`, `aria-hidden="true"`

### Step 2: Determine Locator Priority
Apply the priority ladder from [playwright_locators_guide.md](playwright_locators_guide.md):

1. **Role Locator (Highest Priority)**:
   - Use `page.get_by_role(role, name="...")` if the element has an implicit or explicit ARIA role AND a valid Accessible Name (`aria-label`, `<label>`, or inner text).
   - **Guardrail**: If `aria-hidden="true"` is present, DO NOT use `get_by_role()` (it will be ignored in the accessibility tree).

2. **Text Locator (Exact Match)**:
   - Use `page.get_by_text("...", exact=True)` for visible text elements where role is ambiguous. Always include `exact=True` to prevent Strict Mode violations.

3. **Placeholder / Label Locator**:
   - For input fields, use `page.get_by_placeholder("...")` or `page.get_by_label("...")`.

4. **Attribute / CSS Selector (Fallback)**:
   - For hidden elements (e.g. `<input type="file" name="Filedata">`), use `page.locator('input[name="Filedata"]')`.
   - **Guardrail**: Strip dynamic IDs (e.g., `#mat-mdc-checkbox-13-input` $\rightarrow$ do not use `13` as a static ID selector). Avoid generic class names.

### Step 3: Check Required Actions & Execution State
- **Hidden Elements**: Recommend `.wait_for(state="attached")` and direct manipulation (e.g. `.set_input_files()`).
- **Interactive Elements**: Recommend standard actions (`.click()`, `.fill()`).

---

## Response Format

Present the recommendation clearly:

1. **Recommended Locator**: Provide the clean, copy-pasteable Python code.
2. **Rationale**: Explain why this locator was chosen based on ARIA / Playwright guidelines.
3. **Caveats & Guardrails**: Highlight any hidden state, dynamic IDs, or Strict Mode considerations if applicable.
4. **Alternative Options**: Provide 1-2 secondary choices (e.g. `get_by_text` or CSS selector).

---

## Completion Criterion
- Recommended locator follows the priority ranking in [playwright_locators_guide.md](playwright_locators_guide.md).
- Dynamic IDs and generic classes are filtered out.
- Hidden elements (`aria-hidden="true"`, `display: none`) are correctly handled with attribute selectors and `state="attached"`.
