# Recorded demonstration — 3:40

**Recording status:** real screen capture completed from the running local FastAPI dashboard. The local workspace file is `artifacts/video/fortifiers-incident-memory-demo.mp4`; it is 220.4 seconds, 1920×1080, 15 fps, silent, and captioned with on-screen text. SHA-256: `a662dd0bd82bbb31df5396b0dc83754ac1b80c553ed61dd27733f29e0a741002`. [video-manifest.json](artifacts/video/video-manifest.json) records render metadata and the raw capture checksum. The video is [published Unlisted on YouTube](https://youtu.be/_k0J1XHyVyA) and available from the [public GitHub release](https://github.com/axfrgo/fortifiers-incident-memory/releases/tag/demo-2026-10-27). An unauthenticated YouTube request returned HTTP 200 and the expected title.

## What the recording actually shows

- Opening title, project tagline, and “solo entry · demo build” identification.
- The real local dashboard and OpenCV 5.0.0 status.
- A synthetic water-sensor event with a visible staged image change; the controller investigates and requests human review.
- A blurred synthetic frame; image-quality output causes the controller to request a retake.
- A lighting-only change; normalized comparison does not support a new localized change.
- An older-history case; the agent retrieves earlier evidence and downgrades novelty.
- Architecture and evaluation slides that explicitly state AWS is not deployed and all reported results come from synthetic fixtures.
- Closing statement and limitations.

This recording has no voiceover or user likeness. It labels the project as a solo entry but does not show or name the entrant. Add a short real introduction from the entrant if the competition requires the member’s name or appearance; do not use a generated likeness or voice.

## Current hosting state

YouTube Studio confirmed “Video published” after the entrant approved Unlisted publication. The Studio dialog showed the 3:41 item and share link. A no-credential HTTP GET to the link returned HTTP 200 and the video title. Devpost's saved private draft now contains the video URL; the draft has not been submitted.

## Remaining presentation gaps

1. AWS workload and public endpoint are not deployed. No cloud processing is shown or claimed in this recording.
2. The entrant must decide whether to add their own spoken or visible introduction to satisfy team-identification requirements.
3. The published video is hosted as Unlisted. Judges can watch with the link; its URL is already saved in the Devpost draft.
4. Review the draft before submission. The entrant must complete any missing eligibility and identity declarations and give explicit final action-time approval. No submission has been made.

The measured values shown in the recording are synthetic benchmark outputs only. They are not field leak-detection performance, AWS latency, customer outcomes, or a safety certification.
