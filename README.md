# geo2sat #

Small flask app which will perform a search on an entered address, 
interfacing with Google geocode API to retrieve a longitude and latitude,
which will then be passed to NASA's Landsat 8 API to retrieve a satellite
image of the given address.

API keys required, to be stored in apikeys.yaml as follows

```
apikeys:
    google: insertkeyhere
    nasa: insertkeyhere
```
