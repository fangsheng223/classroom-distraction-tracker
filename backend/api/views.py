"""
API Views — Classroom Distraction Tracker
==========================================
Two execution modes:
  · Offline Batch  — upload a video file, run full pipeline, download report
  · Near Real-Time — connect a camera, receive MJPEG overlay + live stats
"""

import json
import threading
import time
import uuid
from pathlib import Path

from django.conf import settings
from django.http import (
    HttpRequest, HttpResponse, JsonResponse, StreamingHttpResponse
)
from django.views.decorators.csrf import csrf_exempt

# ── In-memory job / session stores ────────────────────────────────────────────
_JOBS: dict[str, dict]          = {}   # job_id → job state
_JOBS_LOCK                      = threading.Lock()
_REALTIME_SESSIONS: dict[str, dict] = {}   # session_id → session state
_RT_LOCK                        = threading.Lock()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _json(data, status=200):
    return JsonResponse(data, status=status, json_dumps_params={"ensure_ascii": False})


def _err(msg, status=400):
    return _json({"error": msg}, status=status)


# ── Warmup ────────────────────────────────────────────────────────────────────

@csrf_exempt
def warmup(request: HttpRequest):
    """Pre-load the YOLOv8 detector and CNN model into GPU memory."""
    # Model loading is handled lazily on first job run.
    return _json({"status": "ready"})


# ── Configuration ─────────────────────────────────────────────────────────────

@csrf_exempt
def list_configs(request: HttpRequest):
    """Return available inference configurations (e.g., different IoU modes)."""
    configs = [
        {
            "id":          "ours_full",
            "label":       "Ours_Full (paper default)",
            "dynamic_iou": True,
            "combined_score": True,
            "context":     True,
        },
        {
            "id":             "no_context",
            "label":          "No_Context (ablation)",
            "dynamic_iou":    True,
            "combined_score": True,
            "context":        False,
        },
        {
            "id":             "basic_iou",
            "label":          "Basic_IoU_Only (ablation)",
            "dynamic_iou":    False,
            "combined_score": False,
            "context":        False,
        },
    ]
    return _json({"configs": configs})


# ── Offline Batch Jobs ─────────────────────────────────────────────────────────

@csrf_exempt
def create_job(request: HttpRequest):
    """
    POST  /api/jobs/
    Body: multipart/form-data  { video: <file>, config_id: str }

    Creates a job record and stores the uploaded video.
    Returns job_id for subsequent polling.
    """
    if request.method != "POST":
        return _err("POST required", 405)

    video_file = request.FILES.get("video")
    config_id  = request.POST.get("config_id", "ours_full")

    if not video_file:
        return _err("No video file provided")

    job_id   = str(uuid.uuid4())[:8]
    media    = Path(settings.MEDIA_ROOT) / "jobs" / job_id
    media.mkdir(parents=True, exist_ok=True)
    video_path = media / video_file.name

    with open(video_path, "wb") as f:
        for chunk in video_file.chunks():
            f.write(chunk)

    with _JOBS_LOCK:
        _JOBS[job_id] = {
            "id":         job_id,
            "status":     "pending",
            "config_id":  config_id,
            "video_path": str(video_path),
            "log":        [],
            "result":     None,
            "created_at": time.time(),
        }

    return _json({"job_id": job_id}, status=201)


@csrf_exempt
def run_job(request: HttpRequest, job_id: str):
    """
    POST  /api/jobs/<job_id>/run/
    Launches the offline inference pipeline in a background thread.
    """
    if request.method != "POST":
        return _err("POST required", 405)

    with _JOBS_LOCK:
        job = _JOBS.get(job_id)
    if not job:
        return _err("Job not found", 404)

    def _worker():
        with _JOBS_LOCK:
            _JOBS[job_id]["status"] = "running"

        try:
            # Import here to avoid loading heavy models at startup
            import sys, os
            sys.path.insert(0, str(Path(settings.BASE_DIR).parent))
            from main_integrated_system import IntegratedDistractionSystem

            system = IntegratedDistractionSystem()
            result = system.process_video(
                job["video_path"],
                log_callback=lambda msg: _JOBS[job_id]["log"].append(msg),
            )
            with _JOBS_LOCK:
                _JOBS[job_id]["status"] = "done"
                _JOBS[job_id]["result"] = result
        except Exception as exc:
            with _JOBS_LOCK:
                _JOBS[job_id]["status"] = "error"
                _JOBS[job_id]["log"].append(f"ERROR: {exc}")

    threading.Thread(target=_worker, daemon=True).start()
    return _json({"status": "started"})


