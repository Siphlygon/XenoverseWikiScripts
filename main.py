# -*- coding: utf-8 -*-
# pylint: disable=locally-disabled, too-many-lines
"""
Created on Sat Mar 16 00:03:52 2024

@author: Siphlygon
"""

# TODO: Future STAB & evolutions are, in general, possible
# Locations should be a whole ass other script imo, no % info given in encounters.txt

# Folder path
FOLDER_PATH = "C:/Program Files (x86)/XenoTeam/Xenoverse/Xenoverse Per Aspera Ad Astra/Xenoverse-public-1.5.5/Xenoverse/PBS/"


def gender_code(gender):
    """
    Holds dictionary of gender codes.

    Args:
        gender (string): The gender represented in pokemon.txt

    Returns:
        string: The corresponding gender code.
    """
    switch = {
        "Genderless": "255",
        "Unknown": "256",
        "AlwaysFemale": "254",
        "Female75Percent": "191",
        "Female50Percent": "127",
        "Female25Percent": "63",
        "FemaleOneEighth": "31",
        "AlwaysMale": "0"
    }
    return switch.get(gender, "Invalid input")


def growth_rate(rate):
    """
    Holds dictionary of growth rates.

    Args:
        rate (string): The growth rate represented in pokemon.txt

    Returns:
        string: The corresponding growth rate.
    """
    switch = {
        "Erratic": "600000",
        "Fast": "800000",
        "Medium": "1000000",
        "Parabolic": "1059860",
        "Slow": "1250000",
        "Fluctuating": "1640000"
    }
    return switch.get(rate, "Invalid input")


def tm_info(number):
    """
    Holds dictionary of TM info.

    Args:
        number (string): The TM number

    Returns:
        string: canHaveStab,Type
    """
    switch = {
        "01": "no,Dark",
        "02": "yes,Dragon",
        "03": "yes,Psychic",
        "04": "no,Psychic",
        "05": "no,Sound",
        "06": "no,Poison",
        "07": "no,Ice",
        "08": "no,Fighting",
        "09": "yes,Poison",
        "10": "no,Normal",
        "11": "no,Fire",
        "12": "no,Dark",
        "13": "yes,Ice",
        "14": "yes,Ice",
        "15": "yes,Normal",
        "16": "no,Psychic",
        "17": "no,Normal",
        "18": "no,Water",
        "19": "no,Flying",
        "20": "no,Normal",
        "21": "yes,Sound",
        "22": "yes,Grass",
        "23": "yes,Rock",
        "24": "yes,Electric",
        "25": "yes,Electric",
        "26": "yes,Ground",
        "27": "yes,Normal",
        "28": "yes,Ground",
        "29": "yes,Psychic",
        "30": "yes,Ghost",
        "31": "yes,Fighting",
        "32": "no,Normal",
        "33": "no,Psychic",
        "34": "yes,Bug",
        "35": "yes,Fire",
        "36": "yes,Poison",
        "37": "no,Rock",
        "38": "yes,Fire",
        "39": "yes,Rock",
        "40": "yes,Flying",
        "41": "no,Dark",
        "42": "yes,Normal",
        "43": "yes,Fire",
        "44": "no,Psychic",
        "45": "no,Normal",
        "46": "yes,Dark",
        "47": "yes,Fighting",
        "48": "yes,Sound",
        "49": "yes,Sound",
        "50": "yes,Fire",
        "51": "yes,Steel",
        "52": "yes,Fighting",
        "53": "yes,Grass",
        "54": "yes,Normal",
        "55": "yes,Water",
        "56": "yes,Dark",
        "57": "yes,Electric",
        "58": "yes,Flying",
        "59": "yes,Dark",
        "60": "no,Dark",
        "61": "no,Fire",
        "62": "yes,Flying",
        "63": "no,Dark",
        "64": "yes,Normal",
        "65": "yes,Ghost",
        "66": "yes,Dark",
        "67": "yes,Steel",
        "68": "yes,Normal",
        "69": "no,Rock",
        "70": "yes,Water",
        "71": "yes,Rock",
        "72": "yes,Electric",
        "73": "no,Electric",
        "74": "yes,Steel",
        "75": "no,Normal",
        "76": "yes,Fighting",
        "77": "no,Normal",
        "78": "yes,Ground",
        "79": "yes,Ice",
        "80": "yes,Rock",
        "81": "yes,Bug",
        "82": "yes,Dragon",
        "83": "yes,Bug",
        "84": "yes,Poison",
        "85": "yes,Psychic",
        "86": "yes,Grass",
        "87": "no,Normal",
        "88": "yes,Water",
        "89": "yes,Bug",
        "90": "no,Normal",
        "91": "yes,Steel",
        "92": "no,Psychic",
        "93": "yes,Electric",
        "94": "yes,Fairy",
        "95": "yes,Dark"
    }
    return switch.get(number, "Invalid input")


