import os
import sys
import json
import time
import wave
import math
import struct
import asyncio
import requests
import subprocess
from playwright.async_api import async_playwright

ACCESS_TOKEN = os.environ.get(
    "IG_ACCESS_TOKEN",
    "SET_IN_GITHUB_SECRETS"
)
IG_USER_ID = os.environ.get("IG_USER_ID", "17841435829048294")
QUEUE_FILE = "queue.json"
GRAPH_URL = "https://graph.facebook.com/v21.0"

WA_WALLPAPER_SVG = """data:image/svg+xml,%3Csvg width='160' height='160' viewBox='0 0 160 160' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' stroke='%23ffffff' stroke-width='1.5' stroke-opacity='0.035'%3E%3Cpath d='M30 25c-4-4-10-4-14 0s-4 10 0 14l14 14 14-14c4-4 4-10 0-14s-10-4-14 0z'/%3E%3Ccircle cx='115' cy='35' r='12'/%3E%3Cpath d='M110 32h10M110 38h7'/%3E%3Cpath d='M25 110a15 15 0 1 0 20 15 12 12 0 0 1-20-15z'/%3E%3Crect x='95' y='100' width='28' height='20' rx='4'/%3E%3Cpath d='M95 105l14 8 14-8'/%3E%3Cpolygon points='75,65 78,73 86,73 80,78 82,86 75,81 68,86 70,78 64,73 72,73'/%3E%3C/g%3E%3C/svg%3E"""

