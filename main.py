import cv2

from vision.camera import Camera
from vision.handtracker import HandTracker
from control.mapper import GestureMapper
from control.smoothing import Smoother
from audio.engine import AudioEngine
from collections import deque
from audio.note import freq_to_note
from control.scale import quantize_freq

camera = Camera()
tracker = HandTracker()
mapper = GestureMapper()

freq_smoother = Smoother(alpha=0.15)
vol_smoother = Smoother(alpha=0.2)

audio = AudioEngine()
audio.start()

trail = deque(maxlen=30)

current_scale = "pentatonic"

while True:
    frame = camera.read()
    if frame is None:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pos = tracker.get_index_finger(rgb)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('1'):
        audio.set_waveform("sine")
    elif key == ord('2'):
        audio.set_waveform("square")
    elif key == ord('3'):
        audio.set_waveform("saw")
    elif key == ord('4'):
        audio.set_waveform("triangle")

    if key == ord('q'):
        current_scale = "pentatonic"
    elif key == ord('w'):
        current_scale = "major"
    elif key == ord('e'):
        current_scale = "minor"
    elif key == ord('r'):
        current_scale = "blues"

    if pos:
        x, y = pos
        freq, _ = mapper.position_to_sound(x, y)

        quantized = quantize_freq(freq, scale=current_scale, root=60)
        audio.freq = freq_smoother.update(quantized)
        audio.volume = 0.2

        # ✅ Y axis → vibrato depth
        if y > 0.8:
            audio.vibrato_depth = 0.0
        else:
            audio.vibrato_depth = ((1 - y) ** 2) * 20.0

        h, w, _ = frame.shape
        px = int(x * w)
        py = int(y * h)
        trail.append((px, py))

        cv2.circle(frame, (px, py), 5, (0, 0, 255), -1)
        for i in range(len(trail) - 1):
            cv2.line(frame, trail[i], trail[i + 1], (0, 255, 0), 2)

        note = freq_to_note(audio.freq)

        cv2.putText(
            frame,
            f"{int(audio.freq)} Hz / {str(note)} / Scale: {current_scale}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 0),
            2
        )
    else:
        audio.volume = 0

    cv2.imshow("Visual Theremin", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

audio.stop()
camera.release()
cv2.destroyAllWindows()