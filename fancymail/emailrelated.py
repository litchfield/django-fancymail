import os
import uuid
from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.mail import *

class EmailMessageRelated(EmailMultiAlternatives):
    """
    Adds attached_related() function to allow adding "related" images to HTML email
    
    Example --

    msg = EmailMessageRelated(...)
    msg.attach_related('img/bla.jpg')  # relative paths are assumed to be relative to STATIC_ROOT
    msg.content_subtype = 'html'
    msg.send()
    """
    #multipart_subtype = 'related'
    mixed_subtype = 'related; type="multipart/alternative"'
    
    def __init__(self, *args, **kwargs):
        super(EmailMessageRelated, self).__init__(*args, **kwargs)
        self.related_ids = {}

    def _get_content_id(self, filename):
        return '%s@%s' % (filename, self.related_ids.get(filename))
        
    def message(self):
        for filename in self.related_ids.keys():
            self.body = self.body.replace(filename, 'cid:' + self._get_content_id(filename))
        return super(EmailMessageRelated, self).message()
        
    def attach_related(self, path, mimetype=None):
        if path[0] != '/':
            # if relative path, use staticfiles to find absolute
            path = finders.find(path)
        super(EmailMessageRelated, self).attach_file(path, mimetype)
        filename = os.path.basename(path)
        self.related_ids[filename] = str(uuid.uuid1())

    def _create_attachment(self, filename, content, mimetype=None):
        attachment = super(EmailMessageRelated, self)._create_attachment(filename, content, mimetype)
        if filename in self.related_ids:
            # change headers to suit
            del(attachment['Content-Disposition'])
            mimetype = attachment['Content-Type']
            del(attachment['Content-Type'])
            attachment.add_header('Content-Type', mimetype, name=filename)
            attachment.add_header('Content-ID', '<%s>' % self._get_content_id(filename))
        return attachment
