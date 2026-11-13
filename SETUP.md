# Finance Animation Automation — setup

This project creates original English personal-finance explainer videos with a recurring illustrated character. It does not copy any existing channel.

## Features
- Gemini drafts an original educational episode.
- Edge TTS creates English narration.
- Pillow draws illustrated scenes and a thumbnail.
- FFmpeg assembles the scenes into an MP4.
- Optional YouTube upload uses Google OAuth credentials.
- GitHub Actions can run weekly or manually.

## Required secret
Add GEMINI_API_KEY in GitHub repository Settings → Secrets and variables → Actions.

## Optional YouTube upload secrets
Only after configuring YouTube Data API v3 OAuth:
- YOUTUBE_CLIENT_ID
- YOUTUBE_CLIENT_SECRET
- YOUTUBE_REFRESH_TOKEN
- ENABLE_YOUTUBE_UPLOAD (set to true to enable upload)

Uploads are private by default. Generated files are saved as a workflow artifact for 7 days.

## Run
Open the Actions tab, choose Weekly Finance Animation, then Run workflow.
The weekly schedule is Monday at 13:00 UTC. GitHub may delay scheduled runs.

## Important
Free quotas and policies can change; this is not guaranteed unlimited or permanently free. Review every generated script and video before publishing. Educational content only, not financial advice. Never commit API keys or OAuth secrets.
