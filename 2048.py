import random 
import sys
import termios
import contextlib
import os

@contextlib.contextmanager
def raw_mode(file):
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)


grid = []
moves = ('up','down','left','right')
keys = ['h','j','k','l']
empty_tiles = []

black = '\x1b[02;30m'
red = '\x1b[02;31m'
green = '\x1b[02;32m'
yellow = '\x1b[02;33m'
blue = '\x1b[02;34m'
magenta = '\x1b[02;35m'
cyan = '\x1b[02;36m'
white = '\x1b[02;37m'

def is_game_over():
    update_empty_tiles()
    if not empty_tiles: 
        return True
    else:
        return False

def update_empty_tiles():
    del empty_tiles[:] #empty the list
    for i in xrange(4):
        for j in xrange(4):
            if grid[i][j] == 0:
                empty_tiles.append((i*4)+j) 
        
def get_empty_tile():
    update_empty_tiles()
    if  not empty_tiles:
        return None
    else:
        return random.choice(empty_tiles)   
    

def move_tiles(user_move):
    if user_move == 'j':#'down':
        for col in xrange(4): #per column
            for row in reversed(xrange(4)):#from below
                k = row - 1 
                while grid[k][col]==0 and k>=0:
                    k = k-1
                if k==-1: #empty column
                    break
                if grid[row][col]==0 or grid[row][col] == grid[k][col]:
                    grid[row][col] += grid[k][col]
                    grid[k][col]=0
        return True
    elif user_move == 'k':#'up':
        for col in xrange(4): 
            for row in xrange(4):
                k = row + 1 
                while k<=3 and grid[k][col]==0:
                    k = k+1
                if k==4: #empty column
                    break
                if grid[row][col]==0 or grid[row][col] == grid[k][col]:
                    grid[row][col] += grid[k][col]
                    grid[k][col]=0
        return True
    elif user_move == 'h':#'left':
        for row in xrange(4): 
            for col in xrange(4):
                k = col + 1 
                while k <=3 and grid[row][k]==0:
                    k = k+1
                if k==4: 
                    break
                if grid[row][col]==0 or grid[row][col] == grid[row][k]:
                    grid[row][col] += grid[row][k]
                    grid[row][k]=0
        return True
    elif user_move == 'l':#'right':
        for row in xrange(4): 
            for col in reversed(xrange(4)):
                k = col - 1 
                while k >=0 and grid[row][k]==0:
                    k = k-1
                if k==-1: 
                    break
                if grid[row][col]==0 or grid[row][col] == grid[row][k]:
                    grid[row][col] += grid[row][k]
                    grid[row][k]=0
        return True
    return False
    
def init_grid():
    for i in xrange(4):
        grid.append([])
        for j in xrange(4):
            grid[i].append(i+j)
            #grid[i][j] = (i*4)+j
            grid[i][j]=0
    #initial config
    tile = pick_random_tile()
    rand = gen_random()
    set_tile_val(tile,rand)
    
    tile = pick_random_tile()
    rand = gen_random()
    set_tile_val(tile,rand)

def print_grid():
    os.system('clear')
    print black+"+-----+-----+-----+-----+"
    for i in xrange(4):
        print black+"|",
        for j in xrange(4):
            if grid[i][j]==0:
                print black+"%*d"%(3,0),
                print black+"|",
            if grid[i][j]==2:
                print blue+"%*d"%(3,2),
                print black+"|",
            elif grid[i][j]==4:
                print red+"%*d"%(3,4),
                print black+"|",
            elif grid[i][j]==8:
                print green+"%*d"%(3,8),
                print black+"|",
            elif grid[i][j]==16:
                print yellow+"%*d"%(3,16),
                print black+"|",
            elif grid[i][j]==32:
                print cyan+"%*d"%(3,32),
                print black+"|",
            elif grid[i][j]==64:
                print magenta+"%*d"%(3,64),
                print black+"|",
            elif grid[i][j]==128:
                print blue+"%*d"%(2,128),
                print black+"|",
            elif grid[i][j]==256:
                print blue+"%*d"%(2,256),
                print black+"|",
            elif grid[i][j]==512:
                print blue+"%*d"%(2,512),
                print black+"|",
            elif grid[i][j]==1024:
                print blue+"%*d"%(1,1024),
                print black+"|",
            elif grid[i][j]==2048:
                print blue+"%*d"%(1,2048),
                print black+"|",
        print black+"\n+-----+-----+-----+-----+\r"

def pick_random_tile():
    while True:
        tile = random.randint(0,15)
        row = tile //4
        col = tile % 4
        if grid[row][col]==0:
            return tile 

def set_tile_val(tile,val):
    if tile >=0 and tile <16:
        row = tile //4
        col = tile % 4
        grid[row][col]=val
    
def gen_random():
    choice = [2,4]
    return random.choice(choice)


def get_user_move():
    print 'exit with ^C or ^D'
    with raw_mode(sys.stdin):
        while True:
            ch = sys.stdin.read(1)
            if not ch or ch == chr(4):
                break
            return ch
        #print ch,ord(ch)
        #f ch in keys:
        #   return ch
        #print ch
    
def start_game():   
    while(is_game_over()==False):
        user_move = get_user_move() 
        #user_move = sys.stdin.read(1)
        move_done = move_tiles(user_move);
        # The following bit of obscure logic is to 
        # to fix the problem where adjacent nums of
		# the same value weren't getting added. It
		# needed an extra move from the user, therefore
		# I'm making the code do it , instead of the user.
        if move_done:
            move_done = move_tiles(user_move)
        print_grid()
        if move_done:   
            tile = pick_random_tile()
            rand = gen_random()
            set_tile_val(tile,rand)
            print_grid()
    print "Game Over :-(" 
        
def main():
    init_grid()
    print_grid()
    update_empty_tiles()
    start_game()    

if __name__ == "__main__":
    main()

