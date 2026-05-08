## The OGD File API

This API is used to browse information about the datasets provided by OpenGameData, typically via the OGD website.
However, it is possible to navigate the API as a human user.

You may, for example, have previously submitted a game for inclusion on the OpenGameData website.
This game might have an initial dataset, but may not yet have its own page included in the OpenGameData website.
In this case, you can find the link to download your dataset via the API.

### Base Location

The base URL for the File API is the following:  
`https://ogd-services.fielddaylab.wisc.edu/apis/files/latest/app.wsgi`

All API requests you make will be relative to this base URL.