def move_info(move):
    """
    Holds dictionary of moves.

    Args:
        move (string): The move represented in pokemon.txt and tm.txt in title case.

    Returns:
        string: MoveName,canHaveSTAB,type
    """
    switch = {
        "Absorb": "Absorb,yes,Grass",
        "Accelerock": "Accelerock,yes,Rock",
        "Acid": "Acid,yes,Poison",
        "Acidarmor": "Acid Armor,no,Poison",
        "Acidrain": "Acid Rain,no,Water",
        "Acidspray": "Acid Spray,yes,Poison",
        "Acousticbomb": "Acoustic Bomb,yes,Sound",
        "Acrobatics": "Acrobatics,yes,Flying",
        "Acupressure": "Acupressure,no,Normal",
        "Aerialace": "Aerial Ace,yes,Flying",
        "Aeroblast": "Aeroblast,yes,Flying",
        "Afteryou": "After You,no,Normal",
        "Agility": "Agility,no,Psychic",
        "Aircutter": "Air Cutter,yes,Flying",
        "Airslash": "Air Slash,yes,Flying",
        "Allyswitch": "Ally Switch,no,Psychic",
        "Amnesia": "Amnesia,no,Psychic",
        "Anchorshot": "Anchor Shot,yes,Steel",
        "Ancientpower": "Ancient Power,yes,Rock",
        "Aquajet": "Aqua Jet,yes,Water",
        "Aquaring": "Aqua Ring,no,Water",
        "Aquatail": "Aqua Tail,yes,Water",
        "Armthrust": "Arm Thrust,yes,Fighting",
        "Aromatherapy": "Aromatherapy,no,Grass",
        "Aromaticmist": "Aromatic Mist,no,Fairy",
        "Assist": "Assist,no,Normal",
        "Assurance": "Assurance,yes,Dark",
        "Astonish": "Astonish,yes,Ghost",
        "Astrallance": "Astral Lance,yes,Steel",
        "Attackorder": "Attack Order,yes,Bug",
        "Attract": "Attract,no,Normal",
        "Aurasphere": "Aura Sphere,yes,Fighting",
        "Aurorabeam": "Aurora Beam,yes,Ice",
        "Auroraveil": "Aurora Veil,no,Ice",
        "Autotomize": "Autotomize,no,Steel",
        "Avalanche": "Avalanche,yes,Ice",
        "Babble": "Babble,yes,Sound",
        "Babydolleyes": "Baby-Doll Eyes,no,Fairy",
        "Banefulbunker": "Baneful Bunker,no,Poison",
        "Barrage": "Barrage,yes,Normal",
        "Barrier": "Barrier,no,Psychic",
        "Batonpass": "Baton Pass,no,Normal",
        "Beakblast": "Beak Blast,yes,Flying",
        "Beatup": "Beat Up,yes,Dark",
        "Belch": "Belch,yes,Poison",
        "Bellydrum": "Belly Drum,no,Normal",
        "Benevolence": "Benevolence,no,Fairy",
        "Bestow": "Bestow,no,Normal",
        "Bide": "Bide,yes,Normal",
        "Bind": "Bind,yes,Normal",
        "Bite": "Bite,yes,Dark",
        "Blastburn": "Blast Burn,yes,Fire",
        "Blazekick": "Blaze Kick,yes,Fire",
        "Blizzard": "Blizzard,yes,Ice",
        "Block": "Block,no,Normal",
        "Blueflare": "Blue Flare,yes,Fire",
        "Bluenote": "Blue Note,no,Sound",
        "Bodyslam": "Body Slam,yes,Normal",
        "Boltstrike": "Bolt Strike,yes,Electric",
        "Boneclub": "Bone Club,yes,Ground",
        "Bonemerang": "Bonemerang,yes,Ground",
        "Bonerush": "Bone Rush,yes,Ground",
        "Boomburst": "Boomburst,yes,Sound",
        "Bounce": "Bounce,yes,Flying",
        "Bravebird": "Brave Bird,yes,Flying",
        "Brickbreak": "Brick Break,yes,Fighting",
        "Brine": "Brine,yes,Water",
        "Brutalhold": "Brutal Hold,yes,Fairy",
        "Brutalswing": "Brutal Swing,yes,Dark",
        "Bubble": "Bubble,yes,Water",
        "Bubblebeam": "Bubble Beam,yes,Water",
        "Bugbite": "Bug Bite,yes,Bug",
        "Bugbuzz": "Bug Buzz,yes,Bug",
        "Bulkup": "Bulk Up,no,Fighting",
        "Bulldoze": "Bulldoze,yes,Ground",
        "Bulletpunch": "Bullet Punch,yes,Steel",
        "Bulletseed": "Bullet Seed,yes,Grass",
        "Burnup": "Burn Up,yes,Fire",
        "Calmmind": "Calm Mind,no,Psychic",
        "Camouflage": "Camouflage,no,Normal",
        "Captivate": "Captivate,no,Normal",
        "Celebrate": "Celebrate,no,Normal",
        "Charge": "Charge,no,Electric",
        "Chargebeam": "Charge Beam,yes,Electric",
        "Charm": "Charm,no,Fairy",
        "Chatter": "Chatter,yes,Flying",
        "Cheering": "Cheering,no,Sound",
        "Chipaway": "Chip Away,yes,Normal",
        "Circlethrow": "Circle Throw,yes,Fighting",
        "Clamp": "Clamp,yes,Water",
        "Clangingscales": "Clanging Scales,yes,Dragon",
        "Clearsmog": "Clear Smog,yes,Poison",
        "Closecombat": "Close Combat,yes,Fighting",
        "Coil": "Coil,no,Poison",
        "Cometpunch": "Comet Punch,yes,Normal",
        "Confide": "Confide,no,Sound",
        "Confuseray": "Confuse Ray,no,Ghost",
        "Confusion": "Confusion,yes,Psychic",
        "Constrict": "Constrict,yes,Normal",
        "Controllopolare": "Magnetic Flux,no,Electric",
        "Conversion": "Conversion,no,Normal",
        "Conversion2": "Conversion 2,no,Normal",
        "Copycat": "Copycat,no,Normal",
        "Coralbreak": "Coral Break,yes,Water",
        "Coreenforcer": "Core Enforcer,yes,Dragon",
        "Corrosivebreath": "Corrosive Breath,yes,Dragon",
        "Cosmicpower": "Cosmic Power,no,Psychic",
        "Cottonguard": "Cotton Guard,no,Grass",
        "Cottonspore": "Cotton Spore,no,Grass",
        "Counter": "Counter,yes,Fighting",
        "Covet": "Covet,yes,Normal",
        "Crabhammer": "Crabhammer,yes,Water",
        "Craftyshield": "Crafty Shield,no,Fairy",
        "Creamwhip": "Cream Whip,yes,Ice",
        "Crosschop": "Cross Chop,yes,Fighting",
        "Crosspoison": "Cross Poison,yes,Poison",
        "Crunch": "Crunch,yes,Dark",
        "Crushclaw": "Crush Claw,yes,Normal",
        "Crushgrip": "Crush Grip,yes,Normal",
        "Curse": "Curse,no,Ghost",
        "Cut": "Cut,yes,Normal",
        "Darkeningbolt": "Darkening Bolt,yes,Dark",
        "Darkestlariat": "Darkest Lariat,yes,Dark",
        "Darkpulse": "Dark Pulse,yes,Dark",
        "Darkvoid": "Dark Void,no,Dark",
        "Dazzlinggleam": "Dazzling Gleam,yes,Fairy",
        "Defendorder": "Defend Order,no,Bug",
        "Defensecurl": "Defense Curl,no,Normal",
        "Defog": "Defog,no,Flying",
        "Destinybond": "Destiny Bond,no,Ghost",
        "Detect": "Detect,no,Fighting",
        "Diamondstorm": "Diamond Storm,yes,Rock",
        "Dig": "Dig,yes,Ground",
        "Disable": "Disable,no,Normal",
        "Disarmingvoice": "Disarming Voice,yes,Fairy",
        "Discharge": "Discharge,yes,Electric",
        "Discofever": "Disco Fever,no,Sound",
        "Dive": "Dive,yes,Water",
        "Dizzypunch": "Dizzy Punch,yes,Normal",
        "Doomdesire": "Doom Desire,yes,Steel",
        "Doubleedge": "Double-Edge,yes,Normal",
        "Doublehit": "Double Hit,yes,Normal",
        "Doubleironbash": "Double Iron Bash,yes,Steel",
        "Doublekick": "Double Kick,yes,Fighting",
        "Doubleslap": "Double Slap,yes,Normal",
        "Doubleteam": "Double Team,no,Normal",
        "Dracometeor": "Draco Meteor,yes,Dragon",
        "Dragonascent": "Dragon Ascent,yes,Flying",
        "Dragonbreath": "Dragon Breath,yes,Dragon",
        "Dragonclaw": "Dragon Claw,yes,Dragon",
        "Dragondance": "Dragon Dance,no,Dragon",
        "Dragonendurance": "Dragon Endurance,no,Dragon",
        "Dragonenergy": "Dragon Energy,yes,Dragon",
        "Dragonhammer": "Dragon Hammer,yes,Dragon",
        "Dragonpledge": "Dragon Pledge,yes,Dragon",
        "Dragonpulse": "Dragon Pulse,yes,Dragon",
        "Dragonrage": "Dragon Rage,no,Dragon",
        "Dragonrush": "Dragon Rush,yes,Dragon",
        "Dragonstream": "Dragon Stream,yes,Dragon",
        "Dragontail": "Dragon Tail,yes,Dragon",
        "Drainingkiss": "Draining Kiss,yes,Fairy",
        "Drainlife": "Drain Life,yes,Dark",
        "Drainpunch": "Drain Punch,yes,Fighting",
        "Dreameater": "Dream Eater,yes,Psychic",
        "Drillpeck": "Drill Peck,yes,Flying",
        "Drillrun": "Drill Run,yes,Ground",
        "Dualchop": "Dual Chop,yes,Dragon",
        "Dynamicpunch": "Dynamic Punch,yes,Fighting",
        "Earthpower": "Earth Power,yes,Ground",
        "Earthquake": "Earthquake,yes,Ground",
        "Echoedvoice": "Echoed Voice,yes,Sound",
        "Eerieimpulse": "Eerie Impulse,no,Electric",
        "Eggbomb": "Egg Bomb,yes,Normal",
        "Electricterrain": "Electric Terrain,no,Electric",
        "Electrify": "Electrify,no,Electric",
        "Electroball": "Electro Ball,yes,Electric",
        "Electroswing": "Electro Swing,no,Sound",
        "Electroweb": "Electroweb,yes,Electric",
        "Embargo": "Embargo,no,Dark",
        "Ember": "Ember,yes,Fire",
        "Encore": "Encore,no,Normal",
        "Endeavor": "Endeavor,no,Normal",
        "Endure": "Endure,no,Normal",
        "Energyball": "Energy Ball,yes,Grass",
        "Entrainment": "Entrainment,no,Normal",
        "Eruption": "Eruption,yes,Fire",
        "Explosion": "Explosion,yes,Normal",
        "Expunge": "Expunge,yes,Nuclear",
        "Extrasensory": "Extrasensory,yes,Psychic",
        "Extremespeed": "Extreme Speed,yes,Normal",
        "Facade": "Facade,yes,Normal",
        "Faintattack": "Feint Attack,yes,Dark",
        "Fairylock": "Fairy Lock,no,Fairy",
        "Fairypledge": "Fairy Pledge,yes,Fairy",
        "Fairywind": "Fairy Wind,yes,Fairy",
        "Fakeout": "Fake Out,yes,Normal",
        "Faketears": "Fake Tears,no,Dark",
        "Fallout": "Fallout,no,Nuclear",
        "Falsesurrender": "False Surrender,yes,Dark",
        "Falseswipe": "False Swipe,yes,Normal",
        "Featherdance": "Feather Dance,no,Flying",
        "Feint": "Feint,yes,Normal",
        "Feintattack": "Feint Attack,yes,Dark",
        "Fellstinger": "Fell Stinger,yes,Bug",
        "Feralclutch": "Feral Clutch,yes,Fairy",
        "Fierydance": "Fiery Dance,yes,Fire",
        "Finalgambit": "Final Gambit,no,Fighting",
        "Fireblast": "Fire Blast,yes,Fire",
        "Firefang": "Fire Fang,yes,Fire",
        "Firekunai": "Fire Kunai,yes,Fire",
        "Firelash": "Fire Lash,yes,Fire",
        "Firepledge": "Fire Pledge,yes,Fire",
        "Firepunch": "Fire Punch,yes,Fire",
        "Firespin": "Fire Spin,yes,Fire",
        "Firstimpression": "First Impression,yes,Bug",
        "Fissionburst": "Fission Burst,yes,Nuclear",
        "Fissure": "Fissure,no,Ground",
        "Flail": "Flail,yes,Normal",
        "Flameburst": "Flame Burst,yes,Fire",
        "Flamecharge": "Flame Charge,yes,Fire",
        "Flameimpact": "Flame Impact,yes,Fire",
        "Flamethrower": "Flamethrower,yes,Fire",
        "Flamewheel": "Flame Wheel,yes,Fire",
        "Flareblitz": "Flare Blitz,yes,Fire",
        "Flash": "Flash,no,Normal",
        "Flashcannon": "Flash Cannon,yes,Steel",
        "Flatter": "Flatter,no,Dark",
        "Flavortest": "Flavor Test,yes,Fairy",
        "Fleurcannon": "Fleur Cannon,yes,Fairy",
        "Fling": "Fling,yes,Dark",
        "Floralhealing": "Floral Healing,no,Fairy",
        "Flowershield": "Flower Shield,no,Fairy",
        "Fly": "Fly,yes,Flying",
        "Flyingpress": "Flying Press,yes,Fighting",
        "Focusblast": "Focus Blast,yes,Fighting",
        "Focusenergy": "Focus Energy,no,Normal",
        "Focuspunch": "Focus Punch,yes,Fighting",
        "Followme": "Follow Me,no,Normal",
        "Forcepalm": "Force Palm,yes,Fighting",
        "Foresight": "Foresight,no,Normal",
        "Forestscurse": "Forest's Curse,no,Grass",
        "Foulplay": "Foul Play,yes,Dark",
        "Freezedry": "Freeze-Dry,yes,Ice",
        "Freezeshock": "Freeze Shock,yes,Ice",
        "Frenzyplant": "Frenzy Plant,yes,Grass",
        "Frostbite": "Frostbite,yes,Ice",
        "Frostbreath": "Frost Breath,yes,Ice",
        "Frustration": "Frustration,yes,Normal",
        "Furyattack": "Fury Attack,yes,Normal",
        "Furycutter": "Fury Cutter,yes,Bug",
        "Furyswipes": "Fury Swipes,yes,Normal",
        "Fusionbolt": "Fusion Bolt,yes,Electric",
        "Fusionflare": "Fusion Flare,yes,Fire",
        "Futuresight": "Future Sight,yes,Psychic",
        "Gastroacid": "Gastro Acid,no,Poison",
        "Geargrind": "Gear Grind,yes,Steel",
        "Gearup": "Gear Up,no,Steel",
        "Geomancy": "Geomancy,no,Fairy",
        "Getlucky": "Get Lucky,yes,Psychic",
        "Gigadrain": "Giga Drain,yes,Grass",
        "Gigaimpact": "Giga Impact,yes,Normal",
        "Glaciate": "Glaciate,yes,Ice",
        "Glare": "Glare,no,Normal",
        "Goldenfist": "Golden Fist,yes,Fighting",
        "Grassknot": "Grass Knot,yes,Grass",
        "Grasspledge": "Grass Pledge,yes,Grass",
        "Grasswhistle": "Grass Whistle,no,Grass",
        "Grassyterrain": "Grassy Terrain,no,Grass",
        "Gravity": "Gravity,no,Psychic",
        "Growl": "Growl,no,Normal",
        "Growth": "Growth,no,Normal",
        "Grudge": "Grudge,no,Ghost",
        "Guardsplit": "Guard Split,no,Psychic",
        "Guardswap": "Guard Swap,no,Psychic",
        "Guillotine": "Guillotine,no,Normal",
        "Gunkshot": "Gunk Shot,yes,Poison",
        "Gust": "Gust,yes,Flying",
        "Gyroball": "Gyro Ball,yes,Steel",
        "Hail": "Hail,no,Ice",
        "Hammerarm": "Hammer Arm,yes,Fighting",
        "Happyhour": "Happy Hour,no,Normal",
        "Harden": "Harden,no,Normal",
        "Hawthorns": "Hawthorns,no,Grass",
        "Haze": "Haze,no,Ice",
        "Headbutt": "Headbutt,yes,Normal",
        "Headcharge": "Head Charge,yes,Normal",
        "Headsmash": "Head Smash,yes,Rock",
        "Healbell": "Heal Bell,no,Sound",
        "Healblock": "Heal Block,no,Psychic",
        "Healingwish": "Healing Wish,no,Psychic",
        "Healorder": "Heal Order,no,Bug",
        "Healpulse": "Heal Pulse,no,Psychic",
        "Heartstamp": "Heart Stamp,yes,Psychic",
        "Heartswap": "Heart Swap,no,Psychic",
        "Heatcrash": "Heat Crash,yes,Fire",
        "Heatwave": "Heat Wave,yes,Fire",
        "Heavyslam": "Heavy Slam,yes,Steel",
        "Helpinghand": "Helping Hand,no,Normal",
        "Hex": "Hex,yes,Ghost",
        "Hiddenpower": "Hidden Power,yes,Normal",
        "Highhorsepower": "High Horsepower,yes,Ground",
        "Hijumpkick": "High Jump Kick,yes,Fighting",
        "Hiss": "Hiss,no,Sound",
        "Holdback": "Hold Back,yes,Normal",
        "Holdhands": "Hold Hands,no,Normal",
        "Honeclaws": "Hone Claws,no,Dark",
        "Hornattack": "Horn Attack,yes,Normal",
        "Horndrill": "Horn Drill,yes,Normal",
        "Hornleech": "Horn Leech,yes,Grass",
        "Hotchilipepper": "Hot Chili Pepper,yes,Grass",
        "Howl": "Howl,no,Normal",
        "Hurricane": "Hurricane,yes,Flying",
        "Hydrocannon": "Hydro Cannon,yes,Water",
        "Hydropump": "Hydro Pump,yes,Water",
        "Hyperbeam": "Hyper Beam,yes,Normal",
        "Hyperfang": "Hyper Fang,yes,Normal",
        "Hyperspacefury": "Hyperspace Fury,yes,Dark",
        "Hyperspacehole": "Hyperspace Hole,yes,Psychic",
        "Hypervoice": "Hyper Voice,yes,Sound",
        "Hypnosis": "Hypnosis,no,Psychic",
        "Iceball": "Ice Ball,yes,Ice",
        "Icebeam": "Ice Beam,yes,Ice",
        "Iceburn": "Ice Burn,yes,Ice",
        "Icefang": "Ice Fang,yes,Ice",
        "Icehammer": "Ice Hammer,yes,Ice",
        "Icepunch": "Ice Punch,yes,Ice",
        "Iceshard": "Ice Shard,yes,Ice",
        "Iciclecrash": "Icicle Crash,yes,Ice",
        "Iciclespear": "Icicle Spear,yes,Ice",
        "Icywind": "Icy Wind,yes,Ice",
        "Imprison": "Imprison,no,Psychic",
        "Incinerate": "Incinerate,yes,Fire",
        "Infernalblade": "Infernal Blade,yes,Fire",
        "Inferno": "Inferno,yes,Fire",
        "Infestation": "Infestation,yes,Bug",
        "Ingrain": "Ingrain,no,Grass",
        "Instantcrush": "Instant Crush,yes,Psychic",
        "Instruct": "Instruct,no,Psychic",
        "Iondeluge": "Ion Deluge,no,Electric",
        "Irondefense": "Iron Defense,no,Steel",
        "Ironhead": "Iron Head,yes,Steel",
        "Irontail": "Iron Tail,yes,Steel",
        "Jetstrike": "Jet Strike,yes,Sound",
        "Judgment": "Judgment,yes,Normal",
        "Jumpkick": "Jump Kick,yes,Fighting",
        "Karatechop": "Karate Chop,yes,Fighting",
        "Kinesis": "Kinesis,no,Psychic",
        "Kingsshield": "King's Shield,no,Steel",
        "Knockoff": "Knock Off,yes,Dark",
        "Landswrath": "Land's Wrath,yes,Ground",
        "Laserfocus": "Laser Focus,no,Normal",
        "Laserpulse": "Laser Pulse,yes,Normal",
        "Lastresort": "Last Resort,yes,Normal",
        "Lavaplume": "Lava Plume,yes,Fire",
        "Leafage": "Leafage,yes,Grass",
        "Leafblade": "Leaf Blade,yes,Grass",
        "Leafstorm": "Leaf Storm,yes,Grass",
        "Leaftornado": "Leaf Tornado,yes,Grass",
        "Leechlife": "Leech Life,yes,Bug",
        "Leechseed": "Leech Seed,no,Grass",
        "Leer": "Leer,no,Normal",
        "Lick": "Lick,yes,Ghost",
        "Lightofruin": "Light of Ruin,yes,Fairy",
        "Lightscreen": "Light Screen,no,Psychic",
        "Liquidation": "Liquidation,yes,Water",
        "Lockon": "Lock-On,no,Normal",
        "Lovelykiss": "Lovely Kiss,no,Normal",
        "Lowkick": "Low Kick,yes,Fighting",
        "Lowsweep": "Low Sweep,yes,Fighting",
        "Luckychant": "Lucky Chant,no,Normal",
        "Lunardance": "Lunar Dance,no,Psychic",
        "Lunge": "Lunge,yes,Bug",
        "Lusterpurge": "Luster Purge,yes,Psychic",
        "Machpunch": "Mach Punch,yes,Fighting",
        "Magicalleaf": "Magical Leaf,yes,Grass",
        "Magiccoat": "Magic Coat,no,Psychic",
        "Magicroom": "Magic Room,no,Psychic",
        "Magicwall": "Magic Wall,no,Fairy",
        "Magmastorm": "Magma Storm,yes,Fire",
        "Magnetbomb": "Magnet Bomb,yes,Steel",
        "Magneticflux": "Magnetic Flux,no,Electric",
        "Magnetrise": "Magnet Rise,no,Electric",
        "Magnitude": "Magnitude,yes,Ground",
        "Matblock": "Mat Block,no,Fighting",
        "Meanlook": "Mean Look,no,Normal",
        "Meditate": "Meditate,no,Psychic",
        "Mefirst": "Me First,no,Normal",
        "Megadrain": "Mega Drain,yes,Grass",
        "Megahorn": "Megahorn,yes,Bug",
        "Megakick": "Mega Kick,yes,Normal",
        "Megapunch": "Mega Punch,yes,Normal",
        "Memento": "Memento,no,Dark",
        "Metalburst": "Metal Burst,yes,Steel",
        "Metalclaw": "Metal Claw,yes,Steel",
        "Metalcruncher": "Metal Cruncher,yes,Steel",
        "Metalsound": "Metal Sound,no,Steel",
        "Metalwhip": "Metal Whip,yes,Steel",
        "Meteormash": "Meteor Mash,yes,Steel",
        "Metronome": "Metronome,no,Normal",
        "Milkdrink": "Milk Drink,no,Normal",
        "Mimic": "Mimic,no,Normal",
        "Mindblown": "Mind Blown,yes,Fire",
        "Mindreader": "Mind Reader,no,Normal",
        "Minimize": "Minimize,no,Normal",
        "Miracleeye": "Miracle Eye,no,Psychic",
        "Mirrorcoat": "Mirror Coat,yes,Psychic",
        "Mirrormove": "Mirror Move,no,Flying",
        "Mirrorshot": "Mirror Shot,yes,Steel",
        "Mist": "Mist,no,Ice",
        "Mistball": "Mist Ball,yes,Psychic",
        "Mistyterrain": "Misty Terrain,no,Fairy",
        "Moonblast": "Moonblast,yes,Fairy",
        "Moongeistbeam": "Moongeist Beam,yes,Ghost",
        "Moonlight": "Moonlight,no,Fairy",
        "Morningsun": "Morning Sun,no,Normal",
        "Mudbomb": "Mud Bomb,yes,Ground",
        "Muddywater": "Muddy Water,yes,Water",
        "Mudshot": "Mud Shot,yes,Ground",
        "Mudslap": "Mud-Slap,yes,Ground",
        "Mudsport": "Mud Sport,no,Ground",
        "Multiattack": "Multi-Attack,yes,Normal",
        "Mysticalfire": "Mystical Fire,yes,Fire",
        "Nastyplot": "Nasty Plot,no,Dark",
        "Naturalgift": "Natural Gift,no,Normal",
        "Nature'Smadness": "Nature's Madness,yes,Fairy",
        "Naturepower": "Nature Power,no,Normal",
        "Needlearm": "Needle Arm,yes,Grass",
        "Nightdaze": "Night Daze,yes,Dark",
        "Nightmare": "Nightmare,no,Ghost",
        "Nightshade": "Night Shade,no,Ghost",
        "Nightslash": "Night Slash,yes,Dark",
        "Nobleroar": "Noble Roar,no,Normal",
        "Noiseburst": "Noise Burst,yes,Sound",
        "Nuzzle": "Nuzzle,yes,Electric",
        "Oblivionwing": "Oblivion Wing,yes,Flying",
        "Octazooka": "Octazooka,yes,Water",
        "Odorsleuth": "Odor Sleuth,no,Normal",
        "Ominouswind": "Ominous Wind,yes,Ghost",
        "Originpulse": "Origin Pulse,yes,Water",
        "Outrage": "Outrage,yes,Dragon",
        "Overdrive": "Overdrive,yes,Electric",
        "Overheat": "Overheat,yes,Fire",
        "Painsplit": "Pain Split,no,Normal",
        "Papercut": "Paper Cut,yes,Steel",
        "Paraboliccharge": "Parabolic Charge,yes,Electric",
        "Partingshot": "Parting Shot,no,Dark",
        "Payback": "Payback,yes,Dark",
        "Payday": "Pay Day,yes,Normal",
        "Peck": "Peck,yes,Flying",
        "Perfectglare": "Perfect Glare,no,Normal",
        "Perishsong": "Perish Song,no,Normal",
        "Petalblizzard": "Petal Blizzard,yes,Grass",
        "Petaldance": "Petal Dance,yes,Grass",
        "Phantomforce": "Phantom Force,yes,Ghost",
        "Photongeyser": "Photon Geyser,yes,Psychic",
        "Pinmissile": "Pin Missile,yes,Bug",
        "Plasmafists": "Plasma Fists,yes,Electric",
        "Playnice": "Play Nice,no,Normal",
        "Playrough": "Play Rough,yes,Fairy",
        "Pluck": "Pluck,yes,Flying",
        "Poisonfang": "Poison Fang,yes,Poison",
        "Poisongas": "Poison Gas,no,Poison",
        "Poisonjab": "Poison Jab,yes,Poison",
        "Poisonpowder": "Poison Powder,no,Poison",
        "Poisonsting": "Poison Sting,yes,Poison",
        "Poisontail": "Poison Tail,yes,Poison",
        "Pollenpuff": "Pollen Puff,yes,Bug",
        "Poltergeist": "Poltergeist,yes,Ghost",
        "Pound": "Pound,yes,Normal",
        "Powder": "Powder,no,Bug",
        "Powdersnow": "Powder Snow,yes,Ice",
        "Powergem": "Power Gem,yes,Rock",
        "Powersplit": "Power Split,no,Psychic",
        "Powerswap": "Power Swap,no,Psychic",
        "Powertrick": "Power Trick,no,Psychic",
        "Powertrip": "Power Trip,yes,Dark",
        "Poweruppunch": "Power-Up Punch,yes,Fighting",
        "Powerwhip": "Power Whip,yes,Grass",
        "Precipiceblades": "Precipice Blades,yes,Ground",
        "Present": "Present,yes,Normal",
        "Primalscream": "Primal Scream,yes,Sound",
        "Prismaticlaser": "Prismatic Laser,yes,Psychic",
        "Protect": "Protect,no,Normal",
        "Protonbeam": "Proton Beam,yes,Nuclear",
        "Psybeam": "Psybeam,yes,Psychic",
        "Psychic": "Psychic,yes,Psychic",
        "Psychicfangs": "Psychic Fangs,yes,Psychic",
        "Psychicterrain": "Psychic Terrain,no,Psychic",
        "Psychoboost": "Psycho Boost,yes,Psychic",
        "Psychocut": "Psycho Cut,yes,Psychic",
        "Psychoshift": "Psycho Shift,no,Psychic",
        "Psychup": "Psych Up,no,Normal",
        "Psyshock": "Psyshock,yes,Psychic",
        "Psystrike": "Psystrike,yes,Psychic",
        "Psywave": "Psywave,yes,Psychic",
        "Punishment": "Punishment,yes,Dark",
        "Purify": "Purify,no,Poison",
        "Pursuit": "Pursuit,yes,Dark",
        "Quantumleap": "Quantum Leap,yes,Nuclear",
        "Quash": "Quash,no,Dark",
        "Quickattack": "Quick Attack,yes,Normal",
        "Quickguard": "Quick Guard,no,Fighting",
        "Quiverdance": "Quiver Dance,no,Bug",
        "Radioacid": "Radioacid,yes,Nuclear",
        "Rage": "Rage,yes,Normal",
        "Ragepowder": "Rage Powder,no,Bug",
        "Raindance": "Rain Dance,no,Water",
        "Rapidspin": "Rapid Spin,yes,Normal",
        "Razorleaf": "Razor Leaf,yes,Grass",
        "Razorshell": "Razor Shell,yes,Water",
        "Razorwind": "Razor Wind,yes,Normal",
        "Recover": "Recover,no,Normal",
        "Recycle": "Recycle,no,Normal",
        "Reflect": "Reflect,no,Psychic",
        "Reflecttype": "Reflect Type,no,Normal",
        "Refresh": "Refresh,no,Normal",
        "Relicsong": "Relic Song,yes,Normal",
        "Rest": "Rest,no,Psychic",
        "Retaliate": "Retaliate,yes,Normal",
        "Return": "Return,yes,Normal",
        "Revelationdance": "Revelation Dance,yes,Normal",
        "Revenge": "Revenge,yes,Fighting",
        "Reversal": "Reversal,yes,Fighting",
        "Revup": "Rev Up,yes,Sound",
        "Roar": "Roar,no,Normal",
        "Roaroftime": "Roar of Time,yes,Dragon",
        "Rockblast": "Rock Blast,yes,Rock",
        "Rockclimb": "Rock Climb,yes,Normal",
        "Rockpolish": "Rock Polish,no,Rock",
        "Rockslide": "Rock Slide,yes,Rock",
        "Rocksmash": "Rock Smash,yes,Fighting",
        "Rockthrow": "Rock Throw,yes,Rock",
        "Rocktomb": "Rock Tomb,yes,Rock",
        "Rockwrecker": "Rock Wrecker,yes,Rock",
        "Roleplay": "Role Play,no,Psychic",
        "Rollingkick": "Rolling Kick,yes,Fighting",
        "Rollout": "Rollout,yes,Rock",
        "Roost": "Roost,no,Flying",
        "Rototiller": "Rototiller,no,Ground",
        "Round": "Round,yes,Normal",
        "Sacredfire": "Sacred Fire,yes,Fire",
        "Sacredsword": "Sacred Sword,yes,Fighting",
        "Safeguard": "Safeguard,no,Normal",
        "Sandattack": "Sand Attack,no,Ground",
        "Sandstorm": "Sandstorm,no,Rock",
        "Sandtomb": "Sand Tomb,yes,Ground",
        "Scald": "Scald,yes,Water",
        "Scaryface": "Scary Face,no,Normal",
        "Scorchedashes": "Scorched Ashes,no,Fire",
        "Scratch": "Scratch,yes,Normal",
        "Screech": "Screech,no,Normal",
        "Searingshot": "Searing Shot,yes,Fire",
        "Secretpower": "Secret Power,yes,Normal",
        "Secretsword": "Secret Sword,yes,Fighting",
        "Seedbomb": "Seed Bomb,yes,Grass",
        "Seedflare": "Seed Flare,yes,Grass",
        "Seismictoss": "Seismic Toss,no,Fighting",
        "Selfdestruct": "Self-Destruct,yes,Normal",
        "Shadowball": "Shadow Ball,yes,Ghost",
        "Shadowbone": "Shadow Bone,yes,Ghost",
        "Shadowclaw": "Shadow Claw,yes,Ghost",
        "Shadowforce": "Shadow Force,yes,Ghost",
        "Shadowpunch": "Shadow Punch,yes,Ghost",
        "Shadowsneak": "Shadow Sneak,yes,Ghost",
        "Sharpen": "Sharpen,no,Normal",
        "Sheercold": "Sheer Cold,no,Ice",
        "Shellsmash": "Shell Smash,no,Normal",
        "Shelltrap": "Shell Trap,yes,Fire",
        "Shiftgear": "Shift Gear,no,Steel",
        "Shockwave": "Shock Wave,yes,Electric",
        "Shoreup": "Shore Up,no,Ground",
        "Signalbeam": "Signal Beam,yes,Bug",
        "Silverwind": "Silver Wind,yes,Bug",
        "Simplebeam": "Simple Beam,no,Normal",
        "Sing": "Sing,no,Normal",
        "Sketch": "Sketch,no,Normal",
        "Skillswap": "Skill Swap,no,Psychic",
        "Skullbash": "Skull Bash,yes,Normal",
        "Skyattack": "Sky Attack,yes,Flying",
        "Skydrop": "Sky Drop,yes,Flying",
        "Skyfall": "Sky Fall,yes,Flying",
        "Skyuppercut": "Sky Uppercut,yes,Fighting",
        "Slackoff": "Slack Off,no,Normal",
        "Slam": "Slam,yes,Normal",
        "Slash": "Slash,yes,Normal",
        "Sleeppowder": "Sleep Powder,no,Grass",
        "Sleeptalk": "Sleep Talk,no,Sound",
        "Sludge": "Sludge,yes,Poison",
        "Sludgebomb": "Sludge Bomb,yes,Poison",
        "Sludgewave": "Sludge Wave,yes,Poison",
        "Smackdown": "Smack Down,yes,Rock",
        "Smartstrike": "Smart Strike,yes,Steel",
        "Smellingsalt": "Smelling Salts,yes,Normal",
        "Smog": "Smog,yes,Poison",
        "Smokescreen": "Smokescreen,no,Normal",
        "Snarl": "Snarl,yes,Dark",
        "Snatch": "Snatch,no,Dark",
        "Snore": "Snore,yes,Sound",
        "Soak": "Soak,no,Water",
        "Softboiled": "Soft-Boiled,no,Normal",
        "Solarbeam": "Solar Beam,yes,Grass",
        "Solarblade": "Solar Blade,yes,Grass",
        "Sonicboom": "Sonic Boom,no,Sound",
        "Soundbarrier": "Sound Barrier,no,Sound",
        "Soundpledge": "Sound Pledge,yes,Sound",
        "Spacialrend": "Spacial Rend,yes,Dragon",
        "Spark": "Spark,yes,Electric",
        "Sparklingaria": "Sparkling Aria,yes,Water",
        "Spectralthief": "Spectral Thief,yes,Ghost",
        "Speedswap": "Speed Swap,no,Psychic",
        "Spiderweb": "Spider Web,no,Bug",
        "Spikecannon": "Spike Cannon,yes,Normal",
        "Spikes": "Spikes,no,Ground",
        "Spikyshield": "Spiky Shield,no,Grass",
        "Spiritshackle": "Spirit Shackle,yes,Ghost",
        "Spite": "Spite,no,Ghost",
        "Spitup": "Spit Up,yes,Normal",
        "Splash": "Splash,no,Normal",
        "Spore": "Spore,no,Grass",
        "Spotlight": "Spotlight,no,Normal",
        "Starburst_Shu": "Star Burst_Shu,yes,Dragon",
        "Starburst_Shy": "Star Burst_Shy,yes,Fairy",
        "Starburst_Tri": "Star Burst_Tri,yes,Sound",
        "Stealthrock": "Stealth Rock,no,Rock",
        "Steameruption": "Steam Eruption,yes,Water",
        "Steamroller": "Steamroller,yes,Bug",
        "Steelwing": "Steel Wing,yes,Steel",
        "Stickyterrain": "Sticky Terrain,no,Poison",
        "Stickyweb": "Sticky Web,no,Bug",
        "Stockpile": "Stockpile,no,Normal",
        "Stomp": "Stomp,yes,Normal",
        "Stompingtantrum": "Stomping Tantrum,yes,Ground",
        "Stoneedge": "Stone Edge,yes,Rock",
        "Storedpower": "Stored Power,yes,Psychic",
        "Stormthrow": "Storm Throw,yes,Fighting",
        "Strength": "Strength,yes,Normal",
        "Strengthsap": "Strength Sap,no,Grass",
        "Stringshot": "String Shot,no,Bug",
        "Struggle": "Struggle,yes,Normal",
        "Strugglebug": "Struggle Bug,yes,Bug",
        "Stunspore": "Stun Spore,no,Grass",
        "Subduction": "Subduction,yes,Ground",
        "Submission": "Submission,yes,Fighting",
        "Substitute": "Substitute,no,Normal",
        "Subwoofer": "Subwoofer,yes,Sound",
        "Suckerpunch": "Sucker Punch,yes,Dark",
        "Suddenstrike": "Sudden Strike,yes,Dark",
        "Sugarrush": "Sugar Rush,yes,Fairy",
        "Sunnyday": "Sunny Day,no,Fire",
        "Sunsteelstrike": "Sunsteel Strike,yes,Steel",
        "Superfang": "Super Fang,no,Normal",
        "Superpower": "Superpower,yes,Fighting",
        "Supersonic": "Supersonic,no,Normal",
        "Surf": "Surf,yes,Water",
        "Swagger": "Swagger,no,Normal",
        "Swallow": "Swallow,no,Normal",
        "Sweetkiss": "Sweet Kiss,no,Fairy",
        "Sweetscent": "Sweet Scent,no,Normal",
        "Swift": "Swift,yes,Normal",
        "Switcheroo": "Switcheroo,no,Dark",
        "Swordsdance": "Swords Dance,no,Normal",
        "Synchronoise": "Synchronoise,yes,Psychic",
        "Synthesis": "Synthesis,no,Grass",
        "Tackle": "Tackle,yes,Normal",
        "Tailglow": "Tail Glow,no,Bug",
        "Tailslap": "Tail Slap,yes,Normal",
        "Tailwhip": "Tail Whip,no,Normal",
        "Tailwind": "Tailwind,no,Flying",
        "Takedown": "Take Down,yes,Normal",
        "Taunt": "Taunt,no,Dark",
        "Tearfullook": "Tearful Look,no,Normal",
        "Technoblast": "Techno Blast,yes,Normal",
        "Teeterdance": "Teeter Dance,no,Normal",
        "Telekinesis": "Telekinesis,no,Psychic",
        "Teleport": "Teleport,no,Psychic",
        "Thief": "Thief,yes,Dark",
        "Thousandarrows": "Thousand Arrows,yes,Ground",
        "Thousandwaves": "Thousand Waves,yes,Ground",
        "Thrash": "Thrash,yes,Normal",
        "Throatchop": "Throat Chop,yes,Dark",
        "Thunder": "Thunder,yes,Electric",
        "Thunderbolt": "Thunderbolt,yes,Electric",
        "Thundercage": "Thunder Cage,yes,Electric",
        "Thunderfang": "Thunder Fang,yes,Electric",
        "Thunderhammer": "Thunderstruck,yes,Electric",
        "Thunderpunch": "Thunder Punch,yes,Electric",
        "Thundershock": "Thunder Shock,yes,Electric",
        "Thunderstorm": "Thunderstorm,no,Electric",
        "Thunderstruck": "Thunderstruck,yes,Electric",
        "Thunderwave": "Thunder Wave,no,Electric",
        "Tickle": "Tickle,no,Normal",
        "Tidaldragoon": "Tidal Dragoon,yes,Dragon",
        "Topsyturvy": "Topsy-Turvy,no,Dark",
        "Torment": "Torment,no,Dark",
        "Toxic": "Toxic,no,Poison",
        "Toxicspikes": "Toxic Spikes,no,Poison",
        "Toxicthread": "Toxic Thread,no,Poison",
        "Transform": "Transform,no,Normal",
        "Triattack": "Tri Attack,yes,Normal",
        "Trick": "Trick,no,Psychic",
        "Trickortreat": "Trick-or-Treat,no,Ghost",
        "Trickroom": "Trick Room,no,Psychic",
        "Triplekick": "Triple Kick,yes,Fighting",
        "Tropkick": "Trop Kick,yes,Grass",
        "Trumpcard": "Trump Card,yes,Normal",
        "Twineedle": "Twineedle,yes,Bug",
        "Twister": "Twister,yes,Dragon",
        "Uproar": "Uproar,yes,Sound",
        "Uturn": "U-turn,yes,Bug",
        "Vacuumwave": "Vacuum Wave,yes,Fighting",
        "Vcreate": "V-create,yes,Fire",
        "Velvetscales": "Velvet Scales,no,Dragon",
        "Venomdrench": "Venom Drench,no,Poison",
        "Venoshock": "Venoshock,yes,Poison",
        "Vicegrip": "Vice Grip,yes,Normal",
        "Vinewhip": "Vine Whip,yes,Grass",
        "Vitalthrow": "Vital Throw,yes,Fighting",
        "Voidstar": "Void Star,yes,Ice",
        "Voltswitch": "Volt Switch,yes,Electric",
        "Volttackle": "Volt Tackle,yes,Electric",
        "Wakeupslap": "Wake-Up Slap,yes,Fighting",
        "Waterfall": "Waterfall,yes,Water",
        "Watergun": "Water Gun,yes,Water",
        "Waterpledge": "Water Pledge,yes,Water",
        "Waterpulse": "Water Pulse,yes,Water",
        "Watershuriken": "Water Shuriken,yes,Water",
        "Watersport": "Water Sport,no,Water",
        "Waterspout": "Water Spout,yes,Water",
        "Weatherball": "Weather Ball,yes,Normal",
        "Whirlpool": "Whirlpool,yes,Water",
        "Whirlwind": "Whirlwind,no,Normal",
        "Wideguard": "Wide Guard,no,Rock",
        "Wildcharge": "Wild Charge,yes,Electric",
        "Wilddance": "Wild Dance,yes,Sound",
        "Willowisp": "Will-O-Wisp,no,Fire",
        "Wingattack": "Wing Attack,yes,Flying",
        "Wish": "Wish,no,Normal",
        "Withdraw": "Withdraw,no,Water",
        "Wonderroom": "Wonder Room,no,Psychic",
        "Woodhammer": "Wood Hammer,yes,Grass",
        "Workup": "Work Up,no,Normal",
        "Worryseed": "Worry Seed,no,Grass",
        "Wrap": "Wrap,yes,Normal",
        "Wringout": "Wring Out,yes,Normal",
        "Xscissor": "X-Scissor,yes,Bug",
        "Xtransform": "X Transform,no,Normal",
        "Yawn": "Yawn,no,Normal",
        "Zapcannon": "Zap Cannon,yes,Electric",
        "Zenheadbutt": "Zen Headbutt,yes,Psychic",
        "Zingzap": "Zing Zap,yes,Electric"
    }
    return switch.get(move, "Invalid input")


