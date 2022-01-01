import discord,requests,random,time
import PIL
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands

client = commands.Bot(command_prefix= "wm!")
client.remove_command("help")
texts = ['It will all end soon','End is near','Reality will break soon',
'It is not possible','This is end','Generations','Why?','Somewhere!','Beyond...','Follow me!',
'Distantly..','Listen closely','The unknown','Over and over',"They don't need to!",'How could you',
'Remember these days!',"I don't like the ending.",'How it ends','What will you have','Never seen the stars!',
'All that remains','There is still good',"You won't have to",'So much hate','Who were you','The same','Analyze',
'None to give']
fonts = ['arial.ttf','times.ttf']
voidimages = ['void1.png','void2.png','void3.png','void4.png','void5.png','void6.png']
lensimages = ['lens_flare1.png','lens_flare2.png','lens_flare3.png','lens_flare4.png','lens_flare5.png','lens_flare6.png','lens_flare7.png','lens_flare8.png','lens_flare9.png']
starimages = ['stars.png','stars2.png','stars3.png']
orbimages = ['orb1.png','orb2.png','orb3.png']

complexlist = [1,2,3,4,5] #1 is void, 2 is censor box, 3 is lens flare, 4 stars, 5 is orb

def add_text(img):

    cut_off = random.choice([True,False])
    big_letters = random.choice([0,0,0,1,1,1,2]) #0 = everything small, 1 = fist letter is big, 2 = every letter is big

    h, w = img.size
    if h < 420 and w < 420:
        font = PIL.ImageFont.truetype(random.choice(fonts),random.randint(18,42))
    else:
        font = PIL.ImageFont.truetype(random.choice(fonts),random.randint(42,60))

    #image = PIL.Image.open(img)

    draw = ImageDraw.Draw(img)

    redval = int(random.choice(['0','255']))
    greenval = int(random.choice(['0','255']))
    blueval = int(random.choice(['0','255']))

    if not cut_off:
        x_coord = int(random.randint(0,int(w/3)))
        y_coord = int(random.randint(0,int(h/3)))
    else:
        x_coord = int(random.randint(-w,w))
        y_coord = int(random.randint(-h,h))

    if big_letters == 0:
        draw.text(xy=(x_coord,y_coord),text = random.choice(texts).lower(), fill=(redval,greenval,blueval), font=font)

    elif big_letters == 1:
        draw.text(xy=(x_coord,y_coord),text = random.choice(texts), fill=(redval,greenval,blueval), font=font)
    
    else:
        draw.text(xy=(x_coord,y_coord),text = random.choice(texts).upper(), fill=(redval,greenval,blueval), font=font)



    
    return img


def fix_large_image(image):
    h, w = image.size

    if h > 1500 or w > 1500:
        image = image.resize((600,int(600/h*w)))

    return image



@client.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title="All commands",colour=0xe59837)
    embed.add_field(name="`ping`",value="Returns bots latency",inline=False)
    embed.add_field(name="`help`",value="how",inline=False)
    embed.add_field(name="`compressrand`",value="Compresses the image randomly.",inline=True)
    embed.add_field(name="`compress` <compression rate>",value="<compression rate> - intiger between 1 and 100 where 1 is maximum compression, and 100 is maximum quality.\nCompresses the image", inline=False)
    embed.add_field(name="`addrandomtext`",value="Adds random text to image", inline=False)
    embed.add_field(name="`addtext` <red> <green> <blue> <size> <text>",value="<red>,<green>,<blue> - values between 0 - 255\n<size> - size of the font\n<text> - text that you want to add to image", inline=False)
    embed.add_field(name="`addvoid`",value="Adds void area", inline=False)
    embed.add_field(name="`addlensflare`",value="Adds random lens flare", inline=False)
    embed.add_field(name="`crop`",value="Crops image randomly", inline=False)
    embed.add_field(name="`addcensor`",value="Adds censor box(exactly what it says)", inline=False)
    embed.add_field(name="`squish` <axis>",value='"Squishes" the image on selected axis (x or y).\n Idea by shwenthe^2.', inline=False)
    embed.add_field(name="`baseimage`",value="Posts random base image from database", inline=False)
    embed.add_field(name="`randomtext`",value="Posts random base text from database", inline=False)
    embed.add_field(name="`addborder`",value="Adds border in random color", inline=False)
    embed.add_field(name="`simplewc` <times>",value="Creates simple edit(compression, crop and text)\n<times> - how many edits it will create", inline=False)
    embed.add_field(name="`complexwc` <times>",value="Creates more complex edit(compression, crop, one random item from this list: void, stars, lens flare,censor box and text)\n<times> - how many edits it will create", inline=False)
    await ctx.send(embed=embed)

