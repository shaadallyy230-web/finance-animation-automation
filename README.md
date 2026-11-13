# Finance Animation Automation

A GitHub Actions pipeline for original English personal-finance explainer videos and vertical YouTube Shorts.

## Weekly publishing target
- Monday–Saturday: 1 long-form 9–10 minute finance animation per day
- Monday–Saturday: 2 original vertical YouTube Shorts per day
- Sunday: no scheduled run
- Weekly target: 6 long videos + 12 Shorts

Each daily run generates one long episode with 45 scenes and two separate 3-scene vertical Shorts. The recurring original 2D host wears a black shirt, beige trousers, brown belt and white sneakers. Character walk-cycle/gesture/blink/talking loops, animated finance props and camera movement are included.

## Setup
1. Add `GEMINI_API_KEY` under repository Settings → Secrets and variables → Actions.
2. For YouTube upload, configure `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`, and `ENABLE_YOUTUBE_UPLOAD=true` as repository secrets.
3. Open Actions → Daily Finance Animation + 2 Shorts → Run workflow to test manually.

The scheduled run is Monday–Saturday at 13:00 UTC (6:30 PM India time). GitHub may delay scheduled runs.

## Important limitations
This is procedural 2D cutout/cartoon animation, not studio-grade hand-drawn animation or a frame-for-frame copy of any reference channel. Free Gemini quotas, Edge TTS availability, GitHub Actions limits and YouTube API quotas apply. The workflow uploads as **private** by default; review the videos before making them public. Without YouTube OAuth secrets, it only creates downloadable workflow artifacts. No unlimited-free or guaranteed-upload promise is made.

Keep all scripts, characters, branding and visuals original. Educational content only; not financial advice.