def item_info(item):
    """
    Holds dictionary of held items.

    Args:
        item (string): The held item represented in pokemon.txt

    Returns:
        string: The real, English name of the held item.
    """
    switch = {
        "Alterball": "Alter Ball",
        "Ancientstone": "Ancient Stone",
        "Armfausta": "Auspicious Armor",
        "Arminfausta": "Malicious Armor",
        "Aspearberry": "Aspear Berry",
        "Babiriberry": "Babiri Berry",
        "Balmmushroom": "Balm Mushroom",
        "Berryjuice": "Berry Juice",
        "Bigmushroom": "Big Mushroom",
        "Bignugget": "Big Nugget",
        "Bigpearl": "Big Pearl",
        "Bigroot": "Big Root",
        "Blackbelt": "Black Belt",
        "Blacksludge": "Black Sludge",
        "Botabisso": "Deep Sea Update",
        "Botantico": "Elder Update",
        "Botcavaliere": "Cavalry Update",
        "Botchele": "Pincer Update",
        "Botdrago": "Dragon Update",
        "Boterrore": "Error Update",
        "Botferro": "Iron Update",
        "Botforza": "Muscular Update",
        "Botinferno": "Blast Update",
        "Botmarino": "South Sea Update",
        "Botmega": "Mega Update",
        "Botmegatone": "Megaton Update",
        "Botombra": "Shadow Update",
        "Botpanna": "Meringue Update",
        "Botpinza": "Gripper Update",
        "Botpressione": "Compressed Update",
        "Botpsico": "Psi Update",
        "Botregale": "Royal Update",
        "Botsaetta": "Thunderbolt Update",
        "Botsgusciato": "Shell Update",
        "Bottenerezza": "Tender Update",
        "Bottrapano": "Drill Update",
        "Botvirtuale": "Virtual Update",
        "Botwes": "Wes Update",
        "Charcoal": "Charcoal",
        "Chartiberry": "Charti Berry",
        "Cheriberry": "Cheri Berry",
        "Chestoberry": "Chesto Berry",
        "Chilanberry": "Chilan Berry",
        "Chopleberry": "Chople Berry",
        "Cobaberry": "Coba Berry",
        "Colburberry": "Colbur Berry",
        "Cometshard": "Comet Shard",
        "Dawnstone": "Dawn Stone",
        "Deepseascale": "Deep Sea Scale",
        "Deepseatooth": "Deep Sea Tooth",
        "Dragonfang": "Dragon Fang",
        "Dragonscale": "Dragon Scale",
        "Duskstone": "Dusk Stone",
        "Edenberry": "Eden Berry",
        "Electirizer": "Electirizer",
        "Everstone": "Ever Stone",
        "Evopuppillon": "Dread Pendant",
        "Expertbelt": "Expert Belt",
        "Firestone": "Fire Stone",
        "Gripclaw": "Grip Claw",
        "Habanberry": "Haban Berry",
        "Hardstone": "Hard Stone",
        "Heartscale": "Heart Scale",
        "Honey": "Honey",
        "Icestone": "Ice Stone",
        "Kasibberry": "Kasib Berry",
        "Kingsrock": "King's Rock",
        "Laggingtail": "Lagging Tail",
        "Leafstone": "Leaf Stone",
        "Leftovers": "Leftovers",
        "Leppaberry": "Leppa Berry",
        "Lightball": "Light Ball",
        "Lightclay": "Light Clay",
        "Luckyegg": "Lucky Egg",
        "Lumberry": "Lum Berry",
        "Mentalherb": "Mental Herb",
        "Metalcoat": "Metal Coat",
        "Metalpowder": "Metal Powder",
        "Metronome": "Metronome",
        "Miracleseed": "Miracle Seed",
        "Moomoomilk": "Moomoo Milk",
        "Moonstone": "Moon Stone",
        "Mysticwater": "Mystic Water",
        "Nevermeltice": "Never-Melt Ice",
        "Nugget": "Nugget",
        "Occaberry": "Occa Berry",
        "Oranberry": "Oran Berry",
        "Ovalstone": "Oval Stone",
        "Passhoberry": "Passho Berry",
        "Payapaberry": "Payapa Berry",
        "Pearl": "Pearl",
        "Pearlstring": "Pearl String",
        "Pechaberry": "Pecha Berry",
        "Persimberry": "Persim Berry",
        "Pezzidiricambio": "Spare Parts",
        "Pinapberry": "Pinap Berry",
        "Pixieplate": "Pixie Plate",
        "Poisonbarb": "Poison Barb",
        "Poisonstone": "Poison Stone",
        "Quickclaw": "Quick Claw",
        "Quickpowder": "Quick Powder",
        "Rarebone": "Rare Bone",
        "Rawstberry": "Rawst Berry",
        "Razorclaw": "Razor Claw",
        "Razorfang": "Razor Fang",
        "Rindoberry": "Rindo Berry",
        "Sharpbeak": "Sharp Beak",
        "Shedshell": "Shed Shell",
        "Shinystone": "Shiny Stone",
        "Shucaberry": "Shuca Berry",
        "Silverpowder": "Silver Powder",
        "Sitrusberry": "Sitrus Berry",
        "Smokeball": "Smoke Ball",
        "Softsand": "Soft Sand",
        "Soundplate": "Sound Plate",
        "Spelltag": "Spell Tag",
        "Stardust": "Stardust",
        "Starpiece": "Star Piece",
        "Stick": "Stick",
        "Stickybarb": "Sticky Barb",
        "Sunstone": "Sun Stone",
        "Tangaberry": "Tanga Berry",
        "Thickclub": "Thick Club",
        "Thunderstone": "Thunder Stone",
        "Tinymushroom": "Tiny Mushroom",
        "Toxicorb": "Toxic Orb",
        "Twistedspoon": "Twisted Spoon",
        "Wacanberry": "Wacan Berry",
        "Waterstone": "Water Stone",
        "Widelens": "Wide Lens",
        "Xenolite": "Xenolite",
        "Yacheberry": "Yache Berry",

    }
    return switch.get(item, "Invalid input")


