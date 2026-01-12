---
name: prd-generator
description: |
  Generates Product Requirements Documents (PRDs) through collaborative dialogue.
  Adapts between lean feature PRDs and comprehensive product PRDs based on scope.
  This skill should be used when users want to create structured product requirements,
  define new features, document product specifications, or prepare product planning
  artifacts for stakeholders and engineering teams.
---

# PRD Generator

Generate production-quality Product Requirements Documents (PRDs) through interactive collaboration. This skill adapts to your needs - creating lean feature PRDs for enhancements or comprehensive product PRDs for new products.

## Before Implementation

Gather context to ensure successful PRD generation:

| Source | Gather |
|--------|--------|
| **Conversation** | User's specific requirements, constraints, and preferences for the PRD |
| **Skill References** | PRD best practices, templates, anti-patterns from `references/` |
| **Codebase** (if applicable) | Existing product context, architecture, conventions |
| **User Guidelines** | Project-specific documentation standards, team conventions |

Only ask user for THEIR specific requirements (domain expertise for PRDs is embedded in this skill).

## What This Skill Does

- Guides you through collaborative PRD creation via targeted questions
- Detects whether you need a feature PRD (lean, 6 sections) or product PRD (comprehensive, 12+ sections)
- Generates structured markdown PRD following industry best practices
- Prevents common PRD anti-patterns (vague requirements, feature bloat, vanity metrics, etc.)
- Outputs markdown file + conversation summary for review

## What This Skill Does NOT Do

- Create PRDs without user input (collaborative, not automated)
- Make product decisions (you decide, skill documents)
- Generate technical specifications (PRD is pre-technical spec)
- Replace product discovery (PRD documents insights, doesn't replace research)

---

## Workflow

### Phase 1: Scope Discovery

**Goal**: Understand what you're building to determine PRD type (feature vs. product).

**Ask 3-5 Core Questions:**

1. **Problem Understanding**
   - "What problem are you trying to solve?"
   - "Who experiences this problem?"

2. **Scope Assessment**
   - "Is this a new feature for an existing product, or a new product entirely?"
   - "How many teams or stakeholders will be involved?"

3. **Impact & Timeline**
   - "What's the desired outcome or impact?"
   - "What's the expected timeline? (weeks, months, quarters)"

4. **Context**
   - "Why now? What makes this important at this time?"

5. **Constraints** (if relevant)
   - "Are there any known constraints? (technical, budget, regulatory)"

**Output**: Gather enough information to determine PRD type in next phase.

---

### Phase 2: PRD Type Detection

**Goal**: Suggest appropriate PRD type and confirm with user.

**Decision Tree:**

```
Scope Analysis:
├─ Is it enhancing existing product?
│  ├─ Yes → Is it a single feature/improvement?
│  │  ├─ Yes → Clear integration point?
│  │  │  ├─ Yes → Suggest FEATURE PRD (Lean)
│  │  │  └─ No → Clarify scope
│  │  └─ No → Multiple features or platform change?
│  │     └─ Yes → Suggest PRODUCT PRD (Comprehensive)
│  └─ No → Is it a new product/major initiative?
│     └─ Yes → Suggest PRODUCT PRD (Comprehensive)
```

**Indicators for Feature PRD (Lean)**:
- Enhancement to existing product
- Clear integration point
- Single team or small cross-functional
- Timeline: Weeks to couple months
- Limited stakeholders

**Indicators for Product PRD (Comprehensive)**:
- New product or major platform initiative
- Market validation needed
- Multiple teams and stakeholders
- Timeline: Months to quarters
- Business strategy alignment required

**Present Recommendation:**

"Based on your answers, this sounds like a [FEATURE/PRODUCT] PRD. Here's why:
- [Reason 1 based on scope]
- [Reason 2 based on timeline/stakeholders]
- [Reason 3 based on complexity]

[FEATURE PRD] will be lean (6 core sections, 2-4 pages) and focus on the problem, users, requirements, and success metrics.

[PRODUCT PRD] will be comprehensive (12+ sections, 5-15 pages) and include market analysis, business strategy, go-to-market, and detailed technical/design requirements.

Does [suggested type] sound right, or should we adjust?"

**Confirm with user before proceeding.**

---

### Phase 3: Interactive Requirements Gathering

**Goal**: Collect information for each PRD section through targeted questions.

**Approach**: Progressive disclosure - ask section-by-section, 2-4 questions per section.

#### For FEATURE PRD (Lean Format)

**Section 1: Problem Statement & Context**

Questions:
- "Describe the problem in 2-3 sentences. What's the user pain point?"
- "Who specifically experiences this problem? (user segment, role)"
- "How do users currently handle this? What workarounds exist?"
- "What evidence do you have? (user research, support tickets, analytics, feedback)"
- "Why is this important now? What's the business/user impact?"

**Section 2: Objectives & Success Metrics**

Questions:
- "If this is successful, what will be different?"
- "How will you measure success? What specific metrics?"
- "What are your targets for each metric? (e.g., 'increase X from Y to Z by date')"
- "How does this connect to business goals? (revenue, retention, efficiency)"

*Red flag check*: If metrics are vague ("improve UX") or vanity metrics ("page views"), probe for specificity.

**Section 3: Target Users**

Questions:
- "Who will use this feature? (role, title, characteristics)"
- "What are they trying to accomplish? (jobs to be done)"
- "How tech-savvy are they? What tools do they use today?"
- "Have you talked to these users? What did they say?"

**Section 4: User Stories & Scenarios**

Questions:
- "Walk me through how a user would use this. What's the main scenario?"
- "What are the 3-5 most important use cases?"
- "How often does each scenario happen? (daily, weekly, monthly)"
- "What does success look like for the user in each scenario?"

**Section 5: Requirements**

Functional Requirements:
- "What must this feature do? (list core capabilities)"
- "Of these, which are must-have (P0), should-have (P1), and nice-to-have (P2)?"
- "What's the minimum for users to get value (MVP)?"

Non-Functional Requirements:
- "How fast must it be? (performance expectations)"
- "Who should have access? Any security/privacy concerns?"
- "How many users/requests/data volume must it support? (scalability)"
- "Any accessibility or compliance requirements?"

**Section 6: Out of Scope**

Questions:
- "What features were considered but you're explicitly NOT including in v1?"
- "Why are they out of scope? (complexity, insufficient demand, etc.)"
- "When might you revisit them? What would trigger reconsidering?"

#### For PRODUCT PRD (Comprehensive Format)

*Includes all Feature PRD sections above, plus:*

**Market Analysis:**
- "What's the market opportunity? (TAM, SAM, SOM if known)"
- "Who are the competitors? What do they offer?"
- "What's your differentiation? Why will users choose you?"
- "What trends make this timely? (market, technology, user behavior)"

**Product Vision:**
- "What's your 3-year vision for this product?"
- "How does this align with company strategy and goals?"
- "What principles will guide product decisions?"

**Personas (Detailed):**
- "Describe your target users in detail (demographics, behaviors, goals, pain points)"
- "Who's the buyer vs. the user? (if B2B)"
- "What's the decision-making process?"

**Go-to-Market:**
- "How will users discover this product? (marketing channels)"
- "What's the pricing strategy? (freemium, subscription, usage-based)"
- "What's the launch plan? (beta, phased rollout, big bang)"
- "What sales/marketing support is needed?"

**Technical Requirements (Detailed):**
- "What's the high-level technical architecture?"
- "What's the technology stack?"
- "What integrations are required?"
- "Any data privacy/compliance requirements? (GDPR, SOC 2, etc.)"

**Timeline & Milestones:**
- "What are the key milestones and dates?"
- "What are the dependencies and critical path?"
- "What are the release criteria for alpha, beta, GA?"

---

### Phase 4: Draft Generation

**Goal**: Create structured markdown PRD document.

**Process:**

1. **Create Directory** (if doesn't exist):
   - `docs/prd/` for PRD files

2. **Generate File Name**:
   - Feature PRD: `docs/prd/<feature-name>-prd.md` (e.g., `analytics-export-prd.md`)
   - Product PRD: `docs/prd/<product-name>-prd.md` (e.g., `taskflow-prd.md`)

3. **Populate Template**:
   - Use appropriate template from `references/prd-structures.md`
   - Fill in all sections with user's answers
   - Use specific, measurable language (reference `references/anti-patterns.md` to avoid common mistakes)
   - Include examples where helpful

4. **Apply Best Practices**:
   - **Problem-first**: Start with problem, not solution
   - **Evidence-based**: Include data, research, user quotes
   - **Specific metrics**: Avoid vague ("better UX") and vanity metrics ("clicks")
   - **Clear scope**: Explicitly state out-of-scope items
   - **Measurable requirements**: Use numbers, timeframes, specific criteria

5. **Format Properly**:
   - Use markdown headers (##, ###)
   - Include bullet lists and tables for readability
   - Add **bold** for emphasis on key points
   - Use code blocks for technical specs if relevant

---

### Phase 5: Review & Refinement

**Goal**: Ensure PRD is accurate, complete, and actionable.

**Show Summary in Conversation:**

Present a concise summary highlighting:
- Problem statement (1-2 sentences)
- Target users
- Key success metrics
- Core requirements (must-haves)
- What's out of scope

**Ask Review Questions:**

1. "Does this accurately capture what we discussed?"
2. "Are there any sections that need more detail or clarification?"
3. "Is anything missing or misunderstood?"
4. "Are the success metrics specific and measurable enough?"
5. "Are the requirements clear enough for engineering to implement?"

**Iterate**:
- If user identifies gaps, ask follow-up questions
- Update PRD sections as needed
- Re-show updated summary
- Repeat until user is satisfied

**Quality Checks** (before finalizing):
- [ ] Problem clearly defined with evidence
- [ ] Success metrics are specific, measurable, and meaningful (not vanity metrics)
- [ ] Target users identified with research backing
- [ ] Requirements are specific (not vague: "fast", "easy", "good")
- [ ] Out of scope section prevents scope creep
- [ ] No major ambiguities or missing information

---

### Phase 6: Output & Next Steps

**Goal**: Deliver final PRD and suggest what comes next.

**Write Final File:**
- Save to `docs/prd/<name>-prd.md`
- Confirm file location in output

**Show Completion Message:**

```markdown
✅ PRD Complete: [Feature/Product Name]

**Saved to**: docs/prd/<filename>.md

**Key Highlights**:
- Problem: [1-sentence problem statement]
- Success: [Primary success metric]
- Users: [Target user segment]
- Timeline: [Expected timeline]

**What's Next**:
1. Share PRD with stakeholders for review and sign-off
2. Schedule kickoff meeting with engineering and design
3. Create design mockups based on requirements
4. Break down requirements into user stories/tasks
5. Set up success metrics tracking

Need any changes to the PRD? Just let me know!
```

---

## Question Frameworks

### When Answers Are Vague

**User says**: "Make it fast"
**You ask**: "What does 'fast' mean in seconds? What's the acceptable response time?"

**User says**: "Improve the user experience"
**You ask**: "Can you describe a specific user problem or pain point? What would 'improved' look like measurably?"

**User says**: "Users want this"
**You ask**: "What evidence supports that? How many users requested it? What did they say?"

### When Answers Are Solution-Focused

**User says**: "Add a blue button in the top-right corner"
**You ask**: "What problem does that solve? What are users trying to accomplish?"

**User says**: "Use technology X"
**You ask**: "What problem are you solving? Are there alternative approaches?"

### When Scope Is Unclear

**User says**: "We need features A, B, C, D, E, F, G for v1"
**You ask**: "If you could only have 3 features, which would they be? What's the minimum users need to get value?"

### When Metrics Seem Wrong

**User says**: "Success is number of clicks"
**You ask**: "Why do clicks matter? What business or user outcome do they represent?"

**User says**: "Increase engagement"
**You ask**: "How specifically? What metric? By how much? By when?"

---

## Common Pitfalls to Avoid

Reference `references/anti-patterns.md` for detailed examples. Watch for:

1. **Vague requirements**: "fast", "easy", "good" → Ask for specifics
2. **Prescribing solutions**: "add X button" → Redirect to problem
3. **Feature bloat**: 20+ must-haves for MVP → Force prioritization
4. **Vanity metrics**: "clicks", "time on page" → Connect to value
5. **No scope boundaries**: Everything in scope → Explicitly list out-of-scope
6. **Missing NFRs**: Only functional requirements → Probe for performance, security, scalability
7. **No evidence**: "I think users want" → Request data/research
8. **Design by committee**: Conflicting stakeholder input → Clarify decision maker

If you notice these patterns, probe deeper with targeted questions.

---

## Reference Files

When generating PRDs, reference these embedded domain expertise files:

| File | Purpose | When to Reference |
|------|---------|-------------------|
| `references/prd-best-practices.md` | Modern PRD philosophy, principles | Always - guides overall approach |
| `references/prd-structures.md` | Feature and Product PRD templates | During draft generation (Phase 4) |
| `references/anti-patterns.md` | Common mistakes to avoid | During gathering (Phase 3) and review (Phase 5) |
| `references/collaboration-guide.md` | Question frameworks | Throughout all phases |
| `references/examples/feature-prd-example.md` | Complete feature PRD example | Reference for feature PRD format/content |
| `references/examples/product-prd-example.md` | Complete product PRD example | Reference for product PRD format/content |

---

## Tips for Success

### For the Skill

1. **Listen more than prescribe**: Your job is to understand and document, not decide
2. **Ask "why" three times**: Surface the real underlying need
3. **Use examples**: "Can you give me a specific example?" makes things concrete
4. **Paraphrase to validate**: "So what I'm hearing is... is that accurate?"
5. **Progressive disclosure**: Don't ask 20 questions upfront; ask section-by-section
6. **Evidence over opinions**: Always ask "What evidence supports that?"

### For the User

1. **Invest time in discovery**: A good PRD requires thinking through the problem deeply
2. **Bring evidence**: Data, user research, feedback - not just opinions
3. **Be specific**: Vague inputs → vague outputs
4. **Prioritize ruthlessly**: Not everything is P0; focus on minimum viable
5. **Define success clearly**: How will you know if this solved the problem?
6. **Update the PRD**: It's a living document, update as you learn

---

## Workflow Checklist

Use this to ensure you've completed all phases:

- [ ] **Phase 1**: Asked 3-5 scope discovery questions
- [ ] **Phase 2**: Suggested PRD type (Feature or Product) and confirmed with user
- [ ] **Phase 3**: Gathered information for all required sections
- [ ] **Phase 4**: Generated complete PRD draft in markdown
- [ ] **Phase 5**: Showed summary, collected feedback, refined
- [ ] **Phase 6**: Wrote final file to `docs/prd/`, confirmed with user
- [ ] **Quality**: No vague language, metrics are specific, scope is clear
- [ ] **Output**: Both file saved and summary shown in conversation

---

## Notes

**This skill is collaborative, not automated.** The quality of the PRD depends on the quality of the conversation. Ask good questions, validate understanding, and iterate until the PRD is clear, complete, and actionable.

**Adapt to context:** If user already has substantial information, don't ask redundant questions. If user provides detailed written specs, incorporate them. Be flexible while ensuring completeness.

**Domain expertise is embedded:** You don't need to research PRD best practices - they're in the references. Focus on understanding the user's specific product/feature needs.
