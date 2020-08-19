###########################################################
## File Name: scouting.py                                ##
## Description: Final project - Amanda Bishop            ##
##  Scouting program used for FIRST Robotics Teams       ##
## This program has file input and output, classes,      ##
## importing, sorting algorithms, videos, pictures,      ##
## different types of inputs                             ##
###########################################################
# Import statements
import pygame, buttons, inputs, random
from os import startfile
pygame.init()

# Initializing constants
W, H = 700, 480 
BLUE = (196, 242, 255)
PINK = (255, 190, 220)
BLACK = (0,0,0)
BROWN = (112, 90, 54)
WHITE = (255, 255, 255)
titleFont = pygame.font.SysFont("centurygothic", 55)
subTitleFont = pygame.font.SysFont("centurygothic", 40)
txtFont = pygame.font.SysFont("yugothicyugothicuilight", 20)
infoFont = pygame.font.SysFont("yugothicyugothicuilight", 30)

# Opens stats file to take out information about teams at competition
fi = open('stats.txt', 'r')
teamNums = []
stats = []
numOfTeams = int(fi.readline().strip())
for team in range(numOfTeams):
    teamNums.append(fi.readline().strip())
    stats.append(fi.readline().split())

# Team class 
class Team(object):
    # Initalizes all variables for the class
    def __init__(self,inputs,stats,file):
        self.number = inputs[0]
        self.hatches = int(inputs[1])
        self.balls = int(inputs[2])
        self.hab = int(inputs[3])
        self.weight = int(inputs[4])
        self.drive = inputs[5]
        self.defence = inputs[6]
        self.w = int(stats[0])
        self.l = int(stats[1])
        self.t = int(stats[2])
        self.opr = float(stats[3])
        self.dpr = float(stats[4])
        if self.w > self.l and self.w > self.t:
            self.wtl = 3
        elif self.t > self.w and self.t > self.l:
            self.wtl = 2
        else:
            self.wtl = 1
        self.file = file
        self.oRanking = 0
        self.dRanking = 0

    # Calculates the offensive ranking of the team based on the users inputs and the information from the file
    def offensiveRanking(self,sliderVs):
        hValue = sliderVs[0] / 10
        bValue = sliderVs[1] / 10
        habValue = sliderVs[2] / 10
        dValue = sliderVs[3] / 10
        wValue = sliderVs[4] / 10
        if self.hatches > 8:
            hatches = 3
        elif self.hatches == 8:
            hatches = 2
        else:
            hatches = 1
        if self.balls > 8:
            balls = 3
        elif self.balls == 8:
            balls = 2
        else:
            balls = 1
        if self.weight >= 100:
            weight = 3
        elif self.weight >= 90:
            weight = 2
        else:
            weight = 1
        if self.drive.lower() == 'swerve' or self.drive.lower() == 'mecanum':
            drive = 3
        elif self.drive.lower() == 'custom':
            drive = 2
        else:
            drive = 1
        ranking = (hatches * hValue) + (balls * bValue) + (self.hab * habValue) + (weight * wValue) + (drive * dValue)
        self.oRanking = (ranking * .7) + (self.wtl * .1) + (self.opr * .2)
        self.oRanking = round(self.oRanking, 2)

    # Calculates the defensive ranking of the team based on the users inputs and the information from the file
    def defensiveRanking(self,sliderVs):
        dValue = sliderVs[0] / 10
        wValue = sliderVs[1] / 10
        defenceValue = sliderVs[2] / 10
        if self.weight >= 100:
            weight = 3
        elif self.weight >= 90:
            weight = 2
        else:
            weight = 1
        if self.drive.lower() == 'swerve' or self.drive.lower() == 'mecanum':
            drive = 3
        elif self.drive.lower() == 'custom':
            drive = 2
        else:
            drive = 1
        if self.defence.lower() == 'yes':
            defence = 1
        else:
            defence = 0
        ranking = (weight * wValue) + (drive * dValue) + (defence * defenceValue)
        self.dRanking = (ranking * .7) + (self.wtl * .1) + (self.dpr * .2)
        self.dRanking = round(self.dRanking, 2)