def get_pokemon_data(name):
    """Given the internal name of a Pokémon, extracts and returns all information in pokemon.txt for
    that Pokémon.

    Args:
        name (string): The internal name of a Pokémon.

    Returns:
        dict: A dictionary containing all relevant information in pokemon.txt
    """

    with open(FOLDER_PATH + "pokemon.txt", encoding="utf8") as file:
        # Grabs the line
        line_list = [item.rstrip() for item in file.readlines()]

        # Contains all the lines including data about the Pokémon
        raw_data = []

        found_pokemon = False
        for x in range(0, len(line_list)):

            # Found the Pokémon we're looking for and it's related data
            if line_list[x] == "InternalName=" + name.upper():
                found_pokemon = True
                raw_data = line_list[x-1:x]
                continue

            # Now we have found the Pokémon, extract the necessary data
            if found_pokemon:
                raw_data.append(line_list[x])

                # Indicates the start of the next Pokémon's data - stop here
                if "InternalName" in line_list[x]:
                    found_pokemon = False
                    raw_data.remove(line_list[x])
                    raw_data.remove(line_list[x-1])
                    raw_data.remove(line_list[x-2])
                    break

        # Convert into a dictionary of key:value pair for easy access
        pokemon_dict = {key: value for line in raw_data for key,
                        value in [line.split('=', 1)]}

        if pokemon_dict["Type1"] == "SUONO":
            pokemon_dict["Type1"] = "SOUND"
        if "Type2" in pokemon_dict:
            if pokemon_dict["Type2"] == "SUONO":
                pokemon_dict["Type2"] = "SOUND"

        return pokemon_dict


