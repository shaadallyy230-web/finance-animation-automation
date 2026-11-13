import os, json, asyncio, subprocess, textwrap
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
    prompt="""Create an original English personal-finance explainer for a general US audience, 1,250-1,400 spoken words (about 9-10 minutes). Friendly and entertaining, not imitating any creator. Topic: choose budgeting, credit scores, compound interest, emergency funds, debt traps or beginner investing. No guaranteed returns or personalized advice. Return ONLY valid JSON: {"title":"...","description":"2 paragraphs with educational disclaimer","tags":["..."],"scenes":[{"narration":"55-75 spoken words","visual":"short visual direction","screen_text":"3-7 word caption"}]}. Make 18-22 scenes."""
    raw=client.models.generate_content(model=os.getenv("GEMINI_MODEL","gemini-2.5-flash"),contents=prompt).text.strip()
    raw=raw[raw.find("{"):raw.rfind("}")+1]
    data=json.loads(raw)
    if len(data.get("scenes",[]))<12: raise ValueError("Too few scenes generated")
    return data

def make_scene(s,i,total,title):
    im=Image.new("RGB",(W,H),"#f4efe5"); d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,105),fill="#151a2d")
    d.text((48,27),"MONEY MADE SIMPLE",font=font(30,True),fill="white")
    d.text((W-180,36),f"{i+1:02d} / {total:02d}",font=font(22,True),fill="#a9c5ff")
    d.rounded_rectangle((55,145,790,620),radius=28,fill="white",outline="#e0d9cd",width=3)
    d.text((90,180),"THE BIG IDEA",font=font(23,True),fill="#315a9a")
    d.multiline_text((90,235),textwrap.fill(s.get("screen_text",""),27),font=font(43,True),fill="#17233d",spacing=12)
    d.multiline_text((92,440),textwrap.fill(s.get("visual",""),40),font=font(20),fill="#626b78",spacing=8)
    d.ellipse((900,170,1170,440),fill="#d9e8ff"); d.ellipse((960,230,1110,380),fill="#f5c95f")
    d.text((985,273),"$",font=font(82,True),fill="#24365c")
    for j,h in enumerate([80,130,190,245]):
        xx=920+j*65; d.rounded_rectangle((xx,520-h,xx+36,520),radius=8,fill="#5488ce")
    character(d,1035,470,.75)
    d.rectangle((0,675,W,720),fill="#151a2d"); d.text((48,685),title[:90],font=font(18),fill="white")
    p=OUT/f"scene_{i:02d}.png"; im.save(p); return p

async def make_voice(txt,path):
    await edge_tts.Communicate(text=txt,voice=os.getenv("VOICE","en-US-GuyNeural")).save(str(path))

def run(cmd): subprocess.run(cmd,check=True)

def render(data):
    parts=[]
    for i,s in enumerate(data["scenes"]):
        pic=make_scene(s,i,len(data["scenes"]),data["title"])
        aud=OUT/f"voice_{i:02d}.mp3"; seg=OUT/f"segment_{i:02d}.mp4"
        asyncio.run(make_voice(s["narration"],aud))
        run(["ffmpeg","-y","-loop","1","-i",str(pic),"-i",str(aud),"-vf","scale=1280:720,format=yuv420p","-c:v","libx264","-preset","veryfast","-tune","stillimage","-c:a","aac","-shortest",str(seg)])
        parts.append(seg)
    listing=OUT/"concat.txt"; listing.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    final=OUT/"finance_episode.mp4"
    run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(listing),"-c","copy",str(final)])
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
