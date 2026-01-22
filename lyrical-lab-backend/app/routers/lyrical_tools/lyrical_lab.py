from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import schemas, oauth2, models, database
from app.syllable_counter import SyllableCounter 
from app.lyrics_n_summarization import StressedSyllableAnotator, OpenRouterClient
import logging 
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

@router.post('/save-song', status_code=status.HTTP_201_CREATED)
def save_song(
    data:schemas.NewSong,
    db: Session = Depends(database.get_db),
    current_user: models.Users = Depends(oauth2.get_current_user)
):
    
    new_song = models.Lyrics(user_id=current_user.uid, **data.dict())
    db.add(new_song)
    db.commit()

    response = {'message': "Song saved successfully"}

    return response

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

@router.get('/user-songs', status_code=status.HTTP_200_OK)
def get_user_songs(
    current_user: models.Users = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db) 
):
    
    user_lyrics = db.query(models.Lyrics).filter(
        models.Lyrics.user_id == current_user.uid
    ).all()
    return user_lyrics if user_lyrics else []

@router.get('/user-songs/{song_id}', status_code=status.HTTP_200_OK)
def get_song_by_id(
    song_id: int,
    current_user: models.Users = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db)
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
    current_use: models.Users = Depends(oauth2.get_current_user),
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