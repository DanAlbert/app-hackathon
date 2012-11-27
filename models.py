"""Models used by the app-hackathon application.

Author: Dan Albert <dan@gingerhq.net>
"""
from google.appengine.ext import db


class Idea(db.Model):
    """A project idea."""
    name = db.StringProperty("Title of the project if the idea is approved")
    author = db.UserProperty("User that had the idea, or null if anonymous")
    description = db.TextProperty("Long description of the project")
    post_time = db.DateTimeProperty("Post time", auto_now_add=True)


class Project(db.Model):
    """A project which represents and idea that was approved by a moderator.

    Discussion:
        Should this model be combined with the Idea model? The idea remains the
        same throughout the process.

        Why do we even have a voting process? Why not let developers choose
        from the list of approved ideas?
    """
    name = db.StringProperty("Project title")
    author = db.UserProperty("User that had the idea, or null if anonymous")
    description = db.TextProperty("Long description of the project")
    post_time = db.DateTimeProperty("Idea submission time", auto_now_add=True)

    def has_voted(self, user):
        """Returns true if the given suer has voted for this project."""
        for vote in self.votes:
            if vote.voter == user:
                return True
        return False

    def vote(self, user):
        """Adds the user's vote to this project."""
        if not self.has_voted(user):
            Vote(project=self, voter=user).put()

    def remove_vote(self, user):
        """Removes the user's vote from this project."""
        for vote in self.votes:
            if vote.voter == user:
                vote.delete()
                return


class Vote(db.Model):
    """Represents a single vote for a given idea."""
    project = db.ReferenceProperty(Project, collection_name='votes')
    voter = db.UserProperty()
