####################################################################
# IMPORT
####################################################################

import sys
import math
import pygame

try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")


####################################################################
# IMPORT
####################################################################


if len(sys.argv) == 2:
    if sys.argv[1] == '-py2':
        PYTHON_V = 2
    elif sys.argv[1] == '-py3':
        PYTHON_V = 3
    else:
        print('Usage: python Corewar_visualizer.py [-py2][-py3]')
        raise SystemExit
else:
    print('Usage: python Corewar_visualizer.py [-py2][-py3]')
    raise SystemExit


####################################################################
# DEFINES
####################################################################

#show memory values
MASKED_MODE = False
# we'll continue to read the std entry until END_REACHED == 1
END_REACHED = 0
# bool == 1 if xml balise is detect, else 0. That allows different output on std out
SAVE_XML = 0

# Define windows size
WIDTH = 1920
HEIGHT = 1080
MAIN_PADDING_LEFT = 105
MAIN_PADDING_TOP = 105
MAIN_PADDING_BOTTOM = 225
MAIN_PADDING_RIGHT = 960

# Define colors
BLACK = ( 0, 0, 0 )
WHITE = ( 255, 255, 255 )
BACKGROUD = ( 0, 0, 60 )
BACKGROUD_LINE = ( 0, 18, 113 )
EDGE_LINE = ( 1, 242, 253 )

# Dark ones
D0 = BACKGROUD
D1 = ( 35, 21, 178 )
D2 = ( 93, 1, 112 )
D3 = ( 108, 54, 90 )
D4 = ( 88, 66, 138 )

# Middle ones
M0 = BACKGROUD_LINE
M1 = ( 255, 0, 255 )
M2 = ( 0, 240, 255 )
M3 = ( 255, 255, 50 )
M4 = ( 255, 0, 80 )

# Light ones
L0 = ( 255, 255, 255 )
L1 = ( 255, 255, 255 )
L2 = BACKGROUD
L3 = BACKGROUD
L4 = ( 255, 255, 255 )

P_COLOR_D = [D0,D1,D2,D3,D4]
P_COLOR_M = [M0,M1,M2,M3,M4]
P_COLOR_L = [L0,L1,L2,L3,L4]

OP_TAB = ["LIVE", "LD", "ST", "ADD", "SUB", "AND", "OR", "XOR", "ZJUMP", "LDI", "STI", "FORK", "LLD", "LLDI", "LFORK", "AFF"]

# initialise the game engine
pygame.init()

CINEMATIC = True
CINEMATIC_PATH = './src/ascii_video.xml'
# Open a new window
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("ULTIMATE VISUALIZER TM - [ESCAPE]:quit")
icon = pygame.image.load("./src/corewar_ico.jpg")
pygame.display.set_icon(icon)

bg_2 = pygame.image.load("./src/background.jpg")
bg_3 = pygame.image.load("./src/corewar_background_r2_mask.png")

spr_1 = pygame.image.load("./src/sprites/tron_disk_m.png")
spr_2 = pygame.image.load("./src/sprites/tron_disk_b.png")
spr_3 = pygame.image.load("./src/sprites/tron_disk_r.png")
spr_4 = pygame.image.load("./src/sprites/tron_disk_y.png")
PLAYERS_SPRITES = [0,spr_1,spr_2,spr_3,spr_4]

#Sounds and musics
click_sound = pygame.mixer.Sound('./src/bip.wav')
music = pygame.mixer.music.load("./src/music.wav")
pygame.mixer.music.play(-1)

# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()


####################################################################
# FUNCTIONS
####################################################################


def get_cells(memory_tree):
    cells = memory_tree.text.split(',')
    size = int(memory_tree.get('size'))
    side = int(math.ceil(math.sqrt(size)))
    cell_height = int((HEIGHT - MAIN_PADDING_TOP - MAIN_PADDING_BOTTOM) / side)

    return (cells, size, side, cell_height)