# Insertion sort which is used to sort the teams in the rankings
def insertionSort(alist):
     # Iterates through the elements of the list starting on the second item
     for i in range( 1,len(alist)):
          # Assigns a variable to the element that is being moved
          tmp = alist[i]
          k = i
          # Iterates through the rest of the list, not including the last element, moving the elements to put the current list item in the list
          while k > 0 and tmp < alist[k - 1]:
               alist[k] = alist[k - 1]
               k -= 1
               alist[k] = tmp
     return alist

# Function to change the rankings of all the teams in the teams list
def calcRanks():
    global offensiveRanks
    global defensiveRanks
    offensiveRanks = []
    defensiveRanks = []
    for t in teams:
        t.offensiveRanking(values)
        offensiveRanks.append(t.oRanking)
        t.defensiveRanking(values2)
        defensiveRanks.append(t.dRanking)
    offensiveRanks = insertionSort(offensiveRanks)
    defensiveRanks = insertionSort(defensiveRanks)
    offensiveRanks.reverse()
    defensiveRanks.reverse()

# Function to write the rankings into the rankings file 
def saveRankings(offence,defence,teams):
    fi = open('rankings.txt','w')
    fi.write('Offensive Teams\n')
    count = 1
    for points in offence:
        for team in teams:
            if team.oRanking == points:
                fi.write(str(count) + '. ' + team.number + '\n')
                count += 1
    fi.write('\n')
    fi.write('Defensive Teams\n')
    count = 1
    for points in defence:
        for team in teams:
            if team.dRanking == points:
                fi.write(str(count) + '. ' + team.number + '\n')
                count += 1

# Function to randomly pick a picture
def pickImg():
    imgNum = random.randint(1,4)
    return 'pic' + str(imgNum) + '.jpg'


numbers = []
for team in teamNums:
    numbers.append(int(team))

# Function to write text on the scouting screen so user knows what to input
def txt(index):
    if index == 0:
        txtSurface = infoFont.render('Teams at competition:',True,BLACK)
        win.blit(txtSurface,((W/2) - (txtSurface.get_width()/2),200))
        nums = str(numbers)
        firstIndex = 1
        nextIndex = nums.index(str(numbers[8]))
        txtSurface = infoFont.render(nums[firstIndex:nextIndex],True,BLACK)
        win.blit(txtSurface,(50,230))
        firstIndex = nextIndex
        nextIndex = nums.index(str(numbers[16]))
        txtSurface = infoFont.render(nums[firstIndex:nextIndex],True,BLACK)
        win.blit(txtSurface,(50,260))
        firstIndex = nextIndex
        nextIndex = nums.index(str(numbers[24]))
        txtSurface = infoFont.render(nums[firstIndex:nextIndex],True,BLACK)
        win.blit(txtSurface,(50,290))
        firstIndex = nextIndex
        nextIndex = -1
        txtSurface = infoFont.render(nums[firstIndex:nextIndex],True,BLACK)
        win.blit(txtSurface,(50,320))
    elif index == 1:
        txtSurface = infoFont.render('Input the number of hatches the team',True,BLACK)
        win.blit(txtSurface,(150,250))
        txtSurface = infoFont.render('can place in one match',True,BLACK)
        win.blit(txtSurface,(200,280))
    elif index == 2:
        txtSurface = infoFont.render('Input the number of balls the team',True,BLACK)
        win.blit(txtSurface,(150,250))
        txtSurface = infoFont.render('can score in one match',True,BLACK)
        win.blit(txtSurface,(200,280))
    elif index == 3:
        txtSurface = infoFont.render('Input which hab level the team',True,BLACK)
        win.blit(txtSurface,(150,250))
        txtSurface = infoFont.render('can climb to. 1, 2, or 3',True,BLACK)
        win.blit(txtSurface,(200,280))
    elif index == 4:
        txtSurface = infoFont.render('Input the weight of the robot in pounds',True,BLACK)
        win.blit(txtSurface,(130,250))
    elif index == 5:
        txtSurface = infoFont.render('Input the drive train of the robot',True,BLACK)
        win.blit(txtSurface,(150,250))
        txtSurface = infoFont.render('swerve, mecanum, custom, or standard',True,BLACK)
        win.blit(txtSurface,(120,280))
    elif index == 6:
        txtSurface = infoFont.render('Input if the team is a defensive',True,BLACK)
        win.blit(txtSurface,(150,250))
        txtSurface = infoFont.render('team. Yes or no',True,BLACK)
        win.blit(txtSurface,(250,280))

