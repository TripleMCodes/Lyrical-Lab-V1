import uuid

from fastapi import status, HTTPException, Depends, APIRouter, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from app import schemas, oauth2, models, database
from app.syllable_counter import SyllableCounter 
from app.lyrics_n_summarization import StressedSyllableAnotator, OpenRouterClient
from datetime import datetime, timedelta
import logging 
import hashlib
logging.basicConfig(level=logging.DEBUG)


router = APIRouter(
    prefix='/api/lyric-tools',
    tags=['lyric-tools']
)

# current_user: schemas.TokenData = Depends(oauth2.get_current_user)

@router.post('/syllabe-counter', status_code=status.HTTP_200_OK)
def count_syllables(
    data: dict,
    db: Session = Depends(database.get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user)
):  
    # print("in the fire")
    # print(data)
    syllable_counter = SyllableCounter()
    results = syllable_counter.count_syllables_in_text(data['message'])

    text = ""

    for line in results:
        text += f'{line[0]} ({str(line[1])}){'\n'}'

    data = {"message": text}
    return data

@router.post("/save-song", status_code=status.HTTP_200_OK)
def save_song(
    data: schemas.NewSong,
    db: Session = Depends(database.get_db),
    current_user: models.Users = Depends(oauth2.get_current_user),
):

    def normalize_lyrics(lyrics):
        return lyrics.replace('\r\n', '\n')
    
    norm_lyrics = normalize_lyrics(data.song_lyrics)
    new_hash = hashlib.sha256(norm_lyrics.encode('utf-8')).hexdigest()
    
    if data.song_id is not None:
        # Update existing song
        song = db.query(models.Lyrics).filter(
            models.Lyrics.song_id == data.song_id,
            models.Lyrics.user_id == current_user.uid
        ).with_for_update().first()
        
        if not song:
            raise HTTPException(status_code=404, detail="Song not found")
        
        if song.lyrics_hash == new_hash:
            # No changes
            return {"message": "No changes"}
        
        # Archive old version
        version_snapshot = models.LyricsVersion(
            lyrics_id=song.song_id,
            version=song.version,
            lyrics=song.song_lyrics,
            lyrics_hash=song.lyrics_hash,
            hash_algo=song.hash_algo,
            note="manual save"
        )
        db.add(version_snapshot)
        
        # Update HEAD
        song.song_lyrics = data.song_lyrics
        song.lyrics_hash = new_hash
        song.version += 1
        song.song_name = data.song_name
        song.song_artist = data.song_artist
        song.song_mood = data.song_mood
        song.song_genre = data.song_genre
        song.song_album = data.song_album
        
        db.commit()
        db.refresh(song)
        return {
            "message": "Song updated successfully",
            "song": {
                "song_id": song.song_id,
                "song_name": song.song_name,
                "song_artist": song.song_artist,
                "song_lyrics": song.song_lyrics,
                "song_genre": song.song_genre,
            },
        }
    
    else:
        # Create new song
        new_song = models.Lyrics(
            user_id=current_user.uid,
            song_name=data.song_name,
            song_artist=data.song_artist,
            song_lyrics=data.song_lyrics,
            song_mood=data.song_mood,
            song_genre=data.song_genre,
            song_album=data.song_album,
            lyrics_hash=new_hash,
            version=1,
            hash_algo="sha256",
            source="web"
        )
        db.add(new_song)
        db.commit()
        db.refresh(new_song)
        return {
            "message": "Song saved successfully",
            "song": {
                "song_id": new_song.song_id,
                "song_name": new_song.song_name,
                "song_artist": new_song.song_artist,
                "song_lyrics": new_song.song_lyrics,
                "song_genre": new_song.song_genre,
            },
        }



@router.delete('/delete-song/{song_id}', status_code=status.HTTP_200_OK)
def delete_song(
    song_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.Users = Depends(oauth2.get_current_user),
):
    song = db.query(models.Lyrics).filter(
        models.Lyrics.song_id == song_id,
        models.Lyrics.user_id == current_user.uid
    ).first()

    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    db.delete(song)
    db.commit()
    return {"message": "Song deleted successfully"}


