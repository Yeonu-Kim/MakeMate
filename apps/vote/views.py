from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from apps.group.models import Group, MemberState, Idea, Vote
from apps.group.views import State, redirect_by_auth
from .forms import VoteForm

# Create your views here.
@login_required(login_url="common:login")
def vote_create(request, group_id):
    group = Group.objects.get(pk=group_id)
    user = request.user
    state = redirect_by_auth(user, group_id)

    if state == State.WITH_HISTORY:
        try:
            user_state, created = MemberState.objects.get_or_create(user=user,
                                                                    group=group)

            if request.method == "POST":
                form = VoteForm(request.POST, group_id=group.id)
                if form.is_valid():
                    vote = form.save(commit=False)
                    vote.user = user
                    vote.group = group

                    idea_vote1_id = (form.cleaned_data["idea_vote1"].id
                                    if form.cleaned_data["idea_vote1"] else None)
                    idea_vote2_id = (form.cleaned_data["idea_vote2"].id
                                    if form.cleaned_data["idea_vote2"] else None)
                    idea_vote3_id = (form.cleaned_data["idea_vote3"].id
                                    if form.cleaned_data["idea_vote3"] else None)

                    idea_vote1 = Idea.objects.get(id=idea_vote1_id)
                    idea_vote2 = Idea.objects.get(id=idea_vote2_id)
                    idea_vote3 = Idea.objects.get(id=idea_vote3_id)

                    idea_vote1.votes += 1
                    idea_vote2.votes += 1
                    idea_vote3.votes += 1

                    idea_vote1.save()
                    idea_vote2.save()
                    idea_vote3.save()

                    user_state.idea_vote1 = idea_vote1
                    user_state.idea_vote2 = idea_vote2
                    user_state.idea_vote3 = idea_vote3
                    user_state.save()

                    vote.save()
                    messages.success(request, "투표가 성공적으로 저장되었습니다.")
                    return redirect("group:group_detail", group_id=group_id)
            else:
                messages.error(request, "중복 선택은 불가능합니다.")
                form = VoteForm(group_id=group_id)

        except MemberState.DoesNotExist:
            messages.error(request, "MemberState가 존재하지 않습니다.")
            return redirect("group_detail", group_id=group_id)

        voted_ideas = [
            user_state.idea_vote1, user_state.idea_vote2, user_state.idea_vote3
        ]
        ideas_for_voting = (Idea.objects.filter(group=group).exclude(
            author=user).exclude(
                id__in=[idea.id for idea in voted_ideas if idea is not None]))

        return render(
            request,
            "group/group_vote_create.html",
            {
                "group": group,
                "ideas_for_voting": ideas_for_voting,
                "form": form
            },
        )
    elif state == State.ADMIN:
        redirect_url = reverse("group:group_detail", kwargs={"group_id": group_id})
        return redirect(redirect_url)
    else:
        return redirect('/')

@login_required(login_url="common:login")
def vote_modify(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    user = request.user

    vote, _ = Vote.objects.get_or_create(user=user, group=group)
    own_ideas = Idea.objects.filter(group=group, author=user)
    ideas_for_voting = Idea.objects.filter(group=group).exclude(author=user)
    state = redirect_by_auth(user, group_id)

    if state == State.WITH_HISTORY:
        if request.method == "POST":
            form = VoteForm(request.POST, instance=vote, group_id=group.id)
            if form.is_valid():
                vote_instance = form.save(commit=False)

                user_state = MemberState.objects.get(user=user, group=group)
                user_state.idea_vote1 = vote_instance.idea_vote1
                user_state.idea_vote2 = vote_instance.idea_vote2
                user_state.idea_vote3 = vote_instance.idea_vote3
                user_state.save()

                messages.success(request, "투표가 수정되었습니다.")
                return redirect("group:group_detail", group_id=group.id)

        else:
            form = VoteForm(instance=vote, group_id=group.id)

        return render(
            request,
            "group/group_vote_modify.html",
            {
                "form": form,
                "group": group,
                "vote": vote,
                "ideas_for_voting": ideas_for_voting,
            },
        )
    else:
        return redirect("/")

