# PRD Anti-Patterns

Common mistakes in Product Requirements Documents and how to avoid them. Each anti-pattern includes examples of what NOT to do, what to do instead, and why it matters.

---

## 1. Vague Requirements

### The Problem

Being too vague with requirements leaves room for misinterpretation and leads to building the wrong thing.

### ❌ Bad Examples

**Vague Performance:**
> "The product should be easy to use."
> "The app must have a fast loading time."
> "The system should be reliable."

**Vague Features:**
> "Users should be able to customize their experience."
> "The dashboard should show relevant metrics."
> "Add social features."

**Vague Success:**
> "Increase user engagement."
> "Improve the user experience."
> "Make customers happy."

### ✅ Good Examples

**Specific Performance:**
> "The dashboard should load in under 2 seconds on a standard broadband connection."
> "API endpoints must respond in < 200ms for p95 of requests."
> "The system should maintain 99.9% uptime during business hours."

**Specific Features:**
> "Users can customize their dashboard by dragging and dropping up to 12 widgets from a library of 20 available visualizations."
> "The dashboard displays 5 key metrics: daily active users, conversion rate, revenue, support tickets, and NPS score."
> "Add ability to @mention teammates in comments and receive in-app notifications."

**Specific Success:**
> "Increase average session duration from 8 minutes to 12 minutes within 30 days of launch."
> "Reduce time-to-first-value from 7 days to 2 days for new users."
> "Achieve NPS score of 40+ among enterprise customers."

### Why It Matters

- **Vague requirements** lead to different interpretations across teams
- **Wastes time** in clarification meetings and rework
- **Results in wrong implementation** that doesn't meet actual needs
- **Makes success measurement impossible**

### How to Fix

1. **Ask "How would we measure this?"** - If you can't measure it, it's too vague
2. **Use specific numbers** - Quantities, percentages, timeframes
3. **Define clear criteria** - What does "done" look like?
4. **Include examples** - Show what you mean, don't just describe

---

## 2. Prescribing Solutions Instead of Defining Problems

### The Problem

Dictating implementation details constrains creativity and prevents discovering better solutions.

### ❌ Bad Examples

**Prescriptive UI:**
> "Add a blue button in the top-right corner that says 'Export'."
> "Use a dropdown menu with 5 options for selecting the report type."
> "The settings page should have 3 tabs with checkboxes for each option."

**Prescriptive Technical:**
> "Use Redis for caching this data."
> "Store user preferences in localStorage."
> "Implement this as a microservice using Kubernetes."

**Prescriptive Workflow:**
> "Users must complete a 7-step onboarding wizard before accessing the product."
> "Send a welcome email exactly 24 hours after signup."

### ✅ Good Examples

**Problem-Focused UI:**
> "Users need a quick way to export their analytics data. The export option should be discoverable within 2 clicks from any chart or dashboard."
> "Users need to select their report type before generating it. Currently, 30% of generated reports are the wrong type, wasting time."
> "Users need to configure notification preferences. Currently we send too many notifications (user feedback) but we're not sure which ones to stop."

**Problem-Focused Technical:**
> "Dashboard load time is 8 seconds due to repeated API calls. We need to reduce this to under 2 seconds."
> "User preferences are lost when they switch devices. We need preferences to sync across sessions and devices."
> "Current monolithic architecture makes deployments risky (all-or-nothing). We need to deploy individual features independently."

**Problem-Focused Workflow:**
> "New users don't understand the product value. 60% churn before completing first core action. We need to get users to their first success faster."
> "Users forget about our product after signing up. Only 20% return within 48 hours. We need to re-engage them while interest is high."

### Why It Matters

- **Stifles creativity** - Engineers and designers can't apply their expertise
- **Misses better solutions** - You might not have the best answer
- **Creates adversarial relationships** - Team feels like order-takers, not problem-solvers
- **Limits adaptability** - Hard to adjust when you discover issues

### How to Fix

1. **Describe the user problem** first, then constraints
2. **State desired outcomes** instead of specific implementations
3. **Ask "What problem are we solving?"** if you catch yourself prescribing solutions
4. **Include "How might we..." questions** to invite creative problem-solving
5. **Separate "requirements" from "possible solutions"**

