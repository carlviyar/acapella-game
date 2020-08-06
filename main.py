import pygame
import helper_fxns
pygame.init()

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import (
#     K_UP,
#     K_DOWN,
#     K_LEFT,
#     K_RIGHT,
#     K_ESCAPE,
#     KEYDOWN,
#     QUIT,
# )

# Define constants for the screen width and height
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 775
SCREEN_CENTER = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

# Define constants for black and white and fonts
black_color = (0, 0, 0)
white_color = (255, 255, 255)
text_font = pygame.font.SysFont('Arial', 30)

class Song():
    '''
    Class to define songs; contains title, skill points, and whether it is memorized (skill > 5)
    '''
    def __init__(self, title, skill=1):
        self.title = title
        self.skill = skill
        self.memorized = False
    def add_skill_point(self, points):
        self.skill += points
        if self.skill >= 5:
            self.memorized = True
   
class Skill():
    '''
    Class to define skills; contains name, and skill points
    '''
    def __init__(self, name):
        self.name = name
        self.points = 1
    def add_skill_point(self, points):
        self.points += points

class Textbox():

    def __init__(self, font, rect_dimensions, text=''):
        # set text box dimensions
        self.box_rect = pygame.Rect(rect_dimensions)
        # set text to be padded with margins
        self.text_rect = pygame.Rect(rect_dimensions[0]+5, rect_dimensions[1]+5, rect_dimensions[2]-10, rect_dimensions[3]-10)
        self.text = text
        self.font = font

    # Draw the text onto the surface wrapped
    def draw_textbox(self, surface, box_color, text_color, aa=False, bkg=None):
        pygame.draw.rect(surface, box_color, self.box_rect)
        rect = self.text_rect
        text_copy = self.text
        y = rect.top
        lineSpacing = -2

        # draw some text into an area of a surface
        # automatically wraps words
        # returns any text that didn't get blitted
        fontHeight = self.font.size("Tg")[1]

        while text_copy:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break

            # determine maximum width of line
            while self.font.size(text_copy[:i])[0] < rect.width and i < len(text_copy):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word      
            if i < len(text_copy): 
                i = text_copy.rfind(" ", 0, i) + 1

            # render the line and blit it to the surface
            if bkg:
                image = self.font.render(text_copy[:i], 1, text_color, bkg)
                image.set_colorkey(bkg)
            else:
                image = self.font.render(text_copy[:i], aa, text_color)

            surface.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing

            # remove the text we just blitted
            text_copy = text_copy[i:]

        return text_copy

class InputTextBox(Textbox):

    def __init__(self, font, rect_dimensions, text, prompt):
        super(InputTextBox, self).__init__(font, rect_dimensions, text)
        self.prompt = prompt
        # Create a display textbox for the prompt
        self.prompt_text_box = Textbox(font, (rect_dimensions[0], rect_dimensions[1], rect_dimensions[2], self.get_prompt_height()+10), self.prompt)
        # Create a rect for the input box that is directly below the display prompt but within the whole box dimensions
        # print(self.prompt_text_box.box_rect)
        self.input_box_rect = pygame.Rect(self.prompt_text_box.box_rect.x, self.prompt_text_box.box_rect.y+self.prompt_text_box.box_rect.height, self.prompt_text_box.box_rect.width, rect_dimensions[3]-self.prompt_text_box.box_rect.height)
        self.input_text_rect = pygame.Rect(self.input_box_rect.x+5, self.input_box_rect.y+5, self.input_box_rect.width-10, self.input_box_rect.height-10)
        # print(self.input_box_rect)
        # Current view:
        # entire input box contains Textbox prompt and Rect input_box_rect

    def get_prompt_height(self):
        # copy of prompt
        prompt_copy = self.prompt
        
        # height of text to calculate text height
        font_height = self.font.size(self.prompt)[1]
        y = 0

        while prompt_copy:
            i = 1

            # determine if the row of text will be outside our area
            if y + font_height > self.text_rect.bottom:
                break

            # determine maximum width of line
            while self.font.size(prompt_copy[:i])[0] < self.text_rect.width and i < len(prompt_copy):
                i += 1
            
            # if we've wrapped the text, then adjust the wrap to the last word     
            if i < len(prompt_copy): 
                i = prompt_copy.rfind(" ", 0, i) + 1
        
            # remove calculated text from self.text
            prompt_copy = prompt_copy[i:]

            y += font_height

        return y

    def draw_prompt(self, surface, box_color, text_color):
        self.prompt_text_box.draw_textbox(surface, box_color, text_color)
    
    def draw_input_box(self, surface, box_color, text_color):
        pygame.draw.rect(surface, box_color, self.input_box_rect)
        # note: text will always be white
        helper_fxns.drawText(surface, self.text, text_color, self.input_text_rect, self.font)

class Scene(object):
    def __init__(self):
        pass

    def render(self, surface):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, game_events):
        raise NotImplementedError

class Rehearsal(Scene):
    def __init__(self):
        super(Rehearsal, self).__init__()
        self.text_font = pygame.font.SysFont('Arial', 30)
        self.prompt = 'Write your command here: [Song], [Skill], [# of points]'
        self.input_textbox = InputTextBox(text_font, (250, 650, 700, 125), '', self.prompt)
        self.dirty_rects = []

    def render(self, surface):
        global acquired_skill_points
        # Display rehearsal screen with skills and song boxes
        screen.fill((255, 255, 255))
        helper_fxns.draw_rehearsal_header(surface, week, acquired_skill_points)
        helper_fxns.draw_songs(surface, songs, self.text_font)
        helper_fxns.draw_skills(surface, skills)
        # Draw textboxes and the text in them
        self.input_textbox.draw_input_box(surface, (0, 0, 0), (255, 255, 255))
        self.input_textbox.draw_prompt(surface, (0, 0, 0), (255, 255, 255))


    def update(self):
        pass

    def handle_events(self, game_events, active=True):
        global acquired_skill_points
        for rhsl_event in game_events:
            # check MOUSEBUTTONDOWN event
            if rhsl_event.type == pygame.MOUSEBUTTONDOWN:
                # if user clicked on input_box rect
                if self.input_textbox.input_box_rect.collidepoint(rhsl_event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
            # Check for KEYDOWN event
            elif rhsl_event.type == pygame.KEYDOWN:
                if active:
                    if rhsl_event.key == pygame.K_RETURN:
                        # if the input wasn't valid, then raise error textbox
                        error_message = self.parse_input(self.input_textbox.text)
                        if error_message is not None:
                            error_box = Textbox(text_font, (400, 300, 400, 200), text=error_message)
                            error_box.draw_textbox(screen, (0, 0, 0), (255, 255, 255))
                            pygame.display.update((400, 300, 400, 200))
                            helper_fxns.wait()
                        self.input_textbox.text = ''
                    elif rhsl_event.key == pygame.K_BACKSPACE:
                        self.input_textbox.text = self.input_textbox.text[:-1]
                    else:
                        self.input_textbox.text += rhsl_event.unicode

    def parse_input(self, input_text):
        global acquired_skill_points
        str_lst = input_text.split(', ')
        print(str_lst)
        if len(str_lst) != 3:
            return "Error: you inputted an incorrect number of arguments. Please list a valid song, skill name, and points to use. Press any key to continue."
        song = str_lst[0]
        skill = str_lst[1]
        if str_lst[2].isnumeric():
            points = int(str_lst[2])
            if points > acquired_skill_points:
                # TOO MANY POINTS
                return "Error: you inputted a number of points too large. Please input an integer number less than or equal to your current skill points for the third argument. Press any key to continue."
        else:
            # INVALID POINTS ARG: return error message
            return "Error: you inputted an invalid number of points. Please input an integer number less than or equal to your current skill points for the third argument. Press any key to continue."

        # check validity of command args
        for song_rep in songs:
            if song_rep.title == song:
                song_rep.add_skill_point(points)
                break
        else:
            # INVALID SONG ARG
            return "Error: you inputted an invalid song name. Please input a song name listed in your repertoire. Press any key to continue."
        for skill_rep in skills:
            if skill_rep.name == skill:
                skill_rep.add_skill_point(points)
                break
        else:
            # INVALID SKILL ARG
            return "Error: you inputted an invalid skill name. Please input a skill name listed under skills. Press any key to continue."
        
        acquired_skill_points -= points

    
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
week = 1

# Create skills
skills = []
skills.append(Skill("Intonation"))
skills.append(Skill("Memorization"))
skills.append(Skill("Musicality"))
skills.append(Skill("Performance"))
skills.append(Skill("Blend"))
# Keeps track of skill points acquired from gigs, weeks, etc.
acquired_skill_points = 5

# Create songs
songs = []
songs.append(Song(title='Happy Birthday'))
songs.append(Song(title='Sally in our Alley (Rat)'))
songs.append(Song(title='Bridge Over Troubled Water'))
songs.append(Song(title='Get Ready'))
songs.append(Song(title='Fly Me to the Moon'))

# Variable for loop
running = True

# For not, default state is rehearsal.
rehearsal_state = Rehearsal()

# Main loop
while running:

    # for loop through the event queue
    events = pygame.event.get()
    for event in events:

        # Check for QUIT event. If QUIT, then set running to false.
        if event.type == pygame.QUIT:
            running = False

        # Check for KEYDOWN event
        elif event.type == pygame.KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == pygame.K_ESCAPE:
                running = False

    rehearsal_state.render(screen)
    rehearsal_state.handle_events(events)
    rehearsal_state.update()
    pygame.display.flip()
    clock.tick(30)
