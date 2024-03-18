from video_generator import FPS
class SecondValidation:
    def __init__(self):
        self.maxVote = int(FPS*5) ## just vote for 5 seconds
        self.votes = [] ## variable with set property
        self.confScore = 0.6
        self.majorAccidents = ["Fall", "Holdingchest", "Hand Up"]
         
    def majorityCounting(self):
        validatedAccidents = []
        totalVotes = [] ## at most 3*maxVote votes in here
        for vote in self.votes:
            for accident in vote:
                totalVotes.append(accident)        
        for accident in self.majorAccidents:
            if totalVotes.count(accident)/self.maxVote >= self.confScore:
                validatedAccidents.append(accident)
        self.reset()
        return validatedAccidents

    def voting(self, vote):
        self.votes.append(list(vote))

    def reset(self):
        self.votes = []

# x = SecondValidation()
# x.voting({"Fall"})
# x.voting({"Fall"})

# x.voting({"Hand Up"})
# x.voting({"Hand Up"})
# x.voting({"Hand Up"})
# print(x.majorityCounting())
