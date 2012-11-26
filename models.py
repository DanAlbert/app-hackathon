from google.appengine.ext import db


class Idea(db.Model):
    name = db.StringProperty("Title of the project if the idea is approved")
    author = db.UserProperty("User that had the idea, or null if anonymous")
    description = db.TextProperty("Long description of the project")
    post_time = db.DateTimeProperty("Post time", auto_now_add=True)


class Project(db.Model):
    name = db.StringProperty("Project title")
    author = db.UserProperty("User that had the idea, or null if anonymous")
    description = db.TextProperty("Long description of the project")
    post_time = db.DateTimeProperty("Idea submission time", auto_now_add=True)
    
    def has_voted(self, user):
        for vote in self.votes:
            if vote.voter == user:
                return True
        return False
    
    def vote(self, user):
        if not self.has_voted(user):
            Vote(project=self, voter=user).put()
    
    def remove_vote(self, user):
        for vote in self.votes:
            if vote.voter == user:
                vote.delete()
                return


class Vote(db.Model):
    project = db.ReferenceProperty(Project, collection_name='votes')
    voter = db.UserProperty()