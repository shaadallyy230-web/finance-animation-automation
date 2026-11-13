# Finance Animation Automation — setup

This project creates original English personal-finance videos for a general US audience.

## Daily output
The scheduled workflow runs Monday–Saturday at 13:00 UTC (6:30 PM India time):
- 1 long-form 9–10 minute episode with 45 scenes
- 2 separate vertical 9:16 YouTube Shorts, each with 3 scenes and approximately 45–60 seconds of narration
- Sunday has no scheduled run

Weekly target: 6 long videos + 12 Shorts.

## Required secret
Add `GEMINI_API_KEY` in GitHub repository Settings → Secrets and variables → Actions.

## Optional YouTube upload secrets
Configure YouTube Data API v3 OAuth and add:
- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN`
- `ENABLE_YOUTUBE_UPLOAD` with value `true`

Uploads are private by default so the owner can review them before publishing. If OAuth is not configured, the workflow only generates MP4 files and saves them as a GitHub Actions artifact for 7 days.

## Run a test
Open Actions → Daily Finance Animation + 2 Shorts → Run workflow.

## Limitations
This is procedural 2D cartoon animation, not studio-grade hand-drawn animation. Gemini free-tier quotas, third-party TTS availability, GitHub Actions limits and YouTube API quotas may limit throughput. Review every video before publishing. Educational content only, not financial advice. Never commit API keys or OAuth secrets.
