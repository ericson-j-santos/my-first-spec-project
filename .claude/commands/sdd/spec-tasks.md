Generate implementation tasks for a specification.

<meta>
argument-hint: <feature-name> [-y] [--sequential]
</meta>

# Implementation Tasks Generator

<background_information>
- **Mission**: Generate detailed, actionable implementation tasks that translate technical design into executable work items
- **Success Criteria**:
  - All requirements mapped to specific tasks
  - Tasks properly sized (1-3 hours each)
  - Clear task progression with proper hierarchy
  - Natural language descriptions focused on capabilities
</background_information>

<instructions>
## Core Task
Generate implementation tasks based on approved requirements and design.

Parse arguments from: $ARGUMENTS
- First token = feature name
- Second token = optional flag `-y` (auto-approve) or `--sequential`
- Third token = optional `--sequential` flag

## Execution Steps

### Step 1: Load Context

**Read all necessary context**:
- `.sdd/specs/<feature>/spec.json`, `requirements.md`, `design.md`
- `.sdd/specs/<feature>/tasks.md` (if exists, for merge mode)
- **Entire `.sdd/steering/` directory** for complete project memory

**Validate approvals**:
- If `-y` flag provided: Auto-approve requirements and design in spec.json
- Otherwise: Verify both approved (stop if not, see Safety & Fallback)
- Determine sequential mode: `sequential = (--sequential flag present)`

### Step 2: Generate Implementation Tasks

**Load generation rules and template**:
- Read `.sdd/settings/rules/tasks-generation.md` for principles
- If not sequential: Read `.sdd/settings/rules/tasks-parallel-analysis.md` for parallel judgement criteria
- Read `.sdd/settings/templates/specs/tasks.md` for format (supports `(P)` markers)

**Generate task list following all rules**:
- Use language specified in spec.json
- Map all requirements to tasks and list numeric requirement IDs only (comma-separated) without extra narration, descriptive suffixes, parentheses, translations, or free-form labels
- Ensure all design components included
- Verify task progression is logical and incremental
- Collapse single-subtask structures by promoting them to major tasks and keep container summaries concise
- Apply `(P)` markers to tasks that satisfy parallel criteria (skip markers when sequential mode)
- Mark optional acceptance-criteria-focused test coverage subtasks with `- [ ]*` only when deferrable post-MVP
- If existing tasks.md found, merge with new content

### Step 3: Finalize

**Write and update**:
- Create/update `.sdd/specs/<feature>/tasks.md`
- Update spec.json metadata:
  - Set `phase: "tasks-generated"`
  - Set `approvals.tasks.generated: true, approved: false`
  - Set `approvals.requirements.approved: true`
  - Set `approvals.design.approved: true`
  - Update `updated_at` timestamp

## Critical Constraints
- **Follow rules strictly**: All principles in tasks-generation.md are mandatory
- **Natural Language**: Describe what to do, not code structure details
- **Complete Coverage**: ALL requirements must map to tasks
- **Maximum 2 Levels**: Major tasks and sub-tasks only (no deeper nesting)
- **Sequential Numbering**: Major tasks increment (1, 2, 3...), never repeat
- **Task Integration**: Every task must connect to the system (no orphaned work)
</instructions>

## Tool Guidance
- **Read first**: Load all context, rules, and templates before generation
- **Write last**: Generate tasks.md only after complete analysis and verification

## Output Description

Provide brief summary in the language specified in spec.json:

1. **Status**: Confirm tasks generated at `.sdd/specs/<feature>/tasks.md`
2. **Task Summary**:
   - Total: X major tasks, Y sub-tasks
   - All Z requirements covered
   - Average task size: 1-3 hours per sub-task
3. **Quality Validation**:
   - All requirements mapped to tasks
   - Task dependencies verified
   - Testing tasks included
4. **Next Action**: Review tasks and proceed when ready

**Format**: Concise (under 200 words)

## Safety & Fallback

### Error Scenarios

**Requirements or Design Not Approved**:
- **Stop Execution**: Cannot proceed without approved requirements and design
- **Suggested Action**: "Re-run with `-y` flag to auto-approve both and proceed"

**Missing Requirements or Design**:
- **Stop Execution**: Both documents must exist
- **Suggested Action**: "Complete requirements and design phases first"

**Incomplete Requirements Coverage**:
- **Warning**: "Not all requirements mapped to tasks. Review coverage."
- **User Action Required**: Confirm intentional gaps or regenerate tasks

**Missing Numeric Requirement IDs**:
- **Stop Execution**: All requirements in requirements.md MUST have numeric IDs. If any requirement lacks a numeric ID, stop and request that requirements.md be fixed before generating tasks.

### Next Phase: Implementation

**Before Starting Implementation**:
- **IMPORTANT**: Clear conversation history and free up context before running `/sdd:spec-impl`
- This applies when starting first task OR switching between tasks
- Fresh context ensures clean state and proper task focus

**If Tasks Approved**:
- Execute specific task: `/sdd:spec-impl <feature> 1.1` (recommended: clear context between each task)
- Execute multiple tasks: `/sdd:spec-impl <feature> 1.1,1.2`
- Without arguments: `/sdd:spec-impl <feature>` (executes all pending tasks - NOT recommended due to context bloat)

**If Modifications Needed**:
- Provide feedback and re-run `/sdd:spec-tasks <feature>`
- Existing tasks used as reference (merge mode)
