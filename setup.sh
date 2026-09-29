#!/usr/bin/env bash
# Prepara o ambiente da fábrica de vídeo (Linux, ~2 min). Só usa GitHub (clone + release) e pip já instalado.
set -e
D="${1:-$PWD}"; mkdir -p /tmp/fab && cd /tmp/fab
# 1) espeak-ng (fonemas pt-BR) — compila do código-fonte
if [ ! -x /tmp/esinst/bin/espeak-ng ]; then
  GIT_LFS_SKIP_SMUDGE=1 git clone -q --depth 1 https://github.com/espeak-ng/espeak-ng espeak-src
  cmake -S espeak-src -B esb -DCMAKE_BUILD_TYPE=Release -DUSE_ASYNC=OFF -DUSE_MBROLA=OFF -DUSE_LIBSONIC=OFF -DUSE_LIBPCAUDIO=OFF -DUSE_SPEECHPLAYER=OFF -DCMAKE_INSTALL_PREFIX=/tmp/esinst >/dev/null
  cmake --build esb -j8 >/dev/null && cmake --install esb >/dev/null
fi
# 2) modelo Kokoro + vozes (GitHub release)
B=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -f "$D/kokoro-v1.0.onnx" ] || curl -sSL -o "$D/kokoro-v1.0.onnx" $B/kokoro-v1.0.onnx
[ -f "$D/voices-v1.0.bin" ] || curl -sSL -o "$D/voices-v1.0.bin" $B/voices-v1.0.bin
python3 -c "import onnxruntime, numpy, PIL" 2>/dev/null || pip install onnxruntime numpy pillow
echo "export ESPEAK_BIN=/tmp/esinst/bin/espeak-ng ESPEAK_DATA_PATH=/tmp/esinst/share/espeak-ng-data"
