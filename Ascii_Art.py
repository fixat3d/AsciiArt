import signal
import threading
import random, json, time
from datetime import datetime
import os, sys

halloween_anim_file_path = "Animations_Halloween.json"
christmas_anim_file_path = "Animations_Christmas.json"
astronomy_anim_file_path = "Animations_Astronomy.json" 
fall_anim_file_path = "Animations_Fall(Season).json"

# Configurable animation speed
ANIMATION_SPEED = 0.7

#animations like transitions
#animations like making pictures move

holidays = {
    "New Year's Day": 1,
    "Valentine's Day": 2,
    "Independence Day": 7,
    "Halloween":10,
    "Christmas": 12,
}
    
colors = {
    #background
    "bbk": "\033[40m",      #black
    "brd": "\033[41m",      #red
    "bgn": "\033[42m",      #green
    "boe": "\033[43m",      #orange
    "bbe": "\033[44m",      #blue
    "bpe": "\033[45m",      #purple
    "bcn": "\033[46m",      #cyan
    "bly": "\033[47m",      #light gray0
    "bwe": "\033[47m",      #white

    #foreground
    "lrd": "\033[91m",      #light red
    "lgy": "\033[37m",      #light gray
    "gy": "\033[90m",       #gray
    "bk": "\033[30m",       #black
    "bn": "\033[93m",       #brown
    "oe": "\033[33m",       #orange
    "rd": "\033[31m",       #red
    "gn": "\033[32m",       #green
    "yw": "\033[93m",       #yellow
    "be": "\033[34m",       #blue
    "pe": "\033[35m",       #magenta
    "ma": "\033[95m",       #purple
    "cn": "\033[36m",       #cyan
    "we": "\033[37m",       #white
}




def color_replacer(s):
    """Replace placeholders with ANSI color codes."""
    for key, val in colors.items():
        s = s.replace(key, val)
    return s


def new_frame(frame):
    """Clear and print a new frame with colors applied."""
    print(end='\033[F' * 2)
    print('\n\n', '\033[33m')
    for line in frame:
        print("\t", color_replacer(line))


def play_animation(header, frames, repeat=4, delay=ANIMATION_SPEED):
    """Play a sequence of frames with header, repeated, with delay."""
    for _ in range(repeat):
        for frame in frames:
            new_frame(header + frame)
            time.sleep(delay)


def Halloween_animations(data):
    header = data["Halloween_Header"]
    anim_number = random.randint(1, 7)

    if anim_number == 6:  # Special case: jack in the box
        frames_box = [data[f"jack_in_the_box_frame_{i+1}"] for i in range(4)]
        frames_pop = [data[f"jack_in_the_box_pop_out_frame_{i+1}"] for i in range(2)]
        play_animation(header, frames_box, repeat=8)
        play_animation(header, frames_pop, repeat=16)
        return

    animations = {
        1: ("three_pumpkins_frame_", 8, 4),
        2: ("Witches_house_frame_", 4, 4),
        3: ("Witches_spell_frame_", 8, 4),
        4: ("spooky_ghosts_frame_", 4, 4),
        5: ("Scarecrow_patch_frame_", 4, 4),
        7: ("Goblin_face_frame_", 8, 4),
    }

    prefix, frame_count, repeat = animations[anim_number]
    frames = [data[f"{prefix}{i+1}"] for i in range(frame_count)]
    play_animation(header, frames, repeat)


def Christmas_animations(data):
    header = data["Christmas_Header"]
    anim_number = random.randint(1, 2)

    animations = {
        1: ("tree_by_the_fire_frame_", 8, 4),
        2: ("group_of_snowmen_frame_", 2, 8),
    }

    prefix, frame_count, repeat = animations[anim_number]
    frames = [data[f"{prefix}{i+1}"] for i in range(frame_count)]
    play_animation(header, frames, repeat)


def Astronomy_animations(data):
    header = data["Astronomy_Header"]
    anim_number = random.randint(1, 2)

    animations = {
        1: ("NASA_Rocket_frame_", 8, 4),
        2: ("NASA_Propelled_rocket_frame_", 8, 2),
    }

    prefix, frame_count, repeat = animations[anim_number]
    frames = [data[f"{prefix}{i+1}"] for i in range(frame_count)]
    play_animation(header, frames, repeat)


def Fall_animations(data):
    header = data["Fall_Header"]
    anim_number = 1

    animations = {
        1: ("fall_wedding_frame_",12,4)
    }

    prefix, frame_count, repeat = animations[anim_number]
    frames = [data[f"{prefix}{i+1}"] for i in range(frame_count)]
    play_animation(header, frames, repeat)


def load_animations():
    with open(halloween_anim_file_path) as f:
        halloween = json.load(f)
    with open(christmas_anim_file_path) as f:
        christmas = json.load(f)
    with open(astronomy_anim_file_path) as f:
        astronomy = json.load(f)
    with open(fall_anim_file_path) as f:
        fall = json.load(f)
    return halloween, christmas, astronomy, fall


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[37m")
    print("\033[40m")
    print(r"""****************************************************************
*  _   _       _ _     _                    __                 *              
* | | | |     | |_|   | |                  /  \           _    *
* | |_| | ___ | |_  __| | __ ___     __   / /\ \  ---__ _| |_  *
* |  _  |/ _ \| | |/ _` |/ _` | \   / /  / ____ \ |  __|_   _| *
* | | | | (_) | | | (_/ | (_| |\ \_/ /  / /    \ \| /    | |   *
* \_| |_/\___/|_|_|\____|\__,_| \_  /  /_/      \_|_|    |_|   *
*                                / /                           *
*                               /_/                            *
****************************************************************""")
    print("****************************************************************")
    print("* Copyright of grim, 2022                                      *")
    print("* Last revised: 12/3/2024                                      *")
    print("*                                                              *")
    print("****************************************************************")
    
    # Preload all JSON animation data
    halloween_data, christmas_data, astronomy_data, fall_data= load_animations()

    animation_dispatch = {
        "halloween": lambda: Halloween_animations(halloween_data),
        "christmas": lambda: Christmas_animations(christmas_data),
        "space":     lambda: Astronomy_animations(astronomy_data),
        "fall":      lambda: Fall_animations(fall_data),
    }

    try:
        user_input = input("Enter a holiday: ")
        while True:
            if user_input.lower() == "q":
                break
            elif user_input.lower() in animation_dispatch:
                animation_dispatch[user_input.lower()]()
            else:
                print("Not a command\n")

    except KeyboardInterrupt:
        print("Animations ended")
    except Exception as e:
        print("Error:", e)