@csrf_exempt
def stream_job_output(request: HttpRequest, job_id: str):
    """
    GET  /api/jobs/<job_id>/output/
    Server-Sent Events stream — delivers log lines as the job runs.
    """
    def _generate():
        sent = 0
        while True:
            with _JOBS_LOCK:
                job    = _JOBS.get(job_id)
                status = job["status"] if job else "error"
                log    = job["log"][sent:] if job else []

            for line in log:
                yield f"data: {json.dumps({'line': line})}\n\n"
            sent += len(log)

            if status in ("done", "error"):
                yield f"data: {json.dumps({'status': status})}\n\n"
                break
            time.sleep(0.3)

    return StreamingHttpResponse(
        _generate(),
        content_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@csrf_exempt
def get_job(request: HttpRequest, job_id: str):
    with _JOBS_LOCK:
        job = _JOBS.get(job_id)
    if not job:
        return _err("Not found", 404)
    return _json({k: v for k, v in job.items() if k != "result"})


@csrf_exempt
def job_overall_report(request: HttpRequest, job_id: str):
    with _JOBS_LOCK:
        job = _JOBS.get(job_id)
    if not job or job["status"] != "done":
        return _err("Report not ready", 404)
    return _json(job.get("result", {}).get("class_report", {}))


@csrf_exempt
def job_student_report(request: HttpRequest, job_id: str, student_id: str):
    with _JOBS_LOCK:
        job = _JOBS.get(job_id)
    if not job or job["status"] != "done":
        return _err("Report not ready", 404)
    students = job.get("result", {}).get("students", {})
    return _json(students.get(student_id, {}))


@csrf_exempt
def list_recent_jobs(request: HttpRequest):
    with _JOBS_LOCK:
        jobs = [
            {"id": j["id"], "status": j["status"], "created_at": j["created_at"]}
            for j in sorted(_JOBS.values(), key=lambda x: x["created_at"], reverse=True)[:20]
        ]
    return _json({"jobs": jobs})


@csrf_exempt
def clear_history(request: HttpRequest):
    if request.method != "POST":
        return _err("POST required", 405)
    with _JOBS_LOCK:
        _JOBS.clear()
    return _json({"cleared": True})


@csrf_exempt
def heartbeat_job(request: HttpRequest, job_id: str):
    with _JOBS_LOCK:
        status = _JOBS[job_id]["status"] if job_id in _JOBS else "not_found"
    return _json({"status": status})


@csrf_exempt
def stop_job(request: HttpRequest, job_id: str):
    if request.method != "POST":
        return _err("POST required", 405)
    with _JOBS_LOCK:
        if job_id in _JOBS:
            _JOBS[job_id]["status"] = "stopped"
    return _json({"stopped": True})


@csrf_exempt
def clear_job_log(request: HttpRequest, job_id: str):
    if request.method != "POST":
        return _err("POST required", 405)
    with _JOBS_LOCK:
        if job_id in _JOBS:
            _JOBS[job_id]["log"] = []
    return _json({"cleared": True})


# ── Near Real-Time Sessions ────────────────────────────────────────────────────

@csrf_exempt
def realtime_list_cameras(request: HttpRequest):
    """Enumerate available camera indices (0, 1, …)."""
    import cv2
    cameras = []
    for i in range(4):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cameras.append({"index": i, "label": f"Camera {i}"})
            cap.release()
    return _json({"cameras": cameras})


@csrf_exempt
def realtime_start(request: HttpRequest):
    """
    POST  /api/realtime/start/
    Body: { camera_index: int, config_id: str }
    Launches an NRT inference session; returns session_id.
    """
    if request.method != "POST":
        return _err("POST required", 405)

    data        = json.loads(request.body or b"{}")
    cam_idx     = int(data.get("camera_index", 0))
    config_id   = data.get("config_id", "ours_full")
    session_id  = str(uuid.uuid4())[:8]

    with _RT_LOCK:
        _REALTIME_SESSIONS[session_id] = {
            "id":         session_id,
            "camera":     cam_idx,
            "config_id":  config_id,
            "status":     "running",
            "frame":      None,       # latest JPEG bytes
            "stats":      {},
            "stop_event": threading.Event(),
        }

    def _nrt_worker(sid):
        import cv2, sys
        sys.path.insert(0, str(Path(settings.BASE_DIR).parent))
        from main_integrated_system import IntegratedDistractionSystem

        sess    = _REALTIME_SESSIONS[sid]
        stop_ev = sess["stop_event"]
        system  = IntegratedDistractionSystem()
        cap     = cv2.VideoCapture(sess["camera"])

        while not stop_ev.is_set():
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.05)
                continue
            result = system.process_frame(frame)
            _, buf  = cv2.imencode(".jpg", result["annotated_frame"],
                                   [cv2.IMWRITE_JPEG_QUALITY, 75])
            with _RT_LOCK:
                sess["frame"] = bytes(buf)
                sess["stats"] = result.get("student_stats", {})

        cap.release()
        with _RT_LOCK:
            sess["status"] = "stopped"

    threading.Thread(target=_nrt_worker, args=(session_id,), daemon=True).start()
    return _json({"session_id": session_id}, status=201)


