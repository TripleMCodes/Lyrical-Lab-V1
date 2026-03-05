I am working on creating a version system for this cross domain app.
I was think of keeping simple, and that is by tracking the version of the entire song. We not going to be keeping track the meta data of the, only just the lyrics
Here is my pipeline upon saving a song:

clicks save -> convert lyrics into hash -> add hash to song data -> save song

On update:
convert lyrics into hash -> compare hash to existing hash of the same song -> if they differ 
            move old song into versions
            add song update into lyrics table