def draw_background(cells, size, side, cell_height):
    cells_space = HEIGHT - MAIN_PADDING_TOP - MAIN_PADDING_BOTTOM

    #frame_pad = PADDING - 2
    #pygame.draw.rect(screen, BACKGROUD_LINE, (frame_pad, frame_pad, HEIGHT - frame_pad * 2, HEIGHT - frame_pad * 2), 4)
    #pygame.draw.rect(screen, EDGE_LINE, (frame_pad, frame_pad, HEIGHT - frame_pad * 2, HEIGHT - frame_pad * 2), 2)

    #pygame.draw.rect(screen, BACKGROUD_LINE, (frame_pad * 2 + HEIGHT, frame_pad, WIDTH - HEIGHT - frame_pad * 3, HEIGHT - frame_pad * 2), 4)
    #pygame.draw.rect(screen, EDGE_LINE, (frame_pad * 2 + HEIGHT, frame_pad, WIDTH - HEIGHT - frame_pad * 3, HEIGHT - frame_pad * 2), 2)

    offset = 50
    i = 0
    while i < side + 1:
        x = (i % (side + 1)) * cells_space / side - 1
        # draw lines
        pygame.draw.line(screen, BACKGROUD_LINE, (MAIN_PADDING_LEFT - offset, MAIN_PADDING_TOP + x), (HEIGHT - MAIN_PADDING_BOTTOM + offset, MAIN_PADDING_TOP + x))
        # draw columns
        pygame.draw.line(screen, BACKGROUD_LINE, (MAIN_PADDING_LEFT + x, MAIN_PADDING_TOP - offset), (MAIN_PADDING_LEFT + x, HEIGHT - MAIN_PADDING_BOTTOM + offset))
        i += 1


def draw_video(memory_tree, cells, size, side, cell_height):
    #font = pygame.font.SysFont("Arial", cell_height)
    #font = pygame.font.Font('./src/NEON CLUB MUSIC.otf', int(cell_height / 2))
    cells_space = HEIGHT - MAIN_PADDING_TOP - MAIN_PADDING_BOTTOM

    i = 0
    while i < len(cells) - 1:
        #val = cells[i]
        char_color = int(cells[i])
        x = (int(i) % side) * cells_space / side + MAIN_PADDING_LEFT
        y = int(int(i) / side) * cells_space / side + MAIN_PADDING_TOP

        #val = font.render(val.upper(), True, WHITE)
        pygame.draw.rect(screen, (char_color, 0, char_color), (x, y, cell_height + 1, cell_height + 1))
        #screen.blit(val, (x + (cell_height / 5), y + (cell_height / 3.5)))
        i += 1


def draw_memory(memory_tree, cells, size, side, cell_height):
    font = pygame.font.Font('./src/arial-black.ttf', int(cell_height / 1.5))
    #font = pygame.font.Font('./src/NEON CLUB MUSIC.otf', int(cell_height / 2))
    cells_space = HEIGHT - MAIN_PADDING_TOP - MAIN_PADDING_BOTTOM

    i = 0
    while i < len(cells) - 1:
        val = cells[i]
        pid = int(cells[i + 1])
        x = (int(i / 2) % side) * cells_space / side + MAIN_PADDING_LEFT
        y = int(int(i / 2) / side) * cells_space / side + MAIN_PADDING_TOP

        val = font.render(val.upper(), True, P_COLOR_L[pid])
        pygame.draw.rect(screen, P_COLOR_M[pid], (x, y, cell_height + 2, cell_height + 2))
        screen.blit(val, (x + 1, y + 1))
        i += 2


def draw_centered_text(surface, text, x_min, x_max, y_min, y_max, font, color):
    text = font.render(text, True, color)
    rect = text.get_rect()
    text_x = x_max - ((x_max - x_min) / 2) - (rect[2] / 2)
    text_y = y_max - ((y_max - y_min) / 2) - (rect[3] / 2)
    print("rect:", rect, " x_min:", x_min, " x_max:", x_max, " text_x:", text_x)
    screen.blit(text, (text_x, text_y))


