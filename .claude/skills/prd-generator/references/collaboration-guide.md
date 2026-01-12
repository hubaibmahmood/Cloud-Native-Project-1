# PRD Collaboration Guide

How to gather requirements interactively and collaboratively to create effective Product Requirements Documents.

---

## Core Collaboration Principles

### 1. Ask, Don't Assume

Never assume you understand the user's problem or requirements. Always ask targeted questions to validate your understanding.

**Bad:** "I'll document the feature for exporting data."
**Good:** "Tell me about the problem users are experiencing. What are they trying to accomplish?"

### 2. Progressive Disclosure

Start broad, then drill into specifics. Don't overwhelm with 20 questions upfront.

**Approach:**
1. Core questions (3-5) to understand scope
2. Section-specific questions (2-4 per section)
3. Clarifying questions as gaps emerge
4. Refinement questions during review

### 3. Evidence-Based Requirements

Always ask for evidence backing requirements: data, research, user quotes, business impact.

**Bad:** "What features should we build?"
**Good:** "What evidence shows users need this? What data, research, or feedback do you have?"

### 4. Problem Before Solution

Help users articulate problems before jumping to solutions.

**When user says:** "We need a blue export button in the corner"
**You ask:** "What problem are users experiencing that led to this requirement?"

---

## Question Frameworks by PRD Section

### Scope Discovery (Initial Questions)

Purpose: Understand if this is a feature PRD (lean) or product PRD (comprehensive).

**Core Questions:**

1. **Problem Understanding**
   - "What problem are you trying to solve?"
   - "Who experiences this problem?"
   - "How do they handle it today?"

2. **Scope Sizing**
   - "Is this a new feature for an existing product, or a new product?"
   - "How many teams or stakeholders will be involved?"
   - "What's the expected timeline?"

3. **Impact Assessment**
   - "What's the desired outcome or impact?"
   - "How will you measure success?"
   - "What happens if we don't build this?"

4. **Context**
   - "Why now? What makes this important at this time?"
   - "Are there any constraints we should know about?"

**Analysis:**
- If answers indicate enhancement, single team, weeks timeframe → Feature PRD
- If answers indicate new product, multiple teams, months timeframe → Product PRD

### Problem Statement & Context

Purpose: Clearly define the problem being solved.

**Questions:**

1. **The Core Problem**
   - "Describe the problem in 2-3 sentences."
   - "What's the underlying user need or pain point?"

2. **Who's Affected**
   - "Which users or user segments experience this problem?"
   - "What percentage of your users are affected?"

3. **Current State**
   - "How do users currently handle this problem?"
   - "What workarounds exist? What breaks down?"

4. **Evidence**
   - "What data or research validates this problem?"
   - "Do you have user quotes, support tickets, or analytics?"
   - "How often does this problem occur?"

5. **Impact**
   - "What's the cost of this problem? (time, money, satisfaction)"
   - "How does it affect your business?"

**Follow-up if answers are vague:**
- "Can you give me a specific example?"
- "Walk me through a recent instance of this problem."

### Objectives & Success Metrics

Purpose: Define measurable outcomes that indicate success.

**Questions:**

1. **Primary Objective**
   - "If this is successful, what will be different?"
   - "What's the single most important outcome?"

2. **Measurability**
   - "How will you know if this solved the problem?"
   - "What metrics will you track?"
   - "What's your target for each metric? By when?"

3. **Business Impact**
   - "How does this objective connect to business goals?"
   - "Is this about revenue, retention, efficiency, or something else?"

4. **Validation**
   - "What are the leading indicators that predict success?"
   - "What are the lagging indicators that confirm it?"

**Red flags to probe:**
- Vague metrics ("increase engagement") → Ask: "How specifically? What number?"
- Vanity metrics ("page views") → Ask: "Why does that matter? What does it enable?"
- Missing baseline → Ask: "What's the current metric? Where are we starting?"

### Target Users & Personas

Purpose: Identify who will use this and understand their needs.

**Questions:**

1. **Primary Users**
   - "Who will use this feature/product?"
   - "What's their role? Title? Responsibilities?"
   - "Where do they fit in the organization?"

