# OwlBot🦉🤖

This is the source code of the OWLBot website.
OwlBot is a free HTTP API for English vocabularies' definitions and it is powered by the <a href='https://www.djangoproject.com/'>Django framework</a>.

API URL: `https://owlbot.info/api/v3/dictionary/<word>`


```
curl --header "Authorization: Token <YOUR_TOKEN>" https://owlbot.info/api/v3/dictionary/owl -s | json_pp

{
  "definitions": [
    {
      "type": "noun",
      "definition": "a nocturnal bird of prey with large eyes, a facial disc, a hooked beak, and typically a loud hooting call.",
      "example": "I love reaching out into that absolute silence, when you can hear the owl or the wind.",
      "image_url": "https://media.owlbot.info/dictionary/images/owl.jpg.400x400_q85_box-403,83,960,640_crop_detail.jpg"
    }
  ],
  "word": "owl",
  "pronunciation": "oul"
}
```
Version 3 of the OwlBot API requires Token authentication and you can register for a free token on https://owlbot.info. The response data schema in version 3 of the API is changed, the `pronunciation` field is added and also `image_url` field is included for some definitions.
