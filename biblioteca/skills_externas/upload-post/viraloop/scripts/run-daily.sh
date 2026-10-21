#!/bin/bash
# Wrapper que carga credenciales y ejecuta viraloop diario
# Usado por el cron job para tener las variables de entorno correctas

set -e

SKILL_DIR="$(dirname "$0")/.."
cd "$SKILL_DIR"

# Load credentials from an env file. Point VIRALOOP_ENV_FILE at yours; it
# defaults to .env.local next to the skill.
#
# `set -a; . file` rather than `export $(grep ... | xargs)`: xargs word-splits,
# so a value containing spaces or quotes would silently become several
# variables — or define ones the file never intended to set.
ENV_FILE="${VIRALOOP_ENV_FILE:-$SKILL_DIR/.env.local}"
if [ -f "$ENV_FILE" ]; then
  set -a
  # shellcheck disable=SC1090
  . "$ENV_FILE"
  set +a
fi

: "${UPLOADPOST_TOKEN:?Error: UPLOADPOST_TOKEN is not set}"
: "${GEMINI_API_KEY:?Error: GEMINI_API_KEY is not set}"
: "${UPLOADPOST_PROFILE:?Error: UPLOADPOST_PROFILE is not set}"

# Report that credentials resolved, never any part of their value — this runs
# under cron and the output lands in a log file.
echo "✅ Credenciales cargadas"
echo "   UPLOADPOST_TOKEN: [set]"
echo "   UPLOADPOST_USER:  $UPLOADPOST_PROFILE"
echo "   GEMINI_API_KEY:   [set]"

# Exportar usuario si no está definido
export UPLOADPOST_USER="$UPLOADPOST_PROFILE"

echo ""
echo "🚀 Ejecutando viraloop..."