2. **User Characteristics**
   - "How tech-savvy are they?"
   - "What tools do they use today?"
   - "What's their workflow context?"

3. **Segmentation**
   - "Are there different user types with different needs?"
   - "Which segment is most important? Why?"

4. **Jobs to Be Done**
   - "What are they trying to accomplish?"
   - "In what context do they need this?"
   - "What constraints do they face?"

5. **Validation**
   - "Have you talked to these users directly?"
   - "What did they say they need?"
   - "How many users fit this profile?"

**For Product PRDs, add:**
- **Buyer vs. User:** "Who makes the purchase decision? Is it the same person who uses it?"
- **Decision Process:** "What's the buying process? Who's involved?"

### User Stories & Scenarios

Purpose: Describe how users will interact with the feature/product.

**Questions:**

1. **Core Use Cases**
   - "Walk me through how a user would use this."
   - "What are the 3-5 most important scenarios?"

2. **Scenario Context**
   - "What triggers this scenario?"
   - "What's the user trying to accomplish?"
   - "What happens before and after?"

3. **Frequency**
   - "How often does this scenario happen?"
   - "Is this daily, weekly, monthly, or occasional?"

4. **Success Criteria**
   - "What does success look like for the user in this scenario?"
   - "How quickly do they need to accomplish this?"

5. **Edge Cases**
   - "What happens if things go wrong?"
   - "What are the unusual scenarios we should handle?"

**Technique: "Show me, don't tell me"**
- "Can you screen-share and show me how you'd use this?"
- "Walk me through your current process step-by-step."

### Requirements (Functional & Non-Functional)

Purpose: Specify what must be built.

**Functional Requirements Questions:**

1. **Core Capabilities**
   - "What must this feature/product do? (verb + noun)"
   - "What are the non-negotiable requirements?"

2. **Prioritization**
   - "Of these requirements, which are must-have vs. nice-to-have?"
   - "What's the minimum for users to get value?"

3. **Constraints**
   - "Are there technical limitations we should know about?"
   - "What can't we do?"

**Non-Functional Requirements Questions:**

1. **Performance**
   - "How fast does this need to be?"
   - "What's acceptable response time?"
   - "What volume of data/users/requests?"

2. **Security & Privacy**
   - "What data are we handling? Is any of it sensitive?"
   - "Who should have access? Who shouldn't?"
   - "Any compliance requirements? (GDPR, SOC 2, HIPAA, etc.)"

3. **Scalability**
   - "How many users at launch? In 6 months? In 1 year?"
   - "What's the expected growth?"

4. **Accessibility**
   - "Do we need screen reader support?"
   - "Any accessibility standards to meet?"

5. **Reliability**
   - "What uptime do users expect?"
   - "What happens if this goes down?"

**Technique: Specific over vague**
- If you hear "fast" → Ask: "What does 'fast' mean in seconds?"
- If you hear "secure" → Ask: "What specific security measures?"

### Constraints & Assumptions

Purpose: Document what's fixed and what we're assuming.

**Questions:**

1. **Technical Constraints**
   - "Are we limited to certain technologies?"
   - "Any integrations that must work?"
   - "What's the existing technical architecture?"

2. **Resource Constraints**
   - "What's the team size?"
   - "What's the budget?"
   - "What's the deadline?"

3. **Business Constraints**
   - "Any regulatory or compliance requirements?"
   - "Partnership dependencies?"
   - "Market timing considerations?"

4. **Assumptions**
   - "What are we assuming about users?"
   - "What are we assuming about the market?"
   - "What are we assuming technically?"
   - For each: "How can we validate this assumption?"

### Out of Scope

Purpose: Explicitly define what won't be included.

**Questions:**

1. **Deferred Features**
   - "What features were considered but deferred?"
   - "Why were they deferred?"
   - "When might you revisit them?"

2. **Excluded Segments**
   - "Are there user segments we're explicitly not targeting?"
   - "Why not?"

3. **Future Considerations**
   - "What might be in v2 or v3?"
   - "What would trigger building those features?"

**Technique: Make it explicit**
- "Let's list everything we're NOT doing to prevent scope creep."
- "What requests should we politely decline?"

### For Product PRDs: Additional Questions

**Market Analysis:**
- "What's the market size?"
- "Who are the competitors?"
- "What's our differentiation?"
- "What's the market opportunity?"

**Go-to-Market:**
- "How will users discover this?"
- "What's the pricing strategy?"
- "What's the launch plan?"
- "What sales/marketing support is needed?"

**Product Vision:**
- "Where do you see this in 3 years?"
- "What's the long-term vision?"

---

## Handling Common Challenges

### Challenge: Vague or Incomplete Answers

**Symptoms:**
- "Make it better"
- "Users want this"
- "It should be fast"

**Response:**
1. **Ask for specifics:** "Can you give me a specific example?"
2. **Ask for evidence:** "What data supports that?"
3. **Ask for measurement:** "How would we measure 'better'?"

**Example:**
```
User: "We need to improve the user experience."
You: "Can you describe a specific user problem or pain point you're trying to solve?
      What user feedback or data led to this?"
```

### Challenge: Solution-Focused Instead of Problem-Focused

**Symptoms:**
- "Add a dropdown menu here"
- "Use technology X"
- "Make it look like competitor Y"

**Response:**
1. **Redirect to problem:** "What problem does that solve?"
2. **Explore alternatives:** "Are there other ways to solve that problem?"
3. **Understand constraints:** "What makes that the right solution?"

**Example:**
```
User: "We need to add a blue export button in the top-right corner."
You: "I want to understand the underlying problem first. What are users trying
      to accomplish? How are they currently trying to export data and where
      does that break down?"
```

### Challenge: Too Many Requirements

**Symptoms:**
- 30+ must-have features for MVP
- Everything is high priority
- No clear focus

**Response:**
1. **Force prioritization:** "If you could only have 3 features, which would they be?"
2. **Explore dependencies:** "Which features unlock the others?"
3. **Test viability:** "What's the minimum users need to get value?"
4. **Reference data:** "Which features do users request most?"

**Example:**
```
User: "We need all these 25 features in v1."
You: "Let's validate that. What's the absolute minimum feature set that
      would solve the core user problem? What could we defer to v2 once
      we validate demand?"
```

### Challenge: No Evidence or Data

**Symptoms:**
- "I think users want..."
- "Everyone says..."
- "Obviously this is needed"

**Response:**
1. **Request evidence:** "What research validates this?"
2. **Suggest validation:** "How can we test this assumption?"
3. **Qualify claims:** "How many users said this? In what context?"

**Example:**
```
User: "Users definitely want AI-powered insights."
You: "That's interesting. What user research or feedback led to that conclusion?
      How many users requested it? What problem would AI insights solve for them?"
```

### Challenge: Conflicting Stakeholder Input

**Symptoms:**
- Different stakeholders have different priorities
- Competing requirements
- No clear decision maker

**Response:**
1. **Identify owner:** "Who makes the final call on requirements?"
2. **Document tradeoffs:** "Let's capture both perspectives and the reasoning."
3. **Escalation path:** "How should we resolve this disagreement?"

**Example:**
```
Marketing wants feature A, Engineering wants to rebuild the architecture, CEO wants feature B.
You: "I'm hearing different priorities. Who owns the final prioritization decision?
      Let's document the business case for each and bring them together for alignment."
```

---

## Iterative Refinement

### Initial Draft Review

After creating the first PRD draft:

**Questions:**
1. "Does this accurately capture what we discussed?"
2. "What's missing or unclear?"
3. "Are there any sections that need more detail?"
4. "Did I misunderstand anything?"

### Section-by-Section Review

For each major section:

**Questions:**
1. "Is the problem statement clear and accurate?"
2. "Are the success metrics measurable and meaningful?"
3. "Are the requirements specific enough to implement?"
4. "Is anything ambiguous?"

### Final Review Checklist

Walk through with stakeholder:

- [ ] Problem clearly defined with evidence
- [ ] Success metrics specific and measurable
- [ ] Target users and scenarios validated
- [ ] Requirements prioritized and complete
- [ ] Out of scope explicitly documented
- [ ] No vague language ("fast", "easy", "good")
- [ ] Technical and business constraints documented

---

## Tips for Effective Collaboration

### 1. Listen More Than You Talk