# Checks if the input of the input box is valid
def inputIsValid(i,ans):
    if i == 0:
        return ans.isdigit() and ans in teamNums
    elif i == 1 or i == 2 or i == 4:
        return ans.isdigit()
    elif i == 3:
        return ans.isdigit() and int(ans) in range(1,4)
    elif i == 5:
        return ans.isalpha() and ans.lower() in ['swerve','mecanum','custom','standard']
    elif i == 6:
        return ans.isalpha() and ans.lower() in ['yes','no']

# Makes an error message for each input box
def error(i):
    if i == 0:
        return 'Invalid input. Please input one of the teams above'
    elif i == 1 or i == 2 or i == 4:
        return 'Invalid input. Please input a number'
    elif i == 3:
        return 'Invalid input. Please input a number from 1-3'
    elif i == 5:
        return 'Invalid input. Please input a drive train specified above'
    elif i == 6:
        return 'Invalid input. Please input yes or no'

# Draws the window
def drawWin():
    win.blit(pygame.image.load(img), (0, 0))
    global isMainScreen
    global isInfoScreen
    global isScoutingScreen
    global isWeightingScreen
    global answer
    global answered
    global teams
    # Draws the main screen
    if isMainScreen:
        txtSurface = titleFont.render('Scouting', True, BLACK)
        win.blit(txtSurface,((W/2) - (txtSurface.get_width()/2),100))
        info.draw(win)
        infotxt.draw(win,info.rect)
        startscout.draw(win)
        startscouttxt.draw(win,startscout.rect)
        weight.draw(win)
        weighttxt.draw(win,weight.rect)
        ranks.draw(win)
        rankstxt.draw(win,ranks.rect)
    # Draws the information screen
    if isInfoScreen:
        txtSurface = subTitleFont.render('Why Scouting is Important', True, BLACK)
        win.blit(txtSurface,((W/2) - (txtSurface.get_width()/2),50))
        txtSurface = txtFont.render('Scouting is important for FRC teams because it allows us',True,BLACK)
        win.blit(txtSurface,((W/2) - (txtSurface.get_width()/2),100))
        txtSurface = txtFont.render('to strategize with the teams on our alliances and make decisions',True,BLACK)
        win.blit(txtSurface,((W/2) - (txtSurface.get_width()/2),125))
        txtSurface = txtFont.render('for who we want on our alliance during the elimination rounds',True,BLACK)
        win.blit(txtSurface,((W/2) - (txtSurface.get_width()/2),150))
        txtSurface = txtFont.render('With over 91,000 students worldwide and over 5,000 in Canada alone this app',True,BLACK)
        win.blit(txtSurface,((W/2) - (txtSurface.get_width()/2),200))
        txtSurface = txtFont.render('will be useful in the many competitions throughout the FIRST Robotics',True,BLACK)
        win.blit(txtSurface,((W/2) - (txtSurface.get_width()/2),225))
        txtSurface = txtFont.render('competition season. It is also adjustable so it can be used in any game',True,BLACK)
        win.blit(txtSurface,((W/2) - (txtSurface.get_width()/2),250))
        txtSurface = txtFont.render('and at any tournament in the future.If you would like to watch a video',True,BLACK)
        win.blit(txtSurface,((W/2) - (txtSurface.get_width()/2),275))
        txtSurface = txtFont.render('from a competition please press the button below and then',True,BLACK)
        win.blit(txtSurface,((W/2) - (txtSurface.get_width()/2),300))
        txtSurface = txtFont.render('close the video player when you are finished the video',True,BLACK)
        win.blit(txtSurface,((W/2) - (txtSurface.get_width()/2),325))
        home.draw(win)
        hometxt.draw(win,home.rect)
        video.draw(win)
        videotxt.draw(win,video.rect)
    # Draws the screen for when the user is missing information
    if isMissingScreen:
        txtSurface = infoFont.render('You are currently missing information', True, BLACK)
        win.blit(txtSurface,((W/2) - (txtSurface.get_width()/2),100))
        txtSurface = infoFont.render('Return to the main screen to add more teams',True,BLACK)
        win.blit(txtSurface,((W/2) - (txtSurface.get_width()/2),150))
        txtSurface = infoFont.render('or to add weightings to the stats',True,BLACK)
        win.blit(txtSurface,((W/2) - (txtSurface.get_width()/2),200))
        home.draw(win)
        hometxt.draw(win,home.rect)
    # Draws the scouting screen
    if isScoutingScreen:
        # Creates input boxes if the user is currently answering the questions
        if answering:
            # Displays the error message if there is an error with the input
            if inputError:
                txtSurface = txtFont.render(error(index),True,BLACK)
                win.blit(txtSurface,((W/2) - (txtSurface.get_width()/2),370))
            # Draws buttons so user can toggle between which question they are answering
            for btn in qBtns:
                btn[0].draw(win)
                btn[1].draw(win,btn[0].rect)
            answer = inputBoxes[index].ask(win)
            txt(index)
        # Draws the file picker so the user can pick an image of a robot
        else:
            picker.draw(win)
    # Draws the screen after the scouting that lets the user scout or return to the main scree
    if isNextScreen:
        win.blit(pygame.image.load('robot.png'), (250, 50))
        scout.draw(win)
        scouttxt.draw(win,scout.rect)
        home.draw(win)
        hometxt.draw(win,home.rect)
    # Draws the screen that allows the user to adjust the weightings on the inputs
    if isWeightingScreen:
        for scale in scales:
            scale.draw(win)
            scale.title(win,(20,scale.y-5))
        nextb.draw(win)
        nexttxt.draw(win,nextb.rect)
        # Displays a message if the sliders don't equal 10
        if not sumTen:
            txtSurface = txtFont.render('Sum of the values must be 10',True,BLACK)
            win.blit(txtSurface,((W/2) - (txtSurface.get_width()/2),390))
    # Draws the second weighting screen
    if isWeighting2Screen:
        for scale in scales2:
            scale.draw(win)
            scale.title(win,(20,scale.y-5))
        nextb.draw(win)
        nexttxt.draw(win,nextb.rect)
        # Displays a message if the sliders don't equal 10
        if not sumTen:
            txtSurface = txtFont.render('Sum of the values must be 10',True,BLACK)
            win.blit(txtSurface,((W/2) - (txtSurface.get_width()/2),380))
    # Draws the screen showing the rankings of the teams
    if isRankingScreen:
        # Displays the top 5 offensive teams
        txtSurface = txtFont.render('Top Offensive Teams',True,BLACK)
        win.blit(txtSurface,(100,100))
        y = 150
        for t in range(5):
            for team in teams:
                if team.oRanking == offensiveRanks[t]:
                    txtSurface = txtFont.render(str(t+1) + '. ' + team.number,True,BLACK)
                    win.blit(txtSurface,(100,y))
                    y += 50
            if len(offensiveRanks) < 5 and t+1 == len(offensiveRanks):
                break
        # Displays the top 5 defensive teams
        txtSurface = txtFont.render('Top Defensive Teams',True,BLACK)
        win.blit(txtSurface,(400,100))
        y = 150
        for t in range(5):
            for team in teams:
                if team.dRanking == defensiveRanks[t]:
                    txtSurface = txtFont.render(str(t+1) + '. ' + team.number,True,BLACK)
                    win.blit(txtSurface,(400,y))
                    y += 50
            if len(defensiveRanks) < 5 and t+1 == len(defensiveRanks):
                break
        allteams.draw(win)
        allteamstxt.draw(win,allteams.rect)
        home.draw(win)
        hometxt.draw(win,home.rect)
    # Draws the screen with all of the team buttons
    if isTeamsScreen:
        for t in teamBtns:
            t[0].draw(win)
            t[1].draw(win,t[0].rect)
        home.draw(win)
        hometxt.draw(win,home.rect)
    # Draws the screen that shows all the details of the specific team
    if isDetailScreen:
        txtSurface = subTitleFont.render(currentTeam.number, True, BLACK)
        win.blit(txtSurface,((W/2) - (txtSurface.get_width()/2),50))
        txtSurface = infoFont.render('Offensive Ranking: ' + str(currentTeam.oRanking), True, BLACK)
        win.blit(txtSurface,(100,120))
        txtSurface = infoFont.render('Defensive Ranking: ' + str(currentTeam.dRanking), True, BLACK)
        win.blit(txtSurface,(100,150))
        txtSurface = infoFont.render('Hatches: ' + str(currentTeam.hatches), True, BLACK)
        win.blit(txtSurface,(100,180))
        txtSurface = infoFont.render('Balls: ' + str(currentTeam.balls), True, BLACK)
        win.blit(txtSurface,(100,210))
        txtSurface = infoFont.render('Hab Level: ' + str(currentTeam.hab), True, BLACK)
        win.blit(txtSurface,(100,240))
        txtSurface = infoFont.render('Weight: ' + str(currentTeam.weight), True, BLACK)
        win.blit(txtSurface,(100,270))
        txtSurface = infoFont.render('Drive Train: ' + str(currentTeam.drive), True, BLACK)
        win.blit(txtSurface,(100,300))
        win.blit(pygame.image.load(currentTeam.file), (400,200))
        allteams.draw(win)
        allteamstxt.draw(win,allteams.rect)
    pygame.display.update()

