Create comprehensive technical design for a specification.

<meta>
argument-hint: <feature-name> [-y]
</meta>

# Technical Design Generator

<background_information>
- **Mission**: Generate comprehensive technical design document that translates requirements (WHAT) into architectural design (HOW)
- **Success Criteria**:
  - All requirements mapped to technical components with clear interfaces
  - Appropriate architecture discovery and research completed
  - Design aligns with steering context and existing patterns
  - Visual diagrams included for complex architectures
</background_information>

<instructions>
## Core Task
Generate technical design document for the feature based on approved requirements.

Parse arguments from: $ARGUMENTS
- First token = feature name
- Second token (if present) = flag (e.g., `-y` to auto-approve requirements)

## Execution Steps

### Step 1: Load Context

**Read all necessary context**:
- `.sdd/specs/<feature>/spec.json`, `requirements.md`, `design.md` (if exists)
- **Entire `.sdd/steering/` directory** for complete project memory
- `.sdd/settings/templates/specs/design.md` for document structure
- `.sdd/settings/rules/design-principles.md` for design principles
- `.sdd/settings/templates/specs/research.md` for discovery log structure

**Validate requirements approval**:
- If `-y` flag provided: Auto-approve requirements in spec.json
- Otherwise: Verify approval status (stop if unapproved, see Safety & Fallback)

### Step 2: Discovery & Analysis

**Critical: This phase ensures design is based on complete, accurate information.**

1. **Classify Feature Type**:
   - **New Feature** (greenfield) → Full discovery required
   - **Extension** (existing system) → Integration-focused discovery
   - **Simple Addition** (CRUD/UI) → Minimal or no discovery
   - **Complex Integration** → Comprehensive analysis required

2. **Execute Appropriate Discovery Process**:

   **For Complex/New Features**:
   - Read and execute `.sdd/settings/rules/design-discovery-full.md`
   - Conduct thorough research using WebSearch/WebFetch:
     - Latest architectural patterns and best practices
     - External dependency verification (APIs, libraries, versions, compatibility)
     - Official documentation, migration guides, known issues
     - Performance benchmarks and security considerations

   **For Extensions**:
   - Read and execute `.sdd/settings/rules/design-discovery-light.md`
   - Focus on integration points, existing patterns, compatibility
   - Use Grep to analyze existing codebase patterns

   **For Simple Additions**:
   - Skip formal discovery, quick pattern check only

3. **Retain Discovery Findings for Step 3**:
   - External API contracts and constraints
   - Technology decisions with rationale
   - Existing patterns to follow or extend
   - Integration points and dependencies
   - Identified risks and mitigation strategies
   - Potential architecture patterns and boundary options (note details in `research.md`)
   - Parallelization considerations for future tasks

4. **Persist Findings to Research Log**:
   - Create or update `.sdd/specs/<feature>/research.md` using the shared template
   - Summarize discovery scope and key findings
   - Record investigations in Research Log topics with sources and implications
   - Document architecture pattern evaluation, design decisions, and risks

### Step 3: Generate Design Document

1. **Load Design Template and Rules**:
   - Read `.sdd/settings/templates/specs/design.md` for structure
   - Read `.sdd/settings/rules/design-principles.md` for principles

2. **Generate Design Document**:
   - **Follow specs/design.md template structure and generation instructions strictly**
   - **Integrate all discovery findings** throughout component definitions, architecture decisions, and integration points
   - If existing design.md found in Step 1, use it as reference context (merge mode)
   - Apply design rules: Type Safety, Visual Communication, Formal Tone
   - Use language specified in spec.json

3. **Update Metadata** in spec.json:
   - Set `phase: "design-generated"`
   - Set `approvals.design.generated: true, approved: false`
   - Set `approvals.requirements.approved: true`
   - Update `updated_at` timestamp

## Critical Constraints
- **Type Safety**: Enforce strong typing aligned with the project's technology stack. For TypeScript, never use `any`.
- **Latest Information**: Use WebSearch/WebFetch for external dependencies and best practices
- **Steering Alignment**: Respect existing architecture patterns from steering context
- **Template Adherence**: Follow specs/design.md template structure strictly
- **Design Focus**: Architecture and interfaces ONLY, no implementation code
- **Requirements Traceability IDs**: Use numeric requirement IDs only (e.g. "1.1", "1.2", "3.1") exactly as defined in requirements.md.
</instructions>

## Tool Guidance
- **Read first**: Load all context before taking action (specs, steering, templates, rules)
- **Research when uncertain**: Use WebSearch/WebFetch for external dependencies, APIs, and latest best practices
- **Analyze existing code**: Use Grep to find patterns and integration points in codebase
- **Write last**: Generate design.md only after all research and analysis complete

## Output Description

**Command execution output** (separate from design.md content):

Provide brief summary in the language specified in spec.json:

1. **Status**: Confirm design document generated at `.sdd/specs/<feature>/design.md`
2. **Discovery Type**: Which discovery process was executed (full/light/minimal)
3. **Key Findings**: 2-3 critical insights from discovery that shaped the design
4. **Next Action**: Approval workflow guidance (see Safety & Fallback)

**Format**: Concise Markdown (under 200 words)

## Safety & Fallback

### Error Scenarios

**Requirements Not Approved**:
- **Stop Execution**: Cannot proceed without approved requirements
- **User Message**: "Requirements not yet approved. Approval required before design generation."
- **Suggested Action**: "Re-run with `-y` flag to auto-approve requirements and proceed"

**Missing Requirements**:
- **Stop Execution**: Requirements document must exist
- **Suggested Action**: "Run `/sdd:spec-requirements <feature>` to generate requirements first"

**Template Missing**:
- **Fallback**: Use inline basic structure with warning

**Steering Context Missing**:
- **Warning**: "Steering directory empty or missing - design may not align with project standards"
- **Proceed**: Continue with generation but note limitation in output

**Invalid Requirement IDs**:
- **Stop Execution**: If requirements.md is missing numeric IDs or uses non-numeric headings, stop and instruct the user to fix requirements.md before continuing.

### Next Phase: Task Generation

**If Design Approved**:
- Review generated design at `.sdd/specs/<feature>/design.md`
- **Optional**: Run `/sdd:validate-design <feature>` for interactive quality review
- Then `/sdd:spec-tasks <feature> -y` to generate implementation tasks

**If Modifications Needed**:
- Provide feedback and re-run `/sdd:spec-design <feature>`
- Existing design used as reference (merge mode)

**Note**: Design approval is mandatory before proceeding to task generation.
