import os
import time
import re
import pyautogui
from itertools import permutations
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LOG_DIRECTORY = r"C:\Users\ZMENIT\.lunarclient\logs\game" # místo ZMENIT musíte dát jméno svého počítače.

print("Made by QUIK")

class LogMonitorHandler(FileSystemEventHandler):
    def __init__(self, log_file):
        self.log_file = log_file
        self.last_activation = 0
        self.cooldown = 10
        self.last_expression = ""
        self.last_keyword = ""
        self.last_scramble = ""

    def find_correct_word(self, scrambled_word):
        scrambled_lower = scrambled_word.lower()
        for item in MINECRAFT_ITEMS:
            if sorted(scrambled_lower) == sorted(item.lower()):
                return item
        return None

    def on_modified(self, event):
        if event.src_path != self.log_file:
            return
        
        try:
            with open(self.log_file, 'r', encoding='utf-8', errors='replace') as file:
                lines = file.readlines()
                for line in lines[-5:]:
                    
                    match_math = re.search(r"vyřeší '(\d+ [+\-*/] \d+)'", line)
                    if match_math and time.time() - self.last_activation > self.cooldown:
                        expression = match_math.group(1)
                        
                        if expression == self.last_expression:
                            continue
                        
                        try:
                            result = eval(expression)
                            if isinstance(result, float) and result.is_integer():
                                result = int(result)
                        except ZeroDivisionError:
                            result = 0

                        print(f"Detekován příklad: {expression}, Výsledek: {result}")
                        self.last_activation = time.time()
                        self.last_expression = expression

                        time.sleep(2)
                        pyautogui.press('t')
                        time.sleep(0.2)
                        pyautogui.write(str(result), interval=0.1)
                        pyautogui.press('enter')
                    
                    # A - Z
                    match_keyword = re.search(r"První, kdo napíše '([A-Za-z]+)' vyhrává!", line)
                    if match_keyword:
                        keyword = match_keyword.group(1)
                        
                        if keyword == self.last_keyword:
                            continue
                        
                        print(f"Detekována výzva: {keyword}")
                        self.last_keyword = keyword

                        time.sleep(1)
                        pyautogui.press('t')
                        time.sleep(0.2)
                        pyautogui.write(keyword, interval=0.1)
                        pyautogui.press('enter')
                    
                    # Seskládá a dešifruje
                    match_scramble = re.search(r"První, kdo seskládá & dešifruje '(.+?)' zpátky do správného tvaru vyhrává!", line)
                    if match_scramble:
                        scrambled_word = match_scramble.group(1)
                        correct_word = self.find_correct_word(scrambled_word)
                        
                        if not correct_word or correct_word == self.last_scramble:
                            continue
                        
                        print(f"Detekována výzva na dešifrování: {scrambled_word} -> {correct_word}")
                        self.last_scramble = correct_word

                        time.sleep(3)
                        pyautogui.press('t')
                        time.sleep(0.2)
                        pyautogui.write(correct_word, interval=0.1)
                        pyautogui.press('enter')
        
        except Exception as e:
            print(f"Chyba při čtení logu: {e}")


def find_latest_log():
    try:
        log_files = [f for f in os.listdir(LOG_DIRECTORY) if f.endswith('.log')]
        if not log_files:
            print("Nenalezen žádný log soubor.")
            return None
        return os.path.join(LOG_DIRECTORY, max(log_files, key=lambda f: os.path.getmtime(os.path.join(LOG_DIRECTORY, f))))
    except Exception as e:
        print(f"Chyba při hledání log souboru: {e}")
        return None


