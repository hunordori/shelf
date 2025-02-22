#!/bin/bash
# install.sh for shelf_organizer

# Function to exit with a message
exit_with_message() {
    echo "$1"
    exit 1
}

# Detect OS type
OS_TYPE="Unknown"
case "$(uname -s)" in
    Darwin*) OS_TYPE="Mac" ;;
    Linux*) OS_TYPE="Linux" ;;
    CYGWIN*|MINGW*|MSYS*) OS_TYPE="Windows" ;;
esac

echo "✅ Detected OS: $OS_TYPE"

# Check if Python is installed (try python3 first, then python)
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    exit_with_message "🚫 Python is not installed. Please install Python and try again."
fi

echo "✅ Using Python: $($PYTHON --version)"

# Get the repository root (requires git)
if command -v git &> /dev/null; then
    REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
    if [ -z "$REPO_ROOT" ]; then
        echo "⚠️ Could not determine repository root. Are you inside a git repository?"
        REPO_ROOT=$(pwd)
    fi
else
    REPO_ROOT=$(pwd)
fi

echo "✅ Repository root: $REPO_ROOT"

# Create virtual environment if it doesn't exist
VENV_DIR="$REPO_ROOT/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "✅ Creating virtual environment in .venv..."
    $PYTHON -m venv "$VENV_DIR" || exit_with_message "🚫 Failed to create virtual environment."
else
    echo "✅ Virtual environment .venv already exists."
fi

# Activate the virtual environment based on OS
if [ "$OS_TYPE" = "Windows" ]; then
    source "$VENV_DIR/Scripts/activate"
else
    source "$VENV_DIR/bin/activate"
fi

echo "✅ Virtual environment activated."

# Install dependencies from requirements.txt if it exists
REQ_FILE="$REPO_ROOT/requirements.txt"
if [ -f "$REQ_FILE" ]; then
    echo "📦 Installing dependencies from requirements.txt..."
    pip install -r "$REQ_FILE" || exit_with_message "🚫 pip install failed."
else
    echo "⚠️ Warning: requirements.txt not found."
fi

# Construct the full path to the db.sqlite3 file
DB_PATH="$REPO_ROOT/shelf_organizer/db.sqlite3"
if [ -f "$DB_PATH" ]; then
    echo "✅ Database file found at $DB_PATH"
else
    echo "🚫 Database file NOT found at $DB_PATH"
    echo "⚠️ Running migrations to create the database..."
    python "$REPO_ROOT/shelf_organizer/manage.py" migrate || exit_with_message "🚫 Failed to run migrations."
fi

# Inform the user how to access the app
echo "🚀 Starting Django development server..."
echo "👉 Visit: http://127.0.0.1:8000/"
echo "👤 Login credentials: username 'administrator' / password 'administrator'"
echo "🙂 Keep this window open to keep the server running. To close, press Ctrl+C"

# Start the Django development server
if [ "$OS_TYPE" = "Windows" ]; then
    winpty python "$REPO_ROOT/shelf_organizer/manage.py" runserver
else
    python "$REPO_ROOT/shelf_organizer/manage.py" runserver
fi