---

## 3. Feature Bloat

### The Problem

Including too many features dilutes focus, delays launch, and creates a confusing user experience.

### ❌ Bad Examples

**MVP Scope Creep:**
> "For v1, we need:
> - Core analytics dashboard
> - Custom report builder
> - Scheduled email reports
> - Mobile apps (iOS and Android)
> - API access
> - White-label branding
> - Multi-language support (10 languages)
> - Integration with 15 third-party tools
> - AI-powered insights
> - Collaborative annotations"

**Everything for Everyone:**
> "This feature should work for individual users, small teams, enterprises, and agencies. It should support all possible use cases we've heard about."

**Future-Proofing:**
> "Let's add these fields/features now in case we need them later."

### ✅ Good Examples

**Focused MVP:**
> "For v1, core feature set:
> - Analytics dashboard with 5 key metrics
> - Export to CSV and PDF
> - User-based access control
>
> Explicitly deferred to v2:
> - Custom report builder (only 15% of users requested)
> - Mobile apps (desktop is primary use case)
> - API access (evaluate post-launch based on demand)
>
> Out of scope:
> - White-label branding (requires brand management infrastructure)
> - AI insights (insufficient data volume for training)"

**Targeted User Focus:**
> "V1 targets individual users and small teams (5-20 people). Enterprise features (SSO, advanced permissions, audit logs) deferred to v2 based on proven demand."

**Just Enough:**
> "Include only fields required for core workflows. Add additional fields when specific use cases emerge."

### Why It Matters

- **Delays launch** - More features = more time to build and test
- **Increases complexity** - More to learn, more to maintain
- **Dilutes value proposition** - Users can't identify core value
- **Wastes resources** - Building features that won't be used
- **Creates technical debt** - Features added "just in case" still need maintenance

### How to Fix

1. **Ruthlessly prioritize** - What's the minimum for users to get value?
2. **Use MoSCoW** - Must have, Should have, Could have, Won't have
3. **Defer, don't delete** - Acknowledge future possibilities without committing now
4. **Validate demand** - Wait for evidence before building speculative features
5. **Focus on one persona/use case first** - Nail one experience before expanding

---

## 4. Vanity Metrics

### The Problem

Tracking metrics that look good but don't indicate real business value or user success.

### ❌ Bad Examples

**Meaningless Numbers:**
> Success metrics:
> - "Number of clicks on the new feature"
> - "Time spent on page"
> - "Page views"
> - "Number of features used"

**Missing Context:**
> "Increase user signups by 50%"
> (What about activation? Retention? Revenue?)

**Lagging Without Leading:**
> "Increase annual revenue by 20%"
> (What user behaviors drive revenue?)

### ✅ Good Examples

**Value-Connected Metrics:**
> Success metrics:
> - "30% of enterprise users export data within first week (indicates value discovery)"
> - "Average session duration increases from 8 to 12 minutes AND users complete 2+ core actions (indicates engaged, productive usage)"
> - "Reduce time-to-first-export from 5 days to 1 day (faster value realization)"

**Full Funnel:**
> "Acquisition: 1000 signups/month
> Activation: 60% complete first export within 7 days (up from 40%)
> Retention: 70% weekly active users return following week
> Revenue: 15% convert to paid within 30 days
> Key driver: Users who export 3+ times in first week have 2x conversion rate"

**Leading + Lagging:**
> "Leading indicators:
> - Feature adoption: 50% of users try export within 30 days
> - Usage frequency: Active exporters use feature 5+ times/month
>
> Lagging indicators:
> - Revenue: $50k ARR from export-related upsells
> - Retention: 10% reduction in enterprise churn"

### Why It Matters

- **False confidence** - Metrics go up but business doesn't improve
- **Wrong optimizations** - Team focuses on meaningless numbers
- **Masks real problems** - Looks successful while users struggle
- **Misallocates resources** - Investing in features that don't drive value

### How to Fix

1. **Ask "So what?"** - Why does this metric matter to users or business?
2. **Connect to outcomes** - How does this metric relate to user success or revenue?
3. **Include context** - Absolute numbers mean little without comparison or context
4. **Track full funnel** - One metric rarely tells the whole story
5. **Identify leading indicators** - What predicts success before lagging indicators show results?

