from django import forms

class AceMarkdownEditor(forms.Textarea):

    def render(self, name, value, attrs):
        original = super(AceMarkdownEditor, self).render(name, value, attrs)
        ret = '''
                %s
                <script>
                    window.addEventListener("load", () => {
                        editor = loadEditor("%s");
                    }, 0);
                </script>
        ''' % (original, attrs["id"])

        return ret
