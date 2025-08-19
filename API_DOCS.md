# API Documentation

## 📚 Class Reference

### Player Class (`player.py`)

The main game controller that manages the PyBoy emulator instance and voting system.

#### Constructor
```python
def __init__(self)
```
Initializes the player with:
- Game state flags
- Voting round tracking
- Database connection
- Move timer (15 seconds per round)

#### Methods

##### `async load_rom(rom: str)`
Loads a Game Boy ROM file and starts the game loop.

**Parameters:**
- `rom`: String path to ROM file relative to `roms/` directory

**Behavior:**
- Initializes PyBoy emulator
- Loads existing save state if available
- Starts the main game loop

##### `async start_game()`
Main game loop that handles voting rounds and game execution.

**Game Loop:**
1. Processes voting results every 15 seconds
2. Executes winning button choice
3. Resets voting round
4. Updates game display
5. Manages move timer countdown

##### `send_input(user_id: int, btn_input: str) -> str`
Processes user button input based on current game mode.

**Parameters:**
- `user_id`: Discord user ID
- `btn_input`: Button name (a, b, up, down, etc.)

**Returns:** Status message string

**Modes:**
- **Democracy**: Adds vote to current round, prevents duplicate voting
- **Anarchy**: Immediately executes button press

##### `save()`
Saves current game state to `saves/save.state`

##### `set_mode(democracy: bool = True)`
Switches between democracy and anarchy modes.

#### Properties
- `is_playing`: Boolean indicating if game is active
- `move_timer`: Countdown timer for voting rounds
- `moves_this_round`: Dictionary tracking vote counts per button
- `players_this_round`: Set of users who voted this round
- `is_democracy`: Boolean for current game mode

---

### Database Class (`db.py`)

Handles SQLite database operations for logging user inputs and game actions.

#### Constructor
```python
def __init__(self, name: str = 'my_database.db')
```
Initializes SQLite connection and creates moves table if it doesn't exist.

#### Methods

##### `add_entry(userid: int, inputs: str)`
Logs a single user button input to the database.

**Parameters:**
- `userid`: Discord user ID
- `inputs`: Button name string

**Validation:**
- Uses Pydantic model for input validation
- Commits transaction to database
- Logs validation errors

##### `add_move_round(round_data: dict, round_timestamp: datetime = None)`
Logs all votes from a completed voting round.

**Parameters:**
- `round_data`: Dictionary like `{'a': 5, 'b': 2, 'up': 1}`
- `round_timestamp`: When the round occurred (defaults to now)

**Behavior:**
- Creates multiple database entries for each vote count
- Uses userid 0 for system/voting round entries

##### `get_user_moves(userid: int, limit: Optional[int] = None) -> list`
Retrieves all moves for a specific user.

**Parameters:**
- `userid`: Discord user ID
- `limit`: Optional maximum number of results

**Returns:** List of move records

##### `get_all_moves(limit: Optional[int] = None) -> list`
Retrieves all moves from all users.

**Parameters:**
- `limit`: Optional maximum number of results

**Returns:** List of move records

##### `get_move_statistics() -> dict`
Returns button usage statistics across all users.

**Returns:** Dictionary mapping button names to usage counts

##### `get_user_statistics(userid: int) -> dict`
Returns button usage statistics for a specific user.

**Parameters:**
- `userid`: Discord user ID

**Returns:** Dictionary mapping button names to usage counts

##### `get_recent_moves(minutes: int = 60) -> list`
Retrieves moves from the last N minutes.

**Parameters:**
- `minutes`: Time window in minutes

**Returns:** List of recent move records

---

### Bot Class (`bot.py`)

Discord bot main entry point with slash command handlers.

#### Commands

##### `/load`
Admin-only command to load a ROM file.

**Behavior:**
- Checks admin permissions
- Displays ROM selection dropdown
- Prevents loading if game is already active

##### `/play`
Opens the game controller interface.

**Behavior:**
- Creates GameboyPad view
- Displays current game screen
- Available to all users

