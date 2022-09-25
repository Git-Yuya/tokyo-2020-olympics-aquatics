from django.db import models


class SwimmingResult(models.Model):
    """ Model class of swimming result """
    
    id = models.IntegerField(verbose_name="ID", primary_key=True)
    sport = models.CharField(verbose_name="競技", max_length=50)
    event = models.CharField(verbose_name="種目", max_length=50)
    rank = models.SmallIntegerField(verbose_name="順位")
    athletes = models.TextField(verbose_name="選手")
    team = models.CharField(verbose_name="チーム", max_length=20)
    record = models.CharField(verbose_name="記録", max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.sport}:{self.event}({self.rank})"
