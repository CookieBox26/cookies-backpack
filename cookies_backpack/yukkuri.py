import os
import subprocess
from datetime import datetime


class Yukkuri:
    def __init__(self, aquestalkplayer, work_dir):
        self.aquestalkplayer = aquestalkplayer
        if not os.path.isfile(aquestalkplayer):
            raise RuntimeError('This class requires AquesTalkPlayer.')
        try:
            from pydub import AudioSegment
        except:
            raise RuntimeError(
                'This class requires pydub. '
                'Install it with `pip install pydub`. '
                'You also need to install ffmpeg separately.'
            )
        self.work_dir = work_dir
        os.makedirs(self.work_dir, exist_ok=True)

    def _path(self, file_name):
        return os.path.join(self.work_dir, file_name)

    def _synthesize(self, li, out_mp3, out_text):
        from pydub import AudioSegment
        tmp_wav = self._path('tmp.wav')
        audio = AudioSegment.silent(duration=1000)
        with open(out_text, mode='w', encoding='utf8', newline='\n') as ofile:
            for s in li:
                subprocess.run([self.aquestalkplayer, '/P', 'まりさ', '/T', s, '/W', tmp_wav])
                audio_ = AudioSegment.from_wav(tmp_wav) + AudioSegment.silent(duration=600)
                seconds = int(audio.duration_seconds)
                seconds_formatted = f'{seconds // 60:02}:{seconds % 60:02}'
                ofile.write(f'[{seconds_formatted}]\n{s}\n')
                audio += audio_
        audio.export(out_mp3, format='mp3', parameters=['-ar', '16000', '-ab', '16k'])
        os.remove(tmp_wav)

    def synthesize(self, in_file, identifier=''):
        li = []
        with open(in_file, mode='r', encoding='utf8') as ifile:
            for line in ifile:
                s = line.strip()
                if s != '':
                    li.append(s)
        if len(li) == 0:
            return
        if identifier == '':
            identifier = datetime.now().strftime('%Y%m%d_%H%M%S')
        out_mp3 = self._path(f'{identifier}.mp3')
        out_text = self._path(f'{identifier}.txt')
        self._synthesize(li, out_mp3, out_text)
        os.startfile(os.path.dirname(out_mp3))
        os.startfile(out_text)
        os.startfile(out_mp3)
        return out_mp3
