from django.core.mail import *
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from emailrelated import EmailMessageRelated

ATTACH_RELATED = getattr(settings, 'FANCY_ATTACH_RELATED', [])

def send_fancy_mail(subject, template, ctx, recipients=None, 
                    from_email=settings.DEFAULT_FROM_EMAIL, reply_to=None, 
                    attach_related=None,
                    fail_silently=False, attachments=[]):
    
    html = render_to_string(template, ctx)

    recipients = recipients or [ m[1] for m in settings.MANAGERS ]
    
    headers = {}
    if reply_to:
        headers = { 'Reply-To': reply_to }
    
    msg = EmailMessageRelated(subject, html, from_email, recipients, headers=headers)

    for att in attachments:
        msg.attach(att)
        
    attach_related = (attach_related or []) + ATTACH_RELATED
    for fn in attach_related:
        try:
            msg.attach_related(fn)
        except IOError:
            if not fail_silently:
                raise

    msg.content_subtype = "html"  
    sent = msg.send(fail_silently=fail_silently)
    if settings.DEBUG:
        print u'Email: %s %s %s - sent: %s' % (subject, template, recipients, sent)
    return sent

