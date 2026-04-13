from machine import I2S, Pin
import rp2
import math
import array


# Default Pico W wiring for Pmod I2S2 DAC side.
# Change pins below to match your actual wiring.
PIN_MCLK = 8
PIN_SDOUT = 9
PIN_BCLK = 10
PIN_LRCLK = 11

I2S_ID = 0
SAMPLE_RATE = 16000
BITS = 16
MCLK_MULT = 256
BUFFER_FRAMES = 512
WAVETABLE_LEN = 1024


@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW)
def _mclk_out():
    # Two PIO instructions per full period.
    nop().side(1)  # type: ignore[name-defined]
    nop().side(0)  # type: ignore[name-defined]


class PmodI2S2TX:
    def __init__(
        self,
        i2s_id=I2S_ID,
        sample_rate=SAMPLE_RATE,
        bits=BITS,
        mclk_mult=MCLK_MULT,
        pin_mclk=PIN_MCLK,
        pin_sdout=PIN_SDOUT,
        pin_bclk=PIN_BCLK,
        pin_lrclk=PIN_LRCLK,
        ibuf=20000,
    ):
        self.sample_rate = sample_rate
        self.bits = bits
        self.mclk_hz = sample_rate * mclk_mult
        self._mclk_sm = None
        self._table_len = WAVETABLE_LEN
        self._table_mask = self._table_len - 1
        self._phase_scale = 1 << 16
        self._sine_table = self._build_sine_table()

        self.audio = I2S(
            i2s_id,
            sck=Pin(pin_bclk),
            ws=Pin(pin_lrclk),
            sd=Pin(pin_sdout),
            mode=I2S.TX,
            bits=bits,
            format=I2S.STEREO,
            rate=sample_rate,
            ibuf=ibuf,
        )

        self._start_mclk(pin_mclk)

    def _build_sine_table(self):
        table = array.array("h", [0] * self._table_len)
        for i in range(self._table_len):
            table[i] = int(32767 * math.sin(2.0 * math.pi * i / self._table_len))
        return table

    def _start_mclk(self, pin_mclk):
        for sm_id in range(8):
            try:
                self._mclk_sm = rp2.StateMachine(
                    sm_id,
                    _mclk_out,
                    freq=self.mclk_hz * 2,
                    sideset_base=Pin(pin_mclk),
                )
                self._mclk_sm.active(1)
                print("MCLK:", self.mclk_hz, "Hz on GP", pin_mclk, "SM", sm_id)
                return
            except ValueError:
                self._mclk_sm = None

        raise RuntimeError("No free PIO StateMachine for MCLK")

    def _fill_tone_buffer(self, buf, amplitude, phase_fp, step_fp):
        for i in range(len(buf) // 2):
            idx = (phase_fp >> 16) & self._table_mask
            sample = (self._sine_table[idx] * amplitude) >> 15
            # Interleave left/right samples for stereo.
            buf[2 * i] = sample
            buf[2 * i + 1] = sample
            phase_fp += step_fp
        return phase_fp

    def play_tone(self, freq_hz=440, seconds=2.0, amplitude=10000, frames=BUFFER_FRAMES):
        freq_hz = max(1, int(freq_hz))
        amplitude = max(0, min(32767, int(amplitude)))
        total_frames = max(1, int(seconds * self.sample_rate))
        buf = array.array("h", [0] * (frames * 2))
        step_fp = int((freq_hz * self._table_len * self._phase_scale) / self.sample_rate)
        phase_fp = 0
        sent = 0

        while sent < total_frames:
            phase_fp = self._fill_tone_buffer(buf, amplitude, phase_fp, step_fp)
            self.audio.write(buf)
            sent += frames

    def deinit(self):
        try:
            self.audio.deinit()
        finally:
            if self._mclk_sm is not None:
                self._mclk_sm.active(0)


def main():
    tx = PmodI2S2TX()
    try:
        # Quick audible test sequence.
        tx.play_tone(220, 1.5, amplitude=7000)
        tx.play_tone(440, 1.5, amplitude=7000)
        tx.play_tone(523, 1.5, amplitude=7000)
    finally:
        tx.deinit()


if __name__ == "__main__":
    main()