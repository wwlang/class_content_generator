# MCP Configuration for Claude Desktop

This directory contains MCP (Model Context Protocol) server configurations for Claude Desktop integration.

## Setup Instructions

### 1. Install MCP Filesystem Server

The filesystem server allows Claude Desktop to read and write files directly in this project.

**No installation needed** - The config uses `npx` to automatically install and run the server.

### 2. Configure Claude Desktop

**Location of Claude Desktop config:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

**Add this configuration:**

```json
{
  "mcpServers": {
    "class-content-generator-filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/williamlang/Projects/class_content_generator"
      ]
    }
  }
}
```

**IMPORTANT:** Replace `/Users/williamlang/Projects/class_content_generator` with your actual project path.

### 3. Restart Claude Desktop

After adding the configuration:
1. Quit Claude Desktop completely
2. Restart Claude Desktop
3. MCP server will load automatically

### 4. Verify MCP is Working

In Claude Desktop, try:
```
Can you read the file at courses/README.md in the class_content_generator project?
```

If Desktop can read/list files, MCP is working correctly.

## What This Enables

With MCP filesystem configured, Claude Desktop can:

1. **Read files** in this project
2. **Write files** to `.working/research/` directories
3. **Create flag files** (`.week-N-ready`) to signal completion
4. **Auto-save research** without manual copy/paste

## Usage in Workflows

### Research Handoff Workflow

**Step 1:** Claude Code generates master research prompt
**Step 2:** User copies prompt to Claude Desktop
**Step 3:** Desktop spawns 10 research agents (via Task tool)
**Step 4:** Each agent writes directly to file system via MCP
**Step 5:** Desktop creates `.week-N-ready` flags
**Step 6:** User returns to Code
**Step 7:** Code auto-detects and validates all research

**No manual file copying needed!**

## Troubleshooting

### MCP Not Loading

**Check:**
1. Config file location correct?
2. JSON syntax valid? (use JSON validator)
3. Project path correct and accessible?
4. Desktop restarted after config change?

**Test:**
```bash
# Verify Node/NPX installed
npx --version

# Test MCP server manually
npx -y @modelcontextprotocol/server-filesystem /path/to/project
```

### Permission Issues

**macOS/Linux:**
Ensure Desktop has filesystem permissions:
- System Preferences → Security & Privacy → Files and Folders
- Grant Claude access to project directory

**Windows:**
Run Desktop as administrator if needed.

### Path Issues

**Use absolute paths** in MCP config:
- ✓ Good: `/Users/williamlang/Projects/class_content_generator`
- ✗ Bad: `~/Projects/class_content_generator`
- ✗ Bad: `./class_content_generator`

## Security Note

MCP filesystem server has **full read/write access** to the configured directory and its subdirectories.

**Scope:** Limited to project directory only (secure by default)

## Further Reading

- [MCP Documentation](https://modelcontextprotocol.io)
- [Filesystem Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
- [Claude Desktop MCP Guide](https://docs.anthropic.com/claude/docs/claude-desktop-mcp)

## Support

If issues persist:
1. Check Desktop logs (Help → Show Logs)
2. Verify MCP server process running
3. Test with simple read/write operations
4. Consult MCP documentation
