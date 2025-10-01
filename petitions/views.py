from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Petition, Vote

def index(request):
    petitions = Petition.objects.all().order_by('-created_at')
    template_data = {}
    template_data['title'] = 'Movie Petitions'
    template_data['petitions'] = petitions
    return render(request, 'petitions/index.html', {'template_data': template_data})

@login_required
def create(request):
    template_data = {}
    template_data['title'] = 'Create Movie Petition'
    
    if request.method == 'GET':
        return render(request, 'petitions/create.html', {'template_data': template_data})
    
    elif request.method == 'POST':
        movie_title = request.POST.get('movie_title', '').strip()
        description = request.POST.get('description', '').strip()
        
        if movie_title and description:
            petition = Petition()
            petition.movie_title = movie_title
            petition.description = description
            petition.created_by = request.user
            petition.save()
            
            messages.success(request, f'Petition for "{movie_title}" has been created successfully!')
            return redirect('petitions.index')
        else:
            template_data['error'] = 'Both movie title and description are required.'
            template_data['movie_title'] = movie_title
            template_data['description'] = description
            return render(request, 'petitions/create.html', {'template_data': template_data})

def show(request, id):
    petition = get_object_or_404(Petition, id=id)
    template_data = {}
    template_data['title'] = f'Petition: {petition.movie_title}'
    template_data['petition'] = petition
    template_data['yes_votes'] = petition.get_yes_votes()
    template_data['no_votes'] = petition.get_no_votes()
    
    if request.user.is_authenticated:
        template_data['user_vote'] = petition.get_user_vote(request.user)
        template_data['has_voted'] = petition.has_user_voted(request.user)
    
    return render(request, 'petitions/show.html', {'template_data': template_data})

@login_required
def vote(request, id):
    petition = get_object_or_404(Petition, id=id)
    
    if request.method == 'POST':
        vote_type = request.POST.get('vote_type')
        
        if vote_type in ['yes', 'no']:
            # Check if user has already voted
            existing_vote = petition.get_user_vote(request.user)
            
            if existing_vote:
                # Update existing vote
                existing_vote.vote_type = vote_type
                existing_vote.save()
                messages.success(request, f'Your vote has been updated to "{vote_type.upper()}"!')
            else:
                # Create new vote
                vote_obj = Vote()
                vote_obj.petition = petition
                vote_obj.user = request.user
                vote_obj.vote_type = vote_type
                vote_obj.save()
                messages.success(request, f'Your "{vote_type.upper()}" vote has been recorded!')
        else:
            messages.error(request, 'Invalid vote type.')
    
    return redirect('petitions.show', id=id)

@login_required
def delete(request, id):
    petition = get_object_or_404(Petition, id=id)
    
    # Only allow the creator to delete their own petition
    if petition.created_by != request.user:
        messages.error(request, 'You can only delete your own petitions.')
        return redirect('petitions.show', id=id)
    
    if request.method == 'POST':
        movie_title = petition.movie_title
        petition.delete()
        messages.success(request, f'Petition for "{movie_title}" has been deleted successfully.')
        return redirect('petitions.index')
    
    # If GET request, show confirmation page
    template_data = {}
    template_data['title'] = f'Delete Petition: {petition.movie_title}'
    template_data['petition'] = petition
    return render(request, 'petitions/delete.html', {'template_data': template_data})
