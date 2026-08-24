#!/bin/bash
set -e

BACKUP_DIR="/tmp/hermes_backup_repo"
HERMES_DIR="/data/.hermes"
WORKSPACE_DIR="/data/workspace"
LOCAL_BACKUP_DIR="/data/backups"

# توکن گیت‌هاب
GITHUB_TOKEN="${GITHUB_PAT:-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}"
REPO_URL="https://${GITHUB_TOKEN}@github.com/junsina5999/hermesBackup.git"

echo "=== شروع فرآیند بکاپ Hermes ==="
date -u

# 1. بکاپ لوکال آرشیو فشرده
mkdir -p "$LOCAL_BACKUP_DIR"
TIMESTAMP=$(date -u '+%Y%m%d_%H%M%S')
ARCHIVE_PATH="$LOCAL_BACKUP_DIR/hermes_backup_${TIMESTAMP}.tar.gz"

echo "در حال ایجاد بکاپ محلی فشرده..."
tar -czf "$ARCHIVE_PATH" \
  -C /data \
  --exclude='.hermes/cache' \
  --exclude='.hermes/audio_cache' \
  --exclude='.hermes/image_cache' \
  --exclude='.hermes/logs' \
  --exclude='.hermes/*.pid' \
  --exclude='.hermes/*.lock' \
  --exclude='workspace/.git' \
  --exclude='workspace/**/__pycache__' \
  --exclude='backups' \
  .hermes workspace 2>/dev/null || true

echo "بکاپ محلی با موفقیت ایجاد شد: $ARCHIVE_PATH"

# فقط ۳ بکاپ آخر لوکال نگه‌داری شود
ls -1t "$LOCAL_BACKUP_DIR"/hermes_backup_*.tar.gz | tail -n +4 | xargs -r rm -f

# 2. آپلود روی گیت‌هاب
echo "در حال تلاش برای اتصال و آپلود روی GitHub..."
rm -rf "$BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

if git clone --depth 1 "$REPO_URL" "$BACKUP_DIR"; then
  cd "$BACKUP_DIR"
  git config user.name "Hermes Backup Bot"
  git config user.email "bot@hermes-agent.local"

  rm -rf "$BACKUP_DIR/hermes_data" "$BACKUP_DIR/workspace_data"
  mkdir -p "$BACKUP_DIR/hermes_data" "$BACKUP_DIR/workspace_data"

  # کپی اطلاعات هرمس بدون فایل‌های حاوی کلید حساس
  tar -C "$HERMES_DIR" \
    --exclude='cache' \
    --exclude='audio_cache' \
    --exclude='image_cache' \
    --exclude='logs' \
    --exclude='*.pid' \
    --exclude='*.lock' \
    --exclude='.env' \
    --exclude='auth.json' \
    --exclude='state.db' \
    --exclude='kanban.db' \
    -cf - . | tar -C "$BACKUP_DIR/hermes_data" -xf -

  if [ -d "$WORKSPACE_DIR" ]; then
    tar -C "$WORKSPACE_DIR" \
      --exclude='.git' \
      --exclude='__pycache__' \
      --exclude='node_modules' \
      -cf - . | tar -C "$BACKUP_DIR/workspace_data" -xf -
  fi

  git add -A
  if git diff --staged --quiet; then
    echo "تغییر جدیدی برای کامیت گیت‌هاب وجود ندارد."
  else
    git commit -m "Auto Backup: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    if git push origin main; then
      echo "بکاپ با موفقیت روی گیت‌هاب Push شد! 🎉"
    else
      echo "خطا در Push به گیت‌هاب."
      exit 1
    fi
  fi
  rm -rf "$BACKUP_DIR"
else
  echo "خطا در اتصال به گیت‌هاب."
  exit 1
fi

echo "=== پایان عملیات بکاپ با موفقیت ==="
