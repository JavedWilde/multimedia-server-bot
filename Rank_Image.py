import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import textwrap

# Global variables, Image sizes and coordinates
pfp_coord = (362,301)
pfp_size = (895, 895)
serverimg_coord = (979,340)
serverimg_size = (756, 756)

name_text_coord = (17,550)
name_text_size = 90
name_char_limit = 14
name_char_subtraction_multiple = 5 # pixel size to reduce for each extra character in the name

id_text_coord = (17,640)
id_text_size = 40

lvl_text_coord = (800,545)
lvl_text_size = 50

rank_text_coord = (989,276)
rank_text_size = 120

role_text_coord = (985,117)
role_text_size = 50
role_text_char_limit = 12

xp_text_coord = (1180,640)
xp_text_size = 20



def center_coord(img, coord):
    final_coordx = int(coord[0] - (img[0]/2))
    final_coordy = int(coord[1] - (img[0]/2))
    return (final_coordx,final_coordy)

def font_size(text, char_limit, default_size, sub_mul = 5):
    if len(text) <= char_limit:
        return default_size
    else:
        count = len(text) - char_limit
        return default_size - (count * sub_mul)

def convert_xp(xp):
    next_xp = (int(xp ** (1/4)) + 1) ** 4
    if xp > 999:
        temp_string = str(xp/1000)
        temp_string_split = temp_string.split('.')
        xp_string = f'{temp_string_split[0]}.{temp_string_split[1][0]}K'
    else:
        xp_string = str(xp)
    
    if next_xp > 999:
        temp_string = str(next_xp/1000)
        temp_string_split = temp_string.split('.')
        nxt_xp_string = f'{temp_string_split[0]}.{temp_string_split[1][0]}K'
    
    else:
        nxt_xp_string = str(next_xp)
    
    return f'{xp_string} / {nxt_xp_string} XP'

def para_text(text, fnt_path, fnt_size, chr_limit, color=(255,255,255,255)):
    x = text.split()
    if len(x) > 1 and len(text) > chr_limit:
        lines = textwrap.wrap(text, width=chr_limit)

        # if paragraph is more than 2 decrease size by a factor of 25 for each extra line
        if len(lines) > 2:
            size = fnt_size - ((len(lines) - 2) * 5)
        else:
            size = fnt_size
        # find the line with most number of characters and create an image using its pixel size
        largest_line = ''
        img_size_y = 0
        font = ImageFont.truetype(fnt_path, size)
        for z in lines:
            if len(z) > len(largest_line):
                largest_line= z
            img_size_y = img_size_y + font.getsize(z)[1]
        img_size_y = img_size_y + 10 # bruteforce

        txt_img = Image.new(size=(font.getsize(largest_line)[0],img_size_y), mode='RGBA')
        offset = 0
        for y in lines:
            ImageDraw.Draw(txt_img).text(((txt_img.size[0]-font.getsize(y)[0])/2,offset), y, color, font=font)
            offset = offset + font.getsize(largest_line)[1]

    else:
        font = ImageFont.truetype(fnt_path, font_size(text, chr_limit, fnt_size))
        txt_img = Image.new(size=font.getsize(text), mode='RGBA')
        ImageDraw.Draw(txt_img).text((0,0), text, color, font=font)

    return txt_img

def pass_1(pfp, server, mask, overlay):

    # resize and place everything and convert them into numpy array
    mask_arr = np.array(mask)

    pfp_img = Image.new(size=mask.size, mode='RGB')
    pfp_img.paste(pfp.resize(pfp_size), center_coord(pfp_size, pfp_coord))
    pfp_arr = np.array(pfp_img)

    server_img = Image.new(size=mask.size, mode='RGB')
    server_img.paste(server.resize(serverimg_size), center_coord(serverimg_size, serverimg_coord))
    server_img.convert('L')
    server_arr = np.array(server_img)

    # final image array container
    final_arr = []

    # do the actual check (pil image goes from top to bottom)
    for x in range(len(mask_arr - 1)):
        column = []
        for y in range(len(mask_arr[0]) - 1):
            if mask_arr[x,y,0] >= 200:
                column.append(pfp_arr[x,y])
            else:
                column.append(server_arr[x,y])

        final_arr.append(column)

    final_img = Image.fromarray(np.array(final_arr), mode='RGB')
    final_img.paste(overlay, (0,0), overlay)
    return final_img

def add_bar(xp):
    nudge_img = Image.open('./Images/nudge.png')
    bar_img = Image.new(size=(352,34),color=(84,187,255), mode='RGB')
    curr_lvl_xp = int(xp ** (1/4)) ** 4
    next_lvl_xp = (int(xp ** (1/4)) + 1) ** 4
    bar_width = 352 * ((xp - curr_lvl_xp)/(next_lvl_xp - curr_lvl_xp))
    if bar_width < 1:
        bar_width = 1
    bar_img = bar_img.resize((int(bar_width),34))
    bar_with_nudge = Image.new(size=(int(bar_width) + nudge_img.size[0], 34), mode='RGBA')
    bar_with_nudge.paste(bar_img,(0,0))
    bar_with_nudge.paste(nudge_img,(int(bar_width) - 1,0), nudge_img)
    return bar_with_nudge

def generate_rank_img(pfp, server, userid, rank, role, xp):    
    final_pass = pass_1(Image.open(pfp),
                        Image.open(server),
                        Image.open(r'./Images/mask.jpg'),
                        Image.open(r'./Images/overlay.png'))
    name = userid[:-5]
    id = userid[-5:]

    # Left Align Texts
    font = ImageFont.truetype('./Fonts/Teko-SemiBold.ttf', font_size(name, name_char_limit, name_text_size, name_char_subtraction_multiple))
    ImageDraw.Draw(final_pass).text(name_text_coord, name, (255,255,255), font=font)

    font = ImageFont.truetype('./Fonts/verdana.ttf', id_text_size)
    ImageDraw.Draw(final_pass).text(id_text_coord, id, (150,150,150), font=font)

    font = ImageFont.truetype('./Fonts/Teko-SemiBold.ttf', lvl_text_size)
    ImageDraw.Draw(final_pass).text(lvl_text_coord, f'Level {int(xp ** (1/4))}', (207,191,212), font=font)

    # Center Align Texts
    font = ImageFont.truetype('./Fonts/Poppins-Regular.ttf', rank_text_size)
    ImageDraw.Draw(final_pass).text((center_coord(font.getsize(str(rank)), rank_text_coord)[0], rank_text_coord[1]),
                                     str(rank), (207,191,212),
                                     font=font)
    
    # Everything below is very much Hard Coded
    role_img = para_text(role, './Fonts/verdana.ttf', role_text_size, role_text_char_limit, (207,191,212,175))
    if role_img.size[1] > 100: # moves the text up depending upon the para image size, 100 is the para image y size limit, beyond that it'll move
        offsety = role_img.size[1] - 100
    else:
        offsety = 0
    final_pass.paste(role_img, (center_coord(role_img.size, role_text_coord)[0], role_text_coord[1] - offsety), role_img)
    bar = add_bar(xp)
    final_pass.paste(bar, (813,601), bar)

    # xp text
    xp_txt=convert_xp(xp)
    font = ImageFont.truetype('./Fonts/verdana.ttf', xp_text_size)
    ImageDraw.Draw(final_pass).text((xp_text_coord[0]-font.getsize(xp_txt)[0], xp_text_coord[1]), xp_txt, (150,150,150), font=font)

    final_pass.save('./Images/rank.png')