def get_tm_tutor_data(name):

    with open(FOLDER_PATH + "tm.txt", encoding="utf8") as file:
        # Grabs the line
        line_list = [item.rstrip() for item in file.readlines()]

        # Contains all the lines including data about the Pokémon
        tm_list = []
        tutor_list = []

        for x in range(0, len(line_list)):
            names = line_list[x].split(",")

            matches = set(names).intersection(set([name.upper()]))
            # If a TM, adds TM num & name
            # if name.upper() in line_list[x]:
            if len(matches) > 0:

                # The highest TM is dark pulse, at 95
                if ((x/2) - 1) < 96:
                    if (x/2 - 1) // 10 > 0:
                        tm_list.append(str(int((x/2) - 1)))
                    else:
                        tm_list.append("0" + str(int((x/2) - 1)))

                # Otherwise, it can only be taught at move tutor
                else:
                    tutor_list.append(line_list[x-1].strip("[]").title())

        return tm_list, tutor_list


def create_infobox(pokemon_dict):
    infobox = []

    infobox.append("{{Pokemon Infobox")

    # Typing
    infobox.append("|type1 = " + pokemon_dict["Type1"].title())
    if "Type2" in pokemon_dict:
        infobox.append("|type2 = " + pokemon_dict["Type2"].title())

    # Name, Species
    infobox.append("|name = " + pokemon_dict["Name"])
    infobox.append("|species = " + pokemon_dict["Kind"])

    # Dex & Image
    dex_nums = pokemon_dict["RegionalNumbers"].split(",")
    if dex_nums[0] != "0":
        if len(dex_nums[0]) == 1:
            infobox.append("|ndex = 00" + dex_nums[0])
        elif len(dex_nums[0]) == 2:
            infobox.append("|ndex = 0" + dex_nums[0])
        else:
            infobox.append("|ndex = " + dex_nums[0])
    elif dex_nums[1] != "0":
        if len(dex_nums[1]) == 1:
            infobox.append("|ndex = X00" + dex_nums[1])
        elif len(dex_nums[1]) == 2:
            infobox.append("|ndex = X0" + dex_nums[1])
        else:
            infobox.append("|ndex = X" + dex_nums[1])
    else:
        if len(dex_nums[2]) == 1:
            infobox.append("|ndex = V00" + dex_nums[2])
        elif len(dex_nums[2]) == 2:
            infobox.append("|ndex = V0" + dex_nums[2])
        else:
            infobox.append("|ndex = V" + dex_nums[2])
    infobox.append("|image = " + pokemon_dict["Name"] + ".png")

    # Abilities
    reg_abilities = pokemon_dict["Abilities"].split(",")
    infobox.append("|ability1 = " + reg_abilities[0].title())
    if len(reg_abilities) > 1:
        infobox.append("|ability2 = " + reg_abilities[1].title())
    if "HiddenAbility" in pokemon_dict:
        infobox.append("|hiddenability = " +
                       pokemon_dict["HiddenAbility"].title())

    # Gender, Catch Rate
    infobox.append("|gendercode = " + gender_code(pokemon_dict["GenderRate"]))
    infobox.append("|catchrate = " + pokemon_dict["Rareness"])

    # Egg Groups & Steps
    egg_groups = pokemon_dict["Compatibility"].split(",")
    infobox.append("|egggroup1 = " + egg_groups[0])
    if len(egg_groups) > 1:
        infobox.append("|egggroup2 = " + egg_groups[1])
    infobox.append("|eggsteps = " + pokemon_dict["StepsToHatch"])

    # Metric height & weight
    infobox.append("|height-m = " + str(int(pokemon_dict["Height"])/10))
    infobox.append("|weight-kg = " + str(int(pokemon_dict["Weight"])/10))

    # Exp Yield & Level Rate
    infobox.append("|expyield = " + pokemon_dict["BaseEXP"])
    infobox.append("|lvrate = " + growth_rate(pokemon_dict["GrowthRate"]))

    # Colour & Friendship
    infobox.append("|color = " + pokemon_dict["Color"])
    infobox.append("|friendship = " + pokemon_dict["Happiness"])

    # Evs
    evs = pokemon_dict["EffortPoints"].split(",")
    if evs[0] != "0":
        infobox.append("|evhp = " + evs[0])
    if evs[1] != "0":
        infobox.append("|evat = " + evs[1])
    if evs[2] != "0":
        infobox.append("|evde = " + evs[2])
    if evs[3] != "0":
        infobox.append("|evsp = " + evs[3])
    if evs[4] != "0":
        infobox.append("|evsa = " + evs[4])
    if evs[5] != "0":
        infobox.append("|evsd = " + evs[5])

    # Closing brackets
    infobox.append("}}")

    return infobox


