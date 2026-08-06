---
name: generate-comments-for-learning
description: Line-by-line contextual code annotation tool designed for learning, omitting repetitive explanations.
disable-model-invocation: true
---

# Generate Comments for Learning

Annotate target source code files line-by-line with rich, context-aware comments for educational self-study. Explanations focus on mechanics, design intent, and API behaviors while enforcing strict non-redundancy across the file.

---

## Core Rules

1. **Context-Aware Interpretation**: Scan and analyze the entire file before writing annotations. Ensure line comments reflect global state, scope, variable origins, imported module mechanisms, and control flow.
2. **First-Occurrence Only (Strict Non-Redundancy)**: Maintain an internal inventory of introduced syntax, patterns, and framework APIs. Explain each concept thoroughly upon its first appearance. When the same concept or syntax recurs later in the file, omit the generic syntax explanation and focus purely on local logic variations (or skip if identical).
3. **Pedagogical Depth**: Explain *why* the code is written a certain way, *what* the underlying API does under the hood, and *how* data flows through the statement.
4. **Preserve Code Execution**: Annotations must be output either inline using valid target-language comment syntax (`#` for Python, `//` for JS/TS) or presented as an annotated code block without corrupting original code structure.

---

## Workflow

### Step 1: Global Context Scan
- Read the entire target file to map imports, class/function definitions, global variables, and main execution entry points.
- Identify core architectural patterns (e.g., async event loops, DOM manipulation, decorator chains).

### Step 2: Initialize Concept Tracker
- Establish a tracking memory for introduced concepts:
  - Language syntax constructs (e.g., `async/await`, context managers `with`, list comprehensions).
  - Framework/Library methods (e.g., `page.goto()`, `requests.get()`, `BeautifulSoup()`).
  - Common patterns (e.g., retry loops, error handling blocks).

### Step 3: Sequential Line-by-Line Annotation
For each line or minimal cohesive block in the target file:
- **First Appearance of Concept**: Provide a detailed explanation of the API/syntax construct, its parameters, return values, and role in this specific code context. Mark concept as introduced in tracker.
- **Subsequent Appearance of Concept**: Skip the general explanation. Only comment on unique variable values or logical outcomes specific to this invocation line.

### Step 4: Verification & Formatting
- Check that no concept explanation is repeated across lines.
- Ensure all comments match the target language's valid comment syntax.
- Verify that every nontrivial statement has appropriate educational guidance.

---

## Output Format

Return the fully annotated code formatted inside markdown code blocks with line comments embedded cleanly alongside or directly above the original code lines.

Example (Python):
```python
# [FIRST OCCURRENCE: async/await] Defines an asynchronous function allowing non-blocking I/O operations.
# [FIRST OCCURRENCE: playwright] Spawns a Chromium browser instance in non-headless mode for visual debugging.
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        
        # Creates an isolated browser context (similar to a fresh incognito window session).
        context = await browser.new_context()
        
        # Opens a new blank tab within the context.
        page = await context.new_page()
        
        # [FIRST OCCURRENCE: page.goto] Navigates to target URL and waits for 'load' event by default.
        await page.goto("https://example.com")
        
        # [RECURRING: page.goto] Only noting destination change; 'goto' mechanics already explained above.
        await page.goto("https://example.com/login")
```

---

## Completion Criteria

- Every functional line or cohesive block contains accurate, context-aware commentary.
- Concept tracker strictly prevents repeated explanations of syntax, patterns, or API methods introduced earlier in the file.
- Generated comments are syntactically valid in the target language.
