from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from group.models import Group

scheduler = BackgroundScheduler()

current_datetime = timezone.now()


##원하는 작업
####팀빌딩 함수 추가 하는 부분
def make_auto(function):
    groups = Group.objects.filter(end_date__gt=current_datetime)
    for group in groups:
        print(group)
        print("서버가 재시작되었습니다")
        scheduler.add_job(function,
                          trigger=DateTrigger(group.end_date),
                          args=[group.id])


# 스케줄링 작업 실행
def start_scheduler():
    scheduler.print_jobs()
    scheduler.start()


##view에서 팀빌딩 함수 실행
def team_building_auto(function, group):
    if group.end_date > current_datetime:
        print("스케줄 추가중")
        scheduler.add_job(function,
                          trigger=DateTrigger(group.end_date),
                          args=[group.id])
        print("스케줄 추가 완료")
