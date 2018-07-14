#OnePiecePaint.py
#Anish Aggarwal
#The program utilizes One Piece Characters in a novel invention (paint program) that makes One Piece Lovers Everywhere Happy. This paint program was made and it taught me the basics of graphics design along with unifying me to other anime lovers.
#2/1/2018

#Features (that are useful)-----------------------------------------------------------------------------------------------------------------------
#-Fill Tool
#-Animation: Flipping Tools when switching modes
#-Animation: When new page is selected, there is a flip animation
#-Animation: Changing colors when mouse is hovering over the slider
#-Animation: scroll opens when resizing or opening program
#-Additional shapes (Call Out, Polygon, Triangle)
#-Crop Tool, Select Tool, Rotate Tool
#-Flip Tool (Horizontal and Vertical, Move Tool
#-Undo/Redo
#-Text Tool,Spray Tool,Eye Dropper
#-Gradient Slider (changes in lightness)
#-Thickness Changing Slider
#-A small screen that shows the saving and opening images
#-Resizable Window with fixed ratios that can be made to fit any screen
#-Keyboard shortcuts for undo/redo and open/save
#-Amazing One Piece Song - The Very Strongest

#Attention To Detail-------------------------------------------------------------------------------------------------------------------------------
#-Resizing a button when hovering over it
#-Resizing screen is kept to aspect ratio
#-Lots of animations and blits are only done when needed to reduce lag
#-Shapes are outlined and circles are drawn at corners to make shapes look nice
#-Smooth Ellipse and Rectangle
#-The undo/redo list is added to when drawing is done not just when mousebutton event up
#-Font gets smaller and larger depending on length when saving
#-pxArray to make fill faster and more efficient
#-made open/save program to help thematic theme of the code

#######################################################################################################################################################
import pygame
import math
import os
import random
#######################################################################################################################################################

pygame.init()#pygame.init() was used to initialize the program

#Setting Screen Size-------------------------------------------------------------------------------------------------------------------------------------
size=[192,95]#Starting Screen Size that can be resized proportionally
screen = pygame.display.set_mode(size,pygame.RESIZABLE)#Makes the resizable screen
pygame.display.set_caption("One Piece Paint")#Makes the title of the program 'One Piece Paint'

#Music Startup-------------------------------------------------------------------------------------------------------------------------------------------
pygame.mixer.music.load("One Piece OST - The Very Very Very Strongest [extended].mp3")#Loads the music to the program
pygame.mixer.music.play(-1,0.0)#Plays the music forever 
pygame.mixer.music.set_volume(0.1)#Sets music at a low volume so that the user does not destroy his ears

#Variables---------------------------------------------------------------------------------------------------------------------------------------------

#Tool Variables---
tools=[["Pencil","Eraser","Fill"],["Eye Dropper","Spray","Text"]]#List of Tools for selection and blitting with indexes in the Img Dictionary
toolrects=[]#After tools are blit, they are appended to this list to check for collidepoint and hovering
curscounter=1#When typing determines when cursor gets blit 
typing=False#Tells the program whether user is typing for the text tool
request_exit=False#Tells the program when user finished typing

#Stamp Variables---
stampTool=["LuffyStamp","ChopperStamp","UssopStamp","ZoroStamp","SanjiStamp","EnelStamp","NamiStamp","RobinStamp","FrankyStamp"]#Liist of stamps for selection and blitting
stampX=[16,16,18,17,13,18,16,20,16]#List of where to blit the stamp ont the based on width of stamp

#Effect Variables---
effectRects=[]#After effects are blit, they are appended to this list to check for collidepoint and hovering
effectSurf=None#Stores the surface that the selection tool has selected for further manipulation
selecttool=False#Tells whether the selecttool is selecting
effectTool=[["Select","Crop","Move"],["Rotate","Flip Horizontal","Flip Vertical"]]#List of effects for selection and blitting with indexes in the Img Dictionary

#Shape Variables---
lisofshapes=[[["Line","Rectangle","Ellipse"],["Triangle","Polygon","Call Out"]]]#List of shapes for selection and blitting with indexes in the Img Dictionary
styleTools=["FilledPoly","UnfilledPoly"]#The styles that the shapes can be drawn in 
polygon_start=None#Tells whether the polygon has started to been drawn
Style=""#Tells whether Polygon is unfilled or filled when drawing

#Thickness Changing Variables---
thicknesscolour=(255,255,0)#The colour of thickness slider that changes when user hovers over it
thicknesslevel=[112,192]#starting position of thickness slider
draggingthick=False#Boolean that states whether thickness slider is being moved

#Colour/Shading Changing Variables---
shadinglevel=[67,192]#starting position of shading slider
gaugecolour=(0,255,0)#starting colour of shading slider that changes when user hovers over it
pos=[[39,3],[192,95],size]#position of color circle on the color selector
draggingshading=False#Boolean that states whether the shading slider is being moved
colour=(0,255,0)#the colour user has selected

#Undo/Redo Variables---
undolis=[]#List containing all previous images that user undid
redolis=[]#List containing all previous images that user redid if the user did not do some action later on

#Save/Load Variables---
openMenu=False#Tells the program whether user wants to go to Open Menu
saveMenu=False#Tells the program whether user wants to go to Save Menu
saving=False#Tells the program that the user is saving
saveFile=""#The name of the file that user is going to save
saveSC=False#Tells the program whether User used the control S shortcut for saving
openSC=False#Tells the program whether User used control O shortcut for opening
path_way = os.path.dirname(os.path.realpath(__file__))#Used to get the path to the file and then get all the saves

#Other Initialization Variables---
UsersItemsToDraw=[]#List that everything user does gets appended to
scroll=True#Tells program whether to use scroll opening animation
bookflip=True#Tells program whether to use bookflipping animation
newitem=True#Tells program if user has selected a new mode
hovermode=False#Tells program if user is hovering over a mode/coin so that the coin gets larger
Tool="..."#Variable that shows the tool that is in use
mode=""#Variable that tells the program the mode that is in use
flippicnum=0#The frame number for which the book is flipping
picnum=0#The frame number for which the scroll is unrolling
buttonrects=[]#The list that stores the coin rectangles and determines whether user is hhovering over the coins
Status=False#The variable that tells whether the mouse button is down 
changingtonorm=-1#The variable that states if a coin is flipping back to its regular side whether than flipping to show it is selected

origmodesmenu=["Tools","Stamps","Shapes","Effects"]#Copy of modesmenu that does not get changed
modesmenu=["Tools","Stamps","Shapes","Effects"]#List of modes that changes to show which mode is selected

toolbckg=["inkicon","inkicon","inkicon","inkicon","inkicon","inkicon"]#button background that shows the ink splatter and it changes to have the regular round ink stamps
origtoolbckg=["inkicon","inkicon","inkicon","inkicon","inkicon","inkicon"]#copy of button background that does not change

modehover=[3,2,1,0]#Mode hover tells which coin should be blit first so that when a user hovers over a coin the coin comes in front
#Image Dictionary that loads all images with their sizes proportional to a 192x95 screen-------------------------------------------------------
NewImgDict={#Coin Pictures and Animation
            "Selected":[pygame.image.load("SelectedMenu.png"),[10,9]],"coinflip_00_delay-0.1s.png":[pygame.image.load("coinflip_00_delay-0.1s.png"),[10,9]],
            "coinflip_01_delay-0.1s.png":[pygame.image.load("coinflip_01_delay-0.1s.png"),[10,9]],"coinflip_02_delay-0.1s.png":[pygame.image.load("coinflip_02_delay-0.1s.png"),[10,9]],
            "coinflip_03_delay-0.1s.png":[pygame.image.load("coinflip_03_delay-0.1s.png"),[10,9]],"coinflip_04_delay-0.1s.png":[pygame.image.load("coinflip_04_delay-0.1s.png"),[10,9]],
            "Stamps":[pygame.image.load("StampsButton.png"),[10,9]],"Shapes":[pygame.image.load("ShapesButton.png"),[10,9]],
            "Tools":[pygame.image.load("ToolsButton.png"),[10,9]],"Effects":[pygame.image.load("EffectsButton.png"),[10,9]],
            #Banner and Background Images/Icons---------------------------------------------------------------------------------------------------
            "title":[pygame.image.load("OPtitle.png"),[30,15]],
            "bckg":[pygame.image.load("onepiecepaintbkg.jpg"),[192,80]],"inkicon":[pygame.image.load("inkicon.png"),[15,15]],"inkstamp":[pygame.image.load("inkstamp.png"),[15,15]],
            "toolbutton":[pygame.image.load("blankmodebutton.png"),[7,7]],
            #Undo/Redo and Save/Open----------------------------------------------------------------------------------------------------------------
            "Undo":[pygame.image.load("undo.png"),[10,10]],"Redo":[pygame.image.load("redo.png"),[10,10]],
            "Save":[pygame.image.load("save.png"),[12,10]],"Open":[pygame.image.load("open.png"),[12,10]],"PicBord":[pygame.image.load("openFrame.png"),[32,50]],
            #Tool Pictures--------------------------------------------------------------------------------------------
            "Pencil":[pygame.image.load("penciltool.png"),[6,6]],"Eraser":[pygame.image.load("erasertool.png"),[6,6]],
            "Spray":[pygame.image.load("spraytool.png"),[6,6]],"Fill":[pygame.image.load("filltool.png"),[6,6]],
            "Eye Dropper":[pygame.image.load("eyedroptool.png"),[6,6]],"Text":[pygame.image.load("texttool.png"),[6,6]],
            #Effect Pictures--------------------------------------------------------------------------------------------
            "Crop":[pygame.image.load("croptool.png"),[6,6]],"Rotate":[pygame.image.load("rotatetool.png"),[6,6]],
            "Select":[pygame.image.load("selecttool.png"),[6,6]],"Flip Horizontal":[pygame.image.load("fliphorizontaltool.png"),[6,6]],
            "Move":[pygame.image.load("movetool.png"),[6,6]],"Flip Vertical":[pygame.image.load("flipverticaltool.png"),[6,6]],
            #Colour Images and Selection-------------------------------------------------------------------------------------------------
            "thicknessCirc":[pygame.image.load("thicknesscircle.jpg"),[6,6]],
            "Colourwheel":[pygame.image.load("colourwheel.png"),[14,14]],"strawhatcolour":[pygame.image.load("strawhatwheel.gif.png"),[12,9]],
            "black-white":[pygame.image.load("darkness_colourspectrum.png"),[30,5]],"strawhatlogo":[pygame.image.load("onepiecelogo.png"),[11,11]],
            #Stamp Pictures----------------------------------------------------------------------------------------------------------------------------
            "LuffyStamp":[pygame.image.load("Stamp1.png"),[25*600/1060,25]],
            "ChopperStamp":[pygame.image.load("Stamp2.png"),[25*650/1000,25]],"UssopStamp":[pygame.image.load("Stamp3.png"),[25*240/579,25]],"ZoroStamp":[pygame.image.load("Stamp4.png"),[25*677/1082,25]],
            "SanjiStamp":[pygame.image.load("Stamp5.png"),[25*1760/2268,25]],"EnelStamp":[pygame.image.load("Stamp6.png"),[25*232/539,25]],"NamiStamp":[pygame.image.load("Stamp7.png"),[25*250/479,25]],
            "RobinStamp":[pygame.image.load("Stamp8.png"),[25*392/1416,25]],"FrankyStamp":[pygame.image.load("Stamp9.png"),[25*331/621,25]],
            "Next":[pygame.image.load("nextarrow.png"),[3,3]],"Previous":[pygame.image.load("previousarrow.png"),[3,3]],"Wanted":[pygame.image.load("WantedPoster.png"),[35,45]],
            #Shape Pictures---------------------------------------------------------------------------------------------------------------------------
            "FilledPoly":[pygame.image.load("filledPoly.png"),[10,5]],"UnfilledPoly":[pygame.image.load("unfilledPoly.png"),[10,5]],"Line":[pygame.image.load("line.png"),[4,4]],
            "Rectangle":[pygame.image.load("rectangle.png"),[4,4]],"Ellipse":[pygame.image.load("ellipse.png"),[4,4]],"Triangle":[pygame.image.load("triangle.png"),[4,4]],
            "Polygon":[pygame.image.load("polygon.png"),[4,4]],"Call Out":[pygame.image.load("callout.png"),[4,4]]}


