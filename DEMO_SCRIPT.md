# Demo video script and current recording status

## Existing video

The published Unlisted video is a genuine 3:40 screen capture of the local FastAPI dashboard. It is 1920×1080, 15 fps, silent/captioned, and its SHA-256 is in artifacts/video/video-manifest.json. It shows synthetic positive and negative investigations, architecture and local synthetic evaluation. The video was recorded before the AWS deployment, so its end card says AWS is not deployed. It does not show or name the solo entrant. It is accessible at https://youtu.be/_k0J1XHyVyA.

A replacement AWS-inclusive recording is not available yet. The installed local recorder tool is not exposed in this session. Do not represent the old video as evidence of AWS execution. A fresh recording also needs the entrant's real name/identity if the judges expect the actual solo participant to appear.

## Recording plan for a replacement (4:45 maximum)

Use the existing screen recorder to capture the actual browser. Keep the interface at a readable desktop resolution, disable notifications, and do not show account IDs, billing details or browser credentials. Use the actual live AWS endpoint and actual outputs. If identifying the entrant on camera or voice, the entrant must record their own introduction.

| Time | Screen and narration |
|---|---|
| 0:00–0:20 | Project title and tagline. The solo entrant introduces themself if required. Explain that alarms report an event while this tool compares visual history and gathers evidence. |
| 0:20–0:55 | Open the public AWS dashboard and select the synthetic clear_change scenario. State that all scenes and sensor events are generated test fixtures. |
| 0:55–1:35 | Run the event. Show before/after images, OpenCV change overlay and region; distinguish observed appearance from confirmed physical cause. |
| 1:35–2:20 | Show the real trace: quality, baseline selection, ORB/RANSAC alignment, region inspection, historical retrieval, sensor correlation and human review. Point out the observation that causes each next action. |
| 2:20–2:55 | Run poor_image. Show quality gate and retake_requested rather than an unsupported diagnosis. |
| 2:55–3:25 | Run historical_match or lighting_shift. Show the older-frame retrieval or normalized brightness outcome changing the final policy. |
| 3:25–3:50 | Open the evidence report or download the ZIP. Show image hashes, report and human-review classification. |
| 3:50–4:15 | Show architecture diagram and describe Python 3.14 Lambda ZIP, actual OpenCV 5 execution, private S3 evidence and CloudWatch logs. |
| 4:15–4:35 | Show evaluation: 7/7 expected policy actions vs 4/7 one-pass on synthetic held-out cases; mask metrics are synthetic pixel overlap, not leak accuracy. Mention 37 passing tests and one or more limitations. |
| 4:35–4:45 | Close with the tagline and note this is decision support, not a certified safety device. |

## Remaining exact recording/publishing step

1. Record the replacement using the approved local screen recorder; capture only the browser content needed for the demo.
2. Include a real entrant introduction or title card with the participant's name if required. Do not synthesize a likeness or voice.
3. Review the final runtime (under five minutes), confirm the endpoint works from a fresh unauthenticated session, and ensure no credentials or account/billing details appear.
4. Upload the replacement video to the entrant's YouTube channel as Unlisted, then verify the final video link while signed out.
5. Replace the video URL in Devpost and update artifacts/video/video-manifest.json, README.md, SUBMISSION.md and FINAL_SUBMISSION_STATUS.md.

The current published video remains accessible but predates AWS deployment. The replacement video and its accessibility have not been verified.
