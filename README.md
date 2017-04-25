# Owlbot

OwlBot is a free online information API. At the moment it the only available database on owlbot is an English dictionary but my aim is to expand it and serve other kinds of information through it.

API URL: `https://owlbot.info/api/v1/dictionary/<word>`

The response is a list of word objects.

```
Sample response for GET /api/v1/dictionary/live

[
    {
        "type": "verb",
        "defenition": "remain alive.",
        "example": "\"the doctors said she had only six months to live\""
    },
    {
        "type": "verb",
        "defenition": "make one's home in a particular place or with a particular person.",
        "example": "\"I've lived in the East End all my life\""
    },
    {
        "type": "adjective",
        "defenition": "not dead or inanimate; living.",
        "example": "\"live animals\""
    },
    {
        "type": "adjective",
        "defenition": "relating to a musical performance given in concert, not on a recording.",
        "example": "\"there is traditional live music played most nights\""
    },
    {
        "type": "adjective",
        "defenition": "(of a wire or device) connected to a source of electric current.",
        "example": "\"he touched a live rail while working on the track\""
    },
    {
        "type": "adjective",
        "defenition": "(of a question or subject) of current or continuing interest and importance.",
        "example": "\"the future organization of Europe has become a live issue\""
    },
    {
        "type": "adverb",
        "defenition": "as or at an actual event or performance.",
        "example": "\"the match will be televised live\""
    }
]
```