# Initializing variables
win = pygame.display.set_mode((W,H))
img = pickImg()

# Initializing buttons and their labels
info = buttons.Button((270,200,170,40))
infotxt = buttons.Label('Information',30)
startscout = buttons.Button((260,250,190,40))
startscouttxt = buttons.Label('Start Scouting',30)
weight = buttons.Button((260,300,190,40))
weighttxt = buttons.Label('Weightings',30)
ranks = buttons.Button((260,350,190,40))
rankstxt = buttons.Label('Rankings',30)
defence = buttons.Button((270,200,170,40))
defencetxt = buttons.Label('Defence',30)
offence = buttons.Button((260,250,190,40))
offencetxt = buttons.Label('Offence',30)
nextb = buttons.Button((330,410,70,40))
nexttxt = buttons.Label('Next',30)
allteams = buttons.Button((285,420,120,40))
allteamstxt = buttons.Label('Teams',30)
scout = buttons.Button((300,280,90,40))
scouttxt = buttons.Label('Scout',30)
home = buttons.Button((300,370,90,40))
hometxt = buttons.Label('Home',30)
video = buttons.Button((255,430,190,40))
videotxt = buttons.Label('Play the Video',30)

inPlay = True

questions = ['Team Number','Number of hatches','Number of balls','Hab climb','Weight','Drive train','Defence']
inputBoxes = []
answers = []
answer = None
answered = False
answering = True
index = 0

