# Chore: Scripts Directory Structure

## Description

Create the `.aura/scripts/` template directory in aura's source that gets copied during `aura init`. This directory will contain portable Python scripts that commands can call.

## Tasks

### 1. Create Template Directory

```
aura/src/aura/templates/aura/scripts/
├── __init__.py          # Empty, makes it a package for easier imports
├── requirements.txt     # Dependencies for scripts
└── .gitkeep             # Ensure directory is tracked
```

### 2. Create requirements.txt

```
# .aura/scripts/requirements.txt
# Install with: pip install -r .aura/scripts/requirements.txt

openai>=1.0.0          # Whisper API for transcription
pydub>=0.25.0          # Audio file manipulation
python-dotenv>=1.0.0   # Environment variable loading
```

### 3. Update init.py to Copy Scripts

Ensure `aura/src/aura/init.py` copies the scripts directory:

```python
# In get_template_files():
# .aura/scripts/ templates
scripts_templates = TEMPLATES / "aura" / "scripts"
if scripts_templates.exists():
    for src in scripts_templates.glob("**/*"):
        if src.is_file():
            rel = src.relative_to(TEMPLATES / "aura")
            dst = Path(".aura") / rel
            files.append((src, dst))
```

### 4. Update .gitignore Template

Create `.aura/.gitignore` template:

```
# Audio files (don't commit)
queue/
output/

# Environment
.env

# Python
__pycache__/
*.pyc
```

## Acceptance Criteria

- [ ] `aura/src/aura/templates/aura/scripts/` directory exists
- [ ] `requirements.txt` lists all dependencies
- [ ] `aura init` creates `.aura/scripts/` in target directory
- [ ] `.aura/.gitignore` excludes queue/ and output/

## Notes

- Scripts directory is where transcribe.py and generate_title.py will live
- This is infrastructure for Phase 1 feature work
