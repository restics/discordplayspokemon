from enum import IntEnum
import os
import asyncio 
from pyboy import PyBoy
from db import Database
from logger import Logger

# Add a consistent temp frame path for current game screenshot
FRAME_DIR = 'temp'
FRAME_FILENAME = 'curr_frame.png'
FRAME_PATH = os.path.join(FRAME_DIR, FRAME_FILENAME)

MAX_MOVE_TIME = 15

class Button(IntEnum):
    A = 1
    B = 2
    SELECT = 3
    START = 4
    UP = 5
    DOWN = 6
    LEFT = 7
    RIGHT = 8

class Player:
    def __init__(self):
        self.is_playing = False
        self.move_timer = 0;
        self.moves_this_round = {
            'a' : 0,
            'b' : 0,
            'select' : 0,
            'start' : 0,
            'up' : 0,
            'down' : 0,
            'left' : 0,
            'right' : 0,
        }
        self.players_this_round = set()
        self.is_democracy = True

        self.db = Database()

    # must be string of relative directory
    async def load_rom(self, rom : str):
        self.pyboy = PyBoy(f'roms/{rom}')
        if os.path.exists('saves/save.state'):
            try:
                with open('saves/save.state', 'rb') as f:
                    self.pyboy.load_state(f)
                Logger.info("Loaded existing save state")
            except Exception as e:
                Logger.warning("Failed to load save state: %s. Starting fresh.", e)
                # Remove corrupted save file
                try:
                    os.remove('saves/save.state')
                except:
                    pass
        else:
            Logger.info("No saves found, starting new run..")

        os.makedirs(FRAME_DIR, exist_ok=True)
        # Try to remove existing frame file, but don't fail if we can't
        if os.path.exists(FRAME_PATH):
            try:
                os.remove(FRAME_PATH)
            except (FileNotFoundError, PermissionError, OSError):
                Logger.warning("Could not remove existing frame file, continuing anyway")
        self.pyboy.screen.image.save(FRAME_PATH)
        await self.start_game()

    async def start_game(self):
        if not self.pyboy:
            return

        Logger.info("Starting pyboy instance")
        self.is_playing = True
        while self.is_playing:
            if sum(self.moves_this_round.values()) > 0:
                selection = max(self.moves_this_round, key=lambda x: self.moves_this_round[x]) 
                Logger.info("button selection %s has won this round!", selection)
                self.pyboy.button(selection,2)
            else:
                Logger.info("No buttons were pressed this round!")

            # reset dict values
            self.moves_this_round = dict(map(lambda item: (item[0], 0), self.moves_this_round.items()))
            self.players_this_round = set()

            self.move_timer = MAX_MOVE_TIME

            Logger.info("saving frame:")
            self.pyboy.screen.image.save(FRAME_PATH)
                
            while self.move_timer > 0 and self.is_playing:
                self.pyboy.tick(60, True, False)
                self.pyboy.screen.image.save(FRAME_PATH)
                self.move_timer -= 1
                Logger.info("Move Countdown: %ss", self.move_timer)
                await asyncio.sleep(1)
    
    def get_current_screen(self):
        if not self.pyboy:
            return
        else:
            return self.pyboy.screen.image

    def send_input(self, user_id: int, btn_input: str):
        print(f'id: {user_id}')
        
            
        if self.is_democracy:
            if user_id in self.players_this_round:
                return f"(DEMOCRACY) You have already moved this round! Time until next move: {self.move_timer}s"
            
            self.players_this_round.add(user_id)
            self.moves_this_round[btn_input] += 1
            
            # Log individual user move
            try:
                self.db.add_entry(user_id, btn_input)
            except Exception as e:
                Logger.error("Failed to log move to database: %s", e)
            
            moves_string = ""
            for key, value in self.moves_this_round.items():
                moves_string += f'{key} : {value}\n'
                
            reply_string = f'(DEMOCRACY) Submitted move input for {btn_input}. \n current tally is:\n{moves_string}'
            Logger.info(reply_string)
            return reply_string
        else:
            # Log individual user move in anarchy mode
            try:
                self.db.add_entry(user_id, btn_input)
            except Exception as e:
                Logger.error("Failed to log move to database: %s", e)
            
            self.pyboy.button(btn_input,2)
            reply_string = f'(ANARCHY) Submitted move input for {btn_input}.'
            Logger.info("%s for user %s", reply_string, user_id)
            return reply_string

    def save(self):
        with open('saves/save.state', 'wb') as f:
            self.pyboy.save_state(f)
    
    def set_mode(self, democracy=True):
        self.is_democracy = democracy

instance = Player()
    
