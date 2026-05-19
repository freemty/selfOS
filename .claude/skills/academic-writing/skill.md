---
name: academic-writing
description: "English prose style rules for academic writing — auto-triggers on paper drafts, grant proposals, research emails. 21 rules from agent-style (Strunk & White / Orwell / Pinker) + 9 LLM-observed anti-patterns. Triggers: writing paper, drafting email, polishing prose, academic writing, 论文英文润色."
user-invocable: true
---

# Academic Writing Style

Auto-apply these rules when writing or polishing English prose for academic contexts: papers, grants, design docs, research emails, README prose.

## Scope

**In scope**: API docs, design docs, research papers, grant proposals, READMEs, runbooks, technical blog posts, postmortems, issue reports, conference rebuttals.

**Out of scope**: Fiction, poetry, marketing copy, casual chat, non-English prose.

## The 12 Canonical Rules

Source: Strunk & White, Orwell ("Politics and the English Language"), Pinker (*The Sense of Style*), Gopen & Swan ("The Science of Scientific Writing"). Redistributed under CC BY 4.0 from [agent-style](https://github.com/yzhao062/agent-style).

### Audience and Reader State

**RULE-01: Do not assume the reader shares your tacit knowledge.**
Define terms on first use. Spell out acronyms. Provide context before detail.

### Voice and Directness

**RULE-02: Do not use passive voice when the agent matters.**
"The model generates tokens" not "Tokens are generated." Passive is fine when the agent is irrelevant or unknown.

### Word Choice

**RULE-03: Do not use abstract or general language when a concrete, specific term exists.**
"latency increased 40ms" not "performance degraded significantly."

**RULE-04: Do not include needless words.**
Cut "it is worth noting that", "it should be mentioned that", "as a matter of fact." Every word must earn its place.

**RULE-05: Do not use dying metaphors or prefabricated phrases.**
Avoid "at the end of the day", "paradigm shift", "leverage synergies", "move the needle."

**RULE-06: Do not use avoidable jargon where an everyday English word exists.**
"use" not "utilize"; "show" not "demonstrate" (unless proving something); "help" not "facilitate."

### Claims and Calibration

**RULE-07: Use affirmative form for affirmative claims.**
"This approach is simple" not "This approach is not complicated."

**RULE-08: Do not linguistically overstate or understate claims relative to evidence.**
Match hedge words to actual confidence. "We observe" (data says so) vs "We believe" (opinion) vs "clearly" (only if truly obvious).

### Sentence Structure

**RULE-09: Express coordinate ideas in similar form (parallel structure).**
"The system reads data, processes tokens, and generates output" not "The system reads data, token processing occurs, and output is generated."

**RULE-10: Keep related words together.**
Move modifiers next to what they modify. Avoid split infinitives that create ambiguity.

**RULE-11: Place new or important information in the stress position (end of sentence).**
The last few words carry emphasis. Put the punchline there.

**RULE-12: Break long sentences; vary length.**
Split sentences over 30 words. Alternate short punchy sentences with longer ones for rhythm.

## The 9 Field-Observed LLM Anti-Patterns

These correct common failure modes of LLM-generated prose:

**RULE-A: Do not convert prose into bullet points unless the content is a genuine list.**
Paragraphs convey argument flow; bullets fragment reasoning.

**RULE-B: Do not use em/en dashes as casual sentence punctuation.**
Use commas, semicolons, or periods. Dashes are for parenthetical asides only.

**RULE-C: Do not start consecutive sentences with the same word or phrase.**
Vary sentence openings. "This method... This approach... This technique..." → restructure.

**RULE-D: Do not overuse transition words ("Additionally", "Furthermore", "Moreover").**
If the logic flows, the transition is unnecessary. Remove and re-read — if it still makes sense, the transition was filler.

**RULE-E: Do not close every paragraph with a summary sentence.**
Trust the reader. One wrap-up sentence per section is enough.

**RULE-F: Use consistent terms; do not redefine abbreviations mid-document.**
Pick one name and stick with it. "VLM" stays "VLM", don't switch to "vision-language model" mid-paragraph.

**RULE-G: Use title case for section and subsection headings.**
"Related Work" not "Related work" or "RELATED WORK."

**RULE-H: Support factual claims with citation or concrete evidence.**
No handwaving. "Prior work shows X [17]" not "It is well-known that X."

**RULE-I: Prefer full forms over contractions in technical prose.**
"does not" not "doesn't"; "cannot" not "can't."

## How to Apply

1. **During drafting**: Keep rules in mind, especially RULE-03 (concrete), RULE-04 (concise), RULE-H (cite).
2. **During revision**: Scan each paragraph for violations. Fix the highest-severity ones first.
3. **Severity order**: RULE-01 (curse of knowledge) and RULE-H (citation) are critical. RULE-04 (needless words) and RULE-08 (overclaiming) are high. Others are medium.

## Escape Hatch

If following a rule makes the prose worse for the specific audience and context, break it — but do so consciously, not by default.

## Attribution

Rules RULE-01..12 distilled from canonical sources. Rules RULE-A..I observed from LLM output patterns 2022-2026. Formatted following [agent-style](https://github.com/yzhao062/agent-style) by Yue Zhao (CC BY 4.0).
