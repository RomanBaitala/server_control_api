from apscheduler.schedulers.background import BackgroundScheduler
from app.bll.services import server_service

def start_health_checker(app):
    scheduler = BackgroundScheduler()

    def check_servers():
        with app.app_context():
            try:
                server_service.cleanup_offline_servers(timeout_minutes=5)
                print("Health check: status cleanup finished.")
            except Exception as e:
                print(f"Health check error: {e}")

    scheduler.add_job(
        func=check_servers,
        trigger="interval",
        minutes=1,
        id="server_status_cleanup",
        replace_existing=True
    )

    scheduler.start()
    print("Scheduler started: server health monitor is active.")