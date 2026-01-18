# Chore: Repository Extraction Preparation

## Description

Prepare the `aura/` directory for extraction to its own standalone repository.

## Extraction Checklist

### 1. Clean Up Whisper References

Search for and remove any references to:
- [ ] `whisper/` paths
- [ ] `brain/` directory
- [ ] whisper-specific commands
- [ ] Any hardcoded paths to parent directory

### 2. Verify Self-Containment

Ensure aura works completely standalone:
- [ ] `cd aura && uv sync` works
- [ ] `aura --version` works
- [ ] `aura init --dry-run` shows correct files
- [ ] No imports reference parent whisper package

### 3. Update pyproject.toml for Publishing

```toml
[project]
name = "aura"
version = "0.1.0"
description = "Agentic workflow layer for codebases"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.12"
dependencies = [
    "click>=8.0",
]

[project.optional-dependencies]
scripts = [
    "openai>=1.0",
    "pydub>=0.25",
    "python-dotenv>=1.0",
]

[project.scripts]
aura = "aura.cli:main"

[project.urls]
Homepage = "https://github.com/username/aura"
Repository = "https://github.com/username/aura"
```

### 4. Create .gitignore for New Repo

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/

# Environment
.env

# IDE
.idea/
.vscode/
*.swp

# Aura test artifacts
tests/tron/.aura/
tests/tron/.beads/
tests/tron/.claude/
tests/tron/specs/
```

### 5. Verify Tests Work

```bash
cd aura
uv sync
python -m pytest tests/ -v  # if tests exist
# or manual verification
cd tests/tron
python -m aura.cli init
```

### 6. Document Extraction Steps

Create `EXTRACTION.md` with steps:

```markdown
# Extracting Aura to Standalone Repository

## Steps

1. Create new GitHub repository: `aura`

2. Copy aura directory:
   ```bash
   cp -r whisper/aura /path/to/new/aura
   cd /path/to/new/aura
   ```

3. Initialize git:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - extracted from whisper incubation"
   ```

4. Push to GitHub:
   ```bash
   git remote add origin git@github.com:username/aura.git
   git push -u origin main
   ```

5. Test installation:
   ```bash
   uv tool install .
   aura --version
   ```
```

## Acceptance Criteria

- [ ] No whisper references remain in aura/
- [ ] `aura/` is completely self-contained
- [ ] pyproject.toml ready for publishing
- [ ] .gitignore appropriate for standalone repo
- [ ] EXTRACTION.md documents the process
- [ ] Can copy aura/ to new location and it works

## Post-Extraction (Future)

After extraction to own repo:
1. Set up GitHub Actions for CI
2. Publish to PyPI (optional)
3. Configure `uv tool install aura` from GitHub
4. Update whisper to optionally use aura instead of native commands

## Notes

- This is the final step of incubation
- After this, aura lives independently
- Whisper can continue using its native commands or adopt aura
