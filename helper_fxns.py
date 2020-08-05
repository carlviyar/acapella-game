import pygame
# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return y

def draw_songs(surface, song_list, font):
    # set up display of title
    title_font = pygame.font.SysFont('Arial', 50)
    title_x = 350 - title_font.size('Songs')[0]/2
    title_y = 100 + title_font.size('Songs')[1]/2
    songs_title = title_font.render('Songs', True, (255, 255, 255))

    # create consonants and positional 'pointers'
    print_song_list = song_list
    song_count = 0
    MAX_WIDTH = 275
    y_pos = 175
    x_pos = 175
    bg_song_box_rect = (150, 100, 400, 500)
    song_box_rect = (175, 175, 350, 400)
    # print background and foreground song box
    pygame.draw.rect(surface, (0, 102, 204), bg_song_box_rect)
    pygame.draw.rect(surface, (0, 0, 0), song_box_rect)

    # print each song in song list
    for song in print_song_list:
        song_print = song.title
        # determine song width
        song_length = font.size(song.title)[0]
        if song_length > MAX_WIDTH:
            # get last index by starting from end and going back until encounter space
            # need to make room for ellipse, which is 6 pixels (per period) * 3.
            last_pixel = MAX_WIDTH - (3 * (font.size('.')[0]))
            last_index = len(song.title) - 1
            while font.size(song.title[:last_index])[0] >= last_pixel:
                last_index -= 1
            song_print = song.title[:last_index] + '...'
        song_text = font.render(song_print, True, (255, 255, 255))
        surface.blit(song_text, (x_pos, y_pos))
        # x_pos end is 525 - font.size
        skill_point_print = font.render(str(song.skill)+'/10', True, (255, 255, 255))
        surface.blit(skill_point_print, (520 - font.size(str(song.skill)+'/10')[0], y_pos))
        y_pos += 25
        song_count += 1
        if song_count == 16:
            break
    surface.blit(songs_title, (title_x, title_y))

def draw_skills(surface, skills):
    POINTS_X_POS = 950
    font = pygame.font.SysFont('Arial', 50)
    skills_title = font.render('Skills', True, (255, 255, 255))
    title_x = 850 - font.size('Skills')[0]/2
    title_y = 100 + font.size('Skills')[1]/2
    y_pos = 200
    x_pos = 675
    bg_skill_box_rect = (650, 100, 400, 500)
    skill_box_rect = (675, 175, 350, 400)
    pygame.draw.rect(surface, (0, 102, 204), bg_skill_box_rect)
    pygame.draw.rect(surface, (0, 0, 0), skill_box_rect)
    for skill in skills:
        skill_text = font.render(skill.name, True, (255, 255, 255))
        skill_points = font.render(str(skill.points) + '/10', True, (255, 255, 255))
        surface.blit(skill_text, (x_pos, y_pos))
        surface.blit(skill_points, (POINTS_X_POS, y_pos))
        y_pos += 75
    surface.blit(skills_title, (title_x, title_y))


    # display box coords:
    # X: 650 to 950
    # Y: 650 to 775

def draw_textbox(surface, input_box_rect, text, font):
    # draw input box
    pygame.draw.rect(surface, (0, 102, 204), input_box_rect)
    # text display rect
    text_display_rect_dimensions = (650+5+5+font.size('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 
                                    650+5, 300-5, 125-5)
    drawText(surface, text, (255, 255, 255), text_display_rect_dimensions, font)

def draw_rehearsal_header(surface, week, acquired_skill_points):
    title_font = pygame.font.SysFont('Arial', 80)
    text_font = pygame.font.SysFont('Arial', 50)
    title_surface = title_font.render(f'REHEARSAL: WEEK {week}', True, (0, 0, 0))
    surface.blit(title_surface, (10, (100-title_font.size('ABCDEFGHIJKLMNOPQRSTUVWYZ')[1])/2))
    text_surface = text_font.render(f'Skill Points: {acquired_skill_points}', True, (0, 0, 0))
    surface.blit(text_surface, (1200-450, (100-text_font.size('ABCDEFGHIJKLMNOPQRSTUVWYZ')[1])/2))
