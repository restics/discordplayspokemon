# Discord Pokemon Bot (DPPBot)

A Discord bot that allows users to play Game Boy ROMs through a collaborative voting system, inspired by Twitch Plays Pokemon. Users can vote on button inputs in democracy mode or directly control the game in anarchy mode.

## 🎮 Features

- **Multiplayer Game Boy Emulation**: Play Game Boy ROMs through Discord
- **Democracy Mode**: Users vote on button inputs, most popular choice wins
- **Anarchy Mode**: Direct button control for immediate response
- **Real-time Game Display**: Live game screen updates in Discord
- **Save State Management**: Automatic and manual game state saving
- **Input Logging**: Database tracking of all user inputs for analysis
- **Admin Controls**: ROM loading and mode switching restricted to admins

## 🏗️ Architecture

### Core Components

```
bottesting/
├── src/
│   ├── bot.py          # Discord bot main entry point
│   ├── player.py       # Game Boy emulation and game logic
│   ├── ui.py           # Discord UI components (buttons, dropdowns)
│   ├── db.py           # Database operations for input logging
│   └── logger.py       # Centralized logging configuration
├── roms/               # Game Boy ROM files
├── saves/              # Game save states
├── templates/          # HTML templates (if any)
└── requirements.txt    # Python dependencies
```

### Data Flow

1. **User Input**: Discord button press → UI callback → Player.send_input()
2. **Voting System**: Democracy mode aggregates votes, anarchy mode executes immediately
3. **Game Execution**: PyBoy emulator processes button input → game state updates
4. **Database Logging**: All inputs logged with user ID, button, and timestamp
5. **Display Update**: Current game frame saved and displayed in Discord

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8+
- Discord Bot Token
- Game Boy ROM files

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bottesting
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   DISCORD_BOT_TOKEN=your_discord_bot_token_here
   ```

4. **ROM Setup**
   Place your Game Boy ROM files in the `roms/` directory

5. **Run the bot**
   ```bash
   python src/bot.py
   ```

## 📱 Discord Commands

### User Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/play` | Opens the game controller interface | Available to all users |
| `/save` | Saves the current game state | Available to all users |

### Admin Commands

| Command | Description | Usage | Admin Only |
|---------|-------------|-------|------------|
| `/load` | Load a ROM file | Select from available ROMs | ✅ |
| `/setmode` | Switch between democracy/anarchy | `democracy` or `anarchy` | ✅ |

## 🎯 Game Modes

### Democracy Mode (Default)
- Users vote on button inputs during a 15-second round
- Most popular button choice wins and executes
- Prevents spam by limiting one vote per user per round
- Inputs are logged to database for analysis

### Anarchy Mode
- Immediate button execution
- No voting delay
- Direct control for fast-paced gameplay
- All inputs still logged to database

## 🗄️ Database Schema

### Moves Table
```sql
CREATE TABLE moves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER,           -- Discord user ID
    input VARCHAR(10),        -- Button pressed (a, b, up, down, etc.)
    created_at INTEGER        -- Unix timestamp
);
```

### Data Analysis Capabilities
- Track most popular buttons
- Analyze user behavior patterns
- Monitor democracy vs anarchy usage
- Time-based input analysis

## 🔧 Technical Details

### Button Mapping
```python
class Button(IntEnum):
    A = 1
    B = 2
    SELECT = 3
    START = 4
    UP = 5
    DOWN = 6
    LEFT = 7
    RIGHT = 8
```

### Game Controller Layout
```
[  ] [UP] [  ] [  ] [  ]
[L] [  ] [R] [A] [B]
[  ] [DN] [  ] [ST] [SL]
```

### Input Validation
- Button inputs validated against allowed values
- User ID tracking for democracy mode
- Error handling for invalid inputs
- Comprehensive logging of all operations

## 🐛 Troubleshooting

### Common Issues

1. **"XDG_RUNTIME_DIR not set"**
   - This is a Linux environment variable issue
   - Usually doesn't affect bot functionality

2. **"No ROMs found"**
   - Ensure ROM files are in the `roms/` directory
   - Check file permissions

3. **"Failed to log move to database"**
   - Verify database file permissions
   - Check logger configuration

4. **ALSA Audio Errors**
   - Audio-related warnings, doesn't affect emulation
   - Can be ignored in headless environments

### Debug Mode
Enable detailed logging by modifying `logger.py`:
```python
Logger.setLevel(logging.DEBUG)
```

## 📊 Performance Considerations

- **Memory Usage**: PyBoy emulator loads entire ROM into memory
- **Database Performance**: SQLite with proper indexing for input logging
- **Discord Rate Limits**: Bot respects Discord API limits
- **Frame Updates**: Optimized image saving and Discord file handling

## 🔒 Security Features

- Admin-only ROM loading and mode switching
- Input validation and sanitization
- User ID verification for voting system
- Safe file handling for ROMs and saves

## 🚧 Future Enhancements

- [ ] Web-based analytics dashboard
- [ ] Multiple ROM support with save state management
- [ ] Advanced voting algorithms
- [ ] Integration with external game databases
- [ ] Mobile-optimized UI components

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License

## 🤝 Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the Discord bot documentation

---

**Note**: This bot is designed for educational and entertainment purposes. Ensure you have the rights to use any ROM files you load.