def resize():#Function that called when screen gets resized so that everything can get blit
    global size
    global UsersItemsToDraw
    global undoRect
    global redoRect
    global openRect
    global saveRect
    pygame.draw.rect(screen,(50,0,0),(0,0,size[0],int(15*size[1]/95)),)#Drawing Upper Banner
    screen.blit(ImgDict["title"],(0,0))#Title On Banner
    screen.blit(ImgDict["bckg"],(int(0*size[0]/192),int(15*size[1]/95)))#Blits background of paint program
    colorchange()
    shadingchange()
    thicknesschange()
    undoRect=screen.blit(ImgDict["Undo"],(int(143*size[0]/192),int(2*size[1]/95)))#Blits the undo arrow image and gets the rectangle so program can check for hovering and selection
    redoRect=screen.blit(ImgDict["Redo"],(int(154*size[0]/192),int(2*size[1]/95)))#Blits the redo arrow image and gets the rectangle so program can check for hovering and selection
    openRect=screen.blit(ImgDict["Open"],(int(165*size[0]/192),int(2*size[1]/95)))#Blits the open image and gets the rectangle so program can check for hovering and selection
    saveRect=screen.blit(ImgDict["Save"],(int(178*size[0]/192),int(2*size[1]/95)))#Blits the save image and gets the rectangle so program can check for hovering and selection

def font(text,fonttype,fontsize,pos,colour):#Function make the font I require based on specific parameters based on text fonttype (Arial) , size, position, and colour
    myfont = pygame.font.SysFont(fonttype, fontsize)#gets the font in relation to the type and size
    main_text = myfont.render(text, True, (255,255,255))#renders the white text outline specified
    #Border/Outline of font is made--------
    screen.blit(main_text,(pos[0]+1,pos[1]))
    screen.blit(main_text,(pos[0],pos[1]+1))
    screen.blit(main_text,(pos[0]-1,pos[1]))
    screen.blit(main_text,(pos[0],pos[1]-1))
    #----------------------------------------
    main_text = myfont.render(text, True, colour)#renders the man text 
    screen.blit(main_text,(pos[0],pos[1]))

def colorchange():#Re Blits the colour changing display
    global colour
    global pos
    global size
    screen.blit(ImgDict["strawhatcolour"],(int(36*size[0]/192),int(2*size[1]/95)))
    colourwheelrect=screen.blit(ImgDict["Colourwheel"],(int(35*size[0]/192),int(0*size[1]/95)))
    pygame.draw.rect(screen,colour,(int(84*size[0]/192),int(2*size[1]/95),int(11*size[0]/192),int(11*size[1]/95)),)#changes teh straw hat image to a different colour
    pygame.draw.circle(screen,(0,0,0),pos[0],int(5*size[0]/1536),int(3*size[0]/1536))#Draws the circle on the pixels of colour user selected
    screen.blit(ImgDict["strawhatlogo"],(int(84*size[0]/192),int(2*size[1]/95)))
    
def shadingchange():#Blits the shading display 
    global shadinglevel
    global size
    global gaugecolour
    pygame.draw.rect(screen,(50,0,0),(int(52*size[0]/192),int(4*size[1]/95),int(33*size[0]/192),int(7*size[1]/95)),)
    screen.blit(ImgDict["black-white"],(int(52*size[0]/192),int(5*size[1]/95)))
    pygame.draw.rect(screen,gaugecolour,(shadinglevel[0],int(4*size[1]/95),int(1*size[0]/192),int(7*size[1]/95)),)#blits the slider proportionally on B-W Spectrum in proportion to shadinglevel
    colorchange()#Ater shading changes the colour changes to match the shading
    
def thicknesschange():#Blits the thickness display
    global thicknesslevel
    global thickness
    pygame.draw.rect(screen,(50,0,0),(int(96*size[0]/192),int(0*size[1]/95),int(46*size[0]/192),int(15*size[1]/95)),)
    pygame.draw.rect(screen,(0,0,0),(int(97*size[0]/192),int(5*size[1]/95),int(30*size[0]/192),int(5*size[1]/95)),)
    pygame.draw.rect(screen,thicknesscolour,(thicknesslevel[0],int(4*size[1]/95),int(1*size[0]/192),int(7*size[1]/95)),)#blits the slider proportionally to thickness spectrum in relation to thickness level
    ratio=(thicknesslevel[0]-int(97*size[0]/192))/int(30*size[0]/192)#gets a ratio for thickness to e multiplied by based on thickness level
    thickness=max(int(7*ratio*size[0]/192),1)#sets a variable for thickness to be used in drawing shapes, tools, etc.
    screen.blit(pygame.transform.smoothscale(pygame.image.load("thicknesscircle.jpg"),(2*thickness,2*thickness)),(int(135*size[0]/192)-thickness,int(7*size[1]/95)-thickness))#changes based on thickness to show users the current thickness
    

def modeMenu(lisofbuttons):#Blits all buttons based on a list that is given and blits the background button image as well(Probably most useful function)
    rects=[]
    screen.blit(GifDict["frameflip_{0:02}.gif"][6],(int(-35*size[0]/192),int(25*size[1]/95)))#blits background so that a new buttons can be blit on top
    for xbutton in range(2):
        for ybutton in range(3):
            rects.append(screen.blit(ImgDict[toolbckg[xbutton*3+ybutton]],(int((6.5+17*(xbutton))*size[0]/192),int((19+15*(ybutton+1))*size[1]/95))))#blits the ink splatter or proper ink button based on the state that is stored in toolckg
            screen.blit(ImgDict[lisofbuttons[xbutton][ybutton]],(int((11+17*(xbutton))*size[0]/192),int((23+15*(ybutton+1))*size[1]/95)))#blits the button on top of the ink splatter or proper ink button
    return rects #returns the rects so I can check is user is hovering over again

def modeschange():#function used to flip coins when mode is selected and to change between different modes
    global modesmenu
    global modehover
    global changingtonorm
    global hovermode
    global flipcoincount
    global mode
    global Style
    global Tool
    rects=[None,None,None,None]#list of rectangle objects that will be returned to test if user is hovering ober the rectangle
    bckgofmode=ImgDict["bckg"].subsurface(int(0*size[0]/192),int(0*size[1]/95),int(45*size[0]/192),int(15*size[1]/95))
    screen.blit(bckgofmode,(int(0*size[0]/192),int(15*size[1]/95)))#blits the background of buttons so that buttons can be blit on top
    if "Selected" in modesmenu and "coinflip_{0:02}_delay-0.1s.png" in modesmenu:#checks if something is already selected
        changingtonorm=modesmenu.index("Selected")
        modesmenu[changingtonorm]="coinflip_{0:02}_delay-0.1s.png"#starts changing the selected mode to a normal button and changingtonorm stores the changing value
    elif modesmenu.count("coinflip_{0:02}_delay-0.1s.png")==0:#if nothing is being flipped, changing to norm becomes -1 so that everything stops
        changingtonorm=-1
    for toolmode in range(len(modehover)):#goes through the modehover to see which one is blit on top
        if modesmenu[modehover[toolmode]]=="coinflip_{0:02}_delay-0.1s.png" and modehover[changingtonorm]!=changingtonorm:#checks if something is being flipped and nothing is being changed back to its original state
            if flipcoincount==5:#if the flip count is 5, the gif is on its final frame 
                modesmenu[modehover[toolmode]]="Selected"#instead of flipping again, the item becomes selected so the selected image can be blit
            elif toolmode==3 and hovermode:#if the user is hovering over the button, the button gets larger
                rects[modehover[toolmode]]=screen.blit(pygame.transform.smoothscale(ImgDict['coinflip_{0:02}_delay-0.1s.png'.format(flipcoincount)],(int(11*size[0]/192),int(10*size[1]/95))),(int((1+10*modehover[toolmode])*size[0]/192),int(17*size[1]/95)))
                flipcoincount+=1
            else:#if the user if not hoveing over the button, the button stays at its normal size but continues to flip
                rects[modehover[toolmode]]=screen.blit(ImgDict['coinflip_{0:02}_delay-0.1s.png'.format(flipcoincount)],(int((2+10*modehover[toolmode])*size[0]/192),int(18*size[1]/95)))
                flipcoincount+=1
        elif modesmenu[modehover[toolmode]]=="coinflip_{0:02}_delay-0.1s.png":#checks if item is flipping but the image is flipping back to its original state
            if flipcoincount==5:
                modesmenu[modehover[toolmode]]=origmodesmenu[modehover[toolmode]]#if the flip is on its final frame, modesmenu item turns back to its original picture
            elif toolmode==3 and hovermode:#if the button is getting hovered over, the button gets larger, count adds 1
                rects[modehover[toolmode]]=screen.blit(pygame.transform.smoothscale(ImgDict['coinflip_{0:02}_delay-0.1s.png'.format(flipcoincount)],(int(11*size[0]/192),int(10*size[1]/95))),(int((1+10*modehover[toolmode])*size[0]/192),int(17*size[1]/95)))
                flipcoincount+=1
            else:#if the button is not getting hovered over, the button stays its original size and flips
                rects[modehover[toolmode]]=screen.blit(ImgDict['coinflip_{0:02}_delay-0.1s.png'.format(flipcoincount)],(int((2+10*modehover[toolmode])*size[0]/192),int(18*size[1]/95)))
                flipcoincount+=1
        if toolmode==3 and hovermode and modesmenu[modehover[toolmode]]!="coinflip_{0:02}_delay-0.1s.png":#checks if item is not flipping but instead getting hovered over and if so it makes the button larger
            rects[modehover[toolmode]]=screen.blit(pygame.transform.smoothscale(ImgDict[modesmenu[modehover[toolmode]]],(int(12*size[0]/192),int(11*size[1]/95))),(int((1+10*modehover[toolmode])*size[0]/192),int(17*size[1]/95)))            
        elif modesmenu[modehover[toolmode]]!="coinflip_{0:02}_delay-0.1s.png":#otherwise the button gets normally blit with its original size
            rects[modehover[toolmode]]=screen.blit(ImgDict[modesmenu[modehover[toolmode]]],(int((2+10*modehover[toolmode])*size[0]/192),int(18*size[1]/95)))
    if modesmenu.count("Selected")==1 and "coinflip_{0:02}_delay-0.1s.png" not in modesmenu:#if the item is selected
        if mode!="Shapes" and origmodesmenu[modesmenu.index("Selected")]=="Shapes":#if the mode is shapes the style changes to "..." so that shapes can be filled and unfilled
            Style="... "
        mode=origmodesmenu[modesmenu.index("Selected")]#the new mode gets set
        
    

    return rects # returns all the rects so that hovering and selection can be checked

      
        
    
