# Responsible use

Fortifiers Incident Memory is a decision-support research prototype. It is not a certified life-safety device and must not replace alarms, inspection, facility procedures or qualified human judgment.

## Evidence and claims

- OBSERVED means only that the image pipeline found a localized pixel/appearance change.
- SENSOR_CORRELATED means a reported active sensor timestamp was within five minutes of the event timestamp; it does not validate the sensor or prove causality.
- HYPOTHESIS is a cautious possible-water interpretation when a staged visual cue coincides with a sensor.
- UNVERIFIED applies to material identity, actual water presence, leak source, root cause and unsupported conclusions.
- RGB frames cannot directly establish invisible gas or fire chemistry. No model makes a root-cause diagnosis.

All demonstration images, rooms, patches and sensor records are procedurally generated synthetic fixtures.

## Human control

The only review actions are acknowledge, reject and request-more-evidence, appended to an audit record. They do not execute physical actions. Never connect this prototype to machinery shutdown, alarm suppression, doors, emergency dispatch or other safety-critical actuation. Significant maintenance/safety decisions require a responsible operator and site-approved process.

## Data, consent and privacy

Use only owned, authorized or appropriately licensed imagery and sensor records. Obtain consent and follow site notices before recording people. Local upload accepts PNG/JPEG/WebP, limits the full request to 17 MiB, each image to 8 MiB and decoded images to 12 megapixels, rejects dimension mismatches, and re-encodes evidence so original EXIF metadata is not retained. OpenCV 5 DNN FaceDetectorYN with YuNet blurs detected faces; this does not provide comprehensive redaction. Upload processing stops if the model or inference fails. Operators must inspect and manually redact people, badges, screens, labels, license plates and other identifiers.

The public AWS endpoint is an unauthenticated Lambda Function URL restricted by application behavior to seven built-in synthetic scenarios. User image uploads are disabled and return 403. Do not send private or sensitive material to the endpoint. Evidence artifacts use a private S3 bucket with SSE-S3 encryption, a seven-day lifecycle and short-lived presigned downloads. Presigned URLs are bearer links while active; handle them accordingly.

## Security and retention

No AWS keys are stored in source, browser code, .env files or reports. The Lambda role is scoped to the project evidence prefix and log group. S3 public access is blocked. CloudWatch logs expire after 14 days; generated evidence expires after seven days. The public function URL has no authentication, and the application does not enforce a hard request or spend limit. Monitor billing and disable public invocation when the judge demo is no longer needed.

## Known limitations

YuNet can miss faces and does not identify many sensitive details. Image-quality and reliability values are uncalibrated heuristics. Color and appearance can change with material, lighting, compression and camera motion. The evaluation uses synthetic generated data and is not field validation. Fail closed on uncertain comparisons and continue the site's normal alarm procedure.
