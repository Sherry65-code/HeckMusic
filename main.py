from music import play, pause, load, stop, unpause, getSongLength
from music import exit
from dynamics import setHeader, goToBottom, getSongList, clearc, clear, isThere, getWidth, getHeight,  Fore, Back, Style, printLines, getSongs
from time import sleep
from calligraphy import printl
from sys import argv, stdin
from os import chdir, system, remove
from meta import getTitle, getArtist, getAlbum, setFileName
from gcolor import gcolor
import threading
import readline

paused = False

# Check for arguments count

if len(argv) == 1:
    print("Too less arguments")
    exit(1)
elif len(argv) > 2:
    print("Too many arguments")
    exit(1)
else:
    songloc = argv[1]

# if correct arguments then try changing directory into the specified directory, if director not found then report user

try:
    chdir(songloc)
except Exception as e:
    print("Wrong location")
    exit(1)

# Then display header

clear()
setHeader("HECKPLAYER")

# Then initialize pygame.mixer.music

# intialize
load()

songs = getSongList()

# Then check if songs are avaliable in the spectified directory

if len(songs) == 0:
    print(f"No Song Found in {songloc}")
    exit(1)
else:
    # If avaliable then print all of the songs that contain the .mp3 or .wav or .m4a title
    print("All Songs at current directory")
    getSongs()

# Then ask for song index in the specified list

while True:
    try:
        si = int(input("Song index to play:"))
        # then decrement the index inorder to fit the tradition of actual array structers
        si-=1
        break
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}NOT A INDEX{Style.RESET_ALL}")
    except KeyboardInterrupt:
        clear()
        print("Exiting")
        exit(0)



# Verify song avaliablity, if not found then exit the program

try:
    if isThere(songs[si]) == False:
        print("Song not found!")
        exit(1)
except Exception as e:
    print("Song not found!")
    exit(1)


def get_input():
    # get user input uninterruptedly
    global paused
    while True:
        input_char = stdin.read(1)
        if input_char == "p":
            if not paused:
                pause()
                paused = True
            else:
                unpause()
                paused = False
        elif input_char == "q":
            stop()

# start a new thread to get user input
input_thread = threading.Thread(target=get_input)
input_thread.daemon = True
input_thread.start()


while True:
    # intialize meta package
    setFileName(songs[si])

    # set song arguments
    songname = getTitle()
    songartist = getArtist()
    songalbum = getAlbum()

    # then start playing the song

    maxl = len(songs)
    load(songs[si])
    play()
    tstart = 0
    tmin = 0

    clear()
    # then set header
    setHeader(f"HECKMUSIC - Playing {songname}")
    printLines(getHeight()-12)
    progressbar=""
    lefttime=""
    righttime=f" {int(getSongLength()/60)}m:{int(getSongLength()%60)}s"
    
    printl(f"{songname}")
    print(f"{gcolor}{Style.BRIGHT}Artist:{Style.RESET_ALL} {songartist}")
    print(f"{gcolor}{Style.BRIGHT}Album:{Style.RESET_ALL}  {songalbum}")
    print()

    while tstart<getSongLength():
        if paused:
            continue
        try:
            # SET PROGRESSBAR LENGTH
            lefttime=f"{int(tstart/60)}m:{int(tstart%60)}s  "
            l = len(f"{lefttime}{righttime}")
            remains = getWidth()-l
            progressbar = f"{Back.WHITE}"
            barlength = (tstart/getSongLength())*remains
            x = 0
            while x<barlength-1:
                progressbar+=" "
                x+=1
            progressbar+=f"{Style.RESET_ALL}"
            leftover = remains-barlength
            x=0
            los = ""
            while x<leftover:
                los += " "
                x+=1
        
            if tstart > 59:
                tmin = int(tstart/60)
                tsec = int(tstart%60)
            else:
                tsec = tstart
            print(f"{lefttime}{progressbar}{los}{righttime}", end="\r", flush=True)
            tstart+=1
            sleep(1)
        except KeyboardInterrupt:
            clear()
            print("Exiting")
            stop()
            exit(0)
        except Exception as e:
            clear()
            print(e)
            exit(1)

    # After song gets over
    if len(songs)-1 == si:
        si = 0
    else:
        si += 1
