import os, json, asyncio, subprocess, textwrap, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import edge_tts
from google import genai
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

OUT=Path("output"); OUT.mkdir(exist_ok=True)
W,H=1280,720
def font(n,b=False):
    p=Path("/usr/share/fonts/truetype/dejavu")/("DejaVuSans-Bold.ttf" if b else "DejaVuSans.ttf")
    return ImageFont.truetype(str(p),n) if p.exists() else ImageFont.load_default()

def character(d,x,y,s=1):
    d.rounded_rectangle((x-35*s,y+75*s,x-8*s,y+155*s),radius=8,fill="#d8c19a")
    d.rounded_rectangle((x+8*s,y+75*s,x+35*s,y+155*s),radius=8,fill="#d8c19a")
    d.rounded_rectangle((x-47*s,y+145*s,x-3*s,y+164*s),radius=8,fill="white",outline="#222222",width=2)
    d.rounded_rectangle((x+3*s,y+145*s,x+47*s,y+164*s),radius=8,fill="white",outline="#222222",width=2)
    d.rounded_rectangle((x-48*s,y-5*s,x+48*s,y+95*s),radius=18,fill="#171717")
    d.rectangle((x-42*s,y+68*s,x+42*s,y+79*s),fill="#79502e")
    d.rectangle((x-5*s,y+68*s,x+5*s,y+79*s),fill="#d7b36a")
    d.line((x-43*s,y+15*s,x-72*s,y+68*s),fill="#d8a47d",width=13)
    d.line((x+43*s,y+15*s,x+72*s,y+68*s),fill="#d8a47d",width=13)
    d.ellipse((x-36*s,y-75*s,x+36*s,y-3*s),fill="#d8a47d")
    d.arc((x-37*s,y-80*s,x+37*s,y-5*s),180,360,fill="#24201e",width=15)
    d.ellipse((x-18*s,y-42*s,x-10*s,y-34*s),fill="#24201e")
    d.ellipse((x+10*s,y-42*s,x+18*s,y-34*s),fill="#24201e")
    d.arc((x-13*s,y-32*s,x+13*s,y-12*s),5,170,fill="#713d32",width=3)

def create_episode():
    client=genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    prompt="""Create a completely original English personal-finance story for a general US audience, 1,200-1,350 spoken words (about 9-10 minutes). Use a strong hook, relatable examples, a clear story arc and practical takeaways. Do not imitate any creator, reuse scripts, promise returns or give personalized advice. Plan EXACTLY 45 scenes for a lively 2D cartoon/whiteboard explainer, not a slideshow. Each scene narration should be about 24-32 words and include narration, setting, action, visual and screen_text. The recurring original host is a young adult man wearing a black shirt, beige trousers, brown belt and white sneakers. Keep him consistent but vary gestures, emotions, backgrounds and props. Return valid JSON with title, description, tags and scenes. Title under 95 characters; description includes an educational-not-financial-advice disclaimer."""
    raw=client.models.generate_content(model=os.getenv("GEMINI_MODEL","gemini-2.5-flash"),contents=prompt).text.strip()
    raw=raw[raw.find("{"):raw.rfind("}")+1]
    data=json.loads(raw)
    if len(data.get("scenes",[])) != 45: raise ValueError("Episode must contain exactly 45 scenes; run again.")
    return data

