alias l := lint

source_dir := join(".", "src", "main", "python")
java_source_dir := join(".", "src", "main", "java")
java_path := "com/github/pareronia/everybody_codes"

java := "java"
mypy := "uvx mypy"
python := "PYTHONOPTIMIZE=1 PYTHONPATH=src/main/python/ uv run"
python_debug := "PYTHONPATH=src/main/python/ uv run"
ruff := "uvx ruff"
vulture := "uvx vulture"

default:
    @just --choose

[group("vim")]
vim-file-run-dev file $LOGLEVEL="DEBUG":
    @echo {{CLEAR}}
    @{{python_debug}} "{{file}}"

[group("vim")]
vim-file-run file:
    @echo {{CLEAR}}
    @{{python}} "{{file}}"

[group("vim")]
vim-file-debug file:
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

# Linting: all
[group("linting")]
lint: ruff-check vulture ruff-format-check mypy

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
