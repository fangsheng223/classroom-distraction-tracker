from django.urls import path
from . import views

urlpatterns = [
    # ── Warmup ────────────────────────────────────────────────────────
    path('warmup/',                                         views.warmup,                  name='warmup'),

    # ── Configuration ─────────────────────────────────────────────────
    path('configs/',                                        views.list_configs,            name='list_configs'),

    # ── Offline Batch Jobs ────────────────────────────────────────────
    path('jobs/recent/',                                    views.list_recent_jobs,        name='list_recent_jobs'),
    path('jobs/clear-history/',                             views.clear_history,           name='clear_history'),
    path('jobs/',                                           views.create_job,              name='create_job'),
    path('jobs/<str:job_id>/',                              views.get_job,                 name='get_job'),
    path('jobs/<str:job_id>/report/',                       views.job_overall_report,      name='job_overall_report'),
    path('jobs/<str:job_id>/students/<str:student_id>/report/', views.job_student_report,  name='job_student_report'),
    path('jobs/<str:job_id>/run/',                          views.run_job,                 name='run_job'),
    path('jobs/<str:job_id>/output/',                       views.stream_job_output,       name='stream_job_output'),  # SSE
    path('jobs/<str:job_id>/heartbeat/',                    views.heartbeat_job,           name='heartbeat_job'),
    path('jobs/<str:job_id>/stop/',                         views.stop_job,                name='stop_job'),
    path('jobs/<str:job_id>/clear-log/',                    views.clear_job_log,           name='clear_job_log'),

    # ── Near Real-Time Sessions ───────────────────────────────────────
    path('realtime/start/',                                         views.realtime_start,          name='realtime_start'),
    path('realtime/cameras/',                                       views.realtime_list_cameras,   name='realtime_list_cameras'),
    path('realtime/<str:session_id>/stop/',                         views.realtime_stop,           name='realtime_stop'),
    path('realtime/<str:session_id>/mjpeg/',                        views.realtime_mjpeg,          name='realtime_mjpeg'),  # MJPEG stream
    path('realtime/<str:session_id>/status/',                       views.realtime_status,         name='realtime_status'),
    path('realtime/<str:session_id>/snapshot.jpg',                  views.realtime_snapshot,       name='realtime_snapshot'),
    path('realtime/<str:session_id>/report/',                       views.realtime_overall_report, name='realtime_overall_report'),
    path('realtime/<str:session_id>/students/<str:student_id>/report/', views.realtime_student_report, name='realtime_student_report'),
]