# Builds a list of inputboxes
for q in questions:
    inputBox = inputs.Inputbox(q,PINK,BLACK)
    inputBoxes.append(inputBox)

# Builds buttons to toggle between input boxes
answers = []
qs = ['Number','Hatches','Balls','Hab','Weight','Drive','Defence']
qBtns = []
x = 40
y = 400
for q in qs:
    btn = buttons.Button((x,y,75,30))
    label = buttons.Label(q,15)
    qBtns.append([btn,label])
    answers.append(None)
    x += 90

titles = ['Hatches','Balls','Hab','Drive','Weight']
scales = []
values = []

# Builds list of sliders
y = 40
for s in range(5):
    scale = inputs.Slider(titles[s],100,600,y,200)
    scales.append(scale)
    values.append(scale.returnValue)
    y += 80


titles2 = ['Drive','Weight','Defence']
scales2 = []
values2 = []

# Builds second list of sliders
y = 40
pos = 300
for s in range(3):
    scale = inputs.Slider(titles2[s],100,600,y,pos)
    scales2.append(scale)
    values2.append(scale.returnValue)
    y += 100
    if pos == 300:
        pos = 250

picker = inputs.Filepicker('Picture of robot',(200,200,300,50))
file = ''

teams = []
offensiveRanks = []
defensiveRanks = []

# Builds list of team buttons
teamBtns = []
x = 75
y = 50
count = 0
for num in teamNums:
    t = buttons.Button((x,y,70,40))
    ttxt = buttons.Label(num,30)
    teamBtns.append([t,ttxt])
    y += 50
    count += 1
    if count == 6:
        x += 100
        y = 50
        count = 0
currentTeam = None

sumTen = True
asking = True
release = False
weightsAdded = False
onPage = False
clicked = False
inputError = False

