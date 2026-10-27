# Responsible use

Fortifiers Incident Memory is a decision-support research prototype. It is not a certified life-safety device and must not replace alarms, inspection, facility procedures or qualified human judgment.

## Evidence and claims

- `OBSERVED` means only that the image pipeline found a localized pixel/appearance change.
- `SENSOR_CORRELATED` means a reported active sensor timestamp was within five minutes of the event timestamp; it does not validate the sensor or prove causality.
- `HYPOTHESIS` is a cautious possible-water interpretation when a staged cool-tone cue coincides with the sensor.
- `UNVERIFIED` applies to material identity, actual water presence, leak source, root cause and every unsupported conclusion.
- RGB frames cannot directly establish invisible gas or fire chemistry. No model makes a root-cause diagnosis.

## Human control

The only review actions are acknowledge, reject and request-more-evidence, appended to an audit record. They do not execute physical actions. Never connect this prototype to machinery shutdown, alarm suppression, doors, emergency dispatch or other safety-critical actuation. Significant maintenance/safety decisions require a responsible operator and site-approved process.

## Data, consent and privacy

Use only owned, authorized or appropriately licensed imagery and sensor records. Obtain consent and follow site notices before recording people. Local upload accepts PNG/JPEG/WebP, limits the full request to 17 MiB, each image to 8 MiB and decoded images to 12 megapixels, rejects dimension mismatches, decodes to pixel arrays and re-encodes evidence so original EXIF metadata is not retained. OpenCV 5 DNN FaceDetectorYN with YuNet blurs detected faces; this does not provide comprehensive redaction. Upload processing stops if the model or inference fails. Operators must inspect and manually redact people, badges, screens, labels, license plates and other identifiers. Avoid credentials, access codes and sensitive layouts.

The supplied scenario data is synthetic and contains no people. The prepared public AWS deployment disables user uploads and only exposes synthetic scenarios. S3 evidence is private, versioned and server-side encrypted; the app returns an expiring presigned download link only after an investigation. A presigned URL is a bearer credential while active; handle it accordingly. Review records go under the private evidence prefix. App Runner has only scoped `GetObject`/`PutObject` access. No real deployment has occurred.

## Security and retention

Do not store AWS keys in source, browser code, `.env` committed to Git, or reports. Use an authorized AWS identity role and service-managed permissions. Keep the S3 public-access block and IAM scope. Rotate any future review API secret through managed configuration. Cloud review actions are authenticated for non-synthetic reports; current cloud configuration prohibits such uploads.

Generated demo artifacts remain in local `artifacts/demo/` until manually removed. S3 versioning preserves evidence versions; establish a retention/deletion policy before any real operational use. Do not add human imagery to the public judge demo.

## Known limitations

YuNet can miss faces and does not detect many identifiers. Image-quality and reliability scores are uncalibrated heuristics. Color/appearance can be affected by material, lighting, compression and camera movement. Synthetic evaluation is not field validation. Fail closed on uncertain comparisons and continue the site's normal alarm procedure.