---

## 5. Design by Committee

### The Problem

Too many voices dilute the vision, creating a Franken-document with conflicting priorities and no clear direction.

### ❌ Bad Examples

**Everyone's Ideas Included:**
> "Marketing wants social sharing, Sales wants enterprise SSO, Engineering wants to rebuild the architecture, Design wants a complete redesign, CEO wants AI features, and Support wants better error messages. Let's include all of these in v1."

**Watered-Down Requirements:**
> Original: "Focus on individual users with simple, fast export"
> After committee: "Support individuals, teams, and enterprises with configurable export workflows, advanced scheduling, white-label options, and API access"

**No Clear Owner:**
> "We'll make decisions as a group. Everyone should have equal input on all requirements."

### ✅ Good Examples

**Input Gathered, PM Decides:**
> "Stakeholder input collected:
> - Marketing: Social sharing (10 requests)
> - Sales: SSO (blocking 3 deals, $150k ARR)
> - Engineering: Architecture debt (slowing team 30%)
> - Design: Navigation improvements (usability test finding)
> - CEO: AI features (market trend)
> - Support: Error messages (15% of tickets)
>
> PM Decision for v1:
> - SSO (P0) - blocking revenue
> - Error messages (P0) - reducing support burden
> - Architecture debt (P1) - enables future velocity
> - Deferred: Social (insufficient demand), AI (premature), navigation (separate initiative)"

**Clear Rationale:**
> "We're focusing on enterprise blockers and support reduction because:
> 1. Three deals ($150k ARR) are blocked on SSO
> 2. Poor error messages drive 15% of support volume
> 3. Architecture debt slows all future development 30%
>
> Marketing and design requests are valid but lower priority based on business impact. We'll revisit in v2 planning."

**Product Owner Authority:**
> "PM owns final PRD. Stakeholders provide input during review cycles. Decisions documented with rationale. Escalate disagreements to VP Product, not by consensus."

### Why It Matters

- **No clear vision** - Trying to please everyone pleases no one
- **Bloated scope** - Every voice adds features
- **Slow decisions** - Consensus-seeking delays progress
- **Mediocre products** - Compromises remove what makes products great
- **Team frustration** - Constantly changing direction based on last conversation

### How to Fix

1. **PM owns PRD** - Gather input, but one person decides
2. **Document tradeoffs** - Explain why you chose X over Y
3. **Prioritize by impact** - Data and evidence, not politics
4. **Set review cycles** - Defined times for input, not ongoing negotiation
5. **Escalation path** - Clear process for resolving disagreements without consensus

---

## 6. Excessively Long PRDs

### The Problem

If you're spending weeks writing a 50-page PRD, you're not doing product discovery.

### ❌ Bad Examples

**Novel-Length Spec:**
> "I spent 4 weeks writing a comprehensive 45-page PRD covering every possible scenario, edge case, and implementation detail."

**Waterfall Thinking:**
> "We need to specify everything up front so engineering knows exactly what to build."

**No Discovery:**
> "The PRD IS the discovery process. Once it's done, we hand it to engineering."

### ✅ Good Examples

**Lean Discovery:**
> "Week 1-2: User research, problem validation
> Week 3: Draft lean PRD (4 pages) capturing key findings
> Week 4: Review with stakeholders, refine
> Engineering kickoff: PRD complete, discovery artifacts available
>
> PRD documents insights, doesn't replace discovery work."

**Right-Sized Documentation:**
> "Feature PRD: 2-4 pages covering problem, users, requirements, success metrics
> Product PRD: 5-10 pages adding market analysis, go-to-market, technical architecture
> Detailed specs: Created collaboratively during design and development"

**Progressive Detail:**
> "Initial PRD (1-2 pages):
> - Problem statement
> - Target users
> - Success metrics
> - Core requirements
>
> Expanded during development:
> - Detailed user scenarios
> - Edge cases
> - Technical decisions
> - Design specifications"

### Why It Matters