def create_opening_paragraph(pokemon_dict):
    opening_paragraph = []

    dual_type = "dual-type" if "Type2" in pokemon_dict else ""
    typing = "{{Type|" + pokemon_dict["Type1"].title() + "}}/{{Type|" + pokemon_dict["Type2"].title(
    ) + "}}" if "Type2" in pokemon_dict else "{{Type|" + pokemon_dict["Type1"].title() + "}}"

    # First line
    opening_paragraph.append(
        f"'''{pokemon_dict['Name']}''' is a {dual_type} {typing}-type Pokémon.")

    # TODO: ADD EVOLUTIONS HERE

    return opening_paragraph


# Really no way to do this without knowing italian, just here for posterity
def create_pokedex_entry(pokemon_dict):
    pokedex_entry = []

    pokedex_entry.append("{{Dex")
    pokedex_entry.append("|type = " + pokemon_dict["Type1"].title())
    if "Type2" in pokemon_dict:
        pokedex_entry.append("|type2 = " + pokemon_dict["Type2"].title())
    pokedex_entry.append("''WIP''")
    pokedex_entry.append("}}")

    return pokedex_entry


def create_wild_items(pokemon_dict):
    wild_items = []

    # Open box & fix colouring
    wild_items.append("{{HeldItems")
    wild_items.append("|type = " + pokemon_dict["Type1"].title())
    if "Type2" in pokemon_dict:
        wild_items.append("|type2 = " + pokemon_dict["Type2"].title())

    # Add wild item data
    if "WildItemCommon" in pokemon_dict and "WildItemUncommon" in pokemon_dict and "WildItemRare" in pokemon_dict:
        if pokemon_dict["WildItemCommon"] == pokemon_dict["WildItemUncommon"] and pokemon_dict["WildItemUncommon"] == pokemon_dict["WildItemRare"]:
            item = item_info(pokemon_dict["WildItemCommon"].title())
            wild_items.append(
                "|always = {{Item|" + item + "}} [[" + item + "]]")
    else:
        if "WildItemCommon" in pokemon_dict:
            item = item_info(pokemon_dict["WildItemCommon"].title())
            wild_items.append(
                "|common = {{Item|" + item + "}} [[" + item + "]]")
        if "WildItemUncommon" in pokemon_dict:
            item = item_info(pokemon_dict["WildItemUncommon"].title())
            wild_items.append(
                "|uncommon = {{Item|" + item + "}} [[" + item + "]]")
        if "WildItemRare" in pokemon_dict:
            item = item_info(pokemon_dict["WildItemRare"].title())
            wild_items.append("|rare = {{Item|" + item + "}} [[" + item + "]]")

    # Close box
    wild_items.append("}}")

    return wild_items


