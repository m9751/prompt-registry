---
id: PRM-NBLM-010
title: NotebookLM Usage Patterns — 20 Prompt Templates
domain: product-delivery
source_format: Any (documents, PDFs, research papers, feedback, meeting notes, training materials)
target_orchestrator: NotebookLM
downstream_consumer: Human (copy-paste)
version: 1.0.0
last_updated: 2026-06-24
hosted_url: https://raw.githubusercontent.com/m9751/prompt-registry/main/prompts/product-delivery/PRM-NBLM-010_notebooklm-usage-patterns.md
use_for: Pick the right prompt template for a NotebookLM task across research, content creation, learning, brainstorming, and deep reading
---

## Overview

20 prompt templates organized across 5 use-case categories. Select the category that matches your task, then copy the relevant prompt into NotebookLM against your uploaded sources.

## Prompt

```
=== CATEGORY 1: RESEARCH & INFORMATION SYNTHESIS ===
Use when: Gathering information for a project, market analysis, or client meeting with many documents to review.

[1] "Summarize the main arguments presented in these research papers about {{Topic}}."

[2] "What are the five biggest takeaways from this client brief?"

[3] "Analyze these customer feedback surveys and identify recurring themes and pain points."

[4] "List all the key stakeholders mentioned in these meeting minutes and their primary concerns."

[5] "Create a concise briefing document summarizing all uploaded materials for an executive audience."


=== CATEGORY 2: CONTENT CREATION & COMMUNICATION ===
Use when: Creating a presentation, writing a report, developing training materials, or drafting a message.

[6] "Create an outline for a presentation on {{Topic}}, drawing key points from the uploaded reports."

[7] "Draft a short internal announcement based on the project update provided in {{Document_Name}}."

[8] "Write an FAQ document based on the information in these product specifications."

[9] "Rewrite this section of the report to be more concise and impactful for a non-technical audience."

[10] "Create a short script for a video explaining the core concepts from this training module."


=== CATEGORY 3: LEARNING & ONBOARDING ===
Use when: Learning a new subject, onboarding to a new role, or quickly grasping unfamiliar processes.

[11] "Generate a study guide with key terms and concepts from these onboarding materials."

[12] "Explain {{Complex_Concept}} from this document in simple terms with a real-world example."

[13] "Break down the methodology described in this research paper into digestible steps."

[14] "Based on these project plans, what are the potential questions a new team member might ask?"

[15] "Identify areas in this training material that might be confusing for someone unfamiliar with the topic."


=== CATEGORY 4: BRAINSTORMING & PROBLEM SOLVING ===
Use when: Generating new ideas, exploring different solutions, or analyzing a problem from multiple angles.

[16] "Brainstorm five innovative solutions to {{Problem}} based on the constraints and goals outlined in these documents."

[17] "Suggest new product features that align with the customer feedback provided in these reviews."

[18] "What untapped opportunities are suggested by the market research data?"

[19] "Analyze these incident reports and identify the root causes of recurring issues."

[20-A] "If {{Condition}} occurs, what are the potential implications and recommended actions based on these contingency plans?"


=== CATEGORY 5: DEEP READING & CRITICAL ANALYSIS ===
Use when: Moving beyond basic comprehension to interrogate texts, uncover hidden biases, and pressure-test arguments.

[20-B] The Dialectical Lens: "From this text, construct a debate between two imaginary scholars who interpret this concept/argument in opposing ways. What evidence from the text would each one use to support their view?"

[21] The Disillusionment Filter: "Analyze this idea from the perspective of someone who once believed it but now feels disillusioned. What made them change their mind, and how would they reinterpret the passages they once admired?"

[22] The Anti-Thesis Method: "Take the central thesis or idea in this chapter and explore its opposite. What would the author have to prove if they were defending the reverse argument? Are there any hints in the text that unintentionally support that?"

[23] The Spider Web Perspective: "Map out all the interconnected ideas around this core concept. What other topics, assumptions, or implications does it silently touch upon, challenge, or depend on?"

[24] The Fictional Interview: "Imagine the author is being interviewed by a skeptical journalist. What tough questions would the journalist ask, and how would the author defend themselves using this text as evidence?"

[25] The Unreliable Narrator Exercise: "If the author or narrator of this document were an unreliable narrator, what biases, blind spots, or agendas might they have? Re-read this section assuming that — what hidden contradictions or power plays emerge?"

[26] The Cultural Mirror: "How would this idea look in a completely different cultural, historical, or philosophical context? Rewrite the argument from the viewpoint of a Stoic, a Sufi, or a postmodernist."

[27] The What-If Scenario: "What if this central idea was applied to a real-world issue or modern dilemma? Trace out what would happen — both the intended outcomes and the unintended consequences."

[28] The Future Scholar Perspective: "A hundred years from now, a scholar is analyzing this work. What would they criticize or find outdated? What would they find revolutionary or prescient?"

[29] The Fragmented Mirror: "Break down this idea into emotional, philosophical, psychological, and social dimensions. How does each lens interpret it differently, and where do they clash or overlap?"
```
