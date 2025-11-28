# /import-research [course-code] [week-number]

Validate research from Claude Desktop for content generation.

## Usage

```
/import-research BCI2AU 5
/import-research BCI2AU all    # Batch import
```

## How It Works

1. **Desktop researches** using template (with MCP auto-write)
2. **Desktop writes** `week-N-research.md` + `.week-N-ready` flag
3. **This command validates** format, content, quality
4. **`/generate-week` uses** validated research

### Ready Flag Mechanism

**Path:** `courses/[CODE]/.working/research/.week-N-ready`

| State | Meaning |
|-------|---------|
| Flag exists | Desktop auto-wrote research, needs validation |
| Flag deleted | Research validated, ready for `/generate-week` |
| No flag | Research manually imported or not yet available |

**`/generate-week` checks for this flag** and auto-validates before generating content.

## Process 🔐

### Step 1: Check for Auto-Import

```
IF research file exists:
  → "Found existing research. Validate or replace?"
ELSE:
  → "Paste research or provide file path"
```

### Step 2: Validation 🔒

| Check | Requirement |
|-------|-------------|
| Format | Week number, topic, 4 articles, APA citations |
| Content | All concepts have ✓ checkmarks |
| Quality | 2 seminal + 2 recent balance |
| Access | URLs accessible or seminal justification |
| Teaching | Key Teaching Content present for each article |

### Step 3: Confirm

```
✓ Week 5 research validated
Ready for: /generate-week 5
```

## MCP Setup (One-Time)

1. Install MCP Filesystem Server in Claude Desktop
2. Configure: `.claude/mcp-config/desktop-commander-research.json`
3. Allow write access to `courses/` directory
4. Use template: `.claude/templates/desktop-course-research-template.md`

## Time

- Auto-write: 1-2 min (validation only)
- Manual paste: 3-7 min

## If Things Go Wrong

- **Format issues:** Check template in `.claude/templates/`
- **Missing concepts:** Return to Desktop, find better articles
- **Paywalled:** Check ResearchGate, override if seminal (1000+ citations)
- **No course directory:** Run `/new-course` first

## Example

```
/import-research BCI2AU 3

✓ Found existing research for Week 3
Validating...
✓ Format passed (4 articles, APA citations)
✓ Content passed (4/4 concepts)
✓ Quality passed (2 seminal + 2 recent)

Ready for: /generate-week 3
```

**Full reference:** See `docs/RESEARCH-HANDOFF-GUIDE.md` for complete workflow and MCP setup.
