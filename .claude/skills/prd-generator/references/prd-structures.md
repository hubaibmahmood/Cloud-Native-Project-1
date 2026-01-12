# PRD Template Structures

This document provides detailed templates for both Feature PRDs (lean) and Product PRDs (comprehensive). Choose the appropriate template based on scope and complexity.

## Template Selection Guide

| Indicator | Feature PRD (Lean) | Product PRD (Comprehensive) |
|-----------|-------------------|----------------------------|
| **Scope** | Single feature or enhancement | New product or major initiative |
| **Integration** | Clear integration point in existing product | Standalone or platform-level |
| **Stakeholders** | Limited (1-2 teams) | Multiple teams and external stakeholders |
| **Timeline** | Weeks to few months | Months to quarters |
| **Market Analysis** | Not needed | Required |
| **Go-to-Market** | Leverages existing channels | New strategy needed |
| **Length** | 2-4 pages | 5-15 pages |

---

## Feature PRD Template (Lean)

### Overview

**Purpose**: Document a feature addition or enhancement to an existing product.

**Target Length**: 2-4 pages

**Typical Timeline**: 2-8 weeks development

### Section 1: Problem Statement & Context

**Purpose**: Clearly define the problem being solved and why it matters now.

```markdown
## Problem Statement & Context

### The Problem
[2-3 sentences describing the core problem]

### Who Experiences This Problem
[Description of affected users/segments]

### Current State
[How users currently handle this problem - workarounds, pain points]

### Why Now
[Business or user context that makes this important now]

### Evidence
- [User research findings, data points, feedback]
- [Quantified impact if possible: "affects 40% of active users"]
```

**Example:**
```markdown
## Problem Statement & Context

### The Problem
Users cannot export their analytics data for use in external reporting tools,
forcing them to manually screenshot or copy-paste data.

### Who Experiences This Problem
Enterprise customers (40% of revenue) who need to include our analytics in
board presentations, investor reports, and cross-platform dashboards.

### Current State
Users take screenshots or manually transcribe data into Excel/Google Sheets.
Support receives 15+ tickets per month requesting this capability.

### Why Now
- 3 enterprise deals blocked due to missing export functionality
- Competitors offer CSV/PDF export as standard
- Q3 goal to reduce manual work for power users

### Evidence
- User interviews: 8/10 enterprise customers cited as "must-have"
- Support data: 15-20 tickets/month requesting export
- Sales: Listed as blocker in 3 deals (total value $180k ARR)
```

### Section 2: Objectives & Success Metrics

**Purpose**: Define what success looks like with measurable outcomes.

```markdown
## Objectives & Success Metrics

### Primary Objective
[Single sentence describing the main goal]

### Success Metrics

**Primary Metrics:**
- [Metric 1]: [Target] (e.g., "30% of enterprise users use export within first month")
- [Metric 2]: [Target]

**Secondary Metrics:**
- [Supporting metric 1]
- [Supporting metric 2]

### Target Timeline
[When you expect to see results]

### How We'll Measure
[Tracking mechanism, analytics events, etc.]
```

**Example:**
```markdown
## Objectives & Success Metrics

### Primary Objective
Enable enterprise users to export analytics data in formats suitable for
external reporting and analysis.

### Success Metrics

**Primary Metrics:**
- Feature adoption: 50% of enterprise users use export within 30 days of launch
- Support ticket reduction: 75% decrease in export-related support requests
- Deal conversion: Unblock 2 pending enterprise deals

**Secondary Metrics:**
- Export usage: Average 5+ exports per active user per month
- Format distribution: Understanding preferred export formats (CSV vs PDF vs Excel)
- Net Promoter Score: +10 point increase among enterprise segment

### Target Timeline
Measure 30 days post-launch, with ongoing monthly tracking

### How We'll Measure
- Analytics events: export_initiated, export_completed, export_format_selected
- Support ticket tags and volume
- Sales pipeline tracking
- Quarterly NPS survey with enterprise segment
```

### Section 3: Target Users

**Purpose**: Identify who will use this feature and their needs.

```markdown
## Target Users

### Primary Users
[Description of main user segment]
- Role/persona
- Key characteristics
- Usage patterns

### Secondary Users
[Additional users who may benefit]

### User Needs
**Jobs to Be Done:**
- [What users are trying to accomplish]
- [Context in which they need this]
- [Constraints they face]
```

