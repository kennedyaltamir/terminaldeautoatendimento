import os
import wave
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Final
from concurrent.futures import ThreadPoolExecutor

# ============================================================
# CONFIGURAÇÕES TÉCNICAS
# ============================================================
DEFAULT_FS: Final[int] = 44100
TARGET_PEAK: Final[float] = 0.85

@dataclass(frozen=True)
class SoundParams:
    """Parâmetros de síntese desacoplados para facilidade de serialização."""
    freq: float
    duration: float
    sweep: float = 0.0
    noise: float = 0.0
    attack: float = 0.004
    decay: float = 0.06
    harmonics: bool = True

# ============================================================
# MOTOR DE ÁUDIO PROFISSIONAL
# ============================================================
class AudioEngine:
    def __init__(self, sample_rate: int = DEFAULT_FS, target_peak: float = TARGET_PEAK):
        self.fs = sample_rate
        self.target_peak = target_peak

    @staticmethod
    def to_db(linear_val: float) -> float:
        """Converte valor linear para Decibéis (Loudness Relativo)."""
        if linear_val <= 0: return -99.0
        return 20 * np.log10(linear_val)

    def _low_pass(self, audio: np.ndarray, window_ms: float = 0.5) -> np.ndarray:
        """Filtro passa-baixa para suavização espectral (Anti-digital harshness)."""
        window = int(self.fs * (window_ms / 1000))
        if window < 2: return audio
        kernel = np.ones(window) / window
        return np.convolve(audio, kernel, mode="same")

    def generate_tone(self, p: SoundParams) -> np.ndarray:
        """Gera um tom sintético com fase integrada e proteção de clipping."""
        n = int(self.fs * p.duration)
        t = np.arange(n, dtype=np.float64) / self.fs

        # Fase Instantânea (Integral f(t)dt)
        phase = 2 * np.pi * (p.freq * t + 0.5 * p.sweep * t**2)
        audio = np.sin(phase)

        # Síntese Aditiva (Harmônicos) com Ganho Compensado
        if p.harmonics:
            if p.freq * 2 < self.fs * 0.45:
                audio += 0.25 * np.sin(2 * phase)
            if p.freq * 0.5 > 20:
                audio += 0.15 * np.sin(0.5 * phase)

        # Injeção de Ruído
        if p.noise > 0:
            audio += np.random.normal(0, p.noise, n)

        # Filtro de Suavização
        audio = self._low_pass(audio)

        # Envelope AD (Attack-Decay) com proteção de overlap
        total_env_time = p.attack + p.decay
        scale = (p.duration / total_env_time) if total_env_time > p.duration else 1.0
        
        a = int(self.fs * p.attack * scale)
        d = int(self.fs * p.decay * scale)

        env = np.ones(n, dtype=np.float32)
        if a > 0: env[:a] = np.linspace(0, 1, a)
        if d > 0: env[-d:] = np.linspace(1, 0, d)

        # Normalização interna (Headroom de síntese)
        final_audio = audio * env
        peak = np.max(np.abs(final_audio))
        return (final_audio / peak).astype(np.float32) if peak > 0 else final_audio

    def sequence(self, clips: List[np.ndarray], gap_s: float = 0.012) -> np.ndarray:
        """Concatenação eficiente em memória (O(n))."""
        gap = np.zeros(int(self.fs * gap_s), dtype=np.float32)
        parts = []
        for i, clip in enumerate(clips):
            parts.append(clip)
            if i < len(clips) - 1: parts.append(gap)
        return np.concatenate(parts)

    def save_wav(self, path: str, audio: np.ndarray):
        """Pipeline de Masterização: Normalização -> TPDF Dither -> PCM 16-bit."""
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Normalização para o Pico Alvo
        peak = np.max(np.abs(audio))
        if peak > 0:
            audio = (audio / peak) * self.target_peak

        # Dither TPDF (Essencial para manter fidelidade em 16 bits)
        # O ruído triangular remove distorções harmônicas de quantização.
        dither = (np.random.rand(len(audio)) - np.random.rand(len(audio))) / 32768.0
        audio_dithered = audio + dither

        # Conversão PCM com Hard Clipping de segurança
        pcm = np.clip(audio_dithered * 32767, -32768, 32767).astype(np.int16)

        with wave.open(path, "w") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(self.fs)
            f.writeframes(pcm.tobytes())

        rms_val = np.sqrt(np.mean(audio**2))
        print(f"✔ {os.path.basename(path):<20} | Peak: {self.target_peak:.2f} | RMS: {self.to_db(rms_val):.2f} dB")

# ============================================================
# DESIGN DOS SOUND ASSETS
# ============================================================
def build_library(engine: AudioEngine) -> Dict[str, np.ndarray]:
    return {
        "ui_confirm": engine.sequence([
            engine.generate_tone(SoundParams(880, 0.12, sweep=40)),
            engine.generate_tone(SoundParams(1320, 0.2, sweep=80))
        ]),
        "ui_error": engine.generate_tone(
            SoundParams(380, 0.3, sweep=-120, noise=0.04)
        ),
        "ui_notification": engine.sequence([
            engine.generate_tone(SoundParams(1100, 0.06)),
            engine.generate_tone(SoundParams(1450, 0.1))
        ], gap_s=0.005),
        "game_item": engine.sequence([
            engine.generate_tone(SoundParams(600, 0.1, sweep=300)),
            engine.generate_tone(SoundParams(1200, 0.15, sweep=600))
        ])
    }

# ============================================================
# PIPELINE DE EXECUÇÃO
# ============================================================
def main():
    engine = AudioEngine()
    library = build_library(engine)
    output_dir = "final_assets_v1"

    print(f"--- Iniciando Pipeline de Áudio (FS: {DEFAULT_FS}Hz) ---")
    
    # Processamento paralelo para escrita em disco
    with ThreadPoolExecutor() as executor:
        for name, data in library.items():
            path = os.path.join(output_dir, name, f"{name}.wav")
            executor.submit(engine.save_wav, path, data)

    print(f"\n✅ Assets gerados com sucesso em: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    main()