@router.post('/upload-song', status_code=status.HTTP_200_OK)
def upload_song(
    data: schemas.UploadingSong,
    db: Session = Depends(database.get_db),
    current_user: models.Users = Depends(oauth2.get_current_user),
):
    """
    Upload a song from the desktop client.
    Handles both creation and updates based on song_id or client_uid.
    """

    # print(f"Payload: {data}")

    try:
        def normalize_lyrics(lyrics: str) -> str:
            if not lyrics or not lyrics.strip():
                raise HTTPException(status_code=400, detail="Song lyrics cannot be empty")
            return lyrics.replace('\r\n', '\n').replace('\r', '\n')

        norm_lyrics = normalize_lyrics(data.song_lyrics)
        new_hash = hashlib.sha256(norm_lyrics.encode('utf-8')).hexdigest()

        client_uid = data.client_uid or str(uuid.uuid4())

        if data.song_id is not None:
            # Update existing song
            song = db.query(models.Lyrics).filter(
                models.Lyrics.song_id == data.song_id,
                models.Lyrics.user_id == current_user.uid
            ).with_for_update().first()

            if not song:
                raise HTTPException(status_code=404, detail="Song not found")

            if song.lyrics_hash == new_hash:
                return {"message": "No changes detected", "song": {"song_id": song.song_id}}

            # Archive old version
            version_snapshot = models.LyricsVersion(
                lyrics_id=song.song_id,
                version=song.version,
                lyrics=song.song_lyrics,
                lyrics_hash=song.lyrics_hash,
                hash_algo=song.hash_algo,
                note="desktop upload"
            )
            db.add(version_snapshot)

            # Update HEAD
            song.song_lyrics = norm_lyrics
            song.lyrics_hash = new_hash
            song.version += 1
            song.song_name = data.song_name
            song.song_artist = data.song_artist
            song.song_mood = data.song_mood
            song.song_genre = data.song_genre
            song.song_album = data.song_album
            song.client_uid = client_uid  # Ensure client_uid is set

            db.commit()
            db.refresh(song)
            return {
                "message": "Song updated successfully",
                "song": {
                    "song_id": song.song_id,
                    "song_name": song.song_name,
                    "song_artist": song.song_artist,
                    "song_lyrics": song.song_lyrics,
                    "song_genre": song.song_genre,
                    "user_id": current_user.uid
                },
            }

        else:
            # Create new song or update by client_uid
            existing_song = db.query(models.Lyrics).filter(
                models.Lyrics.user_id == current_user.uid,
                models.Lyrics.client_uid == client_uid
            ).first()

            if existing_song:
                # Update existing by client_uid
                if existing_song.lyrics_hash == new_hash:
                    return {"message": "No changes detected", "song": {"song_id": existing_song.song_id}}

                # Archive old version
                version_snapshot = models.LyricsVersion(
                    lyrics_id=existing_song.song_id,
                    version=existing_song.version,
                    lyrics=existing_song.song_lyrics,
                    lyrics_hash=existing_song.lyrics_hash,
                    hash_algo=existing_song.hash_algo,
                    note="desktop upload"
                )
                db.add(version_snapshot)

                # Update HEAD
                existing_song.song_lyrics = norm_lyrics
                existing_song.lyrics_hash = new_hash
                existing_song.version += 1
                existing_song.song_name = data.song_name
                existing_song.song_artist = data.song_artist
                existing_song.song_mood = data.song_mood
                existing_song.song_genre = data.song_genre
                existing_song.song_album = data.song_album

                db.commit()
                db.refresh(existing_song)
                return {
                    "message": "Song updated successfully",
                    "song": {
                        "song_id": existing_song.song_id,
                        "song_name": existing_song.song_name,
                        "song_artist": existing_song.song_artist,
                        "song_lyrics": existing_song.song_lyrics,
                        "song_genre": existing_song.song_genre,
                        "user_id": current_user.uid,
                    },
                }

            else:
                # Create new song
                new_song = models.Lyrics(
                    user_id=current_user.uid,
                    song_name=data.song_name,
                    song_artist=data.song_artist,
                    song_lyrics=norm_lyrics,
                    song_mood=data.song_mood,
                    song_genre=data.song_genre,
                    song_album=data.song_album,
                    lyrics_hash=new_hash,
                    client_uid=client_uid,
                    version=1,
                    hash_algo="sha256",
                    source="desktop"
                )

                db.add(new_song)
                db.commit()
                db.refresh(new_song)
                return {
                    "message": "Song uploaded successfully",
                    "song": {
                        "song_id": new_song.song_id,
                        "song_name": new_song.song_name,
                        "song_artist": new_song.song_artist,
                        "song_lyrics": new_song.song_lyrics,
                        "song_genre": new_song.song_genre,
                        "user_id": current_user.uid,
                    },
                }

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error uploading song: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

    # return {'message': "Got it"}


    

