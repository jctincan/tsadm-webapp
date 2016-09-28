import tsadm.db

db = tsadm.db.TSAdmDB()

def maint():
    db.jobq_maint()
    db.activity_log_maint()
    return 0
