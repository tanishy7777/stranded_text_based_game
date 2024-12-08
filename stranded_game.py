import msvcrt
import os
import shutil
from colorama import init, Fore, Back, Style
import random
import time
import contextlib
with contextlib.redirect_stdout(None):
    import pygame



pygame.mixer.init()




def play_music(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(loops=1)  # Loop indefinitely

def play_sound_effect(file_path):
    sound = pygame.mixer.Sound(file_path)
    sound.play()

def stop_music():
    pygame.mixer.music.stop()

def switch_music(new_music_path):
    stop_music()
    play_music(new_music_path)

init()


class Player:
    def __init__(self):
        self.name = None
        self.health = 100
        self.items = []
        self.location = "crash site"
        self.ally = None
        self.village_reputation = "neutral"  # neutral, trusted, or hostile
        self.orb_status = None  # "stolen", "protected", or None
        self.temple_knowledge = False  # Whether player knows about the temple

    def take_damage(self, damage):
        play_sound_effect('audio/damage.mp3')
        self.health -= damage
        if self.health <= 0:
            print(
                f"\n{Fore.RED}Your vision fades to black... You have succumbed to the dangers of the island.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}♥ {self.name}'s health: {self.health}{Style.RESET_ALL}")

    def heal(self, amount):
        play_sound_effect('audio/heal.mp3')
        self.health = min(100, self.health + amount)
        print(f"\n{Fore.GREEN}♥ {self.name}'s health restored to: {self.health}{Style.RESET_ALL}")

    def add_item(self, item):
        self.items.append(item)
        play_sound_effect('audio/clink.mp3')
        print(f"\n{Fore.YELLOW}[!] You acquired: {item}{Style.RESET_ALL}")

    def self_heal(self):
        print(f'{Fore.CYAN}"chocolates" heals {Fore.RED}5 ♥{Style.RESET_ALL}\n'
                   f'{Fore.CYAN}"first aid kit" heals {Fore.RED}30 ♥{Style.RESET_ALL}\n'
                   f'{Fore.CYAN}"protein bars" heal {Fore.RED}10 ♥{Style.RESET_ALL}\n'
                   f'{Fore.CYAN}"water bottle" heals {Fore.RED}5 ♥{Style.RESET_ALL}')

        print(f"\n{Fore.GREEN}Type \"info\" to see the player inventory and other information{Style.RESET_ALL}")
        item = input("Choose an item to heal from your inventory: ")

        if item == "chocolates":
            if item in self.items:
                self.heal(5)
                self.use_item(item)
            else:
                print("Item not found in inventory, type info to check inventory")
        elif item == "water bottle":
            if item in self.items:
                self.heal(5)
                self.use_item(item)
            else:
                print("Item not found in inventory, type info to check inventory")
        elif item == "protein bars":
            if item in self.items:
                self.heal(10)
                self.use_item(item)
            else:
                print("Item not found in inventory, type info to check inventory")
        elif item == "first aid kit":
            if item in self.items:
                self.heal(30)
                self.use_item(item)
            else:
                print("Item not found in inventory, type info to check inventory")
        else:
            print("choose an item that can heal")


    def use_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def print_status(self):
        play_sound_effect('audio/pop_info.mp3')
        width = 50

        print(f"{Fore.CYAN}chocolates heals {Fore.RED}5 ♥{Style.RESET_ALL}\n"
                   f"{Fore.CYAN}first aid kit heals {Fore.RED}30 ♥{Style.RESET_ALL}\n"
                   f"{Fore.CYAN}protein bars heal {Fore.RED}10 ♥{Style.RESET_ALL}\n"
                   f"{Fore.CYAN}water bottle heals {Fore.RED}5 ♥{Style.RESET_ALL}"
                   f"{Fore.GREEN}type heal to choose an item to heal{Style.RESET_ALL}")


        # Border style
        border = f"{Fore.BLUE}║{Style.RESET_ALL}"
        top_border = f"{Fore.BLUE}╔{'═' * (width - 2)}╗{Style.RESET_ALL}"
        bottom_border = f"{Fore.BLUE}╚{'═' * (width - 2)}╝{Style.RESET_ALL}"
        mid_border = f"{Fore.BLUE}╠{'═' * (width - 2)}╣{Style.RESET_ALL}"
        sub_border = f"{Fore.BLUE}╟{'─' * (width - 2)}╢{Style.RESET_ALL}"

        # Top border with character info
        print(top_border)
        print(f"{border}{Fore.YELLOW}{self.name.center(width - 2)}{Style.RESET_ALL}{border}")

        # Health bar
        health_filled = '█' * (self.health // 5)
        health_empty = '░' * (20 - self.health // 5)
        health_color = Fore.GREEN if self.health > 60 else Fore.YELLOW if self.health > 30 else Fore.RED
        health_bar = f"HP: {health_color}{health_filled}{Fore.WHITE}{health_empty} {self.health:>3}%"
        print(f"{border}{health_bar}{' ' * (width - 31)}{Style.RESET_ALL}{border}")
        print(mid_border)

        # Items section
        print(f"{border}{Fore.CYAN} INVENTORY:{' ' * (width - 12)}{Style.RESET_ALL}{border}")
        print(sub_border)
        if not self.items:
            print(f"{border}{Fore.WHITE}     [Your bag is empty]{' ' * (width - 25)}{Style.RESET_ALL}{border}")
        else:
            for item in self.items:
                item_str = f"  {Fore.GREEN}•{Fore.WHITE} {str(item)}"
                print(f"{border}{item_str:<{width - 2}}{Style.RESET_ALL}{border}")

        # Allies section
        print(mid_border)
        print(f"{border}{Fore.CYAN} ALLIES:{' ' * (width - 9)}{Style.RESET_ALL}{border}")
        print(sub_border)
        if not self.ally:
            print(f"{border}{Fore.WHITE}     [Traveling alone]{' ' * (width - 23)}{Style.RESET_ALL}{border}")
        else:
            if self.ally:
                ally_str = f"  {Fore.BLUE}♦{Fore.WHITE} {str(self.ally)}{Style.RESET_ALL}"
                print(f"{border}{ally_str:<{width - 2}}{Style.RESET_ALL}{border}")



        # Bottom border
        print(bottom_border)


def slow_print(text, delay=0.02):
    """Print text slowly for dramatic effect"""

    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

    print()

def center_text(text):
    terminal_width = shutil.get_terminal_size().columns
    lines = text.split('\n')
    centered_lines = [line.center(terminal_width) for line in lines]
    return '\n'.join(centered_lines)

def introduction(player):
    play_music("audio/intro.mp3")

    title = """
    ███████╗████████╗██████╗  █████╗ ███╗   ██╗██████╗ ███████╗██████╗ 
    ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔════╝██╔══██╗
    ███████╗   ██║   ██████╔╝███████║██╔██╗ ██║██║  ██║█████╗  ██║  ██║
    ╚════██║   ██║   ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██╔══╝  ██║  ██║
    ███████║   ██║   ██║  ██║██║  ██║██║ ╚████║██████╔╝███████╗██████╔╝
    ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═════╝ 
        """

    # Smaller ASCII art for START and README options
    start_ascii = """
     ██████╗████████╗ █████╗ ██████╗ ████████╗   ██████╗ ███████╗ █████╗ ██████╗ ███╗   ███╗███████╗
    ╚█████╗    ██║   ███████║██══██╔╝   ██║      ██████╔╝█████╗  ███████║██║  ██║██╔████╔██║█████╗ 
    ██████╔╝   ██║   ██║  ██║██║  ██║   ██║      ██║  ██║███████╗██║  ██║██████╔╝██║ ╚═╝ ██║███████╗
    ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝      ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚══════╝
    
        """

    readme_ascii = f"""
    IMP!!!: Whenever something is being printed on the screen dont press other keys
    otherwise it will be registered as your input for the next choice
    
    {Fore.CYAN}Game made by Tanish Yelgoe(23110328)
    """

    # Clear screen and display centered title
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.CYAN}{center_text(title)}{Style.RESET_ALL}")

    while True:
        print(f"\n{Fore.GREEN}{start_ascii}{Style.RESET_ALL}", end="  ")
        print(f"\n{Fore.RED}{readme_ascii}{Style.RESET_ALL}", end="  ")

        print(
            f"\n{Fore.YELLOW}Choose your option ({Fore.RED}start{Fore.YELLOW} or {Fore.RED}readme{Fore.YELLOW}):{Style.RESET_ALL}")

        choice = input("--> ").lower().strip()

        if choice == "readme":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{Fore.CYAN}=== STRANDED - A Survival Adventure ==={Style.RESET_ALL}")
            print(f"""
    {Fore.YELLOW}Welcome to STRANDED, a text-based survival adventure game where your choices matter.
    You find yourself marooned on a mysterious island after a plane crash.
    Explore the island, solve puzzles, survive the elements, and uncover the island's ancient secrets.
    
    
    IMP!!!: Whenever something is being printed on the screen dont press other keys
    otherwise it will be registered as your input for the next choice

    Commands:
    - Type 'info' to check your inventory and status
    - Type 'heal' to use healing items
    - Follow on-screen prompts to make choices
    
    Key Features:
    - Dynamic inventory system
    - Health management
    - Multiple endings based on your choices
    - Ancient mysteries to uncover
    - Survival mechanics

    Are you ready to begin your adventure?{Style.RESET_ALL}
    """)
            input(f"{Fore.CYAN}Press Enter to return to menu...{Style.RESET_ALL}")
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{Fore.CYAN}{center_text(title)}{Style.RESET_ALL}")

        elif choice == "start":
            os.system('cls' if os.name == 'nt' else 'clear')


            slow_print(f"{Fore.YELLOW}The sound of crashing waves fills your ears...{Style.RESET_ALL}")
            time.sleep(1)
            slow_print("""
            You wake up disoriented, your head throbbing. The acrid smell of smoke fills your nostrils
            as you push yourself up from the warm sand. Around you lies the wreckage of what was once
            your plane. The tropical sun beats down mercilessly as you try to piece together what happened.
        
            The last thing you remember was a flash of lightning, the plane lurching violently,
            and then... darkness. Now you're here, somehow alive, on what appears to be an uncharted island.
        
            But something feels different about this place. The air seems to pulse with an ancient energy,
            and in the distance, through the thick jungle canopy, you catch a glimpse of what appears to
            be stone structures. This is no ordinary island...""")



            slow_print("What is your name?")
            name = input("--> ")
            player.name = name
            play_sound_effect('./audio/pop_info.mp3')
            player.print_status()

            print(f"\n{Fore.CYAN}Type {Fore.RED}\"info\"{Fore.CYAN} to see the player inventory and other information or type {Fore.RED}\"heal\"{Fore.CYAN} to heal yourself{Style.RESET_ALL}")
            break


def explore_crash_site(player, visited_choices=None):
    if visited_choices is None:
        # switch_music('./crash_site.mp3')
        visited_choices = set()

        slow_print(f"\n{Fore.CYAN}--- The Crash Site ---{Style.RESET_ALL}")
        slow_print("""
        The wreckage of the plane is scattered across the beach. Smoke still rises from the
        fuselage, and the waves lap at pieces of metal and luggage. You need to act quickly
        before night falls.""")

        print(f"""{Fore.RED}
        IMP!!!: Whenever something is being printed on the screen dont press other keys
        otherwise it will be registered as your input for the next choice
        {Style.RESET_ALL}""")


    available_choices = {
        "1": "Search the plane's cabin for supplies",
        "2": "Check the scattered debris on the beach",
        "3": "Investigate the partially intact cockpit",
        "4": "Try to find other survivors",
        "5": "Do nothing and survive the night"
    }

    # Filter out already visited choices
    available_choices = {key: val for key, val in available_choices.items() if key not in visited_choices}

    slow_print("\nWhat would you like to do?")
    for key, action in available_choices.items():
        print(f"{key}. {action}")

    slow_print(f"\n{Fore.CYAN}Type {Fore.RED}\"info\"{Fore.CYAN} to see the player inventory and other information or type {Fore.RED}\"heal\"{Fore.CYAN} to heal yourself{Style.RESET_ALL}")
    choice = input(f"{Fore.GREEN}Choose your action ({', '.join(available_choices.keys())}):{Style.RESET_ALL} ").strip()


    if choice in visited_choices:
        slow_print(f"{Fore.RED}You've already done that. Choose something else!{Style.RESET_ALL}")
        return explore_crash_site(player, visited_choices)

    if choice == "1" or choice =="2" or choice =="3" or choice =="4" or choice =="5":
        visited_choices.add(choice)

    if choice == "1":
        play_sound_effect('./audio/thud.mp3')
        slow_print("\nYou carefully make your way into the cabin, pushing aside fallen overhead compartments.")
        time.sleep(1)
        player.add_item("flashlight")
        player.add_item("lighter")
        player.add_item("knife")
        player.add_item("compass")
        player.add_item("chocolates")
        slow_print("These supplies could prove invaluable for survival.")

    elif choice == "2":
        # play_sound_effect('audio/clink.mp3')
        play_sound_effect('./audio/debirs.mp3')
        slow_print("\nYou wade through the scattered debris, keeping an eye out for anything useful.")
        time.sleep(1)
        player.add_item("water bottle")
        player.add_item("protein bars")
        player.add_item("rope")

    elif choice == "3":
        slow_print("\nYou approach the cockpit cautiously. The metal groans under your weight...")
        play_sound_effect('./audio/metal.mp3')
        if random.random() < 0.5:
            slow_print(
                f"{Fore.RED}The structure suddenly gives way! You barely escape, but not unscathed.{Style.RESET_ALL}")
            player.take_damage(10)
        else:
            slow_print("You find a first aid kit and emergency flares.")
            player.add_item("first aid kit")
            player.add_item("flares")

    elif choice == "4":
        slow_print("\nYou search the area, calling out for survivors...")
        slow_print(f"\n{Fore.GREEN}You find Maya, the flight attendant, unconscious but alive!{Style.RESET_ALL}")
        player.ally = "Maya"
        slow_print("She knows basic first aid and will be a valuable ally.")
        player.heal(20)


    elif choice == "5":
        play_sound_effect('audio/yawn.mp3')
        slow_print("\nYou decide to conserve your energy and hunker down for the night.")
        slow_print("The night is long and cold, but you manage to survive unscathed.")
        return

    elif choice == "info":
        player.print_status()
    elif choice == "heal":
        player.self_heal()

    # If all choices except "5" are visited, end the exploration
    if len(visited_choices) == 5:
        slow_print(f"{Fore.YELLOW}You've explored all you can at the crash site. Time to move on.{Style.RESET_ALL}")
        return

    # Offer the player to continue exploring or not
    next_action = input(f"{Fore.GREEN}Do you want to explore more? (yes/no):{Style.RESET_ALL} ").strip().lower()
    while next_action not in ["yes", "no", "n", "y", "ye"]:
        print("info or other command wont work here only yes or no")
        next_action = input(f"{Fore.GREEN}Do you want to explore more? (yes/no):{Style.RESET_ALL} ").strip().lower()

    if next_action in ("yes", "y", "ye"):
        explore_crash_site(player, visited_choices)
    else:
        slow_print(f"{Fore.YELLOW}You decide to leave the crash site and prepare for the challenges ahead.{Style.RESET_ALL}")
        return

def survive_first_night(player):
    play_music('audio/Katawaredoki.mp3')
    print(f"\n{Fore.CYAN}--- As Night Falls ---{Style.RESET_ALL}")
    slow_print("""
    The sun begins to set, painting the sky in brilliant oranges and purples. But with
    the beauty comes danger. Strange sounds emerge from the jungle, and the temperature
    begins to drop. You need to prepare for the night.""")

    print(f"""{Fore.RED}
            IMP!!!: Whenever something is being printed on the screen dont press other keys
            otherwise it will be registered as your input for the next choice
            {Style.RESET_ALL}""")

    print("""
    What will you do?
    1. Build a shelter and fire on the beach
    2. Search for a cave or natural shelter
    3. Climb a tree to stay safe from predators
    4. Keep moving and try to find civilization
    """)

    print(f"\n{Fore.CYAN}Type {Fore.RED}\"info\"{Fore.CYAN} to see the player inventory and other information or type {Fore.RED}\"heal\"{Fore.CYAN} to heal yourself{Style.RESET_ALL}")
    choice = input(f"{Fore.GREEN}Choose your action (1-4):{Style.RESET_ALL} ").strip()

    if choice == "1":
        if "lighter" in player.items:
            play_sound_effect('./audio/Campfire.mp3')
            slow_print("\nYou gather driftwood and use your lighter to start a fire.")
            slow_print("The warmth and light keep the wildlife at bay, allowing you to rest safely.")
            player.heal(10)
        else:
            play_sound_effect('./audio/scary_night.mp3')
            slow_print(
                f"{Fore.RED}Without a lighter, starting a fire proves difficult. The night is cold and dangerous.{Style.RESET_ALL}")
            player.take_damage(5)

    elif choice == "2":
        slow_print("\nYou search the coastline and find a small cave...")
        if "flashlight" in player.items:
            slow_print("Your flashlight reveals it's safe and unoccupied.")
            player.heal(5)
        else:
            play_sound_effect('./audio/scary_night.mp3')
            slow_print(f"{Fore.RED}In the darkness, you disturb a nest of aggressive bats!{Style.RESET_ALL}")
            player.take_damage(10)

    elif choice == "3":
        if player.ally:
            slow_print("\nMaya helps you find a sturdy tree and secure yourselves safely.")
            player.heal(5)
        else:
            play_sound_effect('./audio/scary_night.mp3')
            slow_print(f"{Fore.RED}You slip while climbing in the darkness, injuring yourself.{Style.RESET_ALL}")
            player.take_damage(10)

    elif choice == "4":
        play_sound_effect('./audio/scary_night.mp3')
        slow_print(
            f"{Fore.RED}Walking in the dark proves dangerous. You stumble several times and attract predators.{Style.RESET_ALL}")
        player.take_damage(10)
    elif choice == "info":
        player.print_status()
        survive_first_night(player)

    elif choice == "heal":
        player.self_heal()
        survive_first_night(player)

    else:
        survive_first_night(player)

def jungle_exploration(player, visited_choices=None):
    if visited_choices is None:
        play_music('audio/jungle.mp3')
        visited_choices = set()

        print(f"\n{Fore.CYAN}--- Into the Jungle ---{Style.RESET_ALL}")
        slow_print("""
        As dawn breaks, you know you can't stay at the crash site forever. The dense jungle
        before you holds both danger and the possibility of rescue. Strange stone structures
        peek through the canopy in the distance...""")

        print(f"""{Fore.RED}
                IMP!!!: Whenever something is being printed on the screen dont press other keys
                otherwise it will be registered as your input for the next choice
                {Style.RESET_ALL}""")

    available_choices = {
        "1": "Follow a faint trail through the undergrowth",
        "2": "Use the compass to maintain a straight course",
        "3": "Climb to high ground for a better view",
        "4": "Make noise to attract attention"
    }

    # Filter out already visited choices
    available_choices = {key: val for key, val in available_choices.items() if key not in visited_choices}

    # Stop exploration if all choices are exhausted
    if not available_choices:
        slow_print(f"{Fore.YELLOW}You have explored all available options in the jungle. Time to move on.{Style.RESET_ALL}")
        return

    print("\nHow will you proceed?")
    for key, action in available_choices.items():
        print(f"{key}. {action}")

    print(f"\n{Fore.CYAN}Type {Fore.RED}\"info\"{Fore.CYAN} to see the player inventory and other information or type {Fore.RED}\"heal\"{Fore.CYAN} to heal yourself{Style.RESET_ALL}")
    choice = input(f"{Fore.GREEN}Choose your action ({', '.join(available_choices.keys())}):{Style.RESET_ALL} ").strip()

    if (choice not in available_choices) and (choice != "info") and (choice != "heal"):
        print(choice)
        print(choice not in available_choices)
        print(available_choices)
        print(f"{Fore.RED}Invalid choice or already visited. Please choose again.{Style.RESET_ALL}")
        return jungle_exploration(player, visited_choices)

    if choice == "1" or choice =="2" or choice =="3" or choice =="4":
        visited_choices.add(choice)

    if choice == "1":
        play_sound_effect('./audio/footsteps.mp3')
        slow_print("\nYou follow the trail, noticing it becomes more defined...")
        if player.ally:
            slow_print(f"{Fore.GREEN}Maya recognizes some markings - these are made by humans!{Style.RESET_ALL}")
            player.location = "village outskirts"
            return
        else:
            play_sound_effect('./audio/creepy_animal_noises.mp3')
            slow_print("The path winds deeper into the jungle. You hear distant voices...")
            player.location = "lost in jungle"

    elif choice == "2":
        if "compass" in player.items:
            slow_print("\nYou maintain a steady course north, avoiding walking in circles.")
            player.location = "village outskirts"
            return
        else:
            play_sound_effect('./audio/creepy_animal_noises.mp3')
            slow_print(f"{Fore.RED}Without a compass, you wander in circles, becoming exhausted. You hear distant voices{Style.RESET_ALL}")
            player.take_damage(15)
            player.location = "lost in jungle"

    elif choice == "3":
        slow_print("\nYou find a tall hill and begin climbing...")
        if random.random() < 0.7:
            slow_print(f"{Fore.GREEN}From the top, you spot smoke from what must be a village!{Style.RESET_ALL}")
            player.location = "village outskirts"
            return
        else:
            play_sound_effect('./audio/landslide.mp3')
            slow_print(f"{Fore.RED}You lose your footing and tumble down the slope!{Style.RESET_ALL}")
            player.take_damage(25)
            player.location = "lost in jungle"

    elif choice == "4":
        slow_print("\nYou call out and make noise, hoping to attract attention...")
        if random.random() < 0.3:
            slow_print(f"{Fore.GREEN}Your calls are answered by friendly voices!{Style.RESET_ALL}")
            player.location = "village outskirts"
            return
        else:
            play_sound_effect('./audio/creepy_animal_noises.mp3')
            slow_print(f"{Fore.RED}Your noise attracts a hostile predator!{Style.RESET_ALL}")
            player.take_damage(10)
            player.location = "lost in jungle"

    elif choice == "info":
        player.print_status()

    elif choice == "heal":
        player.self_heal()

    jungle_exploration(player, visited_choices)

def village_encounter(player, visited_choices=None):
    if player.health < 0:
        return

    if visited_choices is None:
        visited_choices = set()
        switch_music('audio/crash_site.mp3')

        print(f"\n{Fore.CYAN}--- The Village of Kalan'tai ---{Style.RESET_ALL}")
        slow_print("""
        You emerge from the jungle into a clearing where a village stands. The architecture
        is unlike anything you've seen - a blend of ancient stone structures and wooden huts.
        The villagers, dressed in colorful traditional garments, notice your approach...
        """)

        print(f"""{Fore.RED}
                IMP!!!: Whenever something is being printed on the screen dont press other keys
                otherwise it will be registered as your input for the next choice
                {Style.RESET_ALL}""")

    available_choices = {
        "1": "Raise your hands in peaceful greeting",
        "2": "Offer items from your inventory as gifts",
        "3": "Try to communicate that you need help",
        "4": "Demonstrate modern technology to impress them"
    }

    # Filter out already visited choices
    available_choices = {key: val for key, val in available_choices.items() if key not in visited_choices}

    # Stop interaction if all choices are exhausted
    if not available_choices:
        slow_print("\nYou have exhausted all options with the villagers. They seem to make their judgment of you.")
        return

    print("Choices:")
    for key, description in available_choices.items():
        print(f"{key}. {description}")

    choice = input(f"{Fore.GREEN}Choose your action ({'/'.join(available_choices.keys())}):{Style.RESET_ALL} ").strip()

    if (choice not in available_choices) and (choice != "info") and (choice != "heal"):
        print("\nInvalid choice or already tried. Please choose again.")
        return village_encounter(player, visited_choices)

    if choice == "1" or choice =="2" or choice =="3" or choice =="4":
        visited_choices.add(choice)

    if choice == "1":
        slow_print("\nThe villagers respond positively to your peaceful gesture.")
        if player.ally:
            slow_print(
                f"{Fore.GREEN}Maya helps bridge the communication gap, making the interaction smoother.{Style.RESET_ALL}")
            player.village_reputation = "trusted"
            player.heal(10)
        else:
            player.village_reputation = "neutral"
        return

    elif choice == "2":
        if "chocolates" in player.items:
            item = "chocolates"
            player.use_item(item)
            slow_print(f"\nYou offer your {item} as a gift. The villagers are intrigued.")
            player.village_reputation = "trusted"
            return
        else:
            slow_print(f"{Fore.RED}With nothing to offer, the villagers remain suspicious.{Style.RESET_ALL}")
            player.village_reputation = "neutral"

    elif choice == "3":
        if player.ally:
            slow_print("\nMaya helps explain your situation. The villagers offer help and shelter.")
            player.village_reputation = "trusted"
            player.heal(20)
            return
        else:
            slow_print("Through gestures, you manage to convey your need for help. But the villagers dont seem to understand your situation")
            player.village_reputation = "neutral"

    elif choice == "4":
        if "flashlight" in player.items or "lighter" in player.items:
            slow_print(f"{Fore.RED}The villagers react with fear to your 'magic'. Guards approach!{Style.RESET_ALL}")
            player.village_reputation = "hostile"
            player.take_damage(20)
        else:
            slow_print("Without any technology to show, you stand awkwardly.")
            player.village_reputation = "neutral"

    elif choice == "info":
        player.print_status()

    elif choice == "heal":
        player.self_heal()

    # Recursively call until all choices are exhausted
    village_encounter(player, visited_choices)



def temple_quest(player):

    def introduction():
        slow_print(f"""
        You gain the trust of the villagers and they tell you about a sacred temple. You embark on you journey to the sacred temple.
        And explore what it has to offer. As you walk through the jungle you see a huge silhouette, surrounded by fog. As you 
        reach closer you see a huge temple entrance.
         
        You are about to embark on a perilous journey into the Sacred Temple, where the legendary Orb awaits.
        Only the clever and brave survive here. Your tools are limited, your life is fragile, and the temple is full of traps.
        Can you emerge victorious and claim the Orb?
        """)

        slow_print(f"\n{Fore.CYAN}Type {Fore.RED}\"info\"{Fore.CYAN} to see the player inventory and other information or type {Fore.RED}\"heal\"{Fore.CYAN} to heal yourself{Style.RESET_ALL}")

    def temple_entrance(player, visited_choices=None):
        if player.health < 0:
            return

        if visited_choices is None:
            visited_choices = set()
            slow_print(f"\n{Fore.CYAN}--- Entering the Temple: A Riddle of Passage ---{Style.RESET_ALL}")
            slow_print("""
            The massive stone door is locked, bearing an inscription:
            'I am not alive, but I grow;
            I don't have lungs, but I need air;
            I don't have a mouth, but water kills me. What am I?'
            """)

        available_choices = {
            "1": "A plant 🌱",
            "2": "A flame 🔥",
            "3": "A shadow 🌑",
            "4": "A whisper 💨",
            "5": "Use the knife to try and pry open the door"
        }

        available_choices = {key: val for key, val in available_choices.items() if key not in visited_choices}

        if not available_choices:
            print("\nYou have tried every option. The temple stands resolved, and you decide to move on.")
            return

        slow_print("Choices:")
        for key, description in available_choices.items():
            slow_print(f"{key}. {description}")

        choice = input("Choose an option ({}): ".format("/".join(available_choices.keys()))).strip()
        slow_print(f"\n{Fore.CYAN}Type {Fore.RED}\"info\"{Fore.CYAN} to see the player inventory and other information or type {Fore.RED}\"heal\"{Fore.CYAN} to heal yourself{Style.RESET_ALL}")

        if (choice not in available_choices) and (choice != "info") and (choice != "heal"):
            slow_print("\nInvalid choice or already tried. Please choose again.")
            return temple_entrance(player, visited_choices)

        if choice == "1" or choice == "2" or choice == "3" or choice == "4" or choice == "5":
            visited_choices.add(choice)

        if choice == "1":
            slow_print("\nThe door remains locked. A dart trap triggers!")
            player.take_damage(10)

        elif choice == "2":
            slow_print("\nThe door creaks open, revealing the temple's shadowy interior. You step inside.")
            return

        elif choice == "3":
            slow_print("\nThe door remains locked. A dart trap triggers!")
            player.take_damage(10)

        elif choice == "4":
            slow_print("\nThe door remains locked. A dart trap triggers!")
            player.take_damage(10)

        elif choice == "5":
            slow_print("\nYou attempt to pry open the door. A hidden blade swings out!")
            player.take_damage(15)

        elif choice == "info":
            player.print_status()
        elif choice == "heal":
            player.self_heal()

        temple_entrance(player, visited_choices)

    def maze_of_shadows(player, visited_choices=None):
        if player.health < 0:
            return

        if visited_choices is None:
            visited_choices = set()
            slow_print(f"\n{Fore.CYAN}--- The Maze of Shadows ---{Style.RESET_ALL}")

            slow_print("""
                    You enter a maze with dimly lit paths. A disembodied voice warns:
                    'Follow the shadows; light leads to peril.'
                    """)

        available_choices = {
            "1": "Follow the darker path",
            "2": "Follow the brighter path",
            "3": "Use the flashlight(check inventory by typing \"info\" to see if you have this item)"
        }

        available_choices = {key: val for key, val in available_choices.items() if key not in visited_choices}

        if not available_choices:
            print("\nYou have tried every option. The maze stands resolved, and you decide to move on.")
            return

        slow_print("Choices:")
        for key, description in available_choices.items():
            slow_print(f"{key}. {description}")

        choice = input("Choose an option ({}): ".format("/".join(available_choices.keys()))).strip()

        if (choice not in available_choices) and (choice != "info") and (choice != "heal"):
            slow_print("\nInvalid choice or already tried. Please choose again.")
            return maze_of_shadows(player, visited_choices)

        if choice == "1" or choice == "2" or choice == "3":
            visited_choices.add(choice)

        if choice == "1":
            slow_print("\nThe darker path leads you safely closer to the Orb.")
            return
        elif choice == "2":
            slow_print("\nThe brighter path crumbles beneath you. You fall into a pit trap!")
            player.take_damage(5)
        elif choice == "3":
            slow_print("\nYou use the flashlight to reveal both paths, but the temple spirits are angered!")
            player.take_damage(5)
        elif choice == "info":
            player.print_status()
        elif choice == "heal":
            player.self_heal()

        maze_of_shadows(player, visited_choices)

    def compass_room(player, visited_choices=None):
        if player.health < 0:
            return

        if visited_choices is None:
            visited_choices = set()
            slow_print(f"\n{Fore.CYAN}--- The Compass Room ---{Style.RESET_ALL}")

            slow_print("""
            You enter a circular chamber with four exits: North, South, East, and West.
            A compass rose is carved into the floor, spinning wildly.
            """)

        available_choices = {
            "1": "Use the compass to align with 'true North' (check inventory by typing \"info\" to see if you have this item)",
            "2": "Try each door manually",
            "3": "Search the room for hidden clues"
        }

        # Filter out already visited choices
        available_choices = {key: val for key, val in available_choices.items() if key not in visited_choices}

        # Stop interaction if all choices are exhausted
        if not available_choices:
            print("\nYou have explored every option in the compass room. The chamber grows quiet.")
            return

        slow_print("Choices:")
        for key, description in available_choices.items():
            slow_print(f"{key}. {description}")

        choice = input("Choose an option ({}): ".format("/".join(available_choices.keys()))).strip()

        if (choice not in available_choices) and (choice != "info") and (choice != "heal"):
            slow_print("\nInvalid choice or already tried. Please choose again.")
            return compass_room(player, visited_choices)

        if choice == "1" or choice == "2" or choice == "3":
            visited_choices.add(choice)

        if choice == "1":
            if "compass" in player.items:
                slow_print("\nThe compass aligns, pointing to the North door. It swings open.")
                player.use_item("compass")
                return
            else:
                slow_print("\nYou realize that you dont have a compass. You have do make a choice though")

        elif choice == "2":
            slow_print("\nYou try the doors one by one and find the way eventually but you trigger dart traps along the way!")
            player.take_damage(10)
            return
        elif choice == "3":
            slow_print("\nYou find a carving showing that 'North' is the correct exit.")
        elif choice == "info":
            player.print_status()
        elif choice == "heal":
            player.self_heal()

        # Recursively call until all choices are exhausted
        compass_room(player, visited_choices)

    def knife_in_mechanism(player, visited_choices=None):
        if player.health < 0:
            return

        if visited_choices is None:
            visited_choices = set()
            slow_print(f"\n{Fore.CYAN}--- Knife in the Mechanism ---{Style.RESET_ALL}")
            slow_print("""
            You encounter a heavy stone door with a slit in its center. An inscription reads:
            'Sacrifice your blade to proceed.'
            """)

        available_choices = {
            "1": "Insert the knife into the slit (check inventory by typing \"info\" to see if you have this item)",
            "2": "Try to push the door manually",
            "3": "Look for another path"
        }

        # Filter out already visited choices
        available_choices = {key: val for key, val in available_choices.items() if key not in visited_choices}

        # Stop interaction if all choices are exhausted
        if not available_choices:
            slow_print("\nYou have exhausted all options. The door remains closed.")
            return

        slow_print("Choices:")
        for key, description in available_choices.items():
            print(f"{key}. {description}")

        choice = input("Choose an option ({}): ".format("/".join(available_choices.keys()))).strip()

        if (choice not in available_choices) and (choice != "info") and (choice != "heal"):
            slow_print("\nInvalid choice or already tried. Please choose again.")
            return knife_in_mechanism(player, visited_choices)

        if choice == "1" or choice == "2" or choice == "3":
            visited_choices.add(choice)

        if choice == "1":
            if "knife" in player.items:
                slow_print("\nThe knife clicks into place, and the door slides open. You proceed, but lose your knife.")
                player.use_item("knife")
                return
            else:
                slow_print("\nYou realize that you dont have a knife. You have do make a choice though")
        elif choice == "2":
            slow_print("\nYou push against the door. The ceiling begins to descend!")
            player.take_damage(20)
        elif choice == "3":
            slow_print("\nYou search for another path but find none. Time is wasted, and random traps close in!")
            random_trap(player)
        elif choice == "info":
            player.print_status()
        elif choice == "heal":
            player.self_heal()

        # Recursively call until all choices are exhausted
        knife_in_mechanism(player, visited_choices)

    def light_and_orb_pedestal(player, visited_choices=None):
        if player.health < 0:
            return

        if visited_choices is None:
            visited_choices = set()
            slow_print(f"\n{Fore.CYAN}--- Light and the Orb's Pedestal ---{Style.RESET_ALL}")
            slow_print("""
            The treasure room gleams as you step inside. The Orb sits atop a pedestal surrounded by mirrors.
            As you approach, the room begins to fill with blinding light.
            """)

        available_choices = {
            "1": "Use the flashlight to align the mirrors and disarm the trap\n(check inventory by typing \"info\" to see if you have this item)",
            "2": "Grab the Orb and run",
            "3": "Attempt to destroy the mirrors"
        }

        # Filter out already visited choices
        available_choices = {key: val for key, val in available_choices.items() if key not in visited_choices}

        # Stop interaction if all choices are exhausted
        if not available_choices:
            slow_print("\nYou have explored all options in the treasure room. The Orb remains out of reach.")
            return

        slow_print("Choices:")
        for key, description in available_choices.items():
            print(f"{key}. {description}")

        choice = input("Choose an option ({}): ".format("/".join(available_choices.keys()))).strip()

        if (choice not in available_choices) and (choice != "info") and (choice != "heal"):
            slow_print("\nInvalid choice or already tried. Please choose again.")
            return light_and_orb_pedestal(player, visited_choices)

        if choice == "1" or choice == "2" or choice == "3":
            visited_choices.add(choice)

        if choice == "1":
            if "flashlight" in player.items:
                slow_print("\nYou carefully align the mirrors with your flashlight, redirecting the light. The trap is disarmed.")
                player.use_item("flashlight")
                return

            else:
                slow_print("\nYou realize that you dont have a flashlight. You have do make a choice though")


        elif choice == "2":
            slow_print("\nYou grab the Orb and sprint! Lasers cut across the room, grazing you as you escape.")
            player.take_damage(15)
            return

        elif choice == "3":
            slow_print("\nYou attempt to smash the mirrors, but the room starts filling up with water. You have do something quick!!!")
            player.take_damage(5)
        elif choice == "info":
            player.print_status()
        elif choice == "heal":
            player.self_heal()


        # Recursively call until all choices are exhausted
        light_and_orb_pedestal(player, visited_choices)

    def random_trap(player):
        traps = [
            {"name": "spike pit", "damage": 5},
            {"name": "poison dart", "damage": 4},
            {"name": "rolling boulder", "damage": 3},
        ]
        trap = random.choice(traps)
        slow_print(f"\nYou trigger a {trap['name']}!")
        player.take_damage(trap["damage"])


    def game():
        introduction()
        temple_entrance(player)

        if player.health > 0:
            maze_of_shadows(player)
        if player.health > 0:
            compass_room(player)
        if player.health > 0:
            knife_in_mechanism(player)
        if player.health > 0:
            light_and_orb_pedestal(player)

        # End of game
        if player.health > 0:
            slow_print(f"\nCongratulations, {player.name}! You have claimed the Orb and survived the Sacred Temple!")
            player.orb_status = "yes"
        else:
            slow_print(f"\n{player.name}'s adventure ends in tragedy.")

        slow_print(f"\n--- Exited Temple successfully ---\n{player.name}'s Final Stats:\n")
        player.print_status()

    game()

def ending(player):
    slow_print("\n--- Epilogue ---\n")

    if player.health <= 0:
        if player.orb_status == "yes":
            slow_print(f"""
            Though {player.name} claimed the legendary Orb, the journey proved too perilous.
            Your mortal wounds took their toll, and you succumbed just as the temple gates came into view.
            The Orb now rests in the hands of the villagers, who mourn your sacrifice and honor your bravery.
            """)
        else:
            slow_print(f"""
            Trapped in the Sacred Temple, {player.name}'s journey ended in darkness.
            Neither the Orb nor the hero returned to the village, and the tale of the temple
            grows even more ominous in the minds of those who dared to dream of its treasures.
            """)
        slow_print("\n--- The End ---\n")
        return

    # Player is alive, present them with a choice
    slow_print(f"""
    Victorious and alive, {player.name}, you stand at the edge of the Sacred Temple.
    With the jungle stretching out before you, the Orb glowing in your hands (if you have it), you ponder your next step.
    """)
    slow_print("Choices:")
    slow_print("1. Return to the village to share your story.")
    slow_print("2. Head back to your home to rest and reflect on your journey.")
    slow_print("3. Wander through the jungle, seeking new adventures.")

    choice = input("Choose an option (1/2/3): ").strip()

    if choice == "1":
        if player.orb_status == "yes":
            slow_print(f"""
            Returning to the village with the Orb, {player.name}, you are celebrated as a hero.
            The villagers rejoice, and the Orb's mystical powers bring prosperity to their lives.
            Your name becomes a legend, and your bravery is remembered for generations.
            """)
        else:
            slow_print(f"""
            You return to the village, alive but empty-handed. The villagers are relieved to see you,
            but they cannot hide their disappointment that the Orb remains in the temple.
            Your story becomes a lesson in survival and humility.
            """)
    elif choice == "2":
        if player.orb_status == "yes":
            slow_print("""With the Orb safely in your possession, you journey back home. 
            The whispers of the jungle fade. You spend your days 
            in quiet reflection, guarding the Orb and pondering its true purpose.""")
        else:
            slow_print(f"""
            Choosing the solace of your home, you return empty-handed but alive.
            The trials of the Sacred Temple weigh heavily on you, and the jungle's dangers now seem like distant nightmares.
            Your adventure has changed you forever, even without the Orb.
            """)
    elif choice == "3":
        if player.orb_status == "yes":
            slow_print(f"""
            With the Orb in your grasp, you set off into the unknown jungle, seeking further mysteries to uncover.
            The jungle becomes your new home, and tales of a wandering adventurer with a glowing artifact spread among the locals.
            Your journey never truly ends.
            """)
        else:
            slow_print(f"""
            You choose to wander through the jungle, leaving the temple and its challenges behind.
            The wild becomes your refuge, and your name is forgotten by the village, though the jungle whispers of your survival.
            Your adventure continues in the untamed wilderness.
            """)


    else:
        slow_print("\nInvalid choice. The jungle seems to have decided for you...")
        ending(player)
        slow_print("You disappear into the wilderness, your fate left untold.")

    slow_print("\n--- The End ---\n")
    slow_print("Thanks for playing")
    slow_print(f"{Fore.CYAN}Made by Tanish Yelgoe (23110328){Style.RESET_ALL}")
    input("Press Enter to exit the game...")



if __name__ == "__main__":
    print("Audio is playing in the background!")
    play_music('./audio/crash_site.mp3')


    player = Player()
    introduction(player)
    if player.health > 0:
        explore_crash_site(player)
    if player.health > 0:
        survive_first_night(player)
    if player.health > 0:
        jungle_exploration(player)
    if player.health > 0:
        village_encounter(player)
    if player.health > 0:
        temple_quest(player)
    ending(player)