**Example:**
```markdown
## Target Users

### Primary Users
**Enterprise Analysts & Managers**
- Roles: Data Analysts, Marketing Managers, Product Managers, Executives
- Characteristics: Use our platform daily, create reports for stakeholders
- Usage patterns: Weekly/monthly reporting cycles, board meetings, investor updates

### Secondary Users
**Agency Partners**
- Manage multiple client accounts
- Need to create consolidated reports across clients
- Frequency: Weekly client reporting

### User Needs

**Jobs to Be Done:**
- Create executive presentations with our analytics data
- Include our metrics in cross-platform dashboards (Tableau, Looker)
- Archive historical data for compliance/audit purposes
- Share insights with team members who don't have platform access
- Automate reporting workflows using exported data
```

### Section 4: User Stories & Scenarios

**Purpose**: Describe how users will interact with the feature.

```markdown
## User Stories & Scenarios

### Core User Stories

**As a [user type], I want to [action] so that [benefit].**

1. As an enterprise analyst, I want to export chart data as CSV so that I can
   import it into Excel for further analysis.

2. As a manager, I want to export dashboards as PDF so that I can include them
   in board presentations.

[3-5 core stories covering main use cases]

### Key Scenarios

**Scenario 1: [Name]**
- User context: [What's happening]
- User action: [What they do]
- Expected outcome: [What happens]

[2-3 detailed scenarios for complex flows]
```

**Example:**
```markdown
## User Stories & Scenarios

### Core User Stories

1. As an enterprise analyst, I want to export individual chart data as CSV
   so that I can perform custom analysis in Excel or Google Sheets.

2. As a marketing manager, I want to export my entire dashboard as PDF
   so that I can include it in monthly board presentations.

3. As a product manager, I want to schedule automated exports so that my
   team receives weekly reports without manual work.

4. As an agency partner, I want to export data across multiple client accounts
   so that I can create consolidated reports.

### Key Scenarios

**Scenario 1: Weekly Board Report**
- User context: Manager preparing for Monday board meeting needs latest metrics
- User action: Opens dashboard, clicks "Export" → selects PDF → chooses date range
- Expected outcome: Downloads branded PDF report with all dashboard charts and data tables

**Scenario 2: Ad-hoc Data Analysis**
- User context: Analyst notices unusual trend, wants to investigate in Excel
- User action: Hovers over specific chart → clicks export icon → selects CSV
- Expected outcome: Downloads CSV with chart data, proper column headers, ready for pivot tables

**Scenario 3: Automated Reporting**
- User context: Team lead wants weekly metrics emailed to stakeholders
- User action: Sets up export schedule → chooses format, recipients, frequency
- Expected outcome: System automatically exports and emails report every Monday at 9am
```

### Section 5: Requirements

**Purpose**: Specify what must be built.

```markdown
## Requirements

### Functional Requirements

**Must Have (P0):**
- [Core requirement 1]
- [Core requirement 2]
- [Core requirement 3]

**Should Have (P1):**
- [Important but not blocking]

**Nice to Have (P2):**
- [Future enhancement]

### Non-Functional Requirements

**Performance:**
- [Load time, response time requirements]

**Security:**
- [Access control, data privacy requirements]

**Usability:**
- [Accessibility, ease of use requirements]

**Scalability:**
- [Volume, growth expectations]

### Technical Constraints
- [Platform limitations, integration requirements]

### Dependencies
- [Other features, teams, systems this depends on]
```

