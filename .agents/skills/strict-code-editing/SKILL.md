---
name: strict-code-editing
description: Apply strict execution rules (micro-diffs, zero chitchat, strict scoping, token limits) strictly when creating or modifying source code directly.
disable-model-invocation: true
---

# Strict Code Editing Guardrails

## 🎯 觸發條件 (Trigger Condition)
當且僅當你準備進行**單純的程式碼撰寫、修改或 Bug 修復**，且當前任務**沒有其他更高階的 Skill 主導**時，自動啟用本規範。

## ⚡ 衝突與優先權規則 (Precedence Rule)
**若當前對話正在執行其他 Skill**（例如 `/implement`, `/tdd`, `/grill-with-docs`, `/improve-codebase-architecture` 或 `code-review` 等）：
- **本 Skill 之限制自動退居次要地位**，一切依據該主導 Skill 的工作流規範與對話需求為準。

---

## 🛡️ 程式碼修改行為規範 (Execution Rules)

1. **Micro-Diffs Only**:
   - 修改既有程式碼時僅輸出變更行 (`- old` / `+ new`)，嚴禁無意義重寫整份檔案。

2. **Zero-Chitchat & Zero-Why**:
   - 不需客套，不需解釋原因或進行背景說明，直接輸出修改後的結果與程式碼。

3. **Strict Scoping**:
   - 僅能編修 Prompt 明確指定的模組與檔案，禁止未經授權的跨檔案重構。

4. **Token Control**:
   - 若單次變更預計會影響超過 3 個檔案，必須先暫停並向使用者確認授權。