def draw_properties(player, process, y_start):
    player_id = int(player.get("id"))
    player_lives = player.get("nb_live")
    player_name = player.get("name").upper()
    font = pygame.font.Font('./src/arial-black.ttf', 10)
    x_start = 1133
    # draw player
    screen.blit(font.render("( " + str(player_id) + " ) " + player_name + " ( " + player_lives + " )", True, P_COLOR_M[player_id]), (x_start, y_start + 4))
    screen.blit(PLAYERS_SPRITES[player_id], (x_start, y_start + 27))

    # draw his process
    if process is not None:
        draw_centered_text(screen, "PID", x_start + 189, x_start + 216, y_start,  y_start +  27, font, P_COLOR_M[player_id])
        draw_centered_text(screen, process.get("process_id"), x_start + 216, x_start + 243, y_start,  y_start +  27, font, P_COLOR_M[player_id])
        draw_centered_text(screen, "LIVE", x_start + 297, x_start + 324, y_start,  y_start +  27, font, P_COLOR_M[player_id])
        draw_centered_text(screen, process.get("nb_live").upper(), x_start + 324, x_start + 351, y_start,  y_start +  27, font, P_COLOR_M[player_id])
        draw_centered_text(screen, "CAR", x_start + 405, x_start + 432, y_start,  y_start +  27, font, P_COLOR_M[player_id])
        draw_centered_text(screen, process.get("carry"), x_start + 432, x_start + 459, y_start,  y_start +  27, font, P_COLOR_M[player_id])

        draw_centered_text(screen, OP_TAB[int(process.find("current_action")[1].get("value"))], x_start + 432 + 54, x_start + 459 + 54, y_start,  y_start +  27, font, P_COLOR_M[player_id])
        draw_centered_text(screen, process.find("current_action")[2].get("value").upper(), x_start + 459 + 54, x_start + 486 + 54, y_start,  y_start +  27, font, P_COLOR_M[player_id])
        draw_centered_text(screen, process.find("current_action")[3].get("value").upper(), x_start + 486 + 54, x_start + 513 + 54, y_start,  y_start +  27, font, P_COLOR_M[player_id])
        draw_centered_text(screen, process.find("current_action")[4].get("value").upper(), x_start + 513 + 54, x_start + 540 + 54, y_start,  y_start +  27, font, P_COLOR_M[player_id])
        draw_centered_text(screen, process.find("current_action")[5].get("value").upper(), x_start + 540 + 54, x_start + 567 + 54, y_start,  y_start +  27, font, P_COLOR_M[player_id])