def create_stats(pokemon_dict):
    stats = []

    stats.append("{{Stats")
    stats.append("|type = " + pokemon_dict["Type1"].title())
    if "Type2" in pokemon_dict:
        stats.append("|type2 = " + pokemon_dict["Type2"].title())

    # Stats are given in HP/ATK/DEF/SPE/SPA/SPD
    raw_stats = pokemon_dict["BaseStats"].split(",")
    stats.append("|HP = " + raw_stats[0])
    stats.append("|Attack = " + raw_stats[1])
    stats.append("|Defense = " + raw_stats[2])
    stats.append("|SpAtk = " + raw_stats[4])
    stats.append("|SpDef = " + raw_stats[5])
    stats.append("|Speed = " + raw_stats[3])

    stats.append("}}")

    return stats


# Going to have to fill this in manually
def create_type_effectiveness(pokemon_dict):
    type_effectiveness = []

    type_effectiveness.append("{{TypeEffectiveness")
    type_effectiveness.append("|type1 = " + pokemon_dict["Type1"].title())
    if "Type2" in pokemon_dict:
        type_effectiveness.append("|type2 = " + pokemon_dict["Type2"].title())
    type_effectiveness.append("}}")

    return type_effectiveness


def create_level_learnlist(pokemon_dict):
    level_learnlist = []

    second_type = pokemon_dict["Type2"].title(
    ) if "Type2" in pokemon_dict else pokemon_dict["Type1"].title()

    level_learnlist.append("{{MoveLevelStart|" + pokemon_dict["Name"].title(
    ) + "|" + pokemon_dict["Type1"].title() + "|" + second_type + "}}")

    moves = pokemon_dict["Moves"].split(",")
    for x in range(0, len(moves)-1, 2):
        move_stuff = move_info(moves[x+1].title()).split(",")
        # print(moves[x+1].title())

        if (move_stuff[1] == "yes") and (move_stuff[2] == pokemon_dict["Type1"].title() or move_stuff[2] == second_type):
            level_learnlist.append(
                "{{MoveLevel+|" + moves[x] + "|" + move_stuff[0] + "|'''}}")
        else:
            level_learnlist.append(
                "{{MoveLevel+|" + moves[x] + "|" + move_stuff[0] + "}}")

    level_learnlist.append("{{MoveLevelEnd|" + pokemon_dict["Name"].title(
    ) + "|" + pokemon_dict["Type1"].title() + "|" + second_type + "}}")

    return level_learnlist


