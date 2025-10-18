set dotenv-filename := ".win-env"

alias l := lint

source_dir := "src/main/python"
java_source_dir := "src/main/java"
java_path := "com/github/pareronia/everybody_codes"

google-java-format := env("GOOGLE_JAVA_FORMAT_CMD", "google-java-format")
java := env("JAVA_CMD", "java")
mypy := if os_family() == "windows" \
            { "uvx mypy --python-executable='.venv\\Scripts\\python'" } \
        else \
            { "uvx mypy --python-executable='.venv/bin/python'" }
pmd := "pmd"
python := "uv run python -O"
python_debug := "uv run python"
ruff := "uvx ruff"
vulture := "uvx vulture"

export PYTHONPATH := "src/main/python"

default:
    @just --choose

[group("vim")]
vim-file-run-dev file $LOGLEVEL="DEBUG" *type:
    @echo {{CLEAR}}
    @{{python_debug}} "{{file}}"

[group("vim")]
vim-file-run file *type:
    @echo {{CLEAR}}
    @{{python}} "{{file}}"

[group("vim")]
vim-file-debug file *type:
    @echo {{CLEAR}}
    @{{python_debug}} -m pdb "{{file}}"

# Linting: ruff check
[group("linting")]
ruff-check:
    @echo "Running ruff check"
    @{{ruff}} --quiet check "{{source_dir}}"

# Linting: vulture - unused code
[group("linting")]
vulture:
    @echo "Running vulture"
    @{{vulture}} "{{source_dir}}"

# Linting: ruff format check
[group("linting")]
ruff-format-check:
    @echo "Running ruff format check"
    @{{ruff}} format --quiet --check "{{source_dir}}"

# Linting: mypy
[group("linting")]
mypy:
    @echo "Running mypy"
    @{{mypy}} --no-error-summary {{source_dir}}

# Linting: pmd
[group("linting")]
pmd:
    @echo "Running pmd check"
    @{{pmd}} check --rulesets=pmd-ruleset.xml --format=textcolor --dir="{{java_source_dir}}"

# Linting: java format check
[group("linting")]
java-format-check:
    #!/usr/bin/env -S uv run --script
    print("Running java format check")

    import subprocess
    import sys
    from pathlib import Path

    files = " ".join(map(str, list(Path("{{java_source_dir}}").rglob("*.java"))))
    completed = subprocess.run(
        "{{google-java-format}}".split() + ["--aosp", "--dry-run", "--set-exit-if-changed", files],
        check=False
    )
    sys.exit(completed.returncode)

# Linting: all
[group("linting")]
lint: ruff-check vulture ruff-format-check mypy java-format-check pmd

# Run all Quests - python
[group("python")]
run-all-py:
    @{{python}} -m ec.runner --all

# Run a Quest - python
[group("python")]
run-py year quest:
    @{{python}} -m ec.runner --quest {{year}} {{quest}}

# Run a Quest - java
[group("java")]
run-java year quest:
    @{{java}} $(echo 'year={{year}};quest={{quest}};print(f"{{java_source_dir}}/{{java_path}}/Quest{year}_{quest:0>2}.java")' | {{python}} -)

# Stats
[group("admin")]
stats year:
    @{{python}} -m ec.stats {{year}}

# Implementation table
[group("admin")]
impl:
    @{{python}} -m ec.table README.md

# Generate Quest - python
[group("admin")]
generate year quest:
    @{{python}} -m ec.generator {{year}} {{quest}}

# git hook
pre-commit: lint