def start_monitoring():
    latest_log = find_latest_log()
    if not latest_log:
        return
    
    event_handler = LogMonitorHandler(latest_log)
    observer = Observer()
    observer.schedule(event_handler, path=LOG_DIRECTORY, recursive=False)
    observer.start()
    print("Monitorování spuštěno. Pro ukončení stiskněte Ctrl+C.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

MINECRAFT_ITEMS = {
    "Red Concrete", "Barrier", "Stone", "Grass Block", "Diamond", "Gold Ingot", "Iron Pickaxe", "Emerald",
    "Wood", "Cobblestone", "Iron Ore", "Gold Ore", "Coal", "Lapis Lazuli", "Obsidian", "Enchanted Book",
    "Netherite Ingot", "TNT", "Elytra", "Ender Pearl", "Blaze Powder", "Potion of Strength", "Fishing Rod",
    
    "Sand", "Dirt", "Oak Planks", "Spruce Planks", "Birch Planks", "Jungle Planks", "Acacia Planks", "Dark Oak Planks",
    "Stone Brick", "Quartz", "Glowstone", "Sea Lantern", "End Stone", "Dragon Egg", "Shulker Box", "Compass",
    "Clock", "Bed", "Chest", "Furnace", "Anvil", "Enchanting Table", "Hopper", "Minecart", "Rails", "Snow Block",
    "Melon", "Pumpkin", "Water Bucket", "Lava Bucket", "Bucket", "Milk Bucket", "Flower Pot", "Iron Door",
    "Wooden Door", "Lever", "Redstone", "Redstone Torch", "Observer", "Piston", "Sticky Piston", "Spawner",
    "Command Block", "Nether Portal", "End Portal", "Fire Charge", "Cake", "Bread", "Cooked Beef", "Cooked Porkchop",
    "Cooked Mutton", "Cooked Chicken", "Cooked Rabbit", "Golden Apple", "Enchanted Golden Apple", "Mushroom Stew",
    
    "Carrot", "Potato", "Baked Potato", "Golden Carrot", "Beetroot", "Beetroot Soup", "Raw Beef", "Raw Porkchop",
    "Raw Mutton", "Raw Chicken", "Raw Rabbit", "Rotten Flesh", "Spider Eye", "Fermented Spider Eye", "Gunpowder",
    "Ender Eye", "Slime Ball", "Snowball", "Bone", "Bone Meal", "String", "Feather", "Arrow", "Spectral Arrow",
    "Tipped Arrow", "Trident", "Saddle", "Name Tag", "Lead", "Totem of Undying", "Shield", "Crossbow",
    "Bow", "Flint and Steel", "Shears", "Carrot on a Stick", "Warped Fungus on a Stick", "Spyglass", "Map",
    "Book", "Paper",
    
    "Fletching Table", "Cartography Table", "Loom", "Smithing Table", "Grindstone", "Lectern", "Jukebox",
    "Note Block", "Crafting Table", "Brewing Stand", "Cauldron", "Barrel", "Smoker", "Blast Furnace", "Campfire",
    
    "Red Bed", "Blue Bed", "Green Bed", "Yellow Bed", "Black Bed", "White Bed", "Brown Bed", "Orange Bed",
    "Magenta Bed", "Light Blue Bed", "Pink Bed", "Lime Bed", "Gray Bed", "Light Gray Bed", "Cyan Bed", "Purple Bed",
    
    "Green Concrete", "Blue Concrete", "Yellow Concrete", "Black Concrete", "White Concrete", "Gray Concrete",
    "Magenta Concrete", "Lime Concrete", "Pink Concrete", "Light Blue Concrete", "Cyan Concrete", "Purple Concrete",
    "Brown Concrete",
    
    "Red Stained Glass", "Blue Stained Glass", "Green Stained Glass", "Yellow Stained Glass", "Black Stained Glass",
    "White Stained Glass", "Glass", "Stained Glass Pane",
    
    "Terracotta", "Glazed Terracotta", "Concrete Powder",
    
    "Diorite", "Andesite", "Granite", "Polished Diorite", "Polished Andesite", "Polished Granite",
    
    "Nether Quartz Ore", "Ancient Debris", "Blackstone", "Polished Blackstone", "Cracked Polished Blackstone",
    "Chiseled Polished Blackstone", "Crying Obsidian", "Respawn Anchor", "Bedrock",
    
    "Obsidian", "Redstone Block", "Iron Block", "Gold Block", "Diamond Block", "Emerald Block", "Lapis Block",
    "Coal Block", "Netherite Block", "Copper Block", "Exposed Copper", "Weathered Copper", "Oxidized Copper",
    "Cut Copper", "Waxed Copper Block", "Waxed Exposed Copper", "Waxed Weathered Copper", "Waxed Oxidized Copper",
    
    "Bamboo", "Bamboo Block", "Bamboo Mosaic", "Bee Nest", "Beehive", "Campfire", "Lava", "Water", "Powder Snow",
    "Scaffolding", "Chain", "Target", "Candle", "Soul Candle", "Copper Lightning Rod", "Bell",
    
    "Repeater", "Comparator", "Activator Rail", "Detector Rail", "Daylight Detector", "Soul Campfire", "Soul Lantern",
    
    "Banner", "Shield", "Armor Stand", "Item Frame", "Glow Item Frame", "Snow Golem", "Iron Golem", "Rabbit",
    
    "Chicken Spawn Egg", "Cow Spawn Egg", "Pig Spawn Egg", "Sheep Spawn Egg", "Zombie Spawn Egg", "Skeleton Spawn Egg",
    "Creeper Spawn Egg", "Spider Spawn Egg", "Enderman Spawn Egg",
    
    "Potion of Healing", "Potion of Regeneration", "Potion of Swiftness", "Potion of Fire Resistance",
    "Potion of Water Breathing", "Potion of Invisibility", "Potion of Night Vision", "Potion of Poison",
    
    "End Crystal", "Shulker Shell", "Banner Pattern", "Suspicious Stew", "Honey Bottle", "Honey Block",
    
    "13", "Cat", "Blocks", "Chirp", "Far", "Mall", "Mellohi", "Stal", "Strad", "Ward", "11", "Wait"
}

if __name__ == "__main__":
    start_monitoring()