def make_scene(s,i,total,title):
    im=Image.new("RGB",(W,H),"#f4efe5"); d=ImageDraw.Draw(im)
    palettes=[("#e8f0fa","#c7d9ed"),("#f5eadc","#e8d3b8"),("#e5f1e8","#c7dfce"),("#f0e9f7","#d9c9e8")]
    top,floor=palettes[i%len(palettes)]
    d.rectangle((0,0,W,590),fill=top); d.rectangle((0,590,W,H),fill=floor)
    d.rectangle((0,0,W,92),fill="#151a2d")
    d.text((42,25),"MONEY MADE SIMPLE",font=font(27,True),fill="white")
    d.text((W-155,30),f"{i+1:02d}/{total:02d}",font=font(22,True),fill="#a9c5ff")
    setting=s.get("setting","").lower()
    if any(k in setting for k in ["home","apartment","living","kitchen"]):
        d.rectangle((65,145,330,390),fill="#d6e9f6",outline="#607c99",width=7)
        d.line((197,145,197,390),fill="#607c99",width=6); d.line((65,265,330,265),fill="#607c99",width=6)
        d.rectangle((55,510,470,565),fill="#9b704c")
    elif any(k in setting for k in ["office","work","classroom"]):
        d.rectangle((75,150,390,350),fill="#fffdf4",outline="#57708d",width=7)
        d.text((105,185),"PLAN",font=font(36,True),fill="#315a9a")
        d.line((110,255,345,255),fill="#86a2c5",width=8); d.line((110,300,295,300),fill="#86a2c5",width=8)
    else:
        d.ellipse((90,175,360,445),fill="#d9e8ff"); d.text((165,255),"IDEA",font=font(48,True),fill="#315a9a")
    words=(s.get("visual","")+" "+setting).lower()
    if any(k in words for k in ["bank","saving","money","cash","budget","wallet","paycheck","income"]):
        d.rounded_rectangle((500,300,660,420),radius=18,fill="#f2c85b",outline="#7d6024",width=4)
        d.text((545,310),"$",font=font(85,True),fill="#253657")
    elif any(k in words for k in ["credit","card","debt","bill","loan"]):
        d.rounded_rectangle((500,310,680,420),radius=15,fill="#304c79",outline="#17233d",width=4)
        d.rectangle((505,345,675,360),fill="#f2c85b"); d.text((535,370),"CARD",font=font(24,True),fill="white")
    elif any(k in words for k in ["invest","stock","market","growth","compound"]):
        d.line((500,420,550,365,600,385,650,320,700,280),fill="#2e9b72",width=10)
    else:
        d.ellipse((520,300,680,460),fill="#f5c95f"); d.text((570,330),"$",font=font(90,True),fill="#24365c")
    d.rounded_rectangle((45,475,700,640),radius=24,fill="white",outline="#d5dce6",width=3)
    d.text((78,495),"THE MONEY LESSON",font=font(18,True),fill="#315a9a")
    d.multiline_text((78,528),textwrap.fill(s.get("screen_text",""),34),font=font(34,True),fill="#17233d",spacing=7)
    d.rectangle((0,675,W,720),fill="#151a2d"); d.text((42,686),title[:95],font=font(17),fill="white")
    p=OUT/f"scene_{i:02d}.png"; im.save(p); return p

