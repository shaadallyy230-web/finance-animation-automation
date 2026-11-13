# Finance Animation Automation — setup

This project creates original English personal-finance explainer videos for a US audience. The visual direction is inspired by the broad whiteboard/2D-cartoon storytelling format of finance education channels, while using original scripts, branding, scenes and a recurring original host.

## Current pipeline
- Gemini writes a 9-10 minute original episode planned as 45 scenes.
- Edge TTS creates American-English narration.
- Pillow draws scene-specific illustrated backgrounds, props, captions and the recurring host.
- FFmpeg adds gentle camera zoom/pan motion and assembles the MP4.
- A custom thumbnail, SEO title, description and tags are generated.
- Optional YouTube upload uses Google OAuth credentials.
- GitHub Actions can run manually or weekly.

## Required secret
Add GEMINI_API_KEY in GitHub repository Settings → Secrets and variables → Actions.

## Optional YouTube upload secrets
Only after configuring YouTube Data API v3 OAuth:
- YOUTUBE_CLIENT_ID
- YOUTUBE_CLIENT_SECRET
- YOUTUBE_REFRESH_TOKEN
- ENABLE_YOUTUBE_UPLOAD (set to true to enable uploading)

Uploads remain private by default. Generated files are saved as a workflow artifact for 7 days.

## Run
Open the Actions tab, choose Weekly Finance Animation, then Run workflow.
The weekly schedule is Monday at 13:00 UTC. GitHub may delay scheduled runs.

## Important
This starter uses illustrated scenes with camera movement; it is not yet full frame-by-frame character animation. Review every script and video before publishing. Free quotas and policies can change; this is not guaranteed unlimited or permanently free. Educational content only, not financial advice. Never commit API keys or OAuth secrets.