**Example:**
```markdown
## Requirements

### Functional Requirements

**Must Have (P0):**
- Export individual charts as CSV with proper headers and formatting
- Export entire dashboard as PDF preserving layout and branding
- Support date range selection for exports
- Limit export file size to prevent performance issues (max 100k rows CSV, 50 pages PDF)
- Include export button on each chart and dashboard-level export option
- Show export progress indicator for large datasets
- Email export file or provide download link

**Should Have (P1):**
- Export as Excel (.xlsx) format with multiple sheets
- Schedule recurring exports (daily, weekly, monthly)
- Export multiple dashboards at once
- Custom branding options (logo, colors) for PDF exports

**Nice to Have (P2):**
- API endpoint for programmatic exports
- Export templates (predefined report layouts)
- Direct integration with Google Sheets/Excel Online

### Non-Functional Requirements

**Performance:**
- Generate CSV export in < 5 seconds for datasets up to 10k rows
- Generate PDF export in < 10 seconds for dashboards up to 10 charts
- Export process should not block user from other actions

**Security:**
- Respect existing role-based access controls (users can only export data they can view)
- Audit log all export actions (who, what, when)
- Expire download links after 24 hours
- Encrypt exports containing sensitive data

**Usability:**
- Export option discoverable within 2 clicks
- Clear feedback on export format options and file size
- Graceful error messages if export fails
- Mobile-responsive export configuration

**Scalability:**
- Support 1000+ concurrent export requests
- Handle enterprise accounts with 100+ dashboards

### Technical Constraints
- Must work with existing chart rendering library (Chart.js)
- PDF generation using existing backend service
- File storage in AWS S3 with 7-day retention

### Dependencies
- Backend team: API endpoints for export generation
- Design team: Export UI and PDF template design
- Infrastructure: S3 bucket configuration and CDN setup
```

### Section 6: Out of Scope

**Purpose**: Explicitly state what is NOT included to prevent scope creep.

```markdown
## Out of Scope

### Explicitly Not Included in This Release

- [Feature or capability deferred]
- [Related but separate initiative]
- [Future enhancement]

### Why Not Included
[Brief rationale for each major exclusion]

### Future Considerations
[Items to potentially revisit in future iterations]
```

**Example:**
```markdown
## Out of Scope

### Explicitly Not Included in This Release

- **PowerPoint export format**: Not in v1, may consider based on demand
- **Direct Salesforce/HubSpot integration**: Requires separate integration project
- **Automated data warehousing**: Different use case, separate initiative
- **White-label PDF reports**: Requires branding infrastructure not yet available
- **Real-time export streaming**: Technical complexity not justified for v1
- **Export of raw event data**: Security/privacy review needed first

### Why Not Included

**PowerPoint export**: User research showed 90% prefer PDF, PowerPoint adds complexity
**Salesforce integration**: Only 15% of users requested, separate partnership discussion needed
**White-label reports**: Requires brand management system (Q3 roadmap item)

### Future Considerations

- **v2**: Scheduled exports, Excel format, white-label PDFs
- **v3**: API access, custom export templates
- Monitor usage data to prioritize v2 features based on actual demand
```

---

## Product PRD Template (Comprehensive)

### Overview

**Purpose**: Document a new product, major initiative, or platform-level capability.

**Target Length**: 5-15 pages

**Typical Timeline**: 3-12 months development

### Section 1: Executive Summary

**Purpose**: 1-page overview for stakeholders who won't read full document.

```markdown
## Executive Summary

### Product Name
[Official product name]

### One-Line Description
[What it is in one sentence]

### The Opportunity
[2-3 sentences on market opportunity]

### Target Market
[Who will use this]

### Core Value Proposition
[Why they'll use it - key benefits]

### Success Metrics
[Top 2-3 metrics that define success]

### Investment Required
[High-level resource/budget estimate]

### Expected Return
[Business impact - revenue, cost savings, strategic value]

### Timeline
[High-level milestones]
```

### Section 2: Problem Statement & Market Context

```markdown
## Problem Statement & Market Context

### The Problem
[Detailed problem description - 1-2 paragraphs]

### Market Size & Opportunity
- Total Addressable Market (TAM)
- Serviceable Addressable Market (SAM)
- Serviceable Obtainable Market (SOM)
- Growth trends

### Current Alternatives
[How people solve this problem today]

**Alternative 1:**
- Description
- Pros
- Cons
- Market share/adoption

### Why Existing Solutions Fall Short
[Gap analysis - why there's room for new solution]

### Evidence
- Market research
- User interviews
- Competitive analysis
- Data/trends
```

### Section 3: Product Vision & Objectives

```markdown
## Product Vision & Objectives

### Vision Statement
[Inspirational 2-3 sentence vision of what this product will become]

### Product Mission
[Concrete mission for this version/phase]

### Strategic Alignment
[How this supports company strategy and goals]

### Product Objectives

**Year 1 Objectives:**
1. [Objective 1]
2. [Objective 2]
3. [Objective 3]

**Long-term Vision (3 years):**
[Where we see this product in 3 years]

### Product Principles
[3-5 guiding principles for product decisions]
```

### Section 4: Target Market & Personas

