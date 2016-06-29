class MonkeyPatchMiddleware(object):
    ''' Ensures that our monkey patching only gets called after it is safe to do so.'''

    def process_request(self, request):
        do_monkey_patch()


def do_monkey_patch():
    patch_speaker_profile_form()

    # Remove this function from existence
    global do_monkey_patch
    do_monkey_patch = lambda: None


def patch_speaker_profile_form():
    ''' Replaces textarea widgets with markdown editors. '''
    
    import widgets
    from symposion.speakers.forms import SpeakerForm

    fields = SpeakerForm.base_fields
    fields["biography"].widget = widgets.AceMarkdownEditor()
    fields["experience"].widget = widgets.AceMarkdownEditor()
    fields["accessibility"].widget = widgets.AceMarkdownEditor()