@client.event
async def on_ready():
  print("Bot ready") #tekst wyświetli się po uruchomieniu bota   

@client.command()
async def ping(ctx):
    pingembed = discord.Embed(Title='Ping', value = f'{round(client.latency*1000)} ms', colour = 0xe59837)
    pingembed.add_field(name = 'Ping', value = f'{round(client.latency*1000)} ms')
    await ctx.send(embed=pingembed)

@client.command()
async def compressrand(ctx,imglink = None):
    if imglink == None:

        try:
            imglink = ctx.message.attachments[0].url
        except IndexError:
            await ctx.send('Please provide the image')


    try:
        r = requests.get(imglink)
    except Exception:
        await ctx.send("Invalid image link")
    imagebytes = r.content
    with open('currentimage.jpg','wb') as f:
        f.write(imagebytes)
    img = PIL.Image.open('./currentimage.jpg')
    img = img.convert('RGB')
    img.save("./compressed.jpg",quality=random.randint(15,30))
    await ctx.send("Compressed!", file = discord.File('compressed.jpg'))

@client.command()
async def compress(ctx,quality,imglink = None):
    if imglink == None:
        try:
            imglink = ctx.message.attachments[0].url
        except IndexError:
            await ctx.send('Please provide the image')


    try:
        quality = int(quality)
    except Exception:
        await ctx.send("Quality must be intiger between 1 - 100")
    if quality not in range(1,101):
        await ctx.send("Quality must be intiger between 1 - 100")
    else:
        try:
            r = requests.get(imglink)
        except Exception:
            await ctx.send("Invalid image link")
        imagebytes = r.content
        with open('currentimage.jpg','wb') as f:
            f.write(imagebytes)
        img = PIL.Image.open('./currentimage.jpg')
        img = img.convert('RGB')
        img.save("./compressed.jpg",quality=quality)
        await ctx.send("Compressed!", file = discord.File('compressed.jpg'))

@client.command()
async def addrandomtext(ctx,imglink = None):
    if imglink == None:
        try:
            imglink = ctx.message.attachments[0].url
        except IndexError:
            await ctx.send('Please provide the image')

    try:
        r = requests.get(imglink)
    except Exception:
        await ctx.send("Invalid image link")
    imagebytes = r.content
    with open('weirdcore.jpg','wb') as f:
        f.write(imagebytes)
    img = PIL.Image.open('./weirdcore.jpg')
    img = img.convert('RGB')
    img = fix_large_image(img)
    img = add_text(img)
    img.save("./weirdcore.jpg")
    await ctx.send("Random text added!", file = discord.File('weirdcore.jpg'))

@client.command()
async def addtext(ctx,r,g,b,size,text):

    try:
        imglink = ctx.message.attachments[0].url
    except IndexError:
        await ctx.send('Please provide the image')

    try:
        r = int(r)
        g = int(g)
        b = int(b)
        size = int(size)
    except Exception:
        await ctx.send("`color` and `size` must be intigers!")
    
    if size not in range(1,128):
        await ctx.send("`size` must be intiger in range 1 - 128")
    else:
        
        try:
            res = requests.get(imglink)
        except Exception:
            await ctx.send("Invalid image link")
        imagebytes = res.content
        with open('weirdcore.jpg','wb') as f:
            f.write(imagebytes)
        img = PIL.Image.open('./weirdcore.jpg')

        img = fix_large_image(img)


        h, w = img.size

        x1 = random.randint(0,int(w/3))
        x2 = random.randint(int(h-h/3),h)
        y1 = random.randint(0,int(h/3))
        y2 = random.randint(int(w-w/3),w)

        font = PIL.ImageFont.truetype('arial.ttf',int(size))
        draw = ImageDraw.Draw(img)

        x_coord = int(random.randint(x1,x2))
        y_coord = int(random.randint(y1,y2))
        if r < 256 and g < 256 and b < 256 and r >= 0 and g >= 0 and b >= 0:
            draw.text(xy=(x_coord,y_coord),text = text, fill=(r,g,b), font=font)
            img = img.convert('RGB')
            img.save("./weirdcore.jpg")
            await ctx.send("Text added!", file = discord.File('weirdcore.jpg'))
        else:
            await ctx.send("Invalid color value!")