#Main Mode################################################################################################################################################################################
running=True

while running:
    clicked=False#clicked is set to False at the beginnig of every loop because it is the variable that check if something was just clicked
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running = False
    #---------------------------------------------------------------------------------------------------
        if e.type == pygame.VIDEORESIZE:#if the window is resized
                x , y = e.w, e.h#the height and width is saved as x and y
                size=[x,y]#size gets saved to the heigth and width
                size[1]=int(size[0]*95/192)#keeps the ratio of the height proportionate to the width
                screen = pygame.display.set_mode(size,pygame.RESIZABLE)#screen gets set agains to accomodate the new size
                bckg=pygame.transform.smoothscale(pygame.image.load("onepiecepaintbkg.jpg"),size)#background gets reset
                #All Gifs get Resized from original ---------------------------------------------------------------------------------------------------------------------------------
                GifDict={"scroll{0:02}.png":[],"frameflip_{0:02}.gif":[]}#holds the empty dictionary of gifs and the individual frames
                Gifframes={"scroll{0:02}.png":[16,[152,80]],"frameflip_{0:02}.gif":[7,[80,70]]}#holds the number of frames and the size in relation to 192x95
                for filenam in list(Gifframes.keys()):#loops throught the gifs in the dictionary and gets the frames for each one
                    for i in range(Gifframes[filenam][0]):
                        GifDict[filenam].append(pygame.transform.scale(pygame.image.load(filenam.format(i)),[int(Gifframes[filenam][1][0]*size[0]/192),int(Gifframes[filenam][1][1]*size[1]/95)]))
                #All images  get resized from original NewGifDict--------------------------------------------------------------------------------------------------------------------
                ImgDict={}#ImgDict that stores all images that are resized to current screen size
                ThirdImgDict={}#copies the Img Dictionary so no shallow copies are traced back to original
                #loops through NewImgDictionary and saves newly sized images into ImgDict---
                for item in NewImgDict:
                    ThirdImgDict[item]=NewImgDict[item][:]
                for item in ThirdImgDict:
                    ImgDict[item]=pygame.transform.smoothscale(ThirdImgDict[item][0],[int(NewImgDict[item][1][0]*size[0]/192),int(NewImgDict[item][1][1]*size[1]/95)])
                #shading level changes in relation to size so that slider move proportionatly------
                shadinglevel[0]=int(shadinglevel[0]*size[0]/shadinglevel[1])
                shadinglevel[1]=size[0]
                #thickness level changes in relation to size so slider for thickness moves proportionatly------
                thicknesslevel[0]=int(thicknesslevel[0]*size[0]/thicknesslevel[1])
                thicknesslevel[1]=size[0]
                #Colour circle location changes----------------------------------------------------------------
                pos[0][0]=int(pos[1][0]*size[0]/pos[2][0])
                pos[0][1]=int(pos[1][1]*size[1]/pos[2][1])
                #---------------------------------------------------------------------------------------------
                scroll=True#when screen is resized scroll animation occurs again
                bookflip=True#when screen is resized bookflip animation occurs again
                newitem=True#when screen is resized the program sets the screen up as a new item
                saving=False#when screen is resized saving=False so that if the user is on savingMenu everything is reblit
                picnum=0#picnum is the frame for  the scroll animation so it is set to 0 to start the scroll animation
                flippicnum=0#flippicnum is the frame for  the book flip animation so it is set to 0 to start the book flip animation
                resize()
        if e.type == pygame.MOUSEBUTTONDOWN and e.button ==1:#checks that left mouse button has been pushed down
            clicked=True

        if e.type == pygame.KEYDOWN:#checks for keys in case of saving and text variable
           keys=pygame.key.get_pressed()
           if saving:#checks if user is saving
               if e.key == pygame.K_BACKSPACE:
                   if len(saveFile) > 0:#if savefile is greater than zero and user clicked backspace the file name deletes last character
                       saveFile = saveFile[:-1]
               elif e.key == pygame.K_KP_ENTER or e.key == pygame.K_RETURN:#otherwise if enter is clicked the text exits
                    request_exit = True
               elif e.key < 256 and e.unicode:#otherwise the key gets put into the save file name
                    saveFile += e.unicode
           if typing:#checks if user is typing
               if e.key == pygame.K_BACKSPACE:#if backspace is clicked and the msg has a character in it the last character gets deleted
                   if len(msg) > 0:
                       msg = msg[:-1]
               elif e.key == pygame.K_KP_ENTER or e.key == pygame.K_RETURN:#if user clicks enter then text stops
                    request_exit = True
               elif e.key < 256:#otherwise key is added to typing
                    msg += e.unicode
           if keys[pygame.K_LCTRL] and keys[pygame.K_z]==1 and len(undolis)>1 and not Status:#if user presses Control+Z-->the undo function occurs
              redolis.append(undolis[-1])#redo lis appends last item of undo
              undolis=undolis[:-1]#undo list deletes last item
              screen.blit(pygame.transform.smoothscale(undolis[-1],(int(113*size[0]/192),int(71*size[1]/95))),(int(63*size[0]/192),int(19*size[1]/95)))#the last item of undo is blit onto the screen
           if keys[pygame.K_LCTRL] and keys[pygame.K_y]==1 and len(redolis)>0 and not Status:#if user presses Control+Y-->the redo function occurs
              undolis.append(redolis[-1])#undo list appends last item of redo lis
              redolis=redolis[:-1]#the redo list deletes its last item
              screen.blit(pygame.transform.smoothscale(undolis[-1],(int(113*size[0]/192),int(71*size[1]/95))),(int(63*size[0]/192),int(19*size[1]/95)))#new last item of undo list gets blit
           if keys[pygame.K_LCTRL] and e.key==111:#if user presses Control+O --> the open short cuts becomes true
                openSC=True
           if keys[pygame.K_LCTRL] and e.key==115:#if user presses Control+S --> the save short cut becomes true
                saveSC=True
                
    mx,my=pygame.mouse.get_pos()
    mb=pygame.mouse.get_pressed()
    
    if picnum==16:#if the scroll animation is on the final frame
        scroll=False#scroll becomes false
        canvasRectangle=pygame.draw.rect(screen,(115,68,27),(int(63*size[0]/192),int(19*size[1]/95),int(113*size[0]/192),int(71*size[1]/95)),)#cavasRectangle gets defined to a rectangle
        if len(undolis)>1:
            screen.blit(pygame.transform.smoothscale(undolis[-1],(int(113*size[0]/192),int(71*size[1]/95))),(int(63*size[0]/192),int(19*size[1]/95)))#if the window was resize then the last item in undo is blit
        flippicnum=8#flippicnum becomes 8 and so that the loop does not go into flippic num after animations all done
        picnum=17#picnum gets set to 17 so undolis[-1] is not continuously blit
    if flippicnum==7:#if the book flip pic is on the last frame
       bookflip=False#bookflip animation becomes false
       if mode=="":
            screen.blit(ImgDict["title"],(int(9*size[0]/192),int(50*size[1]/95)))#if mode is "", the title One Piece Paint is blit onto the book
    if bookflip and flippicnum<7:#if the bookflip animation is true and the flippicnum is less than 7 than the current frame of the animation gets blit and 1 is added to the frame counter
        screen.blit(GifDict["frameflip_{0:02}.gif"][flippicnum],(int(-35*size[0]/192),int(25*size[1]/95)))
        flippicnum+=1
    if scroll:#if the scroll animation is True, the nect frame is blit but it checks if the book flip is not running and if it is not it blits the last frame on top so nothing gets covered up
        scrollrect=(int(40*size[0]/192),int(0*size[1]/95),int(152*size[0]/192),int(80*size[1]/95))
        bckgimage=ImgDict["bckg"].subsurface(scrollrect)#blits subsurfaced background so that scroll can be blit on top
        screen.blit(bckgimage,(int(40*size[0]/192),int(15*size[1]/95)))
        screen.blit(GifDict["scroll{0:02}.png"][abs(picnum)],(int(40*size[0]/192),int(15*size[1]/95)))
        picnum+=1
        if not bookflip:#if not bookflip blits last frame on top
            screen.blit(GifDict["frameflip_{0:02}.gif"][6],(int(-35*size[0]/192),int(25*size[1]/95)))
            if mode=="":
                screen.blit(ImgDict["title"],(int(9*size[0]/192),int(50*size[1]/95)))
        buttonrects=modeschange()#set the mode buttons
    
    if len(undolis)==0 and not scroll:#if undolis == 0, the undolis appends an empty canvas
        undolis.append(screen.copy().subsurface(int(63*size[0]/192),int(19*size[1]/95),int(113*size[0]/192),int(71*size[1]/95)))
    #Undo and Redo--------------------------------------------------------------------------------------------------------------
    if undoRect.collidepoint((mx,my)) and clicked and len(undolis)>1:#if the undo button is clicked the undo function is carried out
        redolis.append(undolis[-1])
        undolis=undolis[:-1]
        screen.blit(pygame.transform.smoothscale(undolis[-1],(int(113*size[0]/192),int(71*size[1]/95))),(int(63*size[0]/192),int(19*size[1]/95)))
    if redoRect.collidepoint((mx,my)) and clicked and len(redolis)!=0:#if the redo button is clicked the redo function is carried out
        undolis.append(redolis[-1])
        redolis=redolis[:-1]
        screen.blit(pygame.transform.smoothscale(undolis[-1],(int(113*size[0]/192),int(71*size[1]/95))),(int(63*size[0]/192),int(19*size[1]/95)))
    #Saving and Opening--------------------------------------------------------------------------------------------------------
    if saveMenu and not scroll and not bookflip:#if the saveMenu is clicked and the animations are not in affect
        if not saving:#if saving is false, everyting is blit once
            OPfont=pygame.font.Font("one piece font.ttf",int(2*size[0]/192))
            OPffont=pygame.font.Font("one piece font.ttf",int(2*size[0]/192))
            s=undolis[-1]
            s.set_colorkey((115,68,27))
            screen.blit(pygame.transform.scale(s,(int(25*size[0]/192),int(18*size[1]/95))),(int(11*size[0]/192),int(50*size[1]/95)))
            screen.blit(ImgDict["PicBord"],(int(7*size[0]/192),int(30*size[1]/95)))
            saving=True#sets saving to True
            saveFile=""#saveFile name becomes none
            ffsize=2#the font size
            txtParam=[17,82]#position of text in relation to 192x95
        curscounter+=1#counter adds 1
        
        txtPos=[int(txtParam[0]*size[0]/192),int(txtParam[1]*size[1]/95)]#txt position becomes sized in relation to the screen
        if saving:#if user is saving txt gets rendered
            txt = OPfont.render(saveFile, True, (0,0,0))#save file message is rendered
            fname=OPffont.render("File name:",True,(150,100,100))
            backgroundfont=GifDict["frameflip_{0:02}.gif"][6].subsurface((int(37*size[0]/192),int(57*size[1]/95),int(40*size[0]/192),int(10*size[1]/95)))#background of font is blit so font can be blit on top
            screen.blit(backgroundfont,((int(2*size[0]/192),int(82*size[1]/95))))#font gets put on top of background 
            screen.blit(fname,(int(10*size[0]/192),int(82*size[1]/95)))
            if txt.get_width()<int(15*size[0]/192) and ffsize<2:#checks if size is small and adds size to it if the font is less than 2
                ffsize+=0.15
                txtParam[1]-=0.15
                OPfont=pygame.font.Font("one piece font.ttf",int(ffsize*size[0]/192))
            elif txt.get_width()<int(20*size[0]/192):#if txt is within acceptable range, font size remains the same
                screen.blit(txt, txtPos)
            else:#if font size is too large, size is subtracted
                ffsize-=0.15
                txtParam[1]+=0.15
                OPfont=pygame.font.Font("one piece font.ttf",int(ffsize*size[0]/192))
            if curscounter // 50 % 2 == 1:#if curscounter is remainder 2==1, a rectangle is drawn for cursor animation
                cursor_pos = (txtPos[0]+txt.get_width()+2,txtPos[1]+3)
                pygame.draw.rect(screen, (150,0,0), (cursor_pos[0],cursor_pos[1],2,txt.get_height()))
            if request_exit:#if the request has been exited, saving becomes False, the file is saved and saveFile becomes nothing again
                if curscounter // 50 % 2 == 0:
                    saving = False
                    pygame.image.save(s,"Saves/"+saveFile+".png")
                    request_exit = False
                    saveFile = ''
    if openMenu and not bookflip and not scroll:#if openMenu and no animation is being used
        if newitem:#if new item, all saves are loaded
            local_saves = {}
            for image in os.listdir(path_way+"\Saves"):#loop through all images and get files into local saves along with the image.load
                save_path = "Saves\\" + image
                if image[-3:]=="png":
                    local_saves[image[:-4]] = pygame.image.load(save_path)
            filenames=list(local_saves.keys())#make a list of all the filenames
            #Pages---------------------------------------------------------------------------------------
            if len(filenames)>0:
                font("Page "+str(bookpage),"Stencil",int(2*size[0]/192),[int(20*size[0]/192),int(86*size[1]/95)],(0,0,0))#makes the font for page with the number
                Tool=filenames[bookpage-1]#makes Tool == the file
                screen.blit(pygame.transform.scale(local_saves[filenames[bookpage-1]],(int(25*size[0]/192),int(18*size[1]/95))),(int(11*size[0]/192),int(50*size[1]/95)))#blit the demo version of the file
                saveRectang=screen.blit(ImgDict["PicBord"],(int(7*size[0]/192),int(30*size[1]/95)))#blit the border of pic
                if bookpage<len(filenames):#if there are more than one page, a next button pops up
                    NextButtonRect=screen.blit(ImgDict["Next"],(int(27*size[0]/192),int(85.4*size[1]/95)))
                if bookpage>1:#if there is more than 1 page a previous button pops up if you are not on the first page
                    PreviousButtonRect=screen.blit(ImgDict["Previous"],(int(16*size[0]/192),int(85.4*size[1]/95)))
                newitem=False#new item is false so nothing get re blit
        if len(filenames)>0:#if filename has a file that is saved
            if bookpage<len(filenames) and not newitem:#if bookpage is not the last page
                if NextButtonRect.collidepoint((mx,my)) and clicked:#if the next button is clicked , the page changes and animation occurs
                    flippicnum=0
                    newitem=True
                    bookflip=True
                    bookpage+=1
            if bookpage>1 and not newitem:#if the previous button is clicked, the page changes, and animation occurs
                if PreviousButtonRect.collidepoint((mx,my)) and clicked:
                    flippicnum=0
                    newitem=True
                    bookflip=True
                    bookpage-=1
            if saveRectang.collidepoint((mx,my)) and clicked:#if the user clicks the picture the image is loaded
                
                undolis=[undolis[0]]
                undolis.append(local_saves[filenames[bookpage-1]])
                redolis=[]
                screen.blit(pygame.transform.smoothscale(undolis[-1],(int(113*size[0]/192),int(71*size[1]/95))),(int(63*size[0]/192),int(19*size[1]/95)))

                    
    #Colour Choosing---------------------------------------------------------------------------------------

    
    
    if ((int(38*size[0]/192)-int(42*size[0]/192))**2)**0.5<((mx-int(42*size[0]/192))**2+(my-int(7*size[1]/95))**2)**0.5<((int(36*size[0]/192)-int(42*size[0]/192))**2)**0.5 and mb[0]==1:#if the usser clicks on to the color wheel
        checkcolour=screen.get_at((mx,my))#the colour is checked so it is not black, otherwise they clicked on their own circle
        if checkcolour!=(0,0,0,255):#otherwise, the color changes
            shadinglevel=[int(67*size[0]/192),size[0]]
            pos=[[mx,my],[mx,my],size]
            colour=checkcolour
            colorchange()
            
        

    #Shading------------------------------------------------------------------------------------------
    
    if pygame.Rect(shadinglevel[0],int(4*size[1]/95),int(1*size[0]/192),int(7*size[1]/95)).collidepoint(mx,my):#if user is hovering over shade rect
        gaugecolour=(0,255,255)#gaugecolour changes
        shadingchange()
        if mb[0]==1:
            draggingshading=True#if they click,drag shading is true
    else:
        gaugecolour=(0,255,0)#otherwise shading color is reset
        shadingchange()#shading color is called
    if draggingshading and int(52*size[0]/192)<mx<int(82*size[0]/192) and mb[0]==1:
        shadinglevel[0]=mx#if the user is changing the dragging shading, the level  of shading is changed
        shadingchange()
    else:
        if draggingshading:#if they are dragging
            shaderatio=((shadinglevel[0]-int(67*size[0]/192))/(15*size[0]/192)+1)/2#lightness ratio
            L=shaderatio
            h,s,l,a=pygame.Color(colour[0],colour[1],colour[2]).hsla#color is converted to hsla
            s=s/100
            #calculations to add change lightness----
            C=(1-abs(2*L-1))*s
            X=C*(1-abs((h/60)%2-1))
            m=L-C/2
            if 0<=h<=60:
                R1,G1,B1=[C,X,0]
            if 60<=h<=120:
                R1,G1,B1=[X,C,0]
            if 120<=h<=180:
                R1,G1,B1=[0,C,X]
            if 180<=h<=240:
                R1,G1,B1=[0,X,C]
            if 240<=h<=300:
                R1,G1,B1=[X,0,C]
            if 300<=h<=360:
                R1,G1,B1=[C,0,X]
            #-------
            colour=(int((R1+m)*255),int((G1+m)*255),int((B1+m)*255))#newcolor is made
        draggingshading=False#otherwise dragging is false
    
    shadingchange()#shading becomes false
    #Thickness----------------------------------------------------------------------------------------------
    if pygame.Rect(thicknesslevel[0],int(4*size[1]/95),int(1*size[0]/192),int(7*size[1]/95)).collidepoint(mx,my):#if thickness slider is hovered
        thicknesscolour=(255,0,255)#color of slider changes
        if mb[0]==1:
            draggingthick=True#if clicked draggingthick becomes true
        thicknesschange()
        
    else:
        if thicknesscolour==(255,0,255):
            thicknesscolour=(255,255,0)#otherwise color is chanegd
            thicknesschange()
    if draggingthick and int(97*size[0]/192)<mx<int(127*size[0]/192) and mb[0]==1:#if dragging thick, level changes
        thicknesslevel[0]=mx
        thicknesschange()
    else:
        draggingthick=False
    #Effects--------------------------------------------------------------------------------------------------------------------------------
    if not scroll:
        if mode =="Effects":#if mode==Effects, if ite new item, the effect buttons are blit
            if newitem and not bookflip:
                effectRects=modeMenu(effectTool)
            for effect in range(len(effectRects)):#loops thorugh rects and checks if something is clicked
                if effectRects[effect].collidepoint((mx,my)) and clicked:
                    if Tool!=effectRects[effect//3][effect%3]:#otherwise tool becomes the clicked item and animation occures
                        Tool=effectTool[effect//3][effect%3]
                        toolbckg=origtoolbckg[:]
                        toolbckg[effect]="inkstamp"
                        modeMenu(effectTool)
    #Shapes--------------------------------------------------------------------------------------------------------------------------------
        if mode == "Shapes" and not bookflip:#if shapes 
            if newitem:
                screen.blit(GifDict["frameflip_{0:02}.gif"][6],(int(-35*size[0]/192),int(25*size[1]/95)))
                styleRects=[]#style rects are made for filled and unfilled shapes
                for xbutton in range(2):
                    styleRects.append(screen.blit(pygame.transform.smoothscale(ImgDict[stylebckg[xbutton]],(int(20*size[0]/192),int(15*size[1]/95))),(int((5+17*(xbutton))*size[0]/192),int(32*size[1]/95))))
                    screen.blit(ImgDict[styleTools[xbutton]],(int((10.25+17*(xbutton))*size[0]/192),int(36.5*size[1]/95)))
                shapeRects=[]#makes the shapes items like the effects
                for xbutton in range(2):
                    for ybutton in range(3):
                        shapeRects.append(screen.blit(pygame.transform.smoothscale(ImgDict[toolbckg[xbutton*3+ybutton]],(int(10*size[0]/192),int(10*size[1]/95))),(int((10+17*(xbutton))*size[0]/192),int((38+11*(ybutton+1))*size[1]/95))))
                        screen.blit(ImgDict[lisofshapes[0][xbutton][ybutton]],(int((13.12+17*(xbutton))*size[0]/192),int((40.5+11*(ybutton+1))*size[1]/95)))
                newitem=False
            
            for n in range(len(styleRects)):#Loops through rects just like previously and checks the style and sets it to the clicked item
                if styleRects[n].collidepoint((mx,my)) and clicked:
                    stylebckg=["inkicon","inkicon"]
                    stylebckg[n]="inkstamp"
                    Style=styleTools[n][:-4]+" "
                    newitem=True
            for n in range(len(shapeRects)):#loops through rects just like with effectss and blits everything
                if shapeRects[n].collidepoint((mx,my)) and clicked:
                    toolbckg=origtoolbckg[:]
                    toolbckg[n]="inkstamp"
                    Tool=lisofshapes[bookpage-1][n//3][n%3]
                    if Tool=="Polygon":
                        circleRect=None
                    newitem=True
                
                    
        
    #Stamps---------------------------------------------------------------------------------------------------------------------------
        
            
        if mode=="Stamps" and not bookflip:#if mode is stamps
            if newitem:#if new item 
                screen.blit(ImgDict["Wanted"],[int(6*size[0]/192),int(34*size[1]/95)])#blite the wanted poster
                font("Page "+str(bookpage),"Stencil",int(2*size[0]/192),[int(20*size[0]/192),int(86*size[1]/95)],(0,0,0))#page font is made
                Tool=stampTool[bookpage-1][:-5]#Tool selected equals the current stamp
                screen.blit(ImgDict[stampTool[bookpage-1]],[int(stampX[bookpage-1]*size[0]/192),int(48*size[1]/95)])#blit the stmp tool
                #Next, Previous is made--------------------------------------------------------
                if bookpage<9:
                    NextButtonRect=screen.blit(ImgDict["Next"],(int(27*size[0]/192),int(85.4*size[1]/95)))
                if bookpage>1:
                    PreviousButtonRect=screen.blit(ImgDict["Previous"],(int(16*size[0]/192),int(85.4*size[1]/95)))
                newitem=False
                #---------------------------------------------------------------------
            #Book Page is made just like with saves----------------------------------------------------------------------------------------
            if bookpage<9 and not newitem:
                if NextButtonRect.collidepoint((mx,my)) and clicked:
                    flippicnum=0
                    newitem=True
                    bookflip=True
                    bookpage+=1
            if bookpage>1 and not newitem:
                if PreviousButtonRect.collidepoint((mx,my)) and clicked:
                    flippicnum=0
                    newitem=True
                    bookflip=True
                    bookpage-=1
        
            
            
    #Tools-----------------------------------------------------------------------------------------------------------------------------
        
        if mode=="Tools":#If mode==Tools
            if newitem and not bookflip:#newitem adn not bookflip
                toolrects=modeMenu(tools)#ToolRects are made
                newitem=False
                    
            for tool in range(len(toolrects)):#loops through tools to check if clicked
                if toolrects[tool].collidepoint((mx,my)) and clicked:
                    if Tool!=tools[tool//3][tool%3]:
                        Tool=tools[tool//3][tool%3]#Tool gets set
                        toolbckg=origtoolbckg[:]
                        toolbckg[tool]="inkstamp"
                        modeMenu(tools)
                    
##    #Changing modes/------------------------------------------------------------------------------------------------------------------------------
##        #Tools, Stamps, etc.80,70
        #Current Tool and Font------------------------------------------------------------------------------------
        if not scroll and mode!="" and not bookflip:
            backgroundfont=GifDict["frameflip_{0:02}.gif"][6].subsurface((int(37*size[0]/192),int(57*size[1]/95),int(40*size[0]/192),int(3*size[1]/95)))#makes background for font
            #checks if fontsize goes off page and resizes accordingly-------------------
            if len(Tool)+len(Style)>13:
                fontsize=1.75
            elif len(Tool)+len(size)>11:
                fontsize=2
            else:
                fontsize=2.25
            #---------------------------------------------------------
                
            if not saving:
                screen.blit(backgroundfont,((int(2*size[0]/192),int(82*size[1]/95))))#blit the background for clean state
                font("Current "+mode[:-1]+" : "+Style+Tool,"Stencil",int(fontsize*size[0]/192),[int(6*size[0]/192),int(82*size[1]/95)],(0,0,0))#font of Current Tool
            
            if pygame.Rect(int(63*size[0]/192)+thickness//2,int(19*size[1]/95)+thickness//2,int(113*size[0]/192)-thickness,int(71*size[1]/95)-thickness).collidepoint(mx,my):#if the user is on the screen
                if Tool!="...":#If they are using a tool
                    if mb[0]==1 and not Status:#Makes sure user is clicking and status is not already true
                        if mode=="Shapes":
                            UsersItemsToDraw.append([Style+Tool,colour,thickness/size[0],True,screen.copy(),"Shapes"])#if shapes is the mode it adds the parameter to UsersItemsToDraw
                            Status=True#Clicking becomes truth
                        elif Tool+"Stamp" in stampTool:#If the tool is in stamp tools it appends following parameters
                            UsersItemsToDraw.append(["Stamp",Style+Tool+"Stamp",colour,thickness/size[0],True,screen.copy()])
                            Status=True#Status also becomes true
                        else:
                            Status=True#Otherwise Status becomes true
                            if len(UsersItemsToDraw)>0:
                                if (Tool=="Select" and UsersItemsToDraw[-1][0]!="Select"):#if Tool == Select and it wasnt select before it appends standard parameters                              
                                    UsersItemsToDraw.append([Style+Tool,colour,thickness/size[0],True,screen.copy()])
                                elif Tool!="Select":#If tool is anything else, the following parameters are appended
                                    UsersItemsToDraw.append([Style+Tool,colour,thickness/size[0],True,screen.copy()])
                            else:
                                 UsersItemsToDraw.append([Style+Tool,colour,thickness/size[0],True,screen.copy()])

                            
                    elif mb[0]==1 and Status:
                       if Tool!="Spray":# if Tool != Spray, list append the point
                            UsersItemsToDraw[-1].append([mx/size[0],my/size[1]])
                       else:#If tool== Spray, does spray function
                            for i in range(10):#looop thorugh 10 times
                                x=random.randint(mx-int(size[0]*UsersItemsToDraw[-1][2]),mx+int(size[0]*UsersItemsToDraw[-1][2]))#gets random x and y coord between thickness range
                                y=random.randint(my-int(size[0]*UsersItemsToDraw[-1][2]),my+int(size[0]*UsersItemsToDraw[-1][2]))
                                coord=[x,y]#uses coord to draw point 
                                if math.hypot(mx-x,my-y)<size[0]*UsersItemsToDraw[-1][2]:
                                    while [coord[0]/size[0],coord[1]/size[1]] in UsersItemsToDraw[-1] and coord[1]<(int(31*size[1]/95)+int(57*size[1]/95)):
                                        coord[1]+=1
                                    coord=[coord[0]/size[0],coord[1]/size[1]]
                                    UsersItemsToDraw[-1].append(coord)
                    else:#if status and tool is not special cases undolis appedns a screen.copy() before status becomes False
                        if Status and Tool!="Select" and Tool!="Text" and Tool!="Polygon":
                            undolis.append(screen.copy().subsurface(int(63*size[0]/192),int(19*size[1]/95),int(113*size[0]/192),int(71*size[1]/95)))
                            redolis=[]
                        Status=False#Status set to false because user stops clicking
                        #Previous Statuses become False----------------------------------
                        if len(UsersItemsToDraw)>0 and UsersItemsToDraw[-1][0]=="Stamp":
                            UsersItemsToDraw[-1][4]=False
                        elif len(UsersItemsToDraw)>0:
                            UsersItemsToDraw[-1][3]=False

                    
            else:#if status and tool is not special cases undolis appedns a screen.copy() before status becomes False
                if Status and Tool!="Select" and Tool!="Text" and Tool!="Polygon":
                    undolis.append(screen.copy().subsurface(int(63*size[0]/192),int(19*size[1]/95),int(113*size[0]/192),int(71*size[1]/95)))
                    redolis=[]
                Status=False#Status set to false because user stops clicking
                #Previous Statuses become False----------------------------------
                if len(UsersItemsToDraw)>0 and UsersItemsToDraw[-1][0]=="Stamp":
                            UsersItemsToDraw[-1][4]=False
                elif len(UsersItemsToDraw)>0:
                    UsersItemsToDraw[-1][3]=False
 
    #Selecting-----------------------------------------------------------------------------------------------

    noneclicked=True#variable that checks if nothing has been clicked
    nonehovered=True# " " has been hovered
    for rect in range(len(buttonrects)):
        clickQuick=True#click is set to True
        if buttonrects[rect].collidepoint((mx,my)) and clicked:
            modesmenu=origmodesmenu[:]#modesmenu becomes original modes meny
            modesmenu[rect]="coinflip_{0:02}_delay-0.1s.png"#if clicked the item of flipping becomes clicked item
            modehover.remove(rect)#modehover appends the rect number to the end so that is shows up last
            modehover.append(rect)
            flipcoincount=0#frame for animation becomes 0 to start at beginning
            noneclicked=False#user hovered over item so nonehovered becomes False
            
        elif buttonrects[rect].collidepoint((mx,my)):#
            clickQuick=False#if user did not click, clickQuick becomes false
            hovermode=True#if user hovered over item
            nonehovered=False#user hovered over item so nonehovered becomes False
            modehover.remove(rect)#modehover appends the rect number to the end so that is shows up last
            modehover.append(rect)
            modeschange()
        else:
            if noneclicked:
                clickQuick=False#if user did not click, clickQuick becomes false
            if nonehovered:
                if hovermode:
                    hovermode=False#if user hovered over nothing
                    modeschange()
            
        if clickQuick:#if an item was clicked
            modeschange()#mode is changed
            flippicnum=0#animatiion frame becomes 0
            newitem=True#newitem since something new will occur
            bookflip=True#animation for bookflipping will occur
            bookpage=1#bookpage number will start at 1
            Tool="..."#Tool becomes new as new mode
            if mode=="Shapes":#if mode is switching from shapes, style becomes nothing
                Style=""
            toolbckg=origtoolbckg[:]#toolbxkg reverts to original
            stylebckg=["inkicon","inkicon"]#stylebckg reverts to original
            shapethick=0
            openMenu=False#since user cannot be opening or saving the following three variables become false
            saveMenu=False
            saving=False
    if (openRect.collidepoint((mx,my)) and clicked) or openSC:#if user clicks open or uses the shortcut
            openSC=False#open shortcut becomes false to stop infinite loop
            modesmenu=origmodesmenu[:]#modesmenuu reverts
            modeschange()
            flippicnum=0#flip pic frame becomes -
            newitem=True#a new item is selected
            bookflip=True#the book flip animation occurs
            #Everything is changed just like previous except OpenMenu=True because user is going to openMenu
            bookpage=1
            Tool=""
            if mode=="Shapes":
                Style=""
            toolbckg=origtoolbckg[:]
            stylebckg=["inkicon","inkicon"]
            shapethick=0
            mode="Files"
            openMenu=True
            saving=False
            saveMenu=False
    if (saveRect.collidepoint((mx,my)) and clicked) or saveSC:# if user decides to save or use short cut
            saveSC=False#shortcut set to false just like before
            #Everything is changed just like previous except saveMenu=True becayse user is going to saveMenu
            modesmenu=origmodesmenu[:]
            modeschange()
            flippicnum=0
            newitem=True
            bookflip=True
            bookpage=1
            Tool=""
            if mode=="Shapes":
                Style=""
            toolbckg=origtoolbckg[:]
            stylebckg=["inkicon","inkicon"]
            shapethick=0
            mode="Files"
            openMenu=False
            saveMenu=True
            saving=False#saving == False because when user goes to saveMenu when saving is false eveerything is blit and then it becomes tru; also user is not saving, he is just going to menu
  
    #DRAWING-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    if len(UsersItemsToDraw)>0:
        screen.set_clip(canvasRectangle)#The following code is just to draw the tools and individual shapes so a clip is set to keep blits in canvas
        if Tool=="Polygon":#if Tool as Polygon is selected
            if clicked and canvasRectangle.collidepoint(mx,my) and not polygon_start: #First point user clicks
                polygon_start = [mx,my]
                polygon_points = [polygon_start]
                
                bf_drawing_canvas = screen.copy().subsurface(canvasRectangle)#get a screen.copy to be used when finishing polygon
                polygon_start = pygame.draw.circle(screen, UsersItemsToDraw[-1][1], polygon_start, 15, 1)#draw a circle to start the polygon
                
            elif clicked and canvasRectangle.collidepoint(mx,my): #if the clicked in the canvasRectangle
                if polygon_start.collidepoint((mx,my)): #They are clicking the first point to finish the poly
                    screen.blit(bf_drawing_canvas, (int(63*size[0]/192),int(19*size[1]/95)))#reblit the screen.copy()
                    if len(polygon_points)>2: #They made more than 2 points, draw the poly
                        if UsersItemsToDraw[-1][0]=="Filled Polygon":
                            pygame.draw.polygon(screen,UsersItemsToDraw[-1][1],polygon_points,) #draw polygon based off points   
                        else:
                            pygame.draw.polygon(screen,UsersItemsToDraw[-1][1],polygon_points,int(UsersItemsToDraw[-1][2]*size[0]))
                            for points in polygon_points:
                                pygame.draw.circle(screen,UsersItemsToDraw[-1][1],points,int(UsersItemsToDraw[-1][2]*size[0])//2-1)
                        undolis.append(screen.copy().subsurface(int(63*size[0]/192),int(19*size[1]/95),int(113*size[0]/192),int(71*size[1]/95)))#append to redo list after drawing
                        redolis=[]

                    else:
                        polygon_points = [] #They didnt not select enough points, cancel the polygon
                    polygon_start = None
                    
                else: #They're connecting more points
                    pygame.draw.circle(screen, UsersItemsToDraw[-1][1], [mx,my], 15, 1)
                    polygon_points.append([mx,my])
                    
            elif not canvasRectangle.collidepoint(mx,my) and polygon_start: #They clicked out of canvas area
                screen.blit(bf_drawing_canvas, (int(63*size[0]/192),int(19*size[1]/95)))
                polygon_points = []
                polygon_start = None
                
        if "Call Out" in UsersItemsToDraw[-1][0]:#If call out is unfilled or filled
            if UsersItemsToDraw[-1][3] and len(UsersItemsToDraw[-1])>6:#if status is true and UsersItemsToDraw has a point
                screen.blit(UsersItemsToDraw[-1][4].subsurface(int(63*size[0]/192),int(19*size[1]/95),int(113*size[0]/192),int(71*size[1]/95)),(int(63*size[0]/192),int(19*size[1]/95)))#blit the canvas 
                startpos=(int(UsersItemsToDraw[-1][6][0]*size[0]),int(UsersItemsToDraw[-1][6][1]*size[1]))#firstpoint user clicks
                endpos=(int(UsersItemsToDraw[-1][-1][0]*size[0]),int(UsersItemsToDraw[-1][-1][1]*size[1]))#last point while dragging
                polygon_points=[startpos,(endpos[0],startpos[1]),(endpos[0],startpos[1]+2*(endpos[1]-startpos[1])//3),(startpos[0]+2*(endpos[0]-startpos[0])//3,endpos[1]),(startpos[0]+(endpos[0]-startpos[0])*3//4,startpos[1]+2*(endpos[1]-startpos[1])//3),(startpos[0],startpos[1]+(endpos[1]-startpos[1])*2//3)]#uses calculations to get points
                if UsersItemsToDraw[-1][0]=="Filled Call Out":#Draws theed or unfilled version
                    pygame.draw.polygon(screen,UsersItemsToDraw[-1][1],polygon_points,)
                else:
                    pygame.draw.polygon(screen,UsersItemsToDraw[-1][1],polygon_points,int(UsersItemsToDraw[-1][2]*size[0]))
                    for points in polygon_points:#loops thorough points and rounds edges
                        pygame.draw.circle(screen,UsersItemsToDraw[-1][1],points,int(UsersItemsToDraw[-1][2]*size[0])//2-1)
        if "Triangle" in UsersItemsToDraw[-1][0]:
            #Same exact code as call out  except with triangle---------------------------------------------------------------------------
            if UsersItemsToDraw[-1][3] and len(UsersItemsToDraw[-1])>6:
                screen.blit(UsersItemsToDraw[-1][4].subsurface(int(63*size[0]/192),int(19*size[1]/95),int(113*size[0]/192),int(71*size[1]/95)),(int(63*size[0]/192),int(19*size[1]/95)))
                startpos=(int(UsersItemsToDraw[-1][6][0]*size[0]),int(UsersItemsToDraw[-1][6][1]*size[1]))
                endpos=(int(UsersItemsToDraw[-1][-1][0]*size[0]),int(UsersItemsToDraw[-1][-1][1]*size[1]))
                polygon_points=[((endpos[0]+startpos[0])//2,startpos[1]),(startpos[0],endpos[1]),(endpos[0],endpos[1])]
                if UsersItemsToDraw[-1][0]=="Filled Triangle":
                    pygame.draw.polygon(screen,UsersItemsToDraw[-1][1],polygon_points,)
                else:
                    pygame.draw.polygon(screen,UsersItemsToDraw[-1][1],polygon_points,int(UsersItemsToDraw[-1][2]*size[0]))
                    for points in polygon_points:
                        pygame.draw.circle(screen,UsersItemsToDraw[-1][1],points,int(UsersItemsToDraw[-1][2]*size[0])//2-1)
                        
        if "Line" in UsersItemsToDraw[-1][0]:
            #Same exact code as Triangle except with line
            if UsersItemsToDraw[-1][3] and len(UsersItemsToDraw[-1])>6:
                screen.blit(UsersItemsToDraw[-1][4].subsurface(int(63*size[0]/192),int(19*size[1]/95),int(113*size[0]/192),int(71*size[1]/95)),(int(63*size[0]/192),int(19*size[1]/95)))
                pos1=(int(UsersItemsToDraw[-1][6][0]*size[0]),int(UsersItemsToDraw[-1][6][1]*size[1]))
                pos2=(int(UsersItemsToDraw[-1][-1][0]*size[0]),int(UsersItemsToDraw[-1][-1][1]*size[1]))
                if UsersItemsToDraw[-1][0]=="Filled Line":
                    shapeThick=int(UsersItemsToDraw[-1][2]*size[0])
                else:
                    shapeThick=1
                pygame.draw.line(screen,UsersItemsToDraw[-1][1],pos1,pos2,shapeThick)

        if "Ellipse" in UsersItemsToDraw[-1][0]:
            if UsersItemsToDraw[-1][3] and len(UsersItemsToDraw[-1])>6:
                pos1=(int(UsersItemsToDraw[-1][6][0]*size[0]),int(UsersItemsToDraw[-1][6][1]*size[1]))
                pos2=(int(UsersItemsToDraw[-1][-1][0]*size[0]),int(UsersItemsToDraw[-1][-1][1]*size[1]))
                if UsersItemsToDraw[-1][0]=="Filled Ellipse":#If tool is filled ellipse, thickness becomes 0
                    shapeThick=0
                else:
                    shapeThick=int(UsersItemsToDraw[-1][2]*size[0])#otherwise shapeThick becomes thickness
                rectParams=[pos1[0],pos1[1],pos2[0]-pos1[0],pos2[1]-pos1[1]]#rectangle parameters
                ellipseRect = pygame.Rect(pos1[0],pos1[1],pos2[0]-pos1[0],pos2[1]-pos1[1])#make the ellipse rect and normalize so nothing becomes negative when drawing ellipse
                ellipseRect.normalize()
                screen.blit(UsersItemsToDraw[-1][4].subsurface(int(63*size[0]/192),int(19*size[1]/95),int(113*size[0]/192),int(71*size[1]/95)),(int(63*size[0]/192),int(19*size[1]/95)))
                if 2*shapeThick < min(abs(rectParams[2]),abs(rectParams[3])):#check if ellipse width is greater than radius
                    pass
                else:
                    shapeThick = 0#otherwise draw filled ellipse
                if shapeThick > 0:#if thickness greater than 0 than alpha surface needs to be made
                    x1,y1,width,height = ellipseRect#get parameters of the ellips
                    alpha = pygame.Surface((width,height))#make surface that is transparent
                    alpha.set_alpha(255)#set layer to transparent
                    alpha.set_colorkey((1,1,1))#set a (1,1,1) to transparent
                    alpha.fill((1,1,1))#fill the surface with that color
                    pygame.draw.ellipse(alpha, UsersItemsToDraw[-1][1], (0,0,width,height))#draw filled ellipse
                    pygame.draw.ellipse(alpha, (1,1,1),(shapeThick,shapeThick,width-shapeThick-shapeThick,height-shapeThick-shapeThick),0)#draw transparent ellipse onto
                    screen.blit(alpha, (x1,y1))#blit the surface on screen
                else:
                    pygame.draw.ellipse(screen, UsersItemsToDraw[-1][1], ellipseRect,0)#draw filled ellipse
        
        elif UsersItemsToDraw[-1][0]=="Stamp":#Draws all stamps
            if UsersItemsToDraw[-1][4] and len(UsersItemsToDraw[-1])>6:#if the user is clicking down and at least one point is in the list
                piclen=int(size[0]*UsersItemsToDraw[-1][3])*4#the length of the picture in relation to thickness scalee
                pos1=[int(UsersItemsToDraw[-1][-1][0]*size[0]),int(UsersItemsToDraw[-1][-1][1]*size[1])]
                newpic=pygame.transform.smoothscale(ImgDict[UsersItemsToDraw[-1][1]],[int(ImgDict[UsersItemsToDraw[-1][1]].get_width()*piclen/ImgDict[UsersItemsToDraw[-1][1]].get_height()),piclen])#scales image to piclen
                cPic=UsersItemsToDraw[-1][5]
                rSurf=cPic.subsurface(int(63*size[0]/192),int(19*size[1]/95),int(113*size[0]/192),int(71*size[1]/95))#subsurfaces screen.copy to make bckg to put stamp on
                screen.blit(rSurf,(int(63*size[0]/192),int(19*size[1]/95)))
                screen.blit(newpic,[pos1[0]-newpic.get_width()//2,pos1[1]-newpic.get_height()//2])#blits stamp at center of mouse by changing position of blit
                    
        elif UsersItemsToDraw[-1][0]=="Pencil" and UsersItemsToDraw[-1][3]==True and len(UsersItemsToDraw[-1])>6:#if Tool is pencil and Dragging and at least two points are in the list
            pos1=(int(UsersItemsToDraw[-1][-2][0]*size[0]),int(UsersItemsToDraw[-1][-2][1]*size[1]))#startpos of where user started clicking
            pos2=(int(UsersItemsToDraw[-1][-1][0]*size[0]),int(UsersItemsToDraw[-1][-1][1]*size[1]))#where user is currently clicking
            dx=pos2[0]-pos1[0]
            dy=pos2[1]-pos1[1]
            dist=max(abs(dx),abs(dy))
            for i in range(dist):#loops through the maximum of the differences between x and y and gets the pixel at each point inbetween the two points
                x=int(pos1[0]+i/dist*dx)
                y=int(pos1[1]+i/dist*dy)
                pygame.draw.circle(screen,UsersItemsToDraw[-1][1],(x,y),int(size[0]*UsersItemsToDraw[-1][2]//2))#draws the circle at the new point
            
        elif UsersItemsToDraw[-1][0]=="Eraser" and UsersItemsToDraw[-1][3]==True and len(UsersItemsToDraw[-1])>6:#Exact same code as pencil except when drawing circle the colour is colour of canvas
            pos1=(int(UsersItemsToDraw[-1][-2][0]*size[0]),int(UsersItemsToDraw[-1][-2][1]*size[1]))
            pos2=(int(UsersItemsToDraw[-1][-1][0]*size[0]),int(UsersItemsToDraw[-1][-1][1]*size[1]))
            dx=pos2[0]-pos1[0]
            dy=pos2[1]-pos1[1]
            dist=max(abs(dx),abs(dy))
            for i in range(dist):
                x=int(pos1[0]+i/dist*dx)
                y=int(pos1[1]+i/dist*dy)
                pygame.draw.circle(screen,(115,68,27),(x,y),int(size[0]*UsersItemsToDraw[-1][2]//2))
            
        elif UsersItemsToDraw[-1][0]=="Spray" and UsersItemsToDraw[-1][3]==True and len(UsersItemsToDraw[-1])>6:#if Tool is Spray and dragging and users has some point in the list
            for n in range(6,len(UsersItemsToDraw[-1])-1):#Spray loops through all points and makes more points faster to make faster spray
                pygame.draw.circle(screen,UsersItemsToDraw[-1][1],(int(UsersItemsToDraw[-1][n][0]*size[0]),int(UsersItemsToDraw[-1][n][1]*size[1])),0)
                
        elif UsersItemsToDraw[-1][0]=="Eye Dropper" and UsersItemsToDraw[-1][3]==True and len(UsersItemsToDraw[-1])>6:#Checks is Tool is Eye Dropper and dragging and at least one point is in is
            shadinglevel=[int(67*size[0]/192),size[0]]#shadinglevel bar gets set to middle
            colour=screen.get_at((int(UsersItemsToDraw[-1][-1][0]*size[0]),int(UsersItemsToDraw[-1][-1][1]*size[1])))#gets colour at where user selects
            colorchange()
        
                                                                
        elif UsersItemsToDraw[-1][0]=="Crop" and len(UsersItemsToDraw[-1])>6:#if user is cropping and the list has at least one point
            if effectSurf and UsersItemsToDraw[-1][3]:#if click
                croppedpic=effectSurf#Takes effect Surf and crops it to the area of cropped pic, both values are gotten from select tool
                croppedpic=pygame.transform.smoothscale(croppedpic,(int(113*size[0]/192),int(71*size[1]/95)))
                screen.blit(croppedpic,(int(63*size[0]/192),int(19*size[1]/95)))
            else:#otherwise effectsur is set to none
                effectSurf=None
                
        elif UsersItemsToDraw[-1][0]=="Move" and len(UsersItemsToDraw[-1])>6:#is user is moving and the list has at least one point
            if UsersItemsToDraw[-1][3] and effectSurf:#if it is clicking and effectSurf has something
                pos1=(int(UsersItemsToDraw[-1][5][0]*size[0]),int(UsersItemsToDraw[-1][5][1]*size[1]))#pos1 is the first position when user started clicking
                pos2=(int(UsersItemsToDraw[-1][-1][0]*size[0]),int(UsersItemsToDraw[-1][-1][1]*size[1]))#current position that users is clicking
                changex=pos2[0]-pos1[0]
                changey=pos2[1]-pos1[1]
                screen.blit(rectsurf,(int(63*size[0]/192),int(19*size[1]/95)))#reblits background
                pygame.draw.rect(screen,(115,68,27),croprect,)#draws brown rectangle in the rectangle area  that is being moved so it disappears from old screen
                newsurface.set_colorkey((115,68,27))#sets transparency to the bckg colour
                screen.blit(newsurface,(startpos[0]+changex,startpos[1]+changey))#draws subsurfaced rectangle area at change in mouse position
            else:
                startpos[0]+=changex#sets startpos and endpos
                startpos[1]+=changey
                effectSurf=None#effectNone = 0 to make user reselect
        elif UsersItemsToDraw[-1][0]=="Rotate" and len(UsersItemsToDraw[-1])>6:#if user is rotating with at least one point in the list
            if UsersItemsToDraw[-1][3] and effectSurf:#if he is clicking and the ffectsurf has been selected
                centerx=startpos[0]+(endpos[0]-startpos[0])/2#calculate center of rectangle to rotate around that position
                centery=startpos[1]+(endpos[1]-startpos[1])/2
                pos1=(int(UsersItemsToDraw[-1][5][0]*size[0]),int(UsersItemsToDraw[-1][5][1]*size[1]))#startposition when user starts clicking
                pos2=(int(UsersItemsToDraw[-1][-1][0]*size[0]),int(UsersItemsToDraw[-1][-1][1]*size[1]))#where user is currently clicking
                rotateRect=[startpos[0],startpos[1],endpos[0]-startpos[0],endpos[1]-startpos[1]]#rectangle object for user mouse
                dx = pos2[0]-centerx#difference in the position to center for finding degrees in between
                dy = pos2[1]-centery
                degs = math.degrees(math.atan2(dx,dy))-90#finds degree change from center and positive x-axis
                tempCopy = UsersItemsToDraw[-2][4]
                rsurf = tempCopy.subsurface(pygame.Rect(rotateRect))#screen.blit the copy of image
                rsurf.set_colorkey((115,68,27))#set transparency to background 
                rsurf = pygame.transform.rotate(rsurf,degs)#rotate image
          
                screen.blit(tempCopy.subsurface(int(63*size[0]/192),int(19*size[1]/95),int(113*size[0]/192),int(71*size[1]/95)),(int(63*size[0]/192),int(19*size[1]/95)))#blit old canvas 
                
                pygame.draw.rect(screen,(115,68,27),(startpos[0],startpos[1],endpos[0]-startpos[0],endpos[1]-startpos[1]),0)#blit space left underneath rotation
                
                screen.blit(rsurf,(centerx-rsurf.get_width()//2,centery-rsurf.get_height()//2))#blit rotated surface
                    
            else:
                effectSurf=None
        elif UsersItemsToDraw[-1][0]=="Flip Horizontal" and len(UsersItemsToDraw[-1])>5:#If user has something in list not checking for point but instead status
            if UsersItemsToDraw[-1][3] and effectSurf:#if clicked and effect surf
                screen.blit(pygame.transform.flip(effectSurf,True,False),startpos)#flip Horizontal
            else:
                effectSurf=None
        #same exact code for flip vertical except boolean parameters swicthced--------
        elif UsersItemsToDraw[-1][0]=="Flip Vertical" and len(UsersItemsToDraw[-1])>5:
            if UsersItemsToDraw[-1][3] and effectSurf:
                screen.blit(pygame.transform.flip(effectSurf,False,True),startpos)
            else:
                effectSurf=None

        elif UsersItemsToDraw[-1][0]=="Fill" and len(UsersItemsToDraw[-1])>6:#if user is filling with at least one point in list
            pos1=[int(UsersItemsToDraw[-1][-1][0]*size[0]),int(UsersItemsToDraw[-1][-1][1]*size[1])]#take last point
            flist=[(pos1)]#list of points covered in flood fill
            fillcolour=screen.map_rgb(UsersItemsToDraw[-1][1])#Variable for color selected
            pxArray=pygame.PixelArray(screen)#makes pixel array with colours of pixels

            if screen.get_at((pos1[0],pos1[1]))==UsersItemsToDraw[-1][1]:#if user clicked a space with the same color value nothing happens
                flist=[]
            else:#otherwise the original colour = that pxArray at that position
                originalCol=pxArray[pos1[0],pos1[1]]#original colour
            while len(flist)!=0:#flist is looped through and all point with original color that are touching the original point are changed to selected color---
                testx,testy=flist.pop()
                if canvasRectangle.collidepoint(testx,testy) and pxArray[testx,testy]==originalCol:
                    flist.append((testx+1,testy))
                    flist.append((testx-1,testy))
                    flist.append((testx,testy+1))
                    flist.append((testx,testy-1))
                    pxArray[testx,testy]=fillcolour
            pxArray=0#pxArray is set to 0 to stop screen lock error
            
        elif UsersItemsToDraw[-1][0]=="Unfilled Rectangle" and len(UsersItemsToDraw[-1])>6:#is User is using Unfilled Rectangle and list has at least one point
            startpos=[min(int(UsersItemsToDraw[-1][6][0]*size[0]),int(UsersItemsToDraw[-1][-1][0]*size[0])),min(int(UsersItemsToDraw[-1][6][1]*size[1]),int(UsersItemsToDraw[-1][-1][1]*size[1]))]
            endpos=[max(int(UsersItemsToDraw[-1][6][0]*size[0]),int(UsersItemsToDraw[-1][-1][0]*size[0])),max(int(UsersItemsToDraw[-1][6][1]*size[1]),int(UsersItemsToDraw[-1][-1][1]*size[1]))]
            shapeThick=int(UsersItemsToDraw[-1][2]*size[0])
            if UsersItemsToDraw[-1][3]:#if clicked, oldcanvas surface is drawn
                screen.blit(UsersItemsToDraw[-1][4].subsurface(int(63*size[0]/192),int(19*size[1]/95),int(113*size[0]/192),int(71*size[1]/95)),(int(63*size[0]/192),int(19*size[1]/95)))
                Newrect = pygame.Rect(startpos[0],startpos[1],endpos[0]-startpos[0],endpos[1]-startpos[1])#makes the new rect
                x,y,nx,ny = Newrect#x,y and new x and new y ar found---
                nx = nx+x
                ny = ny+y
                if 2*shapeThick < min(abs(nx-x),abs(ny-y)):#if the 2*Thicknessis at least smaller than the minumum abs of both differences
                    x += shapeThick//2#getinner coordinates of new rect-----
                    y += shapeThick//2
                    nx -= shapeThick//2
                    ny -= shapeThick//2
                    pygame.draw.rect(screen, UsersItemsToDraw[-1][1], (x,y,nx-x,ny-y),shapeThick)#draw the unfilled rectangle with weird border
                    if shapeThick != 0:#otherwise
                        y -= 1#get coordinates -1 to get border
                        x -= 1
                        nx -= 1
                        ny -= 1
                        pygame.draw.rect(screen, UsersItemsToDraw[-1][1], (x,y,nx-x,ny-y),shapeThick)#Four rectangle for four edges are made-for undilled -----------------------------
                        pygame.draw.rect(screen, UsersItemsToDraw[-1][1], (x-(shapeThick/2)+1,y-(shapeThick/2)+1,(shapeThick/2)+1,(shapeThick/2)+1))
                        pygame.draw.rect(screen, UsersItemsToDraw[-1][1], (nx,y-(shapeThick/2)+1,(shapeThick/2)+1,(shapeThick/2)+1))
                        pygame.draw.rect(screen, UsersItemsToDraw[-1][1], (x-(shapeThick/2)+1,ny,(shapeThick/2)+1,(shapeThick/2)+1))
                        pygame.draw.rect(screen, UsersItemsToDraw[-1][1], (nx,ny,(shapeThick/2)+1,(shapeThick/2)+1))
                else:
                    pygame.draw.rect(screen,UsersItemsToDraw[-1][1],(x,y,nx-x,ny-y),0)#draw the filled rectangle

        elif UsersItemsToDraw[-1][0]=="Text":#Same exact code for saving except with msg as message instead of saveFile----------------------------------------------
            OPfont=pygame.font.Font("one piece font.ttf",int(UsersItemsToDraw[-1][2]*size[0]))
            curscounter+=1
            if UsersItemsToDraw[-1][3] and len(UsersItemsToDraw[-1])>6:
                typing=True
                msg=""
                txtPos=[int(UsersItemsToDraw[-1][5][0]*size[0]),int(UsersItemsToDraw[-1][5][1]*size[1])]
            if typing:
                txt = OPfont.render(msg, True, UsersItemsToDraw[-1][1])
                screen.blit(UsersItemsToDraw[-1][4].subsurface(int(63*size[0]/192),int(19*size[1]/95),int(113*size[0]/192),int(71*size[1]/95)),(int(63*size[0]/192),int(19*size[1]/95)))
                screen.blit(txt, txtPos)
                if curscounter // 50 % 2 == 1:
                    cursor_pos = (txtPos[0]+txt.get_width()+2,txtPos[1]+3)
                    pygame.draw.rect(screen, (150,0,0), (cursor_pos[0],cursor_pos[1],2,txt.get_height()))
                if request_exit:
                    if curscounter // 50 % 2 == 0:
                        undolis.append(screen.copy().subsurface(int(63*size[0]/192),int(19*size[1]/95),int(113*size[0]/192),int(71*size[1]/95)))
                        redolis=[]
                        typing = False
                        request_exit = False
                        msg = ''
        #-------------------------------------------------------------------------------------------------------------------------------------------------------------
        elif UsersItemsToDraw[-1][0]=="Filled Rectangle" and len(UsersItemsToDraw[-1])>6:#Is user has a filled rectangle and has at least one point in the list
            if UsersItemsToDraw[-1][3]:#if dragging, old pi is blit and rectangle is made between startpos and endpos with 0 thickness
                screen.blit(UsersItemsToDraw[-1][4].subsurface(int(63*size[0]/192),int(19*size[1]/95),int(113*size[0]/192),int(71*size[1]/95)),(int(63*size[0]/192),int(19*size[1]/95)))
                startpos=[min(int(UsersItemsToDraw[-1][6][0]*size[0]),int(UsersItemsToDraw[-1][-1][0]*size[0])),min(int(UsersItemsToDraw[-1][6][1]*size[1]),int(UsersItemsToDraw[-1][-1][1]*size[1]))]
                endpos=[max(int(UsersItemsToDraw[-1][6][0]*size[0]),int(UsersItemsToDraw[-1][-1][0]*size[0])),max(int(UsersItemsToDraw[-1][6][1]*size[1]),int(UsersItemsToDraw[-1][-1][1]*size[1]))]
                pygame.draw.rect(screen,UsersItemsToDraw[-1][1],(startpos,[endpos[0]-startpos[0],endpos[1]-startpos[1]]),)
        #----------------------------------------------------------------------------------
        elif UsersItemsToDraw[-1][0]=="Select" and len(UsersItemsToDraw[-1])>5:#if user selecting
            
            if effectSurf==None:#if they did not select
                startpos=[min(int(UsersItemsToDraw[-1][5][0]*size[0]),int(UsersItemsToDraw[-1][-1][0]*size[0])),min(int(UsersItemsToDraw[-1][5][1]*size[1]),int(UsersItemsToDraw[-1][-1][1]*size[1]))]
                endpos=[max(int(UsersItemsToDraw[-1][5][0]*size[0]),int(UsersItemsToDraw[-1][-1][0]*size[0])),max(int(UsersItemsToDraw[-1][5][1]*size[1]),int(UsersItemsToDraw[-1][-1][1]*size[1]))]
                canvasPic=UsersItemsToDraw[-1][4]
                
                if UsersItemsToDraw[-1][3]==True:#if they clicking
                    croprect=pygame.Rect(startpos,[endpos[0]-startpos[0],endpos[1]-startpos[1]])#make rect of that thery are clicking
                    rectsurf=canvasPic.subsurface(int(63*size[0]/192),int(19*size[1]/95),int(113*size[0]/192),int(71*size[1]/95))
                    screen.blit(rectsurf,(int(63*size[0]/192),int(19*size[1]/95)))#blit subsurface of old canvas pic                
                    pygame.draw.rect(screen,0,croprect,1)#blit the rectangle that they are making
                    
                    NewSurf=True
                if UsersItemsToDraw[-1][3]==False:#if user stopped clicking
                    if NewSurf:#they made a rectangle surface
                        newsurface=canvasPic.subsurface(croprect)#subsurface that area
                        effectSurf=newsurface#set it as effectSurf
                    
        
            if mb[2]==1 and effectSurf!=None:#if they rightclick with something in effectSurf
                try:#try to blit last item draw screen before selection
                    screen.blit(UsersItemsToDraw[-1][4].subsurface(int(63*size[0]/192),int(19*size[1]/95),int(113*size[0]/192),int(71*size[1]/95)),(int(63*size[0]/192),int(19*size[1]/95)))
                except:
                    pass
                effectSurf=None#effect Surf = None so user can re-select
                del UsersItemsToDraw[-1]#delete the selection that occurred 
        screen.set_clip(None)#set clip = none so I can blit outside of cavas Rect again

    pygame.display.flip()

quit()


#Thank you for using One Piece Paint, the ULTIMATE PAINT FOR ONE PIECE LOVERS !!!!!!!!!!!!!!!!!!! :)
