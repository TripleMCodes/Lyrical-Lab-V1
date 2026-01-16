from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import schemas, oauth2, models, database
from app.syllable_counter import SyllableCounter 
from app.lyrics_n_summarization import StressedSyllableAnotator


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