Your job is to understand and document, not to prescribe solutions.

**Ratio:** 80% listening/asking, 20% summarizing/validating

### 2. Paraphrase to Validate

After hearing an answer:
- "So what I'm hearing is... [paraphrase]. Is that accurate?"
- "Let me make sure I understand... [summarize]"

### 3. Ask "Why?" Three Times

Surface the real underlying need:
1. "We need feature X" → "Why?"
2. "Because users can't do Y" → "Why does that matter?"
3. "Because it prevents them from Z" → *Now we understand the core problem*

### 4. Use Examples

Abstract discussions get fuzzy. Examples make things concrete.
- "Can you give me a specific example?"
- "Walk me through a real scenario."
- "Show me how you'd use this."

### 5. Visualize Understanding

Draw diagrams, sketch flows, or create quick mockups to validate understanding.
- "Let me sketch what I'm hearing..."
- "Is this the flow you're describing?"

### 6. Document as You Go

Don't wait until the end to write the PRD. Draft sections during or immediately after conversations while context is fresh.

### 7. Set Clear Next Steps

End each collaboration session with:
- What you'll draft/update
- What questions remain open
- When you'll review together again

---

## Stakeholder Identification

### Who to Involve

**Essential Stakeholders:**
- Product Manager (PRD owner)
- User representatives (the people who will actually use this)
- Engineering lead (technical feasibility)

**Important Stakeholders:**
- Design lead (user experience)
- Key business stakeholders (executives, sales, marketing as relevant)

**Optional/Review-Only:**
- Adjacent teams
- Legal/compliance (if relevant)
- Support/ops teams

### When to Involve Them

**Discovery Phase:**
- PM + User representatives + Engineering lead
- Goal: Understand problem, validate feasibility

**Draft Review:**
- Add Design, key business stakeholders
- Goal: Validate approach, align on solution

**Final Review:**
- All stakeholders
- Goal: Final sign-off, identify any blockers

**During Development:**
- Core team (PM, Eng, Design)
- Goal: Clarify details, handle discovered issues

### How to Manage Input

1. **Collect input systematically** - Scheduled reviews, not ad-hoc
2. **PM synthesizes and decides** - One person accountable for PRD
3. **Document disagreements** - Capture rationale for choices
4. **Clear escalation path** - Process for resolving conflicts

---

## Remote Collaboration Tips

### Async Collaboration

**Good for:**
- Initial question gathering
- Draft reviews
- Collecting stakeholder feedback

**Best practices:**
- Use written questions in docs/forms
- Set clear deadlines for responses
- Summarize and share back

### Sync Collaboration

**Good for:**
- Complex problem exploration
- Resolving ambiguities
- Stakeholder alignment
- Whiteboarding/ideation

**Best practices:**
- Prepare questions in advance
- Share screen/collaborate in real-time doc
- Record session (with permission)
- Send summary after

### Hybrid Approach

1. Async: Send pre-read with initial questions
2. Sync: 30-60 min working session
3. Async: Draft PRD sections based on session
4. Sync: Review and refine draft
5. Async: Final stakeholder review

---

## Summary: The Collaborative PRD Process

```
1. Initial Conversation (Sync)
   ├─ Ask 3-5 scope discovery questions
   ├─ Determine PRD type (feature vs. product)
   └─ Schedule working sessions

2. Problem Deep Dive (Sync or Async)
   ├─ Problem statement questions
   ├─ Evidence and validation
   └─ Document findings

3. Requirements Gathering (Series of Sync Sessions)
   ├─ Section-by-section questions
   ├─ Progressive detail gathering
   └─ Draft sections as you go

4. Draft Review (Async → Sync)
   ├─ Share draft for async review
   ├─ Collect feedback
   ├─ Sync session to resolve questions
   └─ Refine draft

5. Stakeholder Alignment (Sync)
   ├─ Present PRD to stakeholders
   ├─ Address concerns
   ├─ Get sign-off
   └─ Document any deferred items

6. Living Document (Ongoing)
   ├─ Update as you learn
   ├─ Maintain changelog
   └─ Keep stakeholders informed
```

The best PRDs emerge from collaboration, not isolation. Ask questions, listen carefully, validate understanding, and iterate.
