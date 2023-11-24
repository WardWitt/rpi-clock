
import pygame, sys, math, time, os, socket, configparser, logging
from pygame.locals import *
from LWRPClient import LWRPClient

logging.basicConfig(level=logging.DEBUG, filename='RPiclock.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s - %(asctime)s')

# Define Global Variables
global LWRP, LWRP_GPIO, LWRP_GPIO_Triggers, GPIO, GPIO1, GPIO2, GPIO3, GPIO4

# get our base path
base_dir = os.path.dirname(os.path.realpath(__file__))

# Load configuration
config = configparser.ConfigParser()
config.read(base_dir + '/RPiclock.ini')

# NTP status
timeStatus = False

counter = 0
logging.info('Start RPiclock')
# Store the Livewire Routing Protocol (LWRP) client connection here
LWRP = None
LWRP_GPIO = None
LWRP_GPIO_Triggers = {}

# Configuration parameters for the communication with the GPIO Device
LWRP_GPI_IpAddress = config['Livewire']['IP_Address']
LWRP_GPI_PortNumber = 93
LWRP_GPI_Password = None
GPO_Sources = [{'GPI_Port': 1, 'GPI_Pin': 0}, {'GPI_Port': 1, 'GPI_Pin': 1},
               {'GPI_Port': 1, 'GPI_Pin': 2}, {'GPI_Port': 1, 'GPI_Pin': 3},
               {'GPI_Port': 1, 'GPI_Pin': 4}]

# Define the GPIO Storage array
GPIO = [0,1,2,3,4]
GPIO[4] = 'high'

# Initialize the pygame class
# pygame.init()
pygame.display.init()
pygame.font.init()

# Figure out our IP Address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# connect() for UDP doesn't send packets
s.connect(('8.8.8.8', 0))
ipAddress = s.getsockname()[0]

##########################################################################
# Uncomment or edit the necessary lines for screen configuration         #
#                                                                        #
# For the Raspberry Pi Official 7" Touchscreen                           #
# bg = pygame.display.set_mode((800,480),pygame.FULLSCREEN)              #
#                                                                        #
# For testing on a PC Screen with Pi Resolution                          #
# bg = pygame.display.set_mode((800,480))                                #
#                                                                        #
# For the HDMI Connected Screen.  Set X and Y size accordingly           #
# bg = pygame.display.set_mode((1366,768),pygame.FULLSCREEN)             #
#                                                                        #
##########################################################################

bg = pygame.display.set_mode(tuple(map(int, config['Display']['Resolution'].split(','))))
pygame.mouse.set_visible(False)

image = pygame.image.load(config['Logo']['Logo_Image'])
# imageXY = tuple(map(int, config['Logo']['Logo_Position'].split(',')))

# Change color to preference (R,G,B) 255 max value
bgcolor = tuple(map(int, config['Color']['Background_Color'].split(',')))
clockcolor = tuple(map(int, config['Color']['Second_Color'].split(',')))
hourcolor = tuple(map(int, config['Color']['Hour_Color'].split(',')))

# Indicator ON colors
ind1color = tuple(map(int, config['Color']['Indicator_1_Color'].split(',')))
ind2color = tuple(map(int, config['Color']['Indicator_2_Color'].split(',')))
ind3color = tuple(map(int, config['Color']['Indicator_3_Color'].split(',')))
ind4color = tuple(map(int, config['Color']['Indicator_4_Color'].split(',')))
ind5color = tuple(map(int, config['Color']['Indicator_5_Color'].split(',')))

# Indicator OFF Colors
ind1offcolor = tuple(map(int, config['Color']['Indicator_1_Off_Color'].split(',')))
ind2offcolor = tuple(map(int, config['Color']['Indicator_2_Off_Color'].split(',')))
ind3offcolor = tuple(map(int, config['Color']['Indicator_3_Off_Color'].split(',')))
ind4offcolor = tuple(map(int, config['Color']['Indicator_4_Off_Color'].split(',')))
ind5offcolor = tuple(map(int, config['Color']['Indicator_5_Off_Color'].split(',')))

ipTxtColor = tuple(map(int, config['Color']['IP_Address_Color'].split(',')))
NTP_GoodColor = tuple(map(int, config['Color']['NTP_Good_Color'].split(',')))
NTP_BadColor = tuple(map(int, config['Color']['NTP_Bad_Color'].split(',')))

# Scaling to the right size for the clock display
digiclocksize  = int(bg.get_height()/4.5)
digiclockspace = int(bg.get_height()/10.5)
dotsize = int(bg.get_height()/90)
hradius = bg.get_height()/2.5
secradius = hradius - (bg.get_height()/26)

