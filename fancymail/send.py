from django.conf import settings
from django.template.loader import render_to_string
from fancymail.emailrelated import EmailMessageRelated

ATTACH_RELATED = getattr(settings, 'FANCY_ATTACH_RELATED', [])
DEFAULT_CTX = getattr(settings, 'FANCY_DEFAULT_CTX', {})

def send_fancy_mail(subject, template, ctx, recipients=None, cc=None,
                    from_email=settings.DEFAULT_FROM_EMAIL, reply_to=None, 
                    attachments=None, attach_related=None,
                    fail_silently=False, connection=None):
    
    render_ctx = DEFAULT_CTX.copy()
    render_ctx.update(ctx)
    html = render_to_string(template, render_ctx)

    recipients = recipients or [ m[1] for m in settings.MANAGERS ]
    
    headers = {}
    if reply_to:
        headers = { 'Reply-To': reply_to }
    
    msg = EmailMessageRelated(subject, html, from_email, recipients, cc=cc, headers=headers, connection=connection)

    if attachments:
        for att in attachments:
            if not isinstance(att, (list, tuple)):
                att = [att]
            msg.attach(*att)
        
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
        print(u'Email: %s %s %s - sent: %s' % (subject, template, recipients, sent))
    return sent

