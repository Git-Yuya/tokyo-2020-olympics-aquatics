from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Q
from .models import SwimmingResult


class IndexView(TemplateView):
    """ Display top page """
    
    template_name = "index.html"


class ResultView(TemplateView):
    """ Display the top 8 records of selected event. """
    
    template_name = "select_event.html"
    
    def post(self, request):
        
        # Get event value.
        event = self.request.POST.get("event")
        
        # Results of selected event
        results = SwimmingResult.objects.filter(event=event).order_by("rank")
        
        # Variables of dictionary type to be passed to the template
        context = {"results": results}
        
        return render(request, "result.html", context)
    
    
class MedalView(TemplateView):
    """ Display the number of medals won. """

    template_name = "medal.html"
    
    def get_context_data(self, **kwargs):
        
        # Query database for rank
        rows = SwimmingResult.objects.filter(Q(rank=1) | Q(rank=2) | Q(rank=3)).values("rank", "team")

        # Dictionary array for storing the number of medals
        medals = []

        for row in rows:

            # Whether the team exists or not
            is_exist = False

            # Judge whether the team exists in the array.
            for i in range(len(medals)):

                # If the team existed in the array
                if row["team"] in medals[i]["team"]:
                    is_exist = True
                    break

            # If the team didn't exist in the array
            if is_exist == False:

                # Add to the array.
                medals.append({
                    "rank": 0,
                    "team": row["team"],
                    "gold": 0,
                    "silver": 0,
                    "bronze": 0,
                    "total": 0
                })

        # Calculate the number of medals.
        for row in rows:
            for j in range(len(medals)):

                if row["team"] in medals[j]["team"]:

                    # If in first place
                    if row["rank"] == 1:
                        medals[j]["gold"] += 1
                        medals[j]["total"] += 1
                        break

                    # If in second place
                    if row["rank"] == 2:
                        medals[j]["silver"] += 1
                        medals[j]["total"] += 1
                        break

                    # If in third place
                    if row["rank"] == 3:
                        medals[j]["bronze"] += 1
                        medals[j]["total"] += 1
                        break

        # Sort the array.
        medals = sorted(medals, key=lambda x: (x["total"], x["gold"], x["silver"], x["bronze"]), reverse=True)

        # Store the rankings.
        for r in range(len(medals)):
            if r >= 1 and medals[r]["gold"] == medals[r - 1]["gold"] and medals[r]["silver"] == medals[r - 1]["silver"] and medals[r]["bronze"] == medals[r - 1]["bronze"]:
                medals[r]["rank"] = medals[r - 1]["rank"]
            else:
                medals[r]["rank"] = r + 1
        
        # Variables of dictionary type to be passed to the template
        context = super().get_context_data(**kwargs)
        
        # Add to context.
        context["medals"] = medals
        
        return context        
    

class ScoreView(TemplateView):
    """ Display the scores of each team. """    
    
    template_name = "score.html"
    
    def get_context_data(self, **kwargs):
    
        # Query database for score
        rows = SwimmingResult.objects.values("sport", "rank", "team")
        
        # Dictionary array for each scores
        scores = []

        for row in rows:

            # Whether the team exists or not
            is_exist = False

            # Judge whether the team exists in the array.
            for i in range(len(scores)):

                # If the team existed in the array
                if row["team"] in scores[i]["team"]:
                    is_exist = True
                    break

            # If the team did not exist in the array
            if is_exist == False:

                # Add to the array.
                scores.append({
                    "rank": 0,
                    "team": row["team"],
                    "swimming": 0,
                    "diving": 0,
                    "water_polo": 0,
                    "marathon_swimming": 0,
                    "artistic_swimming": 0,
                    "total": 0
                })

        # Score list
        score_list = [8, 7, 6, 5, 4, 3, 2, 1]

        # Calculate the scores of each sport.
        for row in rows:
            for j in range(len(scores)):
                if row["team"] in scores[j]["team"]:

                    if row["rank"] == "失格":
                        break
                    
                    sport = "競技"
                    if (row["sport"] == "競泳"):
                        sport = "swimming"
                    elif (row["sport"] == "飛び込み"):
                        sport = "diving"
                    elif (row["sport"] == "水球"):
                        sport = "water_polo"
                    elif (row["sport"] == "マラソンスイミング"):
                        sport = "marathon_swimming"
                    elif (row["sport"] == "アーティスティックスイミング"):
                        sport = "artistic_swimming"

                    scores[j][sport] += score_list[row["rank"] - 1]
                    scores[j]["total"] += score_list[row["rank"] - 1]

        # Sort the array.
        scores = sorted(scores, key=lambda x: x["total"], reverse=True)

        # Store the rankings.
        for r in range(len(scores)):
            if r >= 1 and scores[r]["total"] == scores[r - 1]["total"]:
                scores[r]["rank"] = scores[r - 1]["rank"]
            else:
                scores[r]["rank"] = r + 1

        # Variables of dictionary type to be passed to the template
        context = super().get_context_data(**kwargs)
        
        # Add to context.
        context["scores"] = scores
        
        return context        
    

class AthleteView(TemplateView):
    """ Display the results of athlete. """
    
    def get(self, request):
        """ If request.method == "GET" """
        
        # List of athletes from DB
        rows = SwimmingResult.objects.all().order_by("athletes").distinct().values("athletes")
        pre_athletes = []
        for row in rows:
            pre_athletes.append(row["athletes"])
            
        # List of each athlete
        athletes = []
        for pre_athlete in pre_athletes:
            for athlete in pre_athlete.split(","):
                # Store the name of each athlete
                buff = athlete.strip()
                if buff not in athletes:
                    athletes.append(buff)
        athletes.sort()
        
        # Variables of dictionary type to be passed to the template
        context = {"athletes": athletes}
        
        return render(request, "select_athlete.html", context)
    
    def post(self, request):
        """ If request.method == "POST" """
        
        # Get athlete value.
        athlete = self.request.POST.get("athlete")
        
        # Results of selected athlete
        results = SwimmingResult.objects.filter(athletes__contains=athlete).values("sport", "event", "rank", "athletes", "team", "record")
        
        # Variables of dictionary type to be passed to the template
        context = {"results": results}
        
        return render(request, "athlete.html", context)
        
    
class TeamView(TemplateView):
    """ Display the result of team. """
    
    def get(self, request):
        """ If request.method == "GET" """
        
        # List of teams
        rows = SwimmingResult.objects.all().order_by("team").distinct().values("team")
        teams = []
        for row in rows:
            teams.append(row["team"])
        teams.sort()
        
        # Variables of dictionary type to be passed to the template
        context = {"teams": teams}
        
        return render(request, "select_team.html", context)
    
    def post(self, request):
        """ If request.method == "POST" """
        
        # Get team value.
        team = self.request.POST.get("team")
        
        # Query database for team
        rows = SwimmingResult.objects.filter(team=team).values("sport", "event", "rank", "athletes", "record")
        
        # Dictionary array for results
        results = []
        for row in rows:
            results.append({
                "sport": row["sport"],
                "event": row["event"],
                "rank": row["rank"],
                "athletes": row["athletes"],
                "record": row["record"]
            })
            
        # Variables of dictionary type to be passed to the template
        context = {"results": results}
        
        return render(request, "team.html", context)
 