# Google Colab transcription

`scripts/colab_media_transcriber.ipynb` is the system's Google-hosted transcription option. It runs `faster-whisper` in a Colab runtime, scans an input folder, and writes resumable text, SRT, VTT, and JSON outputs.

Use it when local transcription would be too slow or the user specifically asks for Google-hosted compute. Before opening or running it:

1. Confirm the user wants a Colab session started and, if required, Drive mounted or files uploaded.
2. Set a small first batch and write results to the user's Drive or a local export folder.
3. Preserve source filenames and a completion marker so reruns skip completed files.

Free Colab capacity, GPU access, and session duration can change. Report the actual runtime availability instead of treating it as guaranteed infrastructure.