- **Wastes PM time** - Writing instead of discovering
- **Delays start** - Engineering waits for complete spec
- **False precision** - You don't know what you don't know yet
- **Waterfall mentality** - Assumes you can specify everything up front
- **Gets outdated** - Long docs become stale before implementation starts

### How to Fix

1. **Target 2-4 pages for features, 5-10 for products** - Longer means too much detail
2. **Document insights, not substitute for discovery** - PRD captures what you learned
3. **Progressive elaboration** - Add detail as you learn, don't guess everything up front
4. **Collaborative specification** - Work with design and engineering to add details during execution
5. **Timebox writing** - If it takes more than a week to write, you're over-specifying

---

## 7. Not Updating PRDs

### The Problem

PRD becomes outdated and useless as the project evolves and you learn more.

### ❌ Bad Examples

**Write and Forget:**
> "PRD was written 3 months ago. We've discovered major issues and changed direction, but the PRD still reflects original plan."

**Historical Artifact:**
> "We don't update the PRD during development. It's just a starting point."

**Tribal Knowledge:**
> "The real requirements are in Slack conversations and meeting notes, not the PRD."

### ✅ Good Examples

**Living Document:**
> "PRD updated throughout development:
> - Added user scenarios discovered during design
> - Updated success metrics based on beta feedback
> - Documented scope changes with rationale
> - Maintained changelog of significant updates"

**Single Source of Truth:**
> "PRD is authoritative. Major decisions documented in PRD with links to design specs, technical docs, and ADRs. Team knows to check PRD for current state."

**Clear Ownership:**
> "PM owns PRD updates. Engineers and designers flag sections needing updates. Monthly review to ensure accuracy."

### Why It Matters

- **Lost knowledge** - Decisions and rationale forgotten
- **Misalignment** - Team members working from different assumptions
- **Onboarding pain** - New team members can't get accurate context
- **Repeated discussions** - Same questions debated multiple times
- **Post-launch confusion** - Can't remember why decisions were made

### How to Fix

1. **Update as you learn** - Don't wait for major milestones
2. **Maintain changelog** - Track what changed and why
3. **Version control** - Keep PRD in Git, commit with clear messages
4. **Assign owner** - Clear responsibility for keeping PRD current
5. **Regular reviews** - Monthly check that PRD reflects reality

---

## 8. No Scope Boundaries

### The Problem

Failing to explicitly define what's out of scope leads to endless scope creep and feature bloat.

### ❌ Bad Examples

**Only In Scope:**
> PRD lists what's included but never says what's excluded.

**Implicit Exclusions:**
> "Obviously we're not building a mobile app, everyone knows that."
> (But do they? And will they remember in 3 months?)

**No Justification:**
> "Out of scope: Feature X, Feature Y, Feature Z"
> (Why? Users will ask. Stakeholders will challenge.)

### ✅ Good Examples

**Explicit Out of Scope:**
> "## Out of Scope
>
> ### Mobile Apps (iOS/Android)
> - Rationale: 95% of usage is desktop, mobile apps require separate team
> - Revisit: If mobile usage grows above 15%
>
> ### API Access
> - Rationale: Only 3 customers requested, insufficient demand for v1
> - Revisit: v2 planning based on launch learnings
>
> ### White-Label Branding
> - Rationale: Requires brand management infrastructure (separate project)
> - Revisit: Q3 after brand system is built"

**Deferred with Reason:**
> "## Deferred to Future Releases
>
> ### Scheduled Exports (v2)
> - Why deferred: Adds complexity, validate manual export usage first
> - Success threshold: 40% of users export weekly or more
>
> ### Custom Report Templates (v3)
> - Why deferred: Requires template builder infrastructure
> - Success threshold: Users request 10+ specific template types"

**Clear Scope Boundaries:**
> "## Scope Boundaries
>
> **In Scope:**
> - Individual users and small teams (< 20 people)
> - Desktop web only
> - CSV and PDF export only
> - English language only
>
> **Out of Scope:**
> - Enterprise features (SSO, SAML, audit logs)
> - Mobile experience
> - Excel, PowerPoint, other formats
> - Internationalization"

### Why It Matters

- **Scope creep** - "Why don't we also..." conversations never end
- **Missed expectations** - Stakeholders surprised features are missing
- **Resource drain** - Small additions accumulate into major delays
- **Loss of focus** - Team distracted by scope discussions