@csrf_exempt
def realtime_mjpeg(request: HttpRequest, session_id: str):
    """
    GET  /api/realtime/<session_id>/mjpeg/
    Multipart JPEG stream for the annotated live feed.
    """
    BOUNDARY = b"--frame"

    def _gen():
        while True:
            with _RT_LOCK:
                sess  = _REALTIME_SESSIONS.get(session_id)
                frame = sess["frame"] if sess else None
                if sess and sess["status"] != "running":
                    break
            if frame:
                yield (BOUNDARY + b"\r\nContent-Type: image/jpeg\r\n\r\n"
                       + frame + b"\r\n")
            time.sleep(0.04)

    return StreamingHttpResponse(
        _gen(),
        content_type=f"multipart/x-mixed-replace; boundary=frame",
    )


@csrf_exempt
def realtime_status(request: HttpRequest, session_id: str):
    with _RT_LOCK:
        sess = _REALTIME_SESSIONS.get(session_id, {})
    return _json({
        "status": sess.get("status", "not_found"),
        "stats":  sess.get("stats", {}),
    })


@csrf_exempt
def realtime_snapshot(request: HttpRequest, session_id: str):
    with _RT_LOCK:
        sess  = _REALTIME_SESSIONS.get(session_id)
        frame = sess["frame"] if sess else None
    if not frame:
        return HttpResponse(status=404)
    return HttpResponse(frame, content_type="image/jpeg")


@csrf_exempt
def realtime_stop(request: HttpRequest, session_id: str):
    if request.method != "POST":
        return _err("POST required", 405)
    with _RT_LOCK:
        sess = _REALTIME_SESSIONS.get(session_id)
    if sess:
        sess["stop_event"].set()
    return _json({"stopped": True})


@csrf_exempt
def realtime_overall_report(request: HttpRequest, session_id: str):
    with _RT_LOCK:
        sess = _REALTIME_SESSIONS.get(session_id, {})
    return _json(sess.get("stats", {}))


@csrf_exempt
def realtime_student_report(request: HttpRequest, session_id: str, student_id: str):
    with _RT_LOCK:
        sess = _REALTIME_SESSIONS.get(session_id, {})
    return _json(sess.get("stats", {}).get(student_id, {}))
