#!/bin/bash
source pushbullet-sms-config.sh

get_me() {
  curl --silent \
    --header "Access-Token: $ACCESS_TOKEN" \
    https://api.pushbullet.com/v2/users/me | jq '{name,iden}'
}

list_devices() {
  curl --silent \
    --header "Access-Token: $ACCESS_TOKEN" \
    https://api.pushbullet.com/v2/devices | jq '.devices[] | select(.active?) | select(.nickname?) | {nickname, iden}'
}

send_sms() {
  echo "Sending '$2' to '$1'..."
  curl --silent \
    --header "Access-Token: $ACCESS_TOKEN" \
    --header 'Content-Type: application/json' \
    --data-binary "{\"push\":{\"type\":\"messaging_extension_reply\",\"package_name\":\"com.pushbullet.android\",\"source_user_iden\":\"$USER\",\"target_device_iden\":\"$DEVICE\",\"conversation_iden\":\"$1\",\"message\":\"$2\"},\"type\":\"push\"}" \
    --request POST \
    https://api.pushbullet.com/v2/ephemerals
  echo
}

if [ ! -x /usr/bin/jq ]; then
  echo "Command 'jq' not found. Install it:"
  echo "  sudo apt install jq"
  exit 1
fi

# get_me
# list_devices

if [ $# -ne 2 ]; then
  echo "Example usage:"
  echo "  $0 \"+420777123456\" \"Hello buddy!\""
  exit 1
fi

send_sms "$1" "$2"
