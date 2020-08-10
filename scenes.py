import objects
import helper_fxns
import pygame

class Scene(object):
    def __init__(self):
        pass

    def render(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, game_events):
        raise NotImplementedError

class Rehearsal(Scene):
    def __init__(self, screen, week, songs, skills, acquired_skill_points):
        super(Rehearsal, self).__init__()
        self.text_font = pygame.font.SysFont('Arial', 30)
        self.prompt = 'Write your command here: [Song or Skill name], [# of points]'
        self.input_textbox = objects.InputTextBox(self.text_font, (250, 650, 700, 125), '', self.prompt)
        self.dirty_rects = []
        self.week = week
        self.songs = songs
        self.skills = skills
        self.acquired_skill_points = acquired_skill_points
        self.screen = screen

    def render(self):
        # Display rehearsal screen with skills and song boxes
        self.screen.fill((255, 255, 255))
        helper_fxns.draw_rehearsal_header(self.screen, self.week, self.acquired_skill_points)
        helper_fxns.draw_songs(self.screen, self.songs, self.text_font)
        helper_fxns.draw_skills(self.screen, self.skills)
        # Draw textboxes and the text in them
        self.input_textbox.draw_input_box(self.screen, (0, 0, 0), (255, 255, 255))
        self.input_textbox.draw_prompt(self.screen, (0, 0, 0), (255, 255, 255))


    def update(self):
        pass

    def handle_events(self, game_events, active=True):
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
                        # If a quit command, move to next screen
                        if self.input_textbox.text in ['Q', 'q', 'quit', 'Quit']:
                            pass
                        # If the input wasn't valid, then raise error textbox
                        error_message = self.parse_input(self.input_textbox.text)
                        if error_message is not None:
                            error_box = objects.Textbox(self.text_font, (400, 300, 400, 200), text=error_message)
                            error_box.draw_textbox(self.screen, (0, 0, 0), (255, 255, 255))
                            pygame.display.update((400, 300, 400, 200))
                            helper_fxns.wait()
                        self.input_textbox.text = ''
                    elif rhsl_event.key == pygame.K_BACKSPACE:
                        self.input_textbox.text = self.input_textbox.text[:-1]
                    else:
                        self.input_textbox.text += rhsl_event.unicode

    def parse_input(self, input_text):
        str_lst = input_text.split(', ')
        if len(str_lst) != 2:
            return "Error: you inputted an incorrect number of arguments. Please list a valid song, skill name, and points to use. Press any key to continue."
        song_or_skill = str_lst[0]
        if str_lst[1].isnumeric():
            points = int(str_lst[1])
            if points > self.acquired_skill_points:
                # TOO MANY POINTS
                return "Error: you inputted a number of points too large. Please input an integer number less than or equal to your current skill points for the third argument. Press any key to continue."
        else:
            # INVALID POINTS ARG: return error message
            return "Error: you inputted an invalid number of points. Please input an integer number less than or equal to your current skill points for the third argument. Press any key to continue."

        # check validity of command args
        for song_rep in self.songs:
            if song_rep.title == song_or_skill:
                song_rep.add_skill_point(points)
                break
        else:
            for skill_rep in self.skills:
                if skill_rep.name == song_or_skill:
                    skill_rep.add_skill_point(points)
                    break
            else:
            # INVALID SKILL ARG
                return "Error: you inputted an invalid song or skill name. Please input a skill name listed under skills. Press any key to continue."
        
        self.acquired_skill_points -= points