# Initializes all screens
isMainScreen = True
isInfoScreen = False
isScoutingScreen = False
isNextScreen = False
isWeightingScreen = False
isWeighting2Screen = False
isRankingScreen = False
isTeamsScreen = False
isMissingScreen = False
isDetailScreen = False

# Main game loop
while inPlay:
    drawWin()
    pygame.time.delay(10)
    mousePos = pygame.mouse.get_pos()                               # Gets mouse position
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN:
            # Sends the key that has been pressed to the inputbox
            if isScoutingScreen and not release:
                inputBoxes[index].getKey(event.key)
                release = True
            if event.key == pygame.K_ESCAPE:
                inPlay = False                                      # Lets the user exit the program
            if event.key == pygame.K_RETURN:
                # Sets answered to true once the input has been submitted
                if isScoutingScreen:
                    answered = True
                    inputError = False
                    drawWin()
            if event.key == pygame.K_BACKSPACE:
                # Sets answered to false once the backspace has been hit
                if isScoutingScreen:
                    inputError = False
                    answered = False
                    drawWin()
        if event.type == pygame.KEYUP:
            # Sets key release to false once the key is no longer being pressed down
            if isScoutingScreen:
                release = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if isMainScreen:
                # Sends user to the information screen once they have pressed the button
                if info.collide(mousePos) != -1:
                    img = pickImg()
                    isMainScreen = False
                    isInfoScreen = True
                # Sends user to the scouting screen once they have pressed the button
                if startscout.collide(mousePos) != -1:
                    img = pickImg()
                    asking = True
                    isMainScreen = False
                    isScoutingScreen = True
                # Sends user to the weightings screen if they have already inputted teams and they have pressed the button
                if weight.collide(mousePos) != -1 and len(teams) > 0:
                    img = pickImg()
                    isMainScreen = False
                    isWeightingScreen = True
                    drawWin()
                # Sends user to the ranking screen if they have already inputted teams, added the weights, and pressed the button
                if ranks.collide(mousePos) != -1 and len(teams) > 0 and weightsAdded:
                    img = pickImg()
                    calcRanks()
                    isMainScreen = False
                    isRankingScreen = True
                    drawWin()
                # Sends the user to the missing information screen if they do not have all the data they need
                if weight.collide(mousePos) != -1 and len(teams) == 0 or ranks.collide(mousePos) != -1 and len(teams) == 0 or ranks.collide(mousePos) != -1 and not weightsAdded:
                    img = pickImg()
                    isMainScreen = False
                    isMissingScreen = True
            if isInfoScreen:
                # Sends the user to the main screen if they pressed the button
                if home.collide(mousePos) != -1:
                    img = pickImg()
                    isInfoScreen = False
                    isMainScreen = True
                # Plays a video from a competition if they pressed the button
                if video.collide(mousePos) != -1:
                    movie = startfile('comp.mp4')
            if isMissingScreen:
                # Sends the user to the main screen if they pressed the button
                if home.collide(mousePos) != -1:
                    img = pickImg()
                    isMissingScreen = False
                    isMainScreen = True
            if isScoutingScreen:
                # Checks if the user pressed one of the inputbox buttons and takes them to that inputbox
                if answering:
                    for btn in qBtns:
                        if btn[0].collide(mousePos) != -1:
                            index = qBtns.index(btn)
                            answer = None
                            clicked = True
                # Lets user pick picture of the robot from their computer 
                if picker.btn.collide(mousePos) != -1 and not answering:
                    file = picker.returnFile()
            if isNextScreen:
                # Sends the user to the scouting screen if they pressed the button
                if scout.collide(mousePos) != -1:
                    img = pickImg()
                    isNextScreen = False
                    isScoutingScreen = True
                # Sends the user to the main screen if they pressed the button
                if home.collide(mousePos) != -1:
                    img = pickImg()
                    isNextScreen = False
                    isMainScreen = True
            if isWeightingScreen:
                # Lets the user move the scales to adjust the weightings
                for scale in scales:
                    if mousePos[1] >= (scale.y - 5) and mousePos[1] <= (scale.y + 5): 
                        scale.mouseDown = True
                # Sends the user to the next weighting screen if they pressed the button and the scales add up to 10
                if nextb.collide(mousePos) != -1 and sumTen:
                    img = pickImg()
                    isWeightingScreen = False
                    isWeighting2Screen = True
                    sumTen = False
                    drawWin()
            if isWeighting2Screen:
                # Lets the user move the scales to adjust the weightings
                for scale in scales2:
                    if mousePos[1] >= (scale.y - 5) and mousePos[1] <= (scale.y + 5):
                        scale.mouseDown = True
                # Sends the user to the next main screen if they pressed the button and the scales add up to 10
                if nextb.collide(mousePos) != -1 and sumTen:
                    weightsAdded = True
                    isWeighting2Screen = False
                    isMainScreen = True
            if isRankingScreen:
                # Sends the user to the main screen if they pressed the button
                if home.collide(mousePos) != -1 and onPage:
                    img = pickImg()
                    isRankingScreen = False
                    isMainScreen = True
                # Sends the user to the teams screen if they pressed the button
                if allteams.collide(mousePos) != -1:
                    img = pickImg()
                    isRankingScreen = False
                    isTeamsScreen = True
                onPage = True
            if isTeamsScreen:
                # Iterates through the team buttons 
                for btn in teamBtns:
                    if btn[0].collide(mousePos) != -1:
                        for t in teams:
                            # Sends the user to the team detail screen for the team that they clicked on
                            if btn[1].txt == t.number:
                                currentTeam = t
                                img = pickImg()
                                isTeamsScreen = False
                                isDetailScreen = True
                        # If the team that was picked does not have information about it inputted sends the user to the missing information screen
                        if not isDetailScreen:
                            img = pickImg()
                            isTeamsScreen = False
                            isMissingScreen = True
                # Sends the user to the main screen if the button is pressed
                if home.collide(mousePos) != -1:
                    img = pickImg()
                    isTeamsScreen = False
                    isMainScreen = True
            if isDetailScreen:
                # Sends the user to the teams screen if the button is pressed
                if allteams.collide(mousePos) != -1:
                    img = pickImg()
                    isDetailScreen = False
                    isTeamsScreen = True
        if event.type == pygame.MOUSEBUTTONUP:
            # Resets mouse down to false
            if isWeightingScreen:
                for scale in scales:
                    scale.mouseDown = False
            # Resets mouse down to false
            if isWeighting2Screen:
                for scale in scales2:
                    scale.mouseDown = False
    if isMainScreen:
        onPage = False
    if isScoutingScreen:
        if answering:
            if answered:
                # Puts the answer in the answers list if it is a valid input
                if inputIsValid(index,answer):
                    answers[index] = answer
                    answered = False
                    index += 1
                # Sets the input error as true if the input is not balid
                else:
                    inputError = True
                    answered = False
                    drawWin()
                # Resets the index
                if index == len(inputBoxes):
                    index = 0
                # Allows the user to leave the inputboxes screen if all of the inputs are answered
                if None not in answers:
                    answered = False
                    answering = False
        else:
            if file != '':
                newTeam = Team(answers,stats[teamNums.index(answers[0])],file)              # Creates a new team class from the inputs
                teams.append(newTeam)                                                       # Adds the new team to the team list
                # Resets all the values and sends the user to the next screen
                file = ''
                answers = []
                for q in qBtns:
                    answers.append(None)
                answer = None
                answering = True
                for box in inputBoxes:
                    box.current_string = []
                img = pickImg()
                isScoutingScreen = False
                isNextScreen = True
                drawWin()          
    if isWeightingScreen:
        # Moves the scales based on the mouse and returns the value of the scale once it has been placed 
        for scale in scales:
            scale.moveCirc(mousePos)
            if not scale.mouseDown:
                values[scales.index(scale)] = scale.returnValue()
        # Sets sum ten with if all the scales add up to 10
        if sum(values) == 10:
            sumTen = True
        else:
            sumTen = False
    if isWeighting2Screen:
        # Moves the scales based on the mouse and returns the value of the scale once it has been placed 
        for scale in scales2:
            scale.moveCirc(mousePos)
            if not scale.mouseDown:
                values2[scales2.index(scale)] = scale.returnValue()
        # Sets sum ten with if all the scales add up to 10
        if sum(values2) == 10:
            sumTen = True
        else:
            sumTen = False
            
            
saveRankings(offensiveRanks,defensiveRanks,teams)                                       # Saves the rankings to the text file
pygame.quit()                                                                           # Quits the pygame