```markdown
## Target Market & Personas

### Market Segmentation

**Primary Target Market:**
- Industry/vertical
- Company size
- Geography
- Characteristics

**Secondary Markets:**
[Additional segments to address later]

### User Personas

**Persona 1: [Name/Title]**

**Demographics:**
- Role
- Company type
- Experience level

**Goals:**
- Primary goal 1
- Primary goal 2

**Pain Points:**
- Pain point 1
- Pain point 2

**Behaviors:**
- How they work today
- Tools they use
- Decision-making process

**Success Criteria:**
- What they need to achieve
- How they measure success

[2-4 detailed personas]

### Buyer Personas (if B2B)
[Economic buyer, technical buyer, influencers]
```

### Section 5: Success Metrics & KPIs

```markdown
## Success Metrics & KPIs

### North Star Metric
[Single metric that best represents value delivered]

### Product-Market Fit Metrics

**Leading Indicators:**
- [Early signals of product-market fit]

**Lagging Indicators:**
- [Longer-term validation metrics]

### Business Metrics

**Revenue Metrics:**
- [ARR, MRR, etc.]
- Target: [Specific number by specific date]

**Growth Metrics:**
- User acquisition
- Activation rate
- Retention rate
- Targets for each

**Efficiency Metrics:**
- CAC (Customer Acquisition Cost)
- LTV (Lifetime Value)
- LTV:CAC ratio target

### Product Metrics

**Engagement:**
- DAU/MAU
- Feature adoption
- Usage frequency

**Quality:**
- NPS
- Customer satisfaction
- Support ticket volume

**Performance:**
- Load times
- Error rates
- Uptime

### Success Criteria by Phase

**Alpha (Internal):**
- [Metrics and targets]

**Beta (Limited):**
- [Metrics and targets]

**GA (General Availability):**
- [Metrics and targets]

**6 Months Post-Launch:**
- [Metrics and targets]
```

### Section 6: User Scenarios & User Flows

```markdown
## User Scenarios & User Flows

### Primary Use Cases

**Use Case 1: [Name]**

**Actors:** [Who's involved]

**Trigger:** [What initiates this scenario]

**Scenario:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Outcome:** [What success looks like]

**Frequency:** [How often this happens]

[3-5 primary use cases]

### User Journey Maps
[Key moments in user experience from discovery to success]

### Edge Cases & Error Scenarios
[Important edge cases to handle]
```

### Section 7: Feature Requirements

```markdown
## Feature Requirements

### MVP (Minimum Viable Product)

**Core Features:**

**Feature 1: [Name]**
- Description
- User value
- Acceptance criteria
- Priority: P0

[List all MVP features]

### Post-MVP Roadmap

**Phase 2 (3-6 months post-launch):**
- [Feature/enhancement]
- [Feature/enhancement]

**Phase 3 (6-12 months):**
- [Feature/enhancement]

### Feature Prioritization

**Framework:** [MoSCoW, RICE, etc.]

| Feature | Must Have | Should Have | Could Have | Won't Have |
|---------|-----------|-------------|------------|------------|
| [Feature 1] | ✓ | | | |
```

### Section 8: Technical Requirements

```markdown
## Technical Requirements

### Architecture Overview
[High-level technical architecture]

### Technology Stack
- Frontend: [Technologies]
- Backend: [Technologies]
- Database: [Technologies]
- Infrastructure: [Technologies]

### Integration Requirements
- [System 1]: [What needs to integrate]
- [System 2]: [Integration needs]

### API Requirements
[If providing APIs - endpoints, auth, rate limits]

### Data Requirements

**Data Model:**
[Key entities and relationships]

**Data Volume:**
- Expected data volume
- Growth projections

**Data Privacy & Compliance:**
- GDPR requirements
- SOC 2 compliance
- Data residency
- PII handling

### Performance Requirements

- Response time: [Target]
- Throughput: [Target]
- Concurrent users: [Target]
- Uptime SLA: [Target]

### Security Requirements

- Authentication method
- Authorization model
- Data encryption (at rest, in transit)
- Audit logging
- Vulnerability management

### Scalability Requirements
[Growth expectations and scaling strategy]
```

### Section 9: Design Requirements