@router.post('/check-flow')
def check_flow(
    data:dict,
    current_user: models.Users = Depends(oauth2.get_current_user)
):
    stress_syllables = StressedSyllableAnotator(data['message'])
    html = stress_syllables.analyze_flow_on_stressed_syllables()

    res = {"message": html}

    return res

@router.post('/save-draft')
def save_draft(
    data: dict,
    current_user: models.Users = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    user = db.query(models.StateFold).filter(
        models.StateFold.user_id == current_user.uid
    ).first()

    if user:
        for key, value in data.items():
            setattr(user, key, value)
    else:
        user = models.StateFold(user_id=current_user.uid, **data)
        db.add(user)

    db.commit()
    return {'message': "draft saved"}

@router.get('/get-draft')
def get_draft(
    current_user: models.Users = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.StateFold).filter(
        models.StateFold.user_id == current_user.uid
    ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Draft not found")

    draft_data = {column.name: getattr(user, column.name) for column in user.__table__.columns if column.name != "id" and column.name != "user_id"}
    print(draft_data)

    return draft_data


@router.get("/user-songs", status_code=status.HTTP_200_OK)
def get_user_songs(
    current_user: models.Users = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
    page: int = Query(1, ge=1),
    size: int = Query(4, ge=1, le=100),
):
    base_q = (
        db.query(models.Lyrics)
        .filter(models.Lyrics.user_id == current_user.uid)
        .order_by(models.Lyrics.song_id.desc())
    )

    total = db.query(func.count(models.Lyrics.song_id))\
              .filter(models.Lyrics.user_id == current_user.uid)\
              .scalar() or 0

    items = (
        base_q
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    pages = (total + size - 1) // size if size else 1

    return {
    "debug": "PAGINATED_ROUTE_V1",
    "items": items,
    "total": total,
    "page": page,
    "size": size,
    "pages": pages,
    "next_page": page + 1 if page < pages else None,
    "prev_page": page - 1 if page > 1 else None,
}

@router.get('/get-uploaded-songs', status_code=status.HTTP_200_OK)
def get_uploaded_songs(
    current_user: models.Users = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    songs = db.query(models.Lyrics).filter(models.Lyrics.user_id == current_user.uid).order_by(models.Lyrics.song_id.desc()).all()

    return {
        "message": "Uploaded songs",
        "songs": songs
    }
@router.get('/user-songs/{song_id}', status_code=status.HTTP_200_OK)
def get_song_by_id(
    song_id: int,
    current_user: models.Users = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):

    
    song = db.query(models.Lyrics).filter(
        models.Lyrics.song_id == song_id,
        models.Lyrics.user_id == current_user.uid
    ).first()
    
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found"
        )
    
    return song

@router.post("/generate")
def generate_mode_content(
    data: dict,
    current_user: models.Users = Depends(oauth2.get_current_user),
    db:Session = Depends(database.get_db)
):
    # ai = OpenRouterClient()
    logging.debug(f'Data: {data}')
    try:
        if data["mode"] == "gen-fos":
            # data = ai.cliches_phrase_quotes(data["content"], data["fos"])
            data = {"message": "It may not be clear\nBut fear not, I am here!"} # for testing
        elif data["mode"] == "gen-lyrics":
            # data = ai.generate_lyrics(data["content"], data["genre"])
            data = {"message": "To be or not to be that is the question\nViolence is the answer"} # for testing
    except Exception as e:
        logging.debug(e)
        data ={"message": "An error occurred, please try again."}
        return data
    
    # data = {"message": "Fear not for I am here!"}
    return data


@router.get('/get-notes', status_code=status.HTTP_200_OK)
def get_notes(
    current_user: models.Users = Depends(oauth2.get_current_user),db: Session = Depends(database.get_db)
):

    notes = (
        db.query(models.Scratchpad)
        .filter(models.Scratchpad.user_id == current_user.uid)
        .all()
    )
    print(notes)

    if notes is None:
        return {}
    
    return notes


@router.post("/save-note", status_code=status.HTTP_200_OK)
def save_note(
    data: dict,
    current_user: models.Users = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    note_text = (data.get("note") or "").strip()
    note_id = data.get("id")

    if not note_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide a non-empty note.",
        )

    # Update existing note
    if note_id:
        note_obj = (
            db.query(models.Scratchpad)
            .filter(
                models.Scratchpad.id == note_id,
                models.Scratchpad.user_id == current_user.uid,
            )
            .first()
        )

        if not note_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found.",
            )

        note_obj.note = note_text
        db.commit()
        db.refresh(note_obj)

        return {"message": "Note updated successfully.", "note_obj": note_obj}

    # Create new note
    new_note = models.Scratchpad(user_id=current_user.uid, note=note_text)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return {"message": "Note saved successfully.", "note_obj": new_note}

@router.delete("/notes/{note_id}", status_code=status.HTTP_200_OK)
def delete_note(
    note_id: int,
    current_user: models.Users = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    note_obj = (
        db.query(models.Scratchpad)
        .filter(
            models.Scratchpad.id == note_id,
            models.Scratchpad.user_id == current_user.uid,
        )
        .first()
    )

    if not note_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found.",
        )

    db.delete(note_obj)
    db.commit()

    return {"message": "Note successfully deleted.", "id": note_id}


@router.post('/save-writing-seconds', status_code=status.HTTP_200_OK)
def save_writing_seconds(
    data: dict,
    db: Session = Depends(database.get_db),
    current_user: models.Users = Depends(oauth2.get_current_user),
):
    """Save a writing session in seconds. Adds the seconds to today's
    `total_writing_time`. If no stats row exists for today, create one and
    set `writing_sessions` to 0 per spec.
    """
    try:
        secs = int(data.get('secs', 0))
        print(f'The seconds are {secs}')
        print(f'The data is {data}')
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid secs value")

    if secs <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="secs must be > 0")

    now = datetime.utcnow()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)

    stat = (
        db.query(models.Stats)
        .filter(
            models.Stats.user_id == current_user.uid,
            models.Stats.date_created >= start,
            models.Stats.date_created < end,
        )
        .first()
    )

    if stat:
        stat.total_writing_time = (stat.total_writing_time or 0) + secs
        # If writing_sessions isn't present, follow spec and set to zero.
        if stat.writing_sessions is None:
            stat.writing_sessions = 0
        # Count this stop as a session
        # stat.writing_sessions = stat.writing_sessions + 1
    else:
        stat = models.Stats(user_id=current_user.uid, total_writing_time=secs, writing_sessions=0, date_created=now.date())
        db.add(stat)

    db.commit()
    db.refresh(stat)

    return {"message": "saved", "stats": {"total_writing_time": stat.total_writing_time, "writing_sessions": stat.writing_sessions}}


