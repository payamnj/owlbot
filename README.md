# Owlbot

OwlBot is a free online information API. At the moment, the only available database on owlbot is an English dictionary but my aim is to expand it and serve other kinds of information through it.

API URL: `https://owlbot.info/api/v1/dictionary/<word>`

The response is a list of word objects.

```
Sample response for GET /api/v1/dictionary/live

[
    {
        "type": "verb",
        "definition": "remain alive.",
        "example": "\"the doctors said she had only six months to live\""
    },
    {
        "type": "verb",
        "definition": "make one's home in a particular place or with a particular person.",
        "example": "\"I've lived in the East End all my life\""
    },
    {
        "type": "adjective",
        "definition": "not dead or inanimate; living.",
        "example": "\"live animals\""
    },
    {
        "type": "adjective",
        "definition": "relating to a musical performance given in concert, not on a recording.",
        "example": "\"there is traditional live music played most nights\""
    },
    {
        "type": "adjective",
        "definition": "(of a wire or device) connected to a source of electric current.",
        "example": "\"he touched a live rail while working on the track\""
    },
    {
        "type": "adjective",
        "definition": "(of a question or subject) of current or continuing interest and importance.",
        "example": "\"the future organization of Europe has become a live issue\""
    },
    {
        "type": "adverb",
        "definition": "as or at an actual event or performance.",
        "example": "\"the match will be televised live\""
    }
]
```