#
        ## show registers
        registers = process.find(".//registers")

        # draw registers indexes
        draw_centered_text(screen, "R01", x_start + 189, x_start + 216, y_start + 27,  y_start +  54, font, P_COLOR_M[player_id])
        draw_centered_text(screen, "R02", x_start + 189, x_start + 216, y_start + 54,  y_start +  81, font, P_COLOR_M[player_id])
        draw_centered_text(screen, "R03", x_start + 189, x_start + 216, y_start + 81,  y_start + 108, font, P_COLOR_M[player_id])
        draw_centered_text(screen, "R04", x_start + 189, x_start + 216, y_start + 108, y_start + 135, font, P_COLOR_M[player_id])

        draw_centered_text(screen, "R05", x_start + 297, x_start + 324, y_start + 27,  y_start +  54, font, P_COLOR_M[player_id])
        draw_centered_text(screen, "R06", x_start + 297, x_start + 324, y_start + 54,  y_start +  81, font, P_COLOR_M[player_id])
        draw_centered_text(screen, "R07", x_start + 297, x_start + 324, y_start + 81,  y_start + 108, font, P_COLOR_M[player_id])
        draw_centered_text(screen, "R08", x_start + 297, x_start + 324, y_start + 108, y_start + 135, font, P_COLOR_M[player_id])

        draw_centered_text(screen, "R09", x_start + 405, x_start + 432, y_start + 27,  y_start +  54, font, P_COLOR_M[player_id])
        draw_centered_text(screen, "R10", x_start + 405, x_start + 432, y_start + 54,  y_start +  81, font, P_COLOR_M[player_id])
        draw_centered_text(screen, "R11", x_start + 405, x_start + 432, y_start + 81,  y_start + 108, font, P_COLOR_M[player_id])
        draw_centered_text(screen, "R12", x_start + 405, x_start + 432, y_start + 108, y_start + 135, font, P_COLOR_M[player_id])

        draw_centered_text(screen, "R13", x_start + 513, x_start + 540, y_start + 27,  y_start +  54, font, P_COLOR_M[player_id])
        draw_centered_text(screen, "R14", x_start + 513, x_start + 540, y_start + 54,  y_start +  81, font, P_COLOR_M[player_id])
        draw_centered_text(screen, "R15", x_start + 513, x_start + 540, y_start + 81,  y_start + 108, font, P_COLOR_M[player_id])
        draw_centered_text(screen, "R16", x_start + 513, x_start + 540, y_start + 108, y_start + 135, font, P_COLOR_M[player_id])

        # draw registers values
        screen.blit(font.render(registers.get("r1").upper(), True,  P_COLOR_M[player_id]), (x_start + 216 + 10, y_start + 27  + 6))
        screen.blit(font.render(registers.get("r2").upper(), True,  P_COLOR_M[player_id]), (x_start + 216 + 10, y_start + 54  + 6))
        screen.blit(font.render(registers.get("r3").upper(), True,  P_COLOR_M[player_id]), (x_start + 216 + 10, y_start + 81  + 6))
        screen.blit(font.render(registers.get("r4").upper(), True,  P_COLOR_M[player_id]), (x_start + 216 + 10, y_start + 108 + 6))
        screen.blit(font.render(registers.get("r5").upper(), True,  P_COLOR_M[player_id]), (x_start + 324 + 10, y_start + 27  + 6))
        screen.blit(font.render(registers.get("r6").upper(), True,  P_COLOR_M[player_id]), (x_start + 324 + 10, y_start + 54  + 6))
        screen.blit(font.render(registers.get("r7").upper(), True,  P_COLOR_M[player_id]), (x_start + 324 + 10, y_start + 81  + 6))
        screen.blit(font.render(registers.get("r8").upper(), True,  P_COLOR_M[player_id]), (x_start + 324 + 10, y_start + 108 + 6))
        screen.blit(font.render(registers.get("r9").upper(), True,  P_COLOR_M[player_id]), (x_start + 432 + 10, y_start + 27  + 6))
        screen.blit(font.render(registers.get("r10").upper(), True, P_COLOR_M[player_id]), (x_start + 432 + 10, y_start + 54  + 6))
        screen.blit(font.render(registers.get("r11").upper(), True, P_COLOR_M[player_id]), (x_start + 432 + 10, y_start + 81  + 6))
        screen.blit(font.render(registers.get("r12").upper(), True, P_COLOR_M[player_id]), (x_start + 432 + 10, y_start + 108 + 6))
        screen.blit(font.render(registers.get("r13").upper(), True, P_COLOR_M[player_id]), (x_start + 540 + 10, y_start + 27  + 6))
        screen.blit(font.render(registers.get("r14").upper(), True, P_COLOR_M[player_id]), (x_start + 540 + 10, y_start + 54  + 6))
        screen.blit(font.render(registers.get("r15").upper(), True, P_COLOR_M[player_id]), (x_start + 540 + 10, y_start + 81  + 6))
        screen.blit(font.render(registers.get("r16").upper(), True, P_COLOR_M[player_id]), (x_start + 540 + 10, y_start + 108 + 6))


def get_next_process(player_id, processes_tree):
    next_process = None
    shortest_cycle_to_wait = 99999
    for process in processes_tree:
        if int(process.get("player_id")) == player_id:
            if int(process.get("cycle_wait")) < shortest_cycle_to_wait:
                shortest_cycle_to_wait = int(process.get("cycle_wait"))
                next_process = process

    return next_process


def draw_players(players_tree, processes_tree):
    y_start = 256

    for player in players_tree:
        player_id = int(player.get("id"))
        process = get_next_process(player_id, processes_tree)
        draw_properties(player, process, y_start)
        y_start += 162


def draw_die_bar(arena_tree):
    period = int(arena_tree.get("period"))
    cycle_to_die = int(arena_tree.get("cycle_die"))
    nb_live = int(arena_tree.get("nb_live"))
    nb_check = int(arena_tree.get("nb_check"))
    length = int(1880 * period / cycle_to_die)

    if nb_live < nb_check:
        color = P_COLOR_M[4]
    else:
        color = P_COLOR_M[2]

    pygame.draw.rect(screen, color, (20, 925, length, 70), 0)


def draw_process_bar(cycle_to_wait, player_id, op_code, x, lenght):
    bar_height = int(cycle_to_wait / 6)
    if bar_height > 36:
        bar_height = 36
    pygame.draw.rect(screen, P_COLOR_M[player_id], (x, 1034 - bar_height, lenght, bar_height), 0)
    #font = pygame.font.Font('./src/NEON CLUB MUSIC.otf', 12)
    #screen.blit(font.render(OP_TAB[op_code], True, P_COLOR_L[player_id]), (x,HEIGHT))


def draw_processes_bar(processes_tree):
    sorted_processes = []
    for process in processes_tree:
        key = int(process.get("cycle_wait"))
        sorted_processes.append((key, process))
    #sorted_processes.sort()

    limit = 20
    i = 0
    x = 20
    for process in sorted_processes:
        cycle_to_wait = int(process[0])
        player_id = int(process[1].get("player_id"))
        length = int(1880 / len(sorted_processes))
        op_code = 0
        draw_process_bar(cycle_to_wait, player_id, op_code, x, length)
        x += length
        i += 1
        if i > limit:
            break


def draw_processes(processes_tree, cells, side, cell_height):
    font = pygame.font.SysFont("Arial", 18)
    #font = pygame.font.Font('./src/NEON CLUB MUSIC.otf', 18)
    cells_space = HEIGHT - MAIN_PADDING_TOP - MAIN_PADDING_BOTTOM

    processes_tree_length = len(processes_tree)
    for i in range(processes_tree_length):
        # highligth
        process = processes_tree[i]
        current_action = process.find(".//current_action")
        current_pos = int(current_action.get("pos"))

        val = cells[current_pos * 2].upper()
        pid = int(cells[current_pos * 2 + 1])
        x = (int(current_pos * 2 / 2) % side) * cells_space / side + MAIN_PADDING_LEFT
        y = int(int(current_pos * 2 / 2) / side) * cells_space / side + MAIN_PADDING_TOP

        #font2 = pygame.font.SysFont("Arial", cell_height)
        font2 = pygame.font.Font('./src/arial-black.ttf', int(cell_height / 1.5))
        val = font2.render(val, True, P_COLOR_M[pid])
        #pygame.draw.rect(screen, BACKGROUD, (x, y, cell_height, cell_height))
        pygame.draw.rect(screen, P_COLOR_L[pid], (x, y, cell_height + 1, cell_height + 1), 0)
        #pygame.draw.rect(screen, WHITE, (x, y, cell_height, cell_height), 2)
        screen.blit(val, (x + 1, y + 1))


####################################################################
# MAIN
####################################################################

screen_index = 0
screen_diff = 1
screen_tab = []
line = ''

KEY_LEFT = False
KEY_RIGHT = False
KEEP_MOVING = True

ascii_intro = open(CINEMATIC_PATH, "r")