@router.post('/increment-session')
def save_session(
    data: dict,
    db: Session = Depends(database.get_db),
    current_user: models.Users = Depends(oauth2.get_current_user),
):
    try:
        secs = int(data.get('sess', 0))
        print(f'The seconds are {secs}')
        print(f'The data is {data}')
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid session value")

    if secs <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="session must be > 0")


    now = datetime.utcnow()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)

    stat = (
        db.query(models.Stats)
        .filter(
            models.Stats.user_id == current_user.uid,
            models.Stats.date_created >= start,
            models.Stats.date_created < end,
        )
        .first()
    )

    if stat:
        stat.writing_sessions = (stat.writing_sessions or 0) + 1
    else:
        stat = models.Stats(user_id=current_user.uid, total_writing_time=0, writing_sessions=1, date_created=now.date())
        db.add(stat)

    db.commit()
    db.refresh(stat)

    return {"message": "saved", "stats": {"total_writing_time": stat.total_writing_time, "writing_sessions": stat.writing_sessions}}

@router.get('/songs-library/{song_id}/versions', status_code=status.HTTP_200_OK)
def get_song_versions(
    song_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.Users = Depends(oauth2.get_current_user),
):
    song = db.query(models.Lyrics).filter(
        models.Lyrics.song_id == song_id,
        models.Lyrics.user_id == current_user.uid
    ).first()

    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    versions = db.query(models.LyricsVersion).filter(
        models.LyricsVersion.lyrics_id == song_id
    ).all()

    return {
        "message": "Song versions retrieved successfully",
        "song": {
            "song_id": song.song_id,
            "song_name": song.song_name,
            "song_artist": song.song_artist,
            "song_lyrics": song.song_lyrics,
            "song_genre": song.song_genre,
            "song_mood": song.song_mood,
            "song_album": song.song_album,
            "version": song.version
        },
        "versions": [
            {
                "version": version.version,
                "lyrics": version.lyrics,
                "lyrics_hash": version.lyrics_hash,
                "hash_algo": version.hash_algo,
                "note": version.note
            }
            for version in versions
        ]
    }