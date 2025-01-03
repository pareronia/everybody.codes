# statics
SRC_ROOT := src/main
PYTHON_SRC_ROOT := $(SRC_ROOT)/python
JAVA_SRC_ROOT := $(SRC_ROOT)/java/com/github/pareronia/everybody_codes
DST_ROOT := build
JAVA_DST := $(DST_ROOT)/java/classes
BLACK := black
FLAKE := flake8
VULTURE := vulture
MYPY := mypy
JAVAC_CMD := javac
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# vars
PY_SRCS = $(shell find $(PYTHON_SRC_ROOT) -name "*.py" -not -path "$(PYTHON_SRC_ROOT)/.venv/*")
JAVA_SRCS = $(shell find $(JAVA_SRC_ROOT) -name "*.java")

# functions
msg = (if [ -t 1 ]; then echo ${BLUE}"\n$1\n"${NC}; else echo "$1"; fi)

#: Run Python code Black formating check
black.check:
	@$(call msg,"Running Black check against Python source files...")
	@$(BLACK) --quiet --diff --color --check $(PY_SRCS)

#: Run Flake8 Python code linter
flake:
	@$(call msg,"Running Flake8 against Python source files...")
	@$(FLAKE) $(PY_SRCS)

#: Run Vulture - unused Python code checker
vulture:
	@$(call msg,"Running vulture against Python source files...")
	@$(VULTURE) --min-confidence 80 $(PY_SRCS)

#: Run mypy - Python type checker
mypy:
	@$(call msg,"Running mypy against Python source files...")
	@$(MYPY) --no-error-summary $(PY_SRCS)

#: Run all linters (black.check, flake, vulture, mypy)
lint: black.check flake vulture mypy

#: Build Java
build.java:
	@$(JAVAC_CMD) -d $(JAVA_DST) $(JAVA_SRCS)

#: git pre-push hook
pre-push: lint

dump:
	@echo "PY_SRCS: "$(PY_SRCS)""