# Set relative indicator text size Larger number is smaller text ratio
indtxtsize = int(bg.get_height()/7)
bigtxtsize = int(bg.get_height()/2)

# Set relative indicator box size
indboxy = int(bg.get_height()/6.0)
indboxx = int(bg.get_width()/2.5)

# Off Air Alarm
bigboxy = int(bg.get_height())
bigboxx = int(bg.get_width()*0.55)

# Coordinates of items on display
xclockpos = int(bg.get_width()*0.2875)
ycenter = int(bg.get_height()/2)
xcenter = int(bg.get_width()/2)

# Set relative indicator box 'x' location
xtxtpos = int(bg.get_width()*0.77)

# Center the text in the indicator
xindboxpos = int(xtxtpos-(indboxx/2.0))

ind1y = int((ycenter*0.4)-(indboxy/2))       
ind2y = int((ycenter*0.8)-(indboxy/2))
ind3y = int((ycenter*1.2)-(indboxy/2))
ind4y = int((ycenter*1.6)-(indboxy/2))
ind5y = int((ycenter)-(indboxy/2))

txthmy = int(ycenter)
txtsecy = int(ycenter+digiclockspace)

# Fonts  
clockfont = pygame.font.Font(None,digiclocksize)
indfont = pygame.font.Font(None,indtxtsize)
bigfont = pygame.font.Font(None,bigtxtsize)
ipFont = pygame.font.Font(None, 30)

name1 = config['Indicator']['Indicator_1']
name2 = config['Indicator']['Indicator_2']
name3 = config['Indicator']['Indicator_3']
name4 = config['Indicator']['Indicator_4']
name5 = config['Indicator']['Indicator_5_Line_1']
name5a = config['Indicator']['Indicator_5_Line_2']

def connectLWRP():
    # Tries to establish a connection to the Axia GPIO Node
    
    if LWRP_GPI_IpAddress is not None:
        try:
            # Create new connection for GPI device
            LWRP_GPIO = LWRPClient(LWRP_GPI_IpAddress, LWRP_GPI_PortNumber)
        except Exception as e:
            print("EXCEPTION:", e)
            return (False, "Cannot connect to GPIO LiveWire device")
            
        try:
            LWRP_GPIO.login(LWRP_GPI_Password)
        except Exception as e:
            print("EXCEPTION:", e)
            return (False, "Cannot login to GPIO device")

        if LWRP_GPIO is not None:
##############################################################################
#       Add one of these to select trigger based upon GPI or GPO             #            
#            LWRP_GPIO.GPIDataSub(callbackGPO)                               #                                                                           #
#            LWRP_GPIO.GPODataSub(callbackGPO)                               #
##############################################################################
            LWRP_GPIO.GPODataSub(callbackGPO)
    return (True, LWRP)

def callbackGPO(data):
    # Fill the GPIO array with GPO status from the node
    for sourceNum, source in enumerate(GPO_Sources):
        GPIO[sourceNum] = data[0]['pin_states'][source['GPI_Pin']]['state']
    
def paraeqsmx(smx):
    return xclockpos-(int(secradius*(math.cos(math.radians((smx)+90)))))

def paraeqsmy(smy):
    return ycenter-(int(secradius*(math.sin(math.radians((smy)+90)))))

# Equations for hour markers
def paraeqshx(shx):
    return xclockpos-(int(hradius*(math.cos(math.radians((shx)+90)))))

def paraeqshy(shy):
    return ycenter-(int(hradius*(math.sin(math.radians((shy)+90)))))

# Set up Connection to Livewire System

connectLWRP()

# Indicator text
ind1txt = indfont.render(name1,True,bgcolor)
ind2txt = indfont.render(name2,True,bgcolor)
ind3txt = indfont.render(name3,True,bgcolor)
ind4txt = indfont.render(name4,True,bgcolor)
ipTxt = ipFont.render(ipAddress, True, ipTxtColor)

# Clock cover indicator text
ind5txt = bigfont.render(name5,True,bgcolor)
ind5atxt = bigfont.render(name5a,True,bgcolor)

# Indicator positions
txtposind1 = ind1txt.get_rect(centerx=xtxtpos,centery=int(ycenter*0.4))
txtposind2 = ind2txt.get_rect(centerx=xtxtpos,centery=int(ycenter*0.8))
txtposind3 = ind3txt.get_rect(centerx=xtxtpos,centery=int(ycenter*1.2))
txtposind4 = ind4txt.get_rect(centerx=xtxtpos,centery=int(ycenter*1.6))

# Logo position
imageXY = image.get_rect(centerx = xclockpos, centery = ycenter + int(secradius / 2))

