# Blender MCP setup (local machine)

How Blender was installed and wired into OpenCode on this machine, so the setup
can be repeated or repaired later.

## Components

| Piece | What it is | Where |
| --- | --- | --- |
| Blender 4.5.16 LTS | Portable build (no admin/UAC needed) | `C:\Users\noma1\AppData\Local\Programs\Blender\blender.exe` |
| Add-on | `blender_mcp.py`, served by `mcp-for-blender` | `%APPDATA%\Blender Foundation\Blender\4.5\scripts\addons\` |
| MCP server | `mcp-for-blender` (PyPI), installed as a uv tool | `C:\Users\noma1\.local\bin\mcp-for-blender.exe` |
| OpenCode entry | `mcp.servers.blender` | `C:\Users\noma1\.config\opencode\opencode.json` |

The add-on listens on `localhost:9876`; the MCP server bridges stdio (OpenCode)
to that socket.

## Install steps

```powershell
# 1. Portable Blender (winget needs an admin prompt; zip does not)
curl.exe -L -o blender.zip https://download.blender.org/release/Blender4.5/blender-4.5.16-windows-x64.zip
tar -xf blender.zip
Copy-Item .\blender-4.5.16-windows-x64\* C:\Users\noma1\AppData\Local\Programs\Blender -Recurse

# 2. Add-on into the user addons folder
uv tool install mcp-for-blender
$env:BLENDERMCP_ADDONS_DIR = "$env:APPDATA\Blender Foundation\Blender\4.5\scripts\addons"
mcp-for-blender install-addon

# 3. Enable it (once) and save preferences
& "C:\Users\noma1\AppData\Local\Programs\Blender\blender.exe" --background --factory-startup `
  --python-expr "import bpy, addon_utils; addon_utils.enable('blender_mcp', default_set=True, persistent=True); bpy.ops.wm.save_userpref()"
```

Then launch Blender normally. The add-on's **Auto-Start Server** preference is on
by default, so port 9876 opens on its own. To start it by hand: 3D viewport
sidebar → **BlenderMCP** → *Start MCP Server*.

## OpenCode configuration

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "blender": {
        "type": "local",
        "command": ["C:\\Users\\noma1\\.local\\bin\\mcp-for-blender.exe"],
        "environment": { "BLENDER_HOST": "localhost", "BLENDER_PORT": "9876" }
      }
    }
  }
}
```

Use the installed `.exe` rather than `uvx mcp-for-blender`: `uvx` resolves the
environment on every launch and can exceed OpenCode's ~5 s MCP handshake budget,
which shows up as `failed: Request timed out` in `opencode mcp list`.

## Verify

```powershell
opencode mcp list                 # ✓ blender connected
Test-NetConnection 127.0.0.1 -Port 9876
```

From a session, ask OpenCode to read the scene or create geometry. A raw socket
smoke test without OpenCode:

```powershell
$c = New-Object Net.Sockets.TcpClient('127.0.0.1', 9876)
$s = $c.GetStream()
$b = [Text.Encoding]::UTF8.GetBytes('{"type":"get_scene_info","params":{}}')
$s.Write($b, 0, $b.Length)
$buf = New-Object byte[] 65536
[Text.Encoding]::UTF8.GetString($buf, 0, $s.Read($buf, 0, $buf.Length))
```

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `opencode mcp list` → *Request timed out* | Use the installed `.exe` path (see above), not `uvx` |
| Server not listening | Blender → sidebar **BlenderMCP** → *Start MCP Server*, or restart Blender |
| `install-addon` throws `UnicodeEncodeError` | Cosmetic: the console cannot print `→`. The file is still copied; verify the addons folder |
| Port 9876 already in use | Close the other Blender instance or change the port in the add-on preferences and `BLENDER_PORT` |
| Add-on shows as outdated | `uv tool upgrade mcp-for-blender` then `mcp-for-blender install-addon` and restart Blender |