def make_character_animation(scene,path):
    """Render a looping, transparent frame-by-frame 2D host animation."""
    action=(scene.get("action","")+" "+scene.get("visual","")).lower()
    mode="walk" if any(k in action for k in ["walk","run","arrive","leave"]) else (
        "point" if any(k in action for k in ["point","show","explain","chart","screen"]) else (
        "celebrate" if any(k in action for k in ["celebrat","success","win","happy","excited"]) else (
        "think" if any(k in action for k in ["think","confus","wonder","question"]) else "talk")))
    frames=[]
    fw,fh=300,430
    for f in range(24):
        phase=2*math.pi*f/24
        bob=round(3*math.sin(phase*2))
        sway=round(4*math.sin(phase))
        im=Image.new("RGBA",(fw,fh),(0,0,0,0)); d=ImageDraw.Draw(im)
        cx=150+sway; hip=275+bob
        leg=math.sin(phase) if mode=="walk" else 0.22*math.sin(phase)
        left_knee=(cx-28+int(12*leg),345+int(7*abs(leg)))
        right_knee=(cx+28-int(12*leg),345-int(7*abs(leg)))
        d.line((cx-20,hip,left_knee[0],left_knee[1],cx-36-int(18*leg),398),fill="#d8c19a",width=25)
        d.line((cx+20,hip,right_knee[0],right_knee[1],cx+36+int(18*leg),398),fill="#d8c19a",width=25)
        d.rounded_rectangle((cx-62-int(18*leg),390,cx-20-int(18*leg),414),radius=9,fill="white",outline="#242424",width=3)
        d.rounded_rectangle((cx+18+int(18*leg),390,cx+62+int(18*leg),414),radius=9,fill="white",outline="#242424",width=3)
        d.rounded_rectangle((cx-55,165+bob,cx+55,290+bob),radius=23,fill="#171717")
        d.rectangle((cx-50,267+bob,cx+50,281+bob),fill="#79502e")
        d.rectangle((cx-6,267+bob,cx+6,281+bob),fill="#d7b36a")
        swing=math.sin(phase)*22
        if mode=="point":
            left_end=(cx-92,225+int(8*math.sin(phase))); right_end=(cx+112,145+int(5*math.sin(phase)))
        elif mode=="celebrate":
            left_end=(cx-100,115+int(8*math.sin(phase))); right_end=(cx+100,115-int(8*math.sin(phase)))
        elif mode=="think":
            left_end=(cx-95,245); right_end=(cx+75,145+int(8*math.sin(phase)))
        elif mode=="walk":
            left_end=(cx-75-int(swing),245+int(swing/2)); right_end=(cx+75+int(swing),245-int(swing/2))
        else:
            left_end=(cx-80-int(swing),225+int(8*math.sin(phase))); right_end=(cx+80+int(swing),225-int(8*math.sin(phase)))
        d.line((cx-48,190+bob,left_end[0],left_end[1]),fill="#d8a47d",width=19)
        d.line((cx+48,190+bob,right_end[0],right_end[1]),fill="#d8a47d",width=19)
        for ex,ey in (left_end,right_end): d.ellipse((ex-12,ey-12,ex+12,ey+12),fill="#d8a47d")
        hy=105+bob
        d.ellipse((cx-43,hy-55,cx+43,hy+35),fill="#d8a47d")
        d.pieslice((cx-45,hy-62,cx+45,hy+25),180,360,fill="#24201e")
        if f in (11,12):
            d.line((cx-25,hy-8,cx-12,hy-8),fill="#24201e",width=4); d.line((cx+12,hy-8,cx+25,hy-8),fill="#24201e",width=4)
        else:
            d.ellipse((cx-25,hy-13,cx-15,hy-2),fill="#24201e"); d.ellipse((cx+15,hy-13,cx+25,hy-2),fill="#24201e")
        if mode=="think": d.arc((cx-10,hy+4,cx+18,hy+22),190,330,fill="#713d32",width=3)
        elif f%4 in (0,1): d.ellipse((cx-8,hy+9,cx+8,hy+24),fill="#713d32")
        else: d.arc((cx-12,hy+5,cx+12,hy+22),5,170,fill="#713d32",width=3)
        frames.append(im)
    frames[0].save(path,save_all=True,append_images=frames[1:],duration=83,loop=0,disposal=2)
    return path

def make_money_prop_animation(scene,path):
    """Looping animated finance prop: bouncing coin, rising bars or rocking card."""
    words=(scene.get("visual","")+" "+scene.get("action","")).lower()
    kind="chart" if any(k in words for k in ["invest","stock","market","growth","compound","chart"]) else ("card" if any(k in words for k in ["credit","card","debt","bill","loan"]) else "coin")
    frames=[]
    for f in range(24):
        phase=2*math.pi*f/24
        im=Image.new("RGBA",(220,220),(0,0,0,0)); d=ImageDraw.Draw(im)
        if kind=="chart":
            d.line((22,184,198,184),fill="#30435f",width=5)
            for j,x in enumerate((42,82,122,162)):
                height=45+int((j+1)*25*(0.75+0.25*math.sin(phase-j*.35)))
                d.rounded_rectangle((x,184-height,x+23,184),radius=5,fill="#399b72")
            d.line([(20,145),(65,115),(105,126),(150,65),(196,35+int(5*math.sin(phase)))],fill="#f0b83f",width=7)
        elif kind=="card":
            angle=8*math.sin(phase)
            card=Image.new("RGBA",(170,110),(0,0,0,0)); cd=ImageDraw.Draw(card)
            cd.rounded_rectangle((3,3,167,107),radius=15,fill="#304c79",outline="white",width=4)
            cd.rectangle((5,35,165,52),fill="#f2c85b"); cd.text((20,68),"CARD",font=font(22,True),fill="white")
            im.alpha_composite(card.rotate(angle,resample=Image.Resampling.BICUBIC),(25,55))
        else:
            y=35+int(13*(1-math.cos(phase*2)))
            d.ellipse((25,y+12,195,y+182),fill="#dcae35",outline="#8c681b",width=7)
            d.ellipse((38,y+25,182,y+169),outline="#fff0a8",width=5)
            d.text((77,y+36),"$",font=font(105,True),fill="#24365c")
        frames.append(im)
    frames[0].save(path,save_all=True,append_images=frames[1:],duration=83,loop=0,disposal=2)
    return path

