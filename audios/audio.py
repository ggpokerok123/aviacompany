from pydub import AudioSegment

 
def convert_to_mp3(audio_file):
	audio_file = './audios/' + audio_file
	audio_format = audio_file.split('.')[-1]

	audio_file = AudioSegment.from_file(audio_file, audio_format)
	audio_file.export("./audios/audio.mp3", format = "mp3")

	

