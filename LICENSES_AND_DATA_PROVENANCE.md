# Licenses and data provenance

## Images and labels

- `data/synthetic/**` and runtime demo scenes are procedurally drawn by this project with OpenCV primitives. They use no downloaded photographs, customer footage, personal data or third-party dataset.
- The synthetic mask labels identify the staged cool-toned polygon only. They do not label real water, leaks, root cause, safety severity or operating conditions.
- The privacy aid is OpenCV Zoo's YuNet ONNX model `src/incident_memory/assets/face_detection_yunet_2026may.onnx` (229,738 bytes; SHA-256 `ebafce4e3c118d6554634be5c27ab333b4c047a9a8c3faf1d7cf93101c22f0f0`). Its [upstream model documentation](https://github.com/opencv/opencv_zoo/blob/main/models/face_detection_yunet/README.md) lists the model files in that directory under MIT. The project runs it via OpenCV 5 `FaceDetectorYN`; it is a limited privacy aid and not exhaustive.
- OpenCV version notes are from the [official OpenCV 5 wiki](https://github.com/opencv/opencv/wiki/OpenCV-5). Competition requirements/deadline are from [Devpost overview](https://opencv26.devpost.com/), [Devpost rules](https://opencv26.devpost.com/rules) and the [OpenCV competition page](https://opencv.org/opencv-ai-competition-2026/).

## Software dependencies

Direct Python dependencies and exact versions are listed in `requirements.txt`; the complete resolved environment used here is pinned in `requirements-lock.txt`. The main packages have their respective upstream licenses: OpenCV (`Apache-2.0`), NumPy (`BSD-3-Clause`), FastAPI (`MIT`), Uvicorn (`BSD-3-Clause`), boto3 (`Apache-2.0`), pytest (`MIT`), HTTPX (`BSD-3-Clause`), psutil (`BSD-3-Clause`), python-multipart (`Apache-2.0`). Consult each distribution's included metadata for full notices and transitive dependency terms.

No project-level redistribution license was selected in this build. The repository/archive is intended for judge access under the competition process; do not interpret it as an open-source license grant. Confirm project ownership and choose a license before public source publication.