# MOBILE SAFE-ZONE TEMPLATE:
# Full 1080x1920 dark canvas, with the phone UI safely inset inside a 900x1500 centered frame
# (90px side padding, 150px top padding, 270px bottom padding so Instagram's UI & curved corners NEVER cut anything!)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  body {{
    width: 1080px;
    height: 1920px;
    background-color: #060a0e;
    color: #e9edef;
    font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
    margin: 0;
    padding: 140px 85px 250px 85px; /* Exact Instagram Mobile Safe-Zone Padding! */
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .phone-screen {{
    width: 100%;
    height: 100%;
    background-color: #0b141a;
    background-image: url("{wallpaper_svg}");
    background-repeat: repeat;
    border-radius: 36px;
    border: 2px solid rgba(255,255,255,0.08);
    box-shadow: 0 25px 60px rgba(0,0,0,0.85);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .tail-out {{ position: relative; }}
  .tail-out::after {{
    content: ""; position: absolute; top: 0px; right: -10px;
    border-left: 12px solid #005c4b; border-bottom: 14px solid transparent;
  }}
  .tail-in {{ position: relative; }}
  .tail-in::before {{
    content: ""; position: absolute; top: 0px; left: -10px;
    border-right: 12px solid #202c33; border-bottom: 14px solid transparent;
  }}
</style>
</head>
<body class="select-none">

  <div class="phone-screen">
    <!-- 1. WhatsApp Top Header -->
    <div class="bg-[#202c33] pt-5 pb-3 px-5 z-10 shadow-sm">
      <!-- Status Bar -->
      <div class="flex justify-between items-center text-[#d1d7db] text-[20px] font-medium mb-3 px-1">
        <span>{header_time}</span>
        <div class="flex items-center space-x-2">
          <span class="text-[17px] font-semibold">VoLTE</span>
          <span class="text-[18px] font-bold">5G</span>
          <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M2 22h20V2z"/></svg>
          <span class="text-[18px]">{battery}</span>
          <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24">
            <path d="M15.67 4H14V2h-4v2H8.33C7.6 4 7 4.6 7 5.33v15.33C7 21.4 7.6 22 8.33 22h7.33c.74 0 1.34-.6 1.34-1.33V5.33C17 4.6 16.4 4 15.67 4z"/>
          </svg>
        </div>
      </div>

      <!-- Contact Row -->
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <svg class="w-7 h-7 text-[#e9edef]" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 12H5m7-7l-7 7 7 7"/>
          </svg>
          <img src="{dp_url}" class="w-12 h-12 rounded-full object-cover border border-white/10" />
          <div class="pl-1.5">
            <div class="text-[26px] font-medium text-[#e9edef] leading-tight">{contact_name}</div>
            <div class="text-[19px] {status_color} font-normal leading-tight mt-0.5">{status_text}</div>
          </div>
        </div>

        <div class="flex items-center space-x-6 text-[#e9edef] pr-1">
          <svg class="w-7 h-7" fill="none" stroke="currentColor" stroke-width="1.9" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
          </svg>
          <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.9" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
          </svg>
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
            <circle cx="12" cy="5" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="19" r="2"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- 2. Chat Messages Stream -->
    <div class="flex-1 px-5 py-3 flex flex-col justify-end overflow-hidden">
      <div class="mx-auto bg-[#182229] text-[#8696a0] px-4 py-1 rounded-lg text-[18px] font-medium mb-3 shadow-sm">
        Today
      </div>
      {bubbles_html}
    </div>

    <!-- 3. Bottom Input Bar -->
    <div class="px-3 pt-1.5 pb-2.5 flex items-center space-x-2 z-10">
      <div class="flex-1 bg-[#2a3942] rounded-full px-4 py-2.5 flex items-center justify-between text-[#8696a0]">
        <div class="flex items-center space-x-3 pl-1">
          <svg class="w-7 h-7 text-[#8696a0]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10"/><path stroke-linecap="round" d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9" stroke-width="2.5"/><line x1="15" y1="9" x2="15.01" y2="9" stroke-width="2.5"/>
          </svg>
          <span class="text-[24px] text-[#8696a0] font-normal">Message</span>
        </div>

        <div class="flex items-center space-x-5 pr-2 text-[#8696a0]">
          <svg class="w-6 h-6 -rotate-45" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"/>
          </svg>
          <div class="w-6 h-6 rounded-full border-2 border-[#8696a0] flex items-center justify-center text-[16px] font-bold leading-none">
            &#8377;
          </div>
          <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/><circle cx="12" cy="13" r="3"/>
          </svg>
        </div>
      </div>

      <div class="w-13 h-13 p-3.5 rounded-full bg-[#00a884] flex items-center justify-center text-[#111b21] shadow">
        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5-3c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
        </svg>
      </div>
    </div>

    <div class="pb-2.5 pt-0.5 flex justify-center">
      <div class="w-32 h-1 bg-zinc-500/50 rounded-full"></div>
    </div>
  </div>

</body>
</html>
"""

BLUE_TICKS_SVG = '''<svg class="w-5 h-5 text-[#53bdeb] inline-block ml-1 -mb-0.5" viewBox="0 0 16 15" fill="currentColor"><path d="M15.01 3.316l-.478-.372a.365.365 0 0 0-.51.063L8.666 9.879a.32.32 0 0 1-.484.033l-.358-.325a.319.319 0 0 0-.484.032l-.378.483a.418.418 0 0 0 .036.541l1.32 1.266c.143.14.361.125.484-.033l6.272-8.048a.366.366 0 0 0-.064-.512zm-4.1 0l-.478-.372a.365.365 0 0 0-.51.063L4.566 9.879a.32.32 0 0 1-.484.033L1.891 7.769a.366.366 0 0 0-.515.006l-.423.433a.364.364 0 0 0 .006.514l3.258 3.185c.143.14.361.125.484-.033l6.272-8.048a.365.365 0 0 0-.063-.51z"/></svg>'''

def build_bubbles(msg_list):
    html = []
    prev_sender = None
    for m in msg_list:
        first_in_group = (m["sender"] != prev_sender)
        top_margin = "mt-3" if first_in_group else "mt-1"
        prev_sender = m["sender"]

        if m["sender"] == "me":
            tail_cls = "rounded-xl rounded-tr-none tail-out" if first_in_group else "rounded-xl"
            html.append(f'''
            <div class="self-end max-w-[82%] bg-[#005c4b] text-[#e9edef] px-3.5 py-2 mr-2 {tail_cls} {top_margin} shadow-sm">
              <span class="text-[26px] leading-[1.32]">{m["text"]}</span>
              <span class="float-right text-[16px] text-[#ffffff99] ml-2.5 mt-2 flex items-center select-none">
                {m["time"]} {BLUE_TICKS_SVG}
              </span>
            </div>
            ''')
        else:
            tail_cls = "rounded-xl rounded-tl-none tail-in" if first_in_group else "rounded-xl"
            html.append(f'''
            <div class="self-start max-w-[82%] bg-[#202c33] text-[#e9edef] px-3.5 py-2 ml-2 {tail_cls} {top_margin} shadow-sm">
              <span class="text-[26px] leading-[1.32]">{m["text"]}</span>
              <span class="float-right text-[16px] text-[#8696a0] ml-2.5 mt-2 select-none">
                {m["time"]}
              </span>
            </div>
            ''')
    return "\n".join(html)

def create_audio_track(filename: str, total_duration: float, events: list, music_key: int = 0):
    sr = 48000
    total_samples = int(sr * total_duration)

    # Pitch multiplier shifts the melody across 4 pleasant keys so every video sounds fresh
    key_multipliers = [1.0, 1.122, 0.891, 1.26]
    mult = key_multipliers[music_key % len(key_multipliers)]

    base_chords = [
        [261.63, 329.63, 392.00, 493.88, 523.25, 392.00, 329.63, 261.63],
        [220.00, 261.63, 329.63, 392.00, 440.00, 392.00, 329.63, 261.63],
        [174.61, 220.00, 261.63, 329.63, 349.23, 329.63, 261.63, 220.00],
        [196.00, 246.94, 293.66, 392.00, 440.00, 392.00, 293.66, 246.94],
    ]
    note_len = 0.44

    with wave.open(filename, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)

        buf = bytearray()
        for i in range(total_samples):
            t = i / sr
            step_idx = int(t / note_len)
            note_t = t - (step_idx * note_len)
            chord = base_chords[(step_idx // 8) % len(base_chords)]
            freq = chord[step_idx % 8] * mult

            env = math.exp(-3.2 * note_t) * (1.0 - math.exp(-80.0 * note_t))
            melody = 0.14 * env * (math.sin(2 * math.pi * freq * note_t) + 0.25 * math.sin(2 * math.pi * (freq * 2) * note_t))
            pad = 0.05 * math.sin(2 * math.pi * (chord[0] * 0.5 * mult) * t)

            pop = 0.0
            for ev_time, sender in events:
                dt = t - ev_time
                if 0.0 <= dt < 0.08:
                    base_f = 600.0 if sender == "me" else 900.0
                    f_sweep = base_f + (300.0 * (dt / 0.08))
                    pop += 0.22 * math.sin(2 * math.pi * f_sweep * dt) * math.exp(-38.0 * dt)

            val = max(-0.95, min(0.95, melody + pad + pop))
            buf.extend(struct.pack("<h", int(val * 32767)))

        wf.writeframes(buf)

async def render_item(item: dict, output_mp4: str):
    clips = []
    events = []
    elapsed = 0.0
    messages = item["messages"]

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})

        for idx in range(len(messages)):
            current_msg = messages[idx]
            events.append((elapsed, current_msg["sender"]))
            hold_dur = float(current_msg["hold"])
            elapsed += hold_dur

            current_msgs = messages[:idx+1]
            is_last = (idx == len(messages) - 1)
            next_is_them = (not is_last) and (messages[idx+1]["sender"] == "them")
            status_text = "typing..." if next_is_them else "online"
            status_color = "text-[#00a884]" if next_is_them else "text-[#8696a0]"

            img_path = f"sz_step_{idx}.png"
            clip_path = f"sz_clip_{idx}.mp4"

            html_filled = HTML_TEMPLATE.format(
                wallpaper_svg=WA_WALLPAPER_SVG,
                contact_name=item["contact_name"],
                dp_url=item["dp_url"],
                battery=item["battery"],
                header_time=item["header_time"],
                status_text=status_text,
                status_color=status_color,
                bubbles_html=build_bubbles(current_msgs)
            )
            await page.set_content(html_filled, wait_until="networkidle")
            await page.wait_for_timeout(120)
            await page.screenshot(path=img_path)

            subprocess.run([
                "ffmpeg", "-y",
                "-loop", "1", "-t", str(hold_dur), "-i", img_path,
                "-vf", "scale=1080:1920,format=yuv420p",
                "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-r", "30",
                "-an", clip_path
            ], check=True)
            clips.append(clip_path)

        await browser.close()

    with open("sz_list.txt", "w", encoding="utf-8") as f:
        for c in clips:
            f.write(f"file '{c}'\n")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", "sz_list.txt",
        "-c", "copy", "sz_video_only.mp4"
    ], check=True)

    create_audio_track("sz_track.wav", elapsed, events, item.get("music_key", 0))

    subprocess.run([
        "ffmpeg", "-y",
        "-i", "sz_video_only.mp4",
        "-i", "sz_track.wav",
        "-filter_complex",
        "[1:a]aecho=0.8:0.85:55:0.22,afade=t=out:st=" + str(max(0, elapsed-1.5)) + ":d=1.5[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest", output_mp4
    ], check=True)

    return int(max(1000, (elapsed - 1.0) * 1000))

def publish_to_ig(mp4_path: str, caption: str, thumb_ms: int):
    file_size = os.path.getsize(mp4_path)
    init_res = requests.post(
        f"{GRAPH_URL}/{IG_USER_ID}/media",
        data={
            "media_type": "REELS",
            "upload_type": "resumable",
            "caption": caption,
            "share_to_feed": "true",
            "thumb_offset": str(thumb_ms),
            "access_token": ACCESS_TOKEN
        }
    ).json()

    if "id" not in init_res or "uri" not in init_res:
        raise Exception(f"Container init failed: {init_res}")

    creation_id = init_res["id"]
    with open(mp4_path, "rb") as vf:
        up_res = requests.post(
            init_res["uri"],
            headers={
                "Authorization": f"OAuth {ACCESS_TOKEN}",
                "offset": "0",
                "file_size": str(file_size),
                "Content-Type": "application/octet-stream"
            },
            data=vf
        ).json()

    for _ in range(25):
        time.sleep(5)
        st = requests.get(
            f"{GRAPH_URL}/{creation_id}",
            params={"fields": "status_code", "access_token": ACCESS_TOKEN}
        ).json()
        if st.get("status_code") == "FINISHED":
            break
        elif st.get("status_code") in ("ERROR", "EXPIRED"):
            raise Exception(f"Processing error: {st}")

    pub_res = requests.post(
        f"{GRAPH_URL}/{IG_USER_ID}/media_publish",
        data={"creation_id": creation_id, "access_token": ACCESS_TOKEN}
    ).json()
    print("PUBLISHED REEL:", pub_res)

async def main():
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)

    live_captions = ""
    if IG_ACCESS_TOKEN:
        try:
            from datetime import datetime, timezone
            r_m = requests.get(f"https://graph.facebook.com/v21.0/{IG_USER_ID}/media", params={"fields": "caption,timestamp", "limit": 100, "access_token": IG_ACCESS_TOKEN}).json()
            media_list = r_m.get("data", [])
            live_captions = " ".join([m.get("caption", "") for m in media_list])
            print(f"Checked {len(media_list)} live IG posts for deduplication.")
            if media_list and "timestamp" in media_list[0]:
                last_ts = datetime.strptime(media_list[0]["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
                hours_since = (datetime.now(timezone.utc) - last_ts).total_seconds() / 3600.0
                print(f"Hours since last Instagram Reel: {hours_since:.2f}h")
                if hours_since < 3.5:
                    print("Less than 3.5 hours since last Reel. Exiting cleanly until next window!")
                    return
        except Exception as e:
            print("IG check warning:", e)
    next_item = next((x for x in queue if not x.get("posted") and x["messages"][0]["text"] not in live_captions), None)
    if not next_item:
        print("All 500 Reels have been posted!")
        return

    print(f"Rendering Reel #{next_item['id']} ({next_item['culture'].upper()} - {next_item['contact_name']})...")
    thumb_ms = await render_item(next_item, "SAFEZONE_PREVIEW.mp4")

    if "--publish" in sys.argv:
        print("Uploading SAFEZONE_PREVIEW.mp4 to @loveunlimitedchats...")
        publish_to_ig("SAFEZONE_PREVIEW.mp4", next_item["caption"], thumb_ms)
        next_item["posted"] = True
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=2, ensure_ascii=False)
    else:
        print("\nDONE! Preview SAFEZONE_PREVIEW.mp4 locally (or run 'python auto_reel_poster.py --publish' to post live!)")

if __name__ == "__main__":
    asyncio.run(main())