@client.command(aliases=['addvoid','void','voidadd'])
async def _void(ctx,imglink = None):
    if imglink == None:
        try:
            imglink = ctx.message.attachments[0].url
        except IndexError:
            await ctx.send('Please provide the image')


    try:
        r = requests.get(imglink)
    except Exception:
        await ctx.send("Invalid image link")
    imagebytes = r.content
    with open('currentimage.png','wb') as f:
        f.write(imagebytes)
    img = PIL.Image.open('./currentimage.png')
    img = fix_large_image(img)


    h, w = img.size
    void = random.choice(voidimages)
    voidimage = PIL.Image.open(f'./{void}')
    img.paste(voidimage,(random.randint(0,int(w/3)),random.randint(0,int(h/3))),voidimage)
    img = img.convert('RGBA')
    img.save("./weirdcore.png")
    await ctx.send("Void added!", file = discord.File('weirdcore.png'))

@client.command()
async def addlensflare(ctx,imglink = None):
    if imglink == None:
        try:
            imglink = ctx.message.attachments[0].url
        except IndexError:
            await ctx.send('Please provide the image')

    try:
        r = requests.get(imglink)
    except Exception:
        await ctx.send("Invalid image link")
    imagebytes = r.content
    with open('currentimage.png','wb') as f:
        f.write(imagebytes)
    img = PIL.Image.open('./currentimage.png').convert("RGBA")
    img = fix_large_image(img)



    h, w = img.size
    lens = random.choice(lensimages)
    lensimage = PIL.Image.open(f'./{lens}').convert("RGBA")
    img.paste(lensimage,(random.randint(0,int(w/6)),random.randint(0,int(h/6))),lensimage)
    img.save("./weirdcore.png")
    await ctx.send("Lens flare added!", file = discord.File('weirdcore.png'))

@client.command()
async def crop(ctx,imglink = None):
    if imglink == None:
        try:
            imglink = ctx.message.attachments[0].url
        except IndexError:
            await ctx.send('Please provide the image')

    try:
        r = requests.get(imglink)
    except Exception:
        await ctx.send("Invalid image link")
    imagebytes = r.content
    with open('currentimage.jpg','wb') as f:
        f.write(imagebytes)
    
    img = PIL.Image.open('./currentimage.jpg')
    img = fix_large_image(img)

    h, w = img.size
    #ratio = w/h
    x1 = random.randint(0,int(w/3))
    x2 = random.randint(int(h-h/3),h)
    y1 = random.randint(0,int(h/3))
    y2 = random.randint(int(w-w/3),w)
    img = img.crop((x1,y1,x2,y2))

    img = img.convert('RGB')
    img.save("./weirdcore.jpg")
    await ctx.send("Cropped!", file = discord.File('weirdcore.jpg'))

@client.command(aliases=['addcensorbox','addcensor','censor'])
async def _addcensor(ctx,imglink = None):
    if imglink == None:
        try:
            imglink = ctx.message.attachments[0].url
        except IndexError:
            await ctx.send('Please provide the image')

    try:
        r = requests.get(imglink)
    except Exception:
        await ctx.send("Invalid image link")
    imagebytes = r.content
    with open('weirdcore.jpg','wb') as f:
        f.write(imagebytes)
    img = PIL.Image.open('./weirdcore.jpg')
    img = fix_large_image(img)

    draw = ImageDraw.Draw(img)
    h, w = img.size
    x1 = random.randint(0,int(w/3))
    y1 = random.randint(0,int(h/3))
    x2 = random.randint(x1+150, x1+600)
    y2 = random.randint(y1+150, y1+600)
    draw.rectangle((x1,y1,x2,y2), fill=(0,0,0),width = 12)
    img = img.convert('RGB')

    img.save("./weirdcore.jpg")
    await ctx.send("Censor box added!", file = discord.File('weirdcore.jpg'))

