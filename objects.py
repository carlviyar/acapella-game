import pygame
import helper_fxns

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