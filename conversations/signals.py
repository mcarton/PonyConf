from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Participation
from proposals.models import Talk
from proposals.signals import talk_added, talk_edited

from .models import ConversationAboutTalk, ConversationWithParticipant, Message


@receiver(post_save, sender=Participation, dispatch_uid="Create ConversationWithParticipant")
def create_conversation_with_participant(sender, instance, created, **kwargs):
    if not created:
        return
    conversation = ConversationWithParticipant(participation=instance)
    conversation.save()


@receiver(post_save, sender=Talk, dispatch_uid="Create ConversationAboutTalk")
def create_conversation_about_talk(sender, instance, created, **kwargs):
    if not created:
        return
    conversation = ConversationAboutTalk(talk=instance)
    conversation.save()


def check_talk(talk):
    reviewers = User.objects.filter(Q(topic__talk=talk) | Q(participation__site=talk.site, participation__orga=True))
    # Subscribe the reviewers to the conversation about the talk
    talk.conversation.subscribers.add(*reviewers)
    # Subscribe the reviewers to the conversations with each speaker
    for user in talk.speakers.all():
        participation, created = Participation.objects.get_or_create(user=user, site=talk.site)
        participation.conversation.subscribers.add(*reviewers)


@receiver(talk_added, dispatch_uid="Notify talk added")
def notify_talk_added(sender, instance, author, **kwargs):
    check_talk(instance)
    message = Message(conversation=instance.conversation, author=author,
                      content='The talk has been proposed.', system=True)
    message.save()


@receiver(talk_edited, dispatch_uid="Notify talk edited")
def notify_talk_edited(sender, instance, author, **kwargs):
    check_talk(instance)
    message = Message(conversation=instance.conversation, author=author,
                      content='The talk has been modified.', system=True)
    message.save()


@receiver(post_save, sender=Message, dispatch_uid="Notify new message")
def notify_new_message(sender, instance, created, **kwargs):
    if not created:
        # Possibly send a modification notification?
        return
    instance.conversation.new_message(instance)