while carryOn:

    if CINEMATIC == True :
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                carryOn = False # Flag that we are done so we exit this loop
            if event.type == pygame.KEYDOWN: # If user clicked close
                if event.key == pygame.K_ESCAPE:
                    carryOn = False # Flag that we are done so we exit this loop
                if event.key == pygame.K_SPACE:
                    CINEMATIC = False
                    pygame.mixer.Sound.play(click_sound)
        line = ascii_intro.readline()
        line = str(line)
        corewar_video_src = line
        if '<end_reached/>' in line:
            CINEMATIC = False
        if "<?xml version='1.0' encoding='UTF-8'?>" not in line and '<end_reached/>' not in line:
            #print(corewar_video_src)
            corewar_src_tree = etree.fromstring(corewar_video_src)
            #print("tree added - screen_tab_len: ", len(screen_tab))
        
            # First, clear the screen to white.
            screen.fill(BACKGROUD)
            screen.blit(bg_2, (0, 0))
        
            memory_tree = corewar_src_tree.find(".//memory")
            cells, size, side, cell_height = get_cells(memory_tree)
        
            # Draw memory grid
            draw_video(memory_tree, cells, size, side, cell_height)

    else:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                carryOn = False # Flag that we are done so we exit this loop
            if event.type == pygame.KEYDOWN: # If user clicked close
                if event.key == pygame.K_ESCAPE:
                    carryOn = False # Flag that we are done so we exit this loop
                if event.key == pygame.K_SPACE:
                    KEEP_MOVING = True if KEEP_MOVING == False else False
                    pygame.mixer.Sound.play(click_sound)
                if event.key == pygame.K_LEFT:
                    print("left pressed - screen_index: ", screen_index)
                    KEY_LEFT = True
                    KEEP_MOVING = False
                    pygame.mixer.Sound.play(click_sound)
                    #screen_index = screen_index - 1 if screen_index > 0 else screen_index
                if event.key == pygame.K_RIGHT:
                    print("right pressed - screen_index: ", screen_index)
                    KEY_RIGHT = True
                    KEEP_MOVING = False
                    pygame.mixer.Sound.play(click_sound)
                    #screen_index = screen_index + 1 if screen_index < len(screen_tab) else screen_index
            if event.type == pygame.KEYUP: # If user clicked close
                if event.key == pygame.K_LEFT:
                    KEY_LEFT = False
                if event.key == pygame.K_RIGHT:
                    KEY_RIGHT = False
                if event.key == pygame.K_KP_PLUS:
                    screen_diff *= 2
                    print("screen_diff: ", screen_diff)
                    pygame.mixer.Sound.play(click_sound)
                if event.key == pygame.K_KP_MINUS:
                    screen_diff /= 2 if screen_diff > 1 else 1
                    print("screen_diff: ", screen_diff)
                    pygame.mixer.Sound.play(click_sound)
    
        if KEY_LEFT == True:
            screen_index = screen_index - screen_diff if screen_index > 0 else screen_index
            #print("left pressed - screen_index: ", screen_index)
        if KEY_RIGHT == True or KEEP_MOVING == True:
            screen_index = screen_index + screen_diff if screen_index < len(screen_tab) - screen_diff else screen_index
            #print("right pressed - screen_index: ", screen_index)
    
        if END_REACHED == 0:
            corewar_src = ''
            while True:
                try:
                    if PYTHON_V == 3:
                        line = input()
                    else:
                        line = raw_input()
                except EOFError:
                    break
                line = str(line)
                if (line == '<corewar>'):
                    SAVE_XML = 1
                if SAVE_XML == 1:
                    corewar_src += line
                # check if end of file
                if line == '</corewar>':
                    SAVE_XML = 0
                    break
                if line == '<end_reached/>':
                    END_REACHED = 1
    
        if END_REACHED == 0:
            corewar_src_tree = etree.fromstring(corewar_src)
            screen_tab.append(corewar_src_tree)
            #print("tree added - screen_tab_len: ", len(screen_tab))
    
        # First, clear the screen to white.
        screen.fill(BACKGROUD)
        screen.blit(bg_2, (0, 0))
    
        memory_tree = screen_tab[screen_index].find(".//memory")
        cells, size, side, cell_height = get_cells(memory_tree)
    
        # Draw memory grid
        draw_memory(memory_tree, cells, size, side, cell_height)
    
        # Draw background grid
        #draw_background(cells, size, side, cell_height)
    
        # Draw processes
        processes_tree = screen_tab[screen_index].find(".//processes")
        draw_processes(processes_tree, cells, side, cell_height)
    
        # Draw processes bar
        processes_tree = screen_tab[screen_index].find(".//processes")
        draw_processes_bar(processes_tree)
    
        # Draw die bar
        arena_tree = screen_tab[screen_index].find(".//arena")
        draw_die_bar(arena_tree)
    
        # Draw players
        players_tree = screen_tab[screen_index].find(".//players")
        draw_players(players_tree, processes_tree)
    
        screen.blit(bg_3, (0, 0))

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 60 frames per second.
    clock.tick(120)

#Once we have exited the main program loop we can stop the game engine.
pygame.quit()