# Off Air Alarm
txtposind5 = ind5txt.get_rect(centerx=int(xcenter*0.53),centery=int(ycenter*0.7))
txtposind5a = ind5atxt.get_rect(centerx=int(xcenter*0.6),centery=int(ycenter*1.3))

######################### Main program loop. ####################################

while True :
    pygame.display.update()

    bg.fill(bgcolor)

    # Retrieve seconds and turn them into integers
    sectime = int(time.strftime("%S",time.localtime(time.time())))

    # To get the dots in sync with the seconds
    secdeg  = (sectime+1)*6

    # Draw second markers
    smx=smy=0
    while smx < secdeg:
        pygame.draw.circle(bg, clockcolor, (paraeqsmx(smx),paraeqsmy(smy)),dotsize)
        smy += 6  # 6 Degrees per second
        smx += 6

    # Draw hour markers
    shx=shy=0
    while shx < 360:
        pygame.draw.circle(bg, hourcolor, (paraeqshx(shx),paraeqshy(shy)),dotsize)
        shy += 30  # 30 Degrees per hour
        shx += 30

    # Retrieve time for digital clock
    retrievehm    = time.strftime("%I:%M:%S",time.localtime(time.time()))
    digiclockhm   = clockfont.render(retrievehm,True,hourcolor)
    txtposhm      = digiclockhm.get_rect(centerx=xclockpos,centery=txthmy)

    # NTP warning flag
    counter += 1
    
    if counter == 600:
        chronyc = os.popen('chronyc -c tracking').read().split(',')
        lastTimeUpdate = time.time() - float(chronyc[3])

        if lastTimeUpdate < 2048:
            timeStatus = True
            logging.info('Last valad time update %f seconds ago', lastTimeUpdate)
        else:
            timeStatus = False
            logging.warning('!!! - Last valad time update %f seconds ago - !!!', lastTimeUpdate)
        counter = 0

    if timeStatus:
        pygame.draw.circle(bg, NTP_GoodColor, (dotsize + 5, bg.get_height()-dotsize - 5), dotsize)
    else:
        pygame.draw.circle(bg, NTP_BadColor, (dotsize + 5, bg.get_height()-dotsize - 5), dotsize)

    # Functions for the status indicators
    bg.blit(image, imageXY)
     
    # Render the normal screen
    bg.blit(digiclockhm, txtposhm)
        
    pygame.draw.rect(bg, ind1offcolor,(xindboxpos, ind1y, indboxx, indboxy))
    bg.blit(ind1txt, txtposind1)
        
    pygame.draw.rect(bg, ind2offcolor,(xindboxpos, ind2y, indboxx, indboxy))
    bg.blit(ind2txt, txtposind2)
        
    pygame.draw.rect(bg, ind3offcolor,(xindboxpos, ind3y, indboxx, indboxy))
    bg.blit(ind3txt, txtposind3)
    
    pygame.draw.rect(bg, ind4offcolor,(xindboxpos, ind4y, indboxx, indboxy))
    bg.blit(ind4txt, txtposind4)

    # Display IP address
    
    bg.blit(ipTxt, ipTxt.get_rect())

    # The GPIO Array is filled in the livewire routines with the state of the GPO of a node

    if GPIO[0] == "high":
        pass
    else:
        pygame.draw.rect(bg, ind1color,(xindboxpos, ind1y, indboxx, indboxy))
        bg.blit(ind1txt, txtposind1)

    if GPIO[1] == "high":
        pass
    else:
        pygame.draw.rect(bg, ind2color,(xindboxpos, ind2y, indboxx, indboxy))
        bg.blit(ind2txt, txtposind2)
        
    if GPIO[2] == "high":
        pass
    else:
        pygame.draw.rect(bg, ind3color,(xindboxpos, ind3y, indboxx, indboxy))
        bg.blit(ind3txt, txtposind3)

    if GPIO[3] == "high":
        pass
    else:
        pygame.draw.rect(bg, ind4color,(xindboxpos, ind4y, indboxx, indboxy))
        bg.blit(ind4txt, txtposind4)

    if GPIO[4] == "high":
        pass
    else:
        pygame.draw.rect(bg, ind5color,(0, 0, bigboxx, bigboxy))
        bg.blit(ind5txt, txtposind5)
        bg.blit(ind5atxt, txtposind5a)
    
    time.sleep(0.04)
    pygame.time.Clock().tick(25)
 
    for event in pygame.event.get() :
         if event.type == QUIT:
             pygame.quit()
             sys.exit()
         # Pressing q+t to exit
         elif event.type == KEYDOWN:
             if event.key == K_q and K_t:
                 pygame.quit()
       #          GPIO.cleanup()
                 sys.exit()
