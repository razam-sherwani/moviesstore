from django.db import models
from django.contrib.auth.models import User

class Petition(models.Model):
    id = models.AutoField(primary_key=True)
    movie_title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.movie_title} - Requested by {self.created_by.username}"
    
    def get_yes_votes(self):
        return self.vote_set.filter(vote_type='yes').count()
    
    def get_no_votes(self):
        return self.vote_set.filter(vote_type='no').count()
    
    def has_user_voted(self, user):
        if not user.is_authenticated:
            return False
        return self.vote_set.filter(user=user).exists()
    
    def get_user_vote(self, user):
        if not user.is_authenticated:
            return None
        try:
            return self.vote_set.get(user=user)
        except Vote.DoesNotExist:
            return None

class Vote(models.Model):
    VOTE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    id = models.AutoField(primary_key=True)
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=3, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('petition', 'user')  # Ensures one vote per user per petition
    
    def __str__(self):
        return f"{self.user.username} voted {self.vote_type} on {self.petition.movie_title}"