```markdown
## Design Requirements

### Design Principles
[3-5 principles guiding design decisions]

### User Experience Requirements

**Accessibility:**
- WCAG 2.1 AA compliance
- Screen reader support
- Keyboard navigation

**Responsiveness:**
- Desktop (required)
- Tablet (required/nice-to-have)
- Mobile (required/nice-to-have)

**Localization:**
- Languages supported
- RTL support
- Timezone handling
- Currency handling

### Brand Guidelines
[Consistency with existing brand or new brand requirements]

### Design Deliverables
- Wireframes
- High-fidelity mockups
- Prototype
- Design system components
```

### Section 10: Go-to-Market Considerations

```markdown
## Go-to-Market Considerations

### Launch Strategy

**Launch Type:** [Soft launch, public beta, big bang, phased rollout]

**Launch Phases:**
1. Alpha (Internal): [Date, audience]
2. Beta (Limited): [Date, audience, selection criteria]
3. GA (General Availability): [Date, audience]

### Pricing Strategy

**Pricing Model:** [Free, freemium, subscription, usage-based, one-time]

**Price Points:**
- [Tier 1]: [Price] - [Features]
- [Tier 2]: [Price] - [Features]

**Rationale:** [Why this pricing structure]

### Marketing & Positioning

**Positioning Statement:**
[How we'll position in market]

**Key Messages:**
- [Message 1]
- [Message 2]

**Marketing Channels:**
- [Channel 1]: [Strategy]
- [Channel 2]: [Strategy]

### Sales Enablement
- Sales training needed
- Demo environment
- Sales collateral
- Competitive battle cards

### Customer Success
- Onboarding plan
- Documentation requirements
- Training materials
- Support staffing
```

### Section 11: Constraints & Assumptions

```markdown
## Constraints & Assumptions

### Constraints

**Technical Constraints:**
- [Limitation 1]
- [Limitation 2]

**Resource Constraints:**
- Team size
- Budget
- Timeline

**Business Constraints:**
- [Regulatory requirements]
- [Partnership dependencies]
- [Market timing]

### Assumptions

**Market Assumptions:**
- [Assumption about market/users]
- Validation plan: [How we'll test this]

**Technical Assumptions:**
- [Assumption about technology]
- Validation plan: [How we'll validate]

**Business Assumptions:**
- [Assumption about business model]
- Validation plan: [How we'll prove this]

### Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Strategy] |
```

### Section 12: Out of Scope

```markdown
## Out of Scope

### Not in MVP

**Feature:** [Name]
**Rationale:** [Why deferred]
**Future Plan:** [When/if we'll revisit]

### Explicitly Excluded

**Feature:** [Name]
**Rationale:** [Why we won't build this]

### Adjacent Opportunities
[Related opportunities we're aware of but not pursuing now]
```

### Section 13: Timeline & Milestones

```markdown
## Timeline & Milestones

### Key Milestones

| Milestone | Date | Owner | Deliverable |
|-----------|------|-------|-------------|
| Kickoff | [Date] | [Owner] | PRD approved |
| Design Complete | [Date] | [Owner] | Designs signed off |
| Alpha Release | [Date] | [Owner] | Internal testing |
| Beta Release | [Date] | [Owner] | Limited external |
| GA Release | [Date] | [Owner] | Public launch |
| Post-Launch Review | [Date] | [Owner] | Metrics review |

### Dependencies & Critical Path
[Timeline dependencies and what's on critical path]

### Release Criteria

**Alpha Release Criteria:**
- [Criterion 1]

**Beta Release Criteria:**
- [Criterion 1]

**GA Release Criteria:**
- [Criterion 1]
```

---

## Usage Guidelines

### When to Use Feature PRD

- Adding capability to existing product
- Enhancement to current feature
- Integration or improvement
- Timeline: Weeks to couple months
- Team: Single squad or small cross-functional team

### When to Use Product PRD

- Net new product
- Major platform initiative
- Significant market entry
- Timeline: Quarters to year
- Team: Multiple squads, stakeholders across company

### Customization

Both templates are starting points. Adapt sections based on:
- Company culture and processes
- Product complexity
- Stakeholder needs
- Stage of company (startup vs enterprise)
- Regulatory requirements

### Progressive Detail

Start lean, add detail as you validate:
1. Draft with key sections completed
2. Review with stakeholders, identify gaps
3. Add detail where needed
4. Refine iteratively as you learn more

Not every section needs same depth. Focus detail where uncertainty is highest and decisions are most consequential.
