# Self-Prompting Instructions

> Use these guidelines when constructing prompts for yourself or other LLMs.

---

## Core Template

```xml
<role>[Specific expertise and perspective]</role>

<instructions>
[Numbered, explicit steps — tell the model what TO do, not what to avoid]
</instructions>

<constraints>
[Behavioral boundaries with explanations of WHY]
</constraints>

<examples>
  <example>
    <input>[Representative input]</input>
    <output>[Exact desired output format]</output>
  </example>
  <!-- Include 3-5 diverse examples covering edge cases -->
</examples>

<context>
[All relevant documents, data, or background — place BEFORE the task]
</context>

<task>
[Clear, specific request]
</task>

<output_format>
[Exact structure specification]
</output_format>
```

---

## Quick Rules

1. **Structure first** — Use XML tags to separate components. Tag names should describe content.

2. **Context before query** — Documents at top, instructions and questions at bottom.

3. **Positive framing** — Say what to do, not what to avoid. If prohibiting something, explain why.

4. **Show, don't tell** — 3–5 examples are more effective than lengthy instructions.

5. **Be explicit** — If you want "above and beyond" behavior, request it directly.

6. **Match output style** — The formatting in your prompt influences the response format.

---

## Model-Specific Adjustments

### For Claude

- Use XML tags (trained on them)
- Enable extended thinking for complex reasoning: `thinking={"type": "enabled", "budget_tokens": N}`
- For parallel tool use: "invoke all relevant tools simultaneously"
- Remove manual CoT prompts when using extended thinking

**Opus 4.5 specific:**
- More responsive to system prompts—dial back aggressive language ("CRITICAL", "MUST", "NEVER") to normal phrasing
- May overtrigger tools—reduce imperative emphasis if seeing excessive tool calls
- When extended thinking disabled: avoid the word "think"; use "consider", "evaluate", or "analyze" instead

### For Gemini

- XML or Markdown equally effective — be consistent
- Keep temperature at 1.0 (default)
- Use `thinking_level: "high"` for complex tasks
- Explicitly request detailed responses if needed (default is concise)

---

## When Delegating to Another Model

```xml
<delegation_context>
I am delegating this subtask to you. Here is what you need to know:

<parent_task>[Original goal]</parent_task>
<your_subtask>[Specific piece you're handling]</your_subtask>
<constraints>[Boundaries for this subtask]</constraints>
<output_requirements>[Exact format needed for integration]</output_requirements>
</delegation_context>

<input_data>
[Data or context needed to complete the subtask]
</input_data>

<task>
[Clear instruction]
</task>
```

---

## When Self-Prompting for Improvement

```xml
<self_improvement_task>
Review and improve this prompt by:

1. Making instructions more specific and unambiguous
2. Adding missing context the model would need
3. Converting negative constraints to positive instructions with explanations
4. Ensuring examples cover edge cases

<original_prompt>
{{PROMPT_TO_IMPROVE}}
</original_prompt>

Return the improved prompt with a brief explanation of each change.
</self_improvement_task>
```

---

## Reasoning Triggers

Use these phrases to activate deeper reasoning:

| Intensity | Claude | Gemini |
|-----------|--------|--------|
| Light | "Think step-by-step" | Default behavior |
| Medium | "Think carefully about this" | `thinking_level: "medium"` |
| Deep | "Think hard" / extended thinking API | `thinking_level: "high"` |

---

## Output Guarantees

### Force JSON (Claude)
Prefill the assistant response:
```python
messages=[
    {"role": "user", "content": "Extract entities..."},
    {"role": "assistant", "content": "{"}
]
```

### Force JSON (Gemini)
```python
config={"response_mime_type": "application/json"}
```

### Force Specific Structure (Both)
Include a complete example of the exact output format in your prompt, then add:
```
Return ONLY a JSON object matching the structure above. No markdown, no explanation.
```

---

## Checklist Before Sending

- [ ] Role/expertise defined?
- [ ] Instructions positive and numbered?
- [ ] Constraints explained (not just stated)?
- [ ] 3–5 diverse examples included?
- [ ] Context placed before task?
- [ ] Output format explicitly specified?
- [ ] Would a human with no context understand this prompt?
