from classes.Song import Song

# If you want to make your own Song, look at the Song class and which attributes it needs to create one.
# Example below is also usefull in understanding the working of the different attributes of a Song.

# extra songs kan je gwn in de list zetten de bg_game_header word gebruikt als song naam

songs = [
Song(
    'example_notes.txt',            	# notes_filename
    180,                                # notes_bpm which decides the speed of falling notes
    'RobotoMono-VariableFont_wght.ttf', # font_filename in data folder
    None,                               # bg_image_dir, the subdirectory of the data/backgrounds directory
    500,                                # bg_image_interval_ms
    'Interaction Hero',                 # bg_game_header
),
Song(
    'ode_to_joy.txt',
    180,
    'RobotoMono-VariableFont_wght.ttf',
    None,
    400,
    'Oda a la Alegría'
),
Song(
    'megalovania.txt',
    150,
    'RobotoMono-VariableFont_wght.ttf',
    None,
    500,
    'Megalovenia'
),
Song(
    'La_Cucaracha.txt',
    150,
    'RobotoMono-VariableFont_wght.ttf',
    None,
    500,
    'La Cucaracha'
)
]