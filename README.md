# CSCI3280
Peer-to-peer voice chat system

Nc channels
The total number of blocks is Ns. Each block consists of Nc samples.
Sampling rate F (blocks per second)
Each sample is M bytes long

PCM Data
| Field | Length | Contents |
| --- | --- | --- |
| ckID | 4 | Chunk ID: RIFF |
| cksize | 4 | Chunk size: 4 + 24 + (8 + M*Nc*Ns + (0 or 1)) |
| WAVEID | 4 | WAVE ID: WAVE |
| ckID | 4 | Chunk ID: fmt  |
| cksize | 4 | Chunk size: 16 |
| wFormatTag | 2 | WAVE_FORMAT_PCM |
| nChannels | 2 | Nc |
| nSamplesPerSec | 4 | F (framerate) |
| nAvgBytesPerSec | 4 | F*M*Nc |
| nBlockAlign | 2 | M*Nc |
| wBitsPerSample | 2 | rounds up to 8*M |
| ckID | 4 | Chunk ID: data |
| cksize | 4 | Chunk size: M*Nc*Ns |
| sampled data | M*Nc*Ns | Nc*Ns channel-interleaved M-byte samples |
| pad byte | 0 or 1 | Padding byte if M*Nc*Ns is odd |

To convert the raw data (bytes) to integers, use int.from_bytes(Field, 'little'). To convert integers to bytes that can be written directly in .wav, use struct.pack('<i', integer).