### How to Fix

1. **Explicitly list out of scope items** - Don't rely on what's implied
2. **Explain why** - Rationale prevents repeated challenges
3. **Define revisit conditions** - When might you reconsider?
4. **Update as you go** - Add items to out-of-scope as they come up
5. **Reference in discussions** - "As noted in out-of-scope section..."

---

## 9. Ignoring Non-Functional Requirements

### The Problem

Focusing only on features while ignoring performance, security, scalability, and accessibility.

### ❌ Bad Examples

**Feature-Only Thinking:**
> PRD lists 20 features but never mentions:
> - How fast it needs to be
> - How many users it needs to support
> - What security is required
> - Accessibility requirements

**Vague NFRs:**
> "The system should be fast, secure, and scalable."

**Assumed, Not Specified:**
> "Engineering will obviously make it secure and performant."

### ✅ Good Examples

**Specific NFRs:**
> "## Non-Functional Requirements
>
> **Performance:**
> - Dashboard loads in < 2 seconds on desktop (p95)
> - Export generation completes in < 10 seconds for standard reports
> - API response times < 200ms (p95)
>
> **Security:**
> - Respect existing RBAC (users can only export data they can view)
> - Audit log all export actions (who, what, when)
> - Encrypt exports containing PII
> - Expire download links after 24 hours
>
> **Scalability:**
> - Support 1000 concurrent export requests
> - Handle accounts with 100+ dashboards
> - Export datasets up to 100k rows
>
> **Accessibility:**
> - WCAG 2.1 AA compliance
> - Screen reader support for all features
> - Keyboard navigation for all actions
>
> **Reliability:**
> - 99.9% uptime during business hours
> - Graceful degradation if export service is down
> - Retry failed exports automatically"

**Measurable Criteria:**
> Each NFR has specific, testable criteria that engineering can build to and QA can verify.

### Why It Matters

- **Performance surprises** - Features work but are too slow
- **Security vulnerabilities** - Requirements missed until audit/breach
- **Scalability failures** - Works in testing, fails in production
- **Accessibility lawsuits** - Legal compliance issues
- **Technical debt** - Retrofitting NFRs is much harder than building them in

### How to Fix

1. **Include NFR section in every PRD** - Don't skip it
2. **Be specific and measurable** - Real numbers, not adjectives
3. **Consult specialists** - Security, performance, accessibility experts
4. **Test against NFRs** - Include in acceptance criteria
5. **Consider compliance** - GDPR, SOC 2, WCAG, etc. based on your domain

---

## Quick Reference: Spotting Anti-Patterns

| If you see... | It might indicate... | Fix by... |
|---------------|---------------------|-----------|
| "Easy to use" or "fast" | Vague requirements | Adding specific, measurable criteria |
| "Add a blue button" | Prescribing solutions | Describing the user problem instead |
| 20+ features in MVP | Feature bloat | Ruthless prioritization, deferring to v2+ |
| "Number of clicks" as success metric | Vanity metrics | Connecting to business/user value |
| "Everyone should review" | Design by committee | Clear PM ownership, defined review cycles |
| 30+ page PRD | Excessively long | Shortening to 2-10 pages, progressive detail |
| Unchanged for 3+ months | Not updating | Regular reviews, version control |
| No "Out of Scope" section | No scope boundaries | Explicitly documenting what's excluded |
| No performance/security requirements | Ignoring NFRs | Adding specific non-functional requirements |

## Continuous Improvement

**After each PRD you write, ask:**
1. Was anything misunderstood? (Check for vagueness)
2. Did the solution prevent us from discovering better approaches? (Check for over-prescription)
3. Did scope creep into v1? (Check for feature bloat)
4. Did we track metrics that didn't matter? (Check for vanity metrics)
5. Did conflicting requirements emerge? (Check for design by committee)
6. Did it take too long to write? (Check for excessive length)
7. Did it become outdated? (Check for lack of updates)
8. Did features get added that weren't documented? (Check for scope boundaries)
9. Did we miss performance/security requirements? (Check for NFRs)

Learn from each PRD to improve the next one.
