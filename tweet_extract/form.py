from django import forms


class TweetInputForm(forms.Form):
    tweet_id = forms.CharField()

    def clean_tweet_id(self):
        id_list = self.cleaned_data['tweet_id'].split()
        no_of_id = len(id_list)
        for id in range(no_of_id):
            if len(id_list[id]) != 18:
                raise forms.ValidationError("Invalid tweet id")
        return id_list, no_of_id


class LoginForm(forms.Form):
    username = forms.CharField(max_length=25, required=True)
    password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput)