async def make_voice(txt,path):
    await edge_tts.Communicate(text=txt,voice=os.getenv("VOICE","en-US-GuyNeural")).save(str(path))

def run(cmd): subprocess.run(cmd,check=True)

def render(data):
    parts=[]
    for i,s in enumerate(data["scenes"]):
        pic=make_scene(s,i,len(data["scenes"]),data["title"])
        character_gif=OUT/f"host_{i:02d}.gif"
        prop_gif=OUT/f"prop_{i:02d}.gif"
        make_character_animation(s,character_gif)
        make_money_prop_animation(s,prop_gif)
        aud=OUT/f"voice_{i:02d}.mp3"; seg=OUT/f"segment_{i:02d}.mp4"
        asyncio.run(make_voice(s["narration"],aud))
        run(["ffmpeg","-y","-loop","1","-framerate","25","-i",str(pic),"-stream_loop","-1","-i",str(character_gif),"-stream_loop","-1","-i",str(prop_gif),"-i",str(aud),
             "-filter_complex","[0:v]zoompan=z='min(zoom+0.00025,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1280x720:fps=25[bg];[1:v]scale=300:430[host];[2:v]scale=220:220[prop];[bg][prop]overlay=560:285[tmp];[tmp][host]overlay=850:245:shortest=1,format=yuv420p[v]",
             "-map","[v]","-map","3:a","-c:v","libx264","-preset","veryfast","-c:a","aac","-shortest","-movflags","+faststart",str(seg)])
        parts.append(seg)
    listing=OUT/"concat.txt"; listing.write_text("".join(f"file '{p.resolve()}\\n" for p in parts))
    final=OUT/"finance_episode.mp4"
    run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(listing),"-c","copy","-movflags","+faststart",str(final)])
    return final

def make_thumbnail(title):
    im=Image.new("RGB",(1280,720),"#17233d"); d=ImageDraw.Draw(im)
    d.ellipse((820,110,1190,480),fill="#f5c95f"); d.text((905,195),"$",font=font(190,True),fill="#17233d")
    character(d,1000,535,1)
    d.multiline_text((70,130),textwrap.fill(title.upper(),22),font=font(66,True),fill="white",spacing=12)
    p=OUT/"thumbnail.jpg"; im.save(p,quality=92); return p

def upload(video,thumb,data):
    names=["YOUTUBE_CLIENT_ID","YOUTUBE_CLIENT_SECRET","YOUTUBE_REFRESH_TOKEN"]
    missing=[n for n in names if not os.getenv(n)]
    if missing: raise RuntimeError("Missing YouTube secrets: "+", ".join(missing))
    creds=Credentials(token=None,refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],token_uri="https://oauth2.googleapis.com/token",client_id=os.environ["YOUTUBE_CLIENT_ID"],client_secret=os.environ["YOUTUBE_CLIENT_SECRET"],scopes=["https://www.googleapis.com/auth/youtube.upload"])
    yt=build("youtube","v3",credentials=creds)
    body={"snippet":{"title":data["title"][:100],"description":(data.get("description","")+"\n\nEducational content only; not financial advice.")[:4900],"tags":data.get("tags",[])[:20],"categoryId":"27","defaultLanguage":"en"},"status":{"privacyStatus":"private","selfDeclaredMadeForKids":False}}
    result=yt.videos().insert(part="snippet,status",body=body,media_body=MediaFileUpload(str(video),chunksize=-1,resumable=True)).execute()
    try: yt.thumbnails().set(videoId=result["id"],media_body=MediaFileUpload(str(thumb))).execute()
    except Exception as e: print("Thumbnail upload skipped:",e)
    print("Uploaded video:", "https://youtube.com/watch?v="+result["id"])

def main():
    if not os.getenv("GEMINI_API_KEY"): raise RuntimeError("Add GEMINI_API_KEY in GitHub Actions secrets.")
    data=create_episode(); (OUT/"episode.json").write_text(json.dumps(data,indent=2))
    video=render(data); thumb=make_thumbnail(data["title"])
    if os.getenv("ENABLE_YOUTUBE_UPLOAD","false").lower()=="true": upload(video,thumb,data)
    else: print("Video rendered. YouTube upload is disabled until OAuth secrets are configured.")
    print("Finished:",video)

if __name__=="__main__": main()
