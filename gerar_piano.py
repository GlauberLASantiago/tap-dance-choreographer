import math
import wave
import struct
import os

frequencies = {
    'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61, 'G3': 196.00, 'A3': 220.00, 'B3': 246.94,
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23, 'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
    'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99, 'A5': 880.00, 'B5': 987.77,
    'C6': 1046.50
}

def generate_piano_note(filename, frequency, duration=1.5, sample_rate=44100):
    # Additive synthesis: Fundamental + overtones (harmonics)
    harmonics = [1, 2, 3, 4, 5]
    weights = [0.6, 0.25, 0.12, 0.06, 0.03]
    
    num_samples = int(duration * sample_rate)
    data = []
    
    for i in range(num_samples):
        t = i / sample_rate
        # Amplitude envelope: 5ms attack, exponential decay
        if t < 0.005:
            envelope = t / 0.005
        else:
            envelope = math.exp(-2.2 * (t - 0.005))
            
        # Mix harmonics with decaying volume
        val = 0
        for idx, (h, w) in enumerate(zip(harmonics, weights)):
            # Higher overtones decay faster
            h_decay = math.exp(-1.5 * idx * t)
            val += w * h_decay * math.sin(2 * math.pi * frequency * h * t)
            
        sample = val * envelope
        # Clip to avoid distortion
        sample = max(-1.0, min(1.0, sample))
        
        # Convert to 16-bit PCM integer
        data.append(int(sample * 32767))
        
    # Write to WAV
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'w') as f:
        f.setnchannels(1)  # Mono
        f.setsampwidth(2)  # 16-bit
        f.setframerate(sample_rate)
        # Pack short integers into binary data
        for val in data:
            f.writeframesraw(struct.pack('<h', val))

def main():
    print("Generating C Major scale piano notes...")
    for note, freq in frequencies.items():
        filename = f"audio/piano_{note.lower()}.wav"
        print(f"Generating {note} ({freq} Hz) -> {filename}")
        generate_piano_note(filename, freq)
    print("All piano notes generated successfully!")

if __name__ == "__main__":
    main()