@client.command(aliases=['simpleweirdcore','simplewc','simple'])
async def _simplewc(ctx,times = 1, imglink = None):
    if imglink == None:
        try:
            imglink = ctx.message.attachments[0].url
        except IndexError:
            await ctx.send('Please provide the image')

    try:
        times = int(times)
    except Exception:
        await ctx.send("Please input a number smaller than or equal 6")

    if times > 6:
        await ctx.send("Please input a number smaller than or equal 6")
    else:
        for i in range(0,times):
            try:
                try:
                    r = requests.get(imglink)
                except Exception:
                    await ctx.send("Invalid image link")
                imagebytes = r.content
                with open('weirdcore.jpg','wb') as f:
                    f.write(imagebytes)
                img = PIL.Image.open('./weirdcore.jpg')
                img = fix_large_image(img)

                h, w = img.size

                x1 = random.randint(0,int(w/3))
                x2 = random.randint(int(h-h/3),h)
                y1 = random.randint(0,int(h/3))
                y2 = random.randint(int(w-w/3),w)
                img = img.crop((x1,y1,x2,y2))

                img = add_text(img)

                img = img.convert('RGB')
                img.save("./compressed.jpg",quality=random.randint(15,30))
                await ctx.send("Finished edit!", file = discord.File('compressed.jpg'))
            except Exception:
                await ctx.send("An error occured! Please try again.")

@client.command(aliases=['complexweirdcore','complexwc','complex'])
async def _complexwc(ctx,times = 1, imglink = None):
    if imglink == None:
        try:
            imglink = ctx.message.attachments[0].url
        except IndexError:
            await ctx.send('Please provide the image')

    try:
        times = int(times)
    except Exception:
        await ctx.send("Please input a number smaller than or equal 6")

    if times > 6:
        await ctx.send("Please input a number smaller than or equal 6")
    else:
        for i in range(0,times):
            try:
                try:
                    r = requests.get(imglink)
                except Exception:
                    await ctx.send("Invalid image link")
                imagebytes = r.content
                with open('weirdcore.jpg','wb') as f:
                    f.write(imagebytes)
                img = PIL.Image.open('./weirdcore.jpg')

                img = fix_large_image(img)

                h, w = img.size
                withborder = random.choice([True,False])

                x1 = random.randint(0,int(w/3))
                x2 = random.randint(int(h-h/3),h)
                y1 = random.randint(0,int(h/3))
                y2 = random.randint(int(w-w/3),w)
                img = img.crop((x1,y1,x2,y2))


                addition = random.choice(complexlist)
                if addition == 1: #void
                    h, w = img.size
                    void = random.choice(voidimages)
                    voidimage = PIL.Image.open(f'./{void}')
                    img.paste(voidimage,(random.randint(0,int(w/3)),random.randint(0,int(h/3))),voidimage)
                elif addition == 2: #censor box
                    draw = ImageDraw.Draw(img)
                    h, w = img.size
                    x1 = random.randint(0,h)
                    y1 = random.randint(0,w)
                    x2 = random.randint(x1-150, x1+150)
                    y2 = random.randint(y1-150, y1+150)
                    draw.rectangle((x1,y1,x2,y2), fill=(0,0,0),width = 12)
                elif addition == 3: #lens flare
                    h, w = img.size
                    lens = random.choice(lensimages)
                    lensimage = PIL.Image.open(f'./{lens}').convert("RGBA")
                    img.paste(lensimage,(random.randint(0,int(w/6)),random.randint(0,int(h/6))),lensimage)
                elif addition == 5: #orb
                    h, w = img.size
                    orb = random.choice(orbimages)
                    orbimage = PIL.Image.open(f'./{orb}').convert("RGBA")
                    img.paste(orbimage,(random.randint(0,int(w/6)),random.randint(0,int(h/6))),orbimage)
                else: #stars
                    h, w = img.size
                    star = random.choice(starimages)
                    starimage = PIL.Image.open(f'./{star}').convert("RGBA")
                    img.paste(starimage,(random.randint(0,int(w/6)),random.randint(0,int(h/6))),starimage)


                if withborder:
                    r = int(random.choice(['0','128','255']))
                    g = int(random.choice(['0','128','255']))
                    b = int(random.choice(['0','128','255']))

                    draw = ImageDraw.Draw(img)
                    draw.rectangle((0,0,h,w),width=random.randint(9,30),outline=(r, g, b))


                img = add_text(img)
                img = img.convert('RGB')
                img.save("./compressed.jpg",quality=random.randint(15,30))
                await ctx.send("Finished edit!", file = discord.File('compressed.jpg'))
            except Exception:
                await ctx.send("An error occured! Please try again.")

@client.command()
async def squish(ctx,axis,imglink = None):
    if imglink == None:
        try:
            imglink = ctx.message.attachments[0].url
        except IndexError:
            await ctx.send('Please provide the image')
    try:
        r = requests.get(imglink)
    except Exception:
        await ctx.send("Invalid image link")
    imagebytes = r.content
    with open('currentimage.jpg','wb') as f:
        f.write(imagebytes)
    img = PIL.Image.open('./currentimage.jpg')
    img = img.convert('RGB')
    h, w = img.size
    if axis == 'x' or axis == 'X':
        img = img.resize((h,random.randint(w-int(w/1.8),w+int(w/1.8))))
        img.save("./weirdcore.jpg")
        await ctx.send("Squished on x axis", file = discord.File('weirdcore.jpg'))

    elif axis == 'y' or axis == 'Y':
        img = img.resize((random.randint(h-int(h/1.8),h+int(h/1.8)),w))
        img.save("./weirdcore.jpg")
        await ctx.send("Squished on y axis", file = discord.File('weirdcore.jpg'))
    else:
        await ctx.send('Please enter X or Y in `axis` field')

@client.command(aliases=['baseimage','baseimages','base','baseimg'])
async def _base(ctx):
    await ctx.send("Random base image: ", file=discord.File(f'./baseimages/{str(random.randint(1,15))}.jpg'))

@client.command(aliases=["addborder",'frame','addframe'])
async def _border(ctx,imglink = None):
    if imglink == None:


        try:
            imglink = ctx.message.attachments[0].url
        except IndexError:
            await ctx.send('Please provide the image')

    try:
        r = requests.get(imglink)
    except Exception:
        await ctx.send("Invalid image link")
    imagebytes = r.content
    with open('currentimage.jpg','wb') as f:
        f.write(imagebytes)
    img = PIL.Image.open('./currentimage.jpg')
    img = img.convert('RGB')

    h, w = img.size

    red = int(random.choice(['0','128','255']))
    g = int(random.choice(['0','128','255']))
    b = int(random.choice(['0','128','255']))

    draw = ImageDraw.Draw(img)
    draw.rectangle((0,0,h,w),width=random.randint(9,30),outline=(red, g, b))

    img = img.convert('RGB')
    img.save("./weirdcore.jpg")
    await ctx.send("Frame added!", file = discord.File('weirdcore.jpg'))

@client.command(aliases = ['randomtext','text'])
async def _text(ctx):
    await ctx.send(f'Random text: `{random.choice(texts)}`')



@client.command(aliases=['addorb','orb','orbadd'])
async def _orb(ctx,imglink = None):
    if imglink == None:
        try:
            imglink = ctx.message.attachments[0].url
        except IndexError:
            await ctx.send('Please provide the image')


    try:
        r = requests.get(imglink)
    except Exception:
        await ctx.send("Invalid image link")
    imagebytes = r.content
    with open('currentimage.png','wb') as f:
        f.write(imagebytes)
    img = PIL.Image.open('./currentimage.png')
    img = fix_large_image(img)


    h, w = img.size
    orb = random.choice(orbimages)
    orbimage = PIL.Image.open(f'./{orb}')
    img.paste(orbimage,(random.randint(0,int(w/3)),random.randint(0,int(h/3))),orbimage)
    img = img.convert('RGBA')
    img.save("./weirdcore.png")
    await ctx.send("Orb added!", file = discord.File('weirdcore.png'))

client.load_extension('extension')
  
client.run('token goes here')