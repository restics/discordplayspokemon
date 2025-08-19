# Development Guide

## 🛠️ Development Environment Setup

### Prerequisites
- Python 3.8+
- Git
- Discord Developer Account
- SQLite (usually included with Python)

### Local Development Setup

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd bottesting
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   cp .env.example .env  # Create from template
   # Edit .env with your Discord bot token
   ```

3. **Database Setup**
   ```bash
   # The database will be created automatically on first run
   # Or manually initialize:
   python -c "from src.db import Database; db = Database()"
   ```

4. **ROM Files**
   ```bash
   mkdir roms
   # Add your .gb or .gbc files here
   ```

## 🏗️ Project Structure

```
bottesting/
├── src/                    # Source code
│   ├── __init__.py        # Package initialization
│   ├── bot.py             # Discord bot entry point
│   ├── player.py          # Game logic and emulation
│   ├── ui.py              # Discord UI components
│   ├── db.py              # Database operations
│   └── logger.py          # Logging configuration
├── roms/                   # Game ROM files
├── saves/                  # Save states
├── tests/                  # Test files (create this)
├── docs/                   # Documentation
├── .env                    # Environment variables
├── .gitignore             # Git ignore rules
├── requirements.txt        # Python dependencies
└── README.md              # Project overview
```

## 📝 Coding Standards

### Python Style Guide
- Follow PEP 8 conventions
- Use type hints for function parameters and return values
- Maximum line length: 88 characters (Black formatter)
- Use descriptive variable and function names

### Code Organization
```python
# Standard import order
import os
import sys
from typing import Optional, List

# Third-party imports
import discord
from pyboy import PyBoy

# Local imports
from .db import Database
from .logger import Logger
```

### Error Handling
```python
# Good: Specific exception handling
try:
    result = risky_operation()
except ValidationError as e:
    Logger.error("Validation failed: %s", e)
    return None
except Exception as e:
    Logger.error("Unexpected error: %s", e)
    raise

# Bad: Generic exception handling
try:
    result = risky_operation()
except:
    pass  # Never do this
```

### Logging Best Practices
```python
# Good: Lazy formatting
Logger.info("User %s pressed button %s", user_id, button)

# Bad: F-string in logging
Logger.info(f"User {user_id} pressed button {button}")

# Good: Structured logging
Logger.info("Game state updated", extra={
    "user_id": user_id,
    "button": button,
    "mode": "democracy"
})
```

## 🧪 Testing

### Test Structure
```bash
tests/
├── __init__.py
├── test_player.py
├── test_database.py
├── test_bot.py
└── test_ui.py
```

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-mock

# Run all tests
pytest

# Run specific test file
pytest tests/test_player.py

# Run with coverage
pytest --cov=src tests/
```

### Example Test
```python
import pytest
from src.player import Player
from src.db import Database

class TestPlayer:
    @pytest.fixture
    def player(self):
        return Player()
    
    def test_player_initialization(self, player):
        assert player.is_playing == False
        assert player.move_timer == 0
        assert player.is_democracy == True
    
    @pytest.mark.asyncio
    async def test_load_rom(self, player, tmp_path):
        # Test ROM loading functionality
        pass
```

## 🔍 Debugging

### Common Issues and Solutions

#### 1. Discord Bot Not Responding
```python
# Check bot permissions
intents = discord.Intents.default()
intents.message_content = True  # Required for slash commands
intents.guilds = True           # Required for guild events
```

#### 2. Database Connection Issues
```python
# Verify database file permissions
import os
db_path = 'my_database.db'
print(f"Database exists: {os.path.exists(db_path)}")
print(f"Database readable: {os.access(db_path, os.R_OK)}")
print(f"Database writable: {os.access(db_path, os.W_OK)}")
```

#### 3. PyBoy Emulation Issues
```python
# Check ROM file validity
try:
    pyboy = PyBoy('roms/game.gb')
    print("ROM loaded successfully")
except Exception as e:
    print(f"ROM loading failed: {e}")
```

### Debug Logging
```python
# Enable debug logging
import logging
Logger.setLevel(logging.DEBUG)

# Add debug statements
Logger.debug("Processing input: user_id=%s, button=%s", user_id, button)
```

### Performance Profiling
```python
import cProfile
import pstats

def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Your code here
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 functions
```

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**
   ```bash
   # Production .env
   DISCORD_BOT_TOKEN=your_production_token
   LOG_LEVEL=INFO
   DATABASE_PATH=/var/lib/dppbot/moves.db
   ```

2. **Process Management**
   ```bash
   # Using systemd
   sudo systemctl enable dppbot
   sudo systemctl start dppbot
   sudo systemctl status dppbot
   ```

3. **Database Backup**
   ```bash
   # Backup script
   sqlite3 moves.db ".backup backup_$(date +%Y%m%d_%H%M%S).db"
   ```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY roms/ ./roms/
COPY saves/ ./saves/

CMD ["python", "src/bot.py"]
```

## 📊 Monitoring and Analytics

### Database Queries for Insights
```sql
-- User engagement metrics
SELECT 
    userid,
    COUNT(*) as total_moves,
    COUNT(DISTINCT DATE(created_at)) as active_days
FROM moves 
WHERE userid != 0
GROUP BY userid
ORDER BY total_moves DESC;

-- Button popularity over time
SELECT 
    DATE(created_at) as date,
    input,
    COUNT(*) as usage
FROM moves
WHERE created_at >= DATE('now', '-7 days')
GROUP BY DATE(created_at), input
ORDER BY date DESC, usage DESC;
```

### Log Analysis
```bash
# Find error patterns
grep "ERROR" logs/dppbot.log | cut -d' ' -f4- | sort | uniq -c | sort -nr

# Monitor user activity
grep "User.*pressed button" logs/dppbot.log | tail -100
```

## 🔧 Development Tools

### Code Quality Tools
```bash
# Install development tools
pip install black isort flake8 mypy

# Format code
black src/
isort src/

# Lint code
flake8 src/
mypy src/
```

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
```

### IDE Configuration
```json
// .vscode/settings.json
{
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true
}
```

## 🐛 Troubleshooting

### Common Development Issues

1. **Import Errors**
   - Ensure `src/` is in Python path
   - Check `__init__.py` files exist
   - Use relative imports within the package

2. **Async/Await Issues**
   - Use `pytest-asyncio` for testing async functions
   - Ensure proper event loop handling
   - Check for missing `await` keywords

3. **Database Lock Issues**
   - Close database connections properly
   - Use context managers for database operations
   - Check for concurrent access patterns

### Getting Help
1. Check existing issues in the repository
2. Review the API documentation
3. Look at the code examples
4. Create a minimal reproduction case
5. Include relevant logs and error messages

## 📚 Additional Resources

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [PyBoy Documentation](https://pyboy.readthedocs.io/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Python AsyncIO Documentation](https://docs.python.org/3/library/asyncio.html)