def create_tm_learnlist(pokemon_dict, tm_list):
    tm_learnlist = []

    second_type = pokemon_dict["Type2"].title(
    ) if "Type2" in pokemon_dict else pokemon_dict["Type1"].title()

    tm_learnlist.append("{{MoveTMStart|" + pokemon_dict["Name"].title(
    ) + "|" + pokemon_dict["Type1"].title() + "|" + second_type + "}}")

    for num in tm_list:
        tm_stuff = tm_info(num).split(",")
        if (tm_stuff[0] == "yes") and (tm_stuff[1] == pokemon_dict["Type1"].title() or tm_stuff[1] == second_type):
            tm_learnlist.append("{{MoveTM+|TM" + num + "|'''}}")
        else:
            tm_learnlist.append("{{MoveTM+|TM" + num + "}}")

    tm_learnlist.append("{{MoveTMEnd|" + pokemon_dict["Name"].title(
    ) + "|" + pokemon_dict["Type1"].title() + "|" + second_type + "}}")

    return tm_learnlist


def create_breeding_learnlist(pokemon_dict):
    breeding_learnlist = []

    second_type = pokemon_dict["Type2"].title(
    ) if "Type2" in pokemon_dict else pokemon_dict["Type1"].title()

    breeding_learnlist.append("{{MoveBreedStart|" + pokemon_dict["Name"].title(
    ) + "|" + pokemon_dict["Type1"].title() + "|" + second_type + "}}")

    if "EggMoves" in pokemon_dict:
        egg_moves = pokemon_dict["EggMoves"].split(",")
        breeding_moves = []

        breed_string = "{{EM|107|Smeargle}} '''WIP'''" if "Field" in pokemon_dict[
            "Compatibility"] else "'''WIP'''"

        for move in egg_moves:
            # print(move.title())
            egg_stuff = move_info(move.title()).split(",")
            if (egg_stuff[1] == "yes") and (egg_stuff[2] == pokemon_dict["Type1"].title() or egg_stuff[2] == second_type):
                breeding_moves.append(
                    "{{MoveBreed+|" + breed_string + "|" + egg_stuff[0] + "|'''}}")
            else:
                breeding_moves.append(
                    "{{MoveBreed+|" + breed_string + "|" + egg_stuff[0] + "}}")

        for line in sorted(breeding_moves):
            breeding_learnlist.append(line)
    else:
        breeding_learnlist.append("{{MoveBreedNone}}")

    breeding_learnlist.append("{{MoveBreedEnd|" + pokemon_dict["Name"].title(
    ) + "|" + pokemon_dict["Type1"].title() + "|" + second_type + "}}")

    return breeding_learnlist


def create_tutor_learnlist(pokemon_dict, tutor_list):
    tutor_learnlist = []

    second_type = pokemon_dict["Type2"].title(
    ) if "Type2" in pokemon_dict else pokemon_dict["Type1"].title()

    tutor_learnlist.append("{{MoveTutorStart|" + pokemon_dict["Name"].title(
    ) + "|" + pokemon_dict["Type1"].title() + "|" + second_type + "}}")

    tutor_moves = []
    for move in tutor_list:
        move_stuff = move_info(move).split(",")
        # print(move.title())
        if (move_stuff[1] == "yes") and (move_stuff[2] == pokemon_dict["Type1"].title() or move_stuff[2] == second_type):
            tutor_moves.append(
                "{{MoveTutor+|" + move_stuff[0] + "|'''|Varies}}")
        else:
            tutor_moves.append(
                "{{MoveTutor+|" + move_stuff[0] + "||Varies}}")

    for line in sorted(tutor_moves):
        tutor_learnlist.append(line)

    tutor_learnlist.append("{{MoveTutorEnd|" + pokemon_dict["Name"].title(
    ) + "|" + pokemon_dict["Type1"].title() + "|" + second_type + "}}")

    return tutor_learnlist


def create_sprites(pokemon_dict):

    second_type = pokemon_dict["Type2"].title(
    ) if "Type2" in pokemon_dict else pokemon_dict["Type1"].title()
    sprites = "{{sprites|name=" + pokemon_dict["Name"].title(
    ) + "|type=" + pokemon_dict["Type1"].title() + "|type2=" + second_type + "}}"

    return sprites


def main():
    # Get the name of the Pokémon for the wiki page
    print()
    internal_name = input("Input the name of the pokemon: ")

    # Get pokemon, move, and location data
    pokemon_data = get_pokemon_data(internal_name)
    tm_data, tutor_data = get_tm_tutor_data(internal_name)

    # Create the necessary components of the pokemon wiki page
    info_box = create_infobox(pokemon_data)
    open_para = create_opening_paragraph(pokemon_data)
    dex_entry = create_pokedex_entry(pokemon_data,)
    held_items = create_wild_items(pokemon_data)
    base_stats = create_stats(pokemon_data)
    type_eff = create_type_effectiveness(pokemon_data)
    level_learnset = create_level_learnlist(pokemon_data)
    tm_learnset = create_tm_learnlist(pokemon_data, tm_data)
    egg_learnset = create_breeding_learnlist(pokemon_data)
    tutor_learnset = create_tutor_learnlist(pokemon_data, tutor_data)
    sprite_string = create_sprites(pokemon_data)

    # Adding it all together
    wiki_page = []

    for line in info_box:
        wiki_page.append(str(line))
    for line in open_para:
        wiki_page.append(str(line))
    # Need to add evolution line here

    wiki_page.append("")
    wiki_page.append("")
    wiki_page.append("")

    wiki_page.append("=='''Pokédex entries'''==")
    for line in dex_entry:
        wiki_page.append(str(line))

    wiki_page.append("=='''Game locations'''==")

    wiki_page.append("=='''Held items'''==")
    for line in held_items:
        wiki_page.append(str(line))

    wiki_page.append("=='''Stats'''==")
    for line in base_stats:
        wiki_page.append(str(line))

    wiki_page.append("=='''Type effectiveness'''==")
    for line in type_eff:
        wiki_page.append(str(line))

    wiki_page.append("=='''Learnset'''==")
    wiki_page.append("==='''By leveling up'''===")
    for line in level_learnset:
        wiki_page.append(str(line))

    wiki_page.append("==='''By TM/HM'''===")
    for line in tm_learnset:
        wiki_page.append(str(line))

    wiki_page.append("==='''By breeding'''===")
    for line in egg_learnset:
        wiki_page.append(str(line))

    wiki_page.append("==='''By tutoring'''===")
    for line in tutor_learnset:
        wiki_page.append(str(line))

    wiki_page.append("=='''Sprites'''==")
    wiki_page.append(sprite_string)

    wiki_page.append("")
    wiki_page.append("")

    for line in wiki_page:
        print(line)


if __name__ == "__main__":

    while True:
        main()