##### `/save`
Saves the current game state.

**Behavior:**
- Calls player.save()
- Confirms save operation
- Available to all users

##### `/setmode`
Admin-only command to switch game modes.

**Parameters:**
- `mode`: String - 'democracy' or 'anarchy'

**Behavior:**
- Validates mode parameter
- Updates player.is_democracy
- Confirms mode change

#### Admin System
```python
def is_admin(interaction: discord.Interaction) -> bool
```
Hardcoded admin check for user ID `418986435144581130`.

---

### UI Components (`ui.py`)

Discord UI components for game interaction.

#### RomsDropdown
Dropdown menu for ROM selection.

**Behavior:**
- Displays available ROM files
- Calls player.load_rom() on selection
- Sends confirmation message

#### GameboyPad
Main game controller interface.

**Layout:**
```
[  ] [UP] [  ] [  ] [  ]
[L] [  ] [R] [A] [B]
[  ] [DN] [  ] [ST] [SL]
```

**Features:**
- 3x5 grid layout
- Dummy buttons for spacing
- Functional game buttons
- No timeout (persistent interface)

#### GameboyButton
Individual button component.

**Behavior:**
- Checks if game is loaded
- Calls player.send_input()
- Updates game display
- Refreshes controller view

---

### Logger (`logger.py`)

Centralized logging configuration.

```python
Logger = logging.getLogger("DPPBot")
```

**Usage:**
```python
Logger.info("Message %s", variable)
Logger.error("Error in %s: %s", field, message)
```

**Best Practices:**
- Use lazy % formatting for performance
- Avoid f-strings in logging calls
- Consistent log level usage

---

## 🔄 Data Flow Diagrams

### User Input Flow
```
Discord Button Press
       ↓
   UI Callback
       ↓
  Player.send_input()
       ↓
   Mode Check (Democracy/Anarchy)
       ↓
   Database Logging
       ↓
   Game Execution (if applicable)
```

### Voting Round Flow
```
Round Start (15s timer)
       ↓
   User Votes Collected
       ↓
   Timer Expires
       ↓
   Winning Button Selected
       ↓
   PyBoy.button() Executed
       ↓
   Round Data Logged to DB
       ↓
   Round Reset
```

### ROM Loading Flow
```
Admin /load Command
       ↓
   ROM Selection Dropdown
       ↓
   ROM File Selected
       ↓
   PyBoy Instance Created
       ↓
   Save State Loaded (if exists)
       ↓
   Game Loop Started
```

---

## 📊 Database Queries

### Common Analysis Queries

#### Most Popular Buttons
```sql
SELECT input, COUNT(*) as count
FROM moves
GROUP BY input
ORDER BY count DESC;
```

#### User Activity by Time
```sql
SELECT userid, COUNT(*) as moves
FROM moves
WHERE created_at >= datetime('now', '-1 hour')
GROUP BY userid
ORDER BY moves DESC;
```

#### Democracy vs Anarchy Usage
```sql
SELECT 
    CASE 
        WHEN userid = 0 THEN 'Voting Round'
        ELSE 'Individual Move'
    END as move_type,
    COUNT(*) as count
FROM moves
GROUP BY move_type;
```

---

## 🚨 Error Handling

### Validation Errors
- Pydantic model validation for database inputs
- Button input validation against allowed values
- User permission checks for admin commands

### Database Errors
- Connection error handling
- Transaction rollback on failures
- Logging of all database errors

### Game Errors
- ROM loading failures
- Save state corruption handling
- PyBoy emulator error recovery

---

## 🔧 Configuration

### Environment Variables
- `DISCORD_BOT_TOKEN`: Required Discord bot authentication

### File Paths
- `roms/`: ROM file directory
- `saves/`: Save state directory
- `curr_frame.png`: Current game screen capture

### Constants
- `MAX_MOVE_TIME = 15`: Voting round duration in seconds
- Button enum values: A=1, B=2, SELECT=3, etc.
