# Finance Animation Automation

A free-tier, GitHub Actions-based pipeline for original English personal-finance explainer videos.

## What the bot creates
- Original 9–10 minute English finance scripts for a general US audience
- 45 planned scenes with narration, setting, action, visual direction and on-screen captions
- American-English narration using Edge TTS
- A recurring original 2D host in a black shirt, beige trousers, brown belt and white sneakers
- Frame-by-frame looping character animation: walk-cycle motion, arm gestures, blinking and talking-mouth movement
- Animated finance props: bouncing dollar coin, moving chart bars/line or rocking credit card
- Camera movement, thumbnail, SEO metadata and optional YouTube upload

## Setup
1. Add `GEMINI_API_KEY` under repository Settings → Secrets and variables → Actions.
2. For YouTube upload, configure the optional OAuth secrets described in [SETUP.md](SETUP.md).
3. Open Actions → Weekly Finance Animation → Run workflow to test manually.

The weekly workflow is scheduled for Monday 13:00 UTC. GitHub may delay scheduled runs.

## Important limitations
This is a procedural 2D cutout/cartoon animation starter, not a studio-grade hand-drawn cartoon and not a frame-for-frame copy of any reference channel. Character and prop motion are generated from reusable loops and scene directions. Review the rendered video before publishing. Free API quotas, GitHub Actions limits and third-party voice service availability can change. No unlimited-free or guaranteed-upload promise is made.

All scripts, characters, branding and visuals should remain original. Educational content only; not financial advice.
