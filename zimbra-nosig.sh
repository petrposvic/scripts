#!/bin/bash -e

SCRIPT_DIR="$(dirname $(readlink -f $0))"
. "$SCRIPT_DIR/zimbra-nosig-config.sh"

# Get ZM_AUTH_TOKEN
HEADERS=`curl -sSL --user "$USERNAME:$PASSWORD" -D - "$SERVER_URL/home/$USERNAME/Inbox/?fmt=sync&auth=sc" -o /dev/null`
PATTERN="Set-Cookie: ZM_AUTH_TOKEN=([^;]+)"
if [[ "$HEADERS" =~ $PATTERN ]]; then
  ZM_AUTH_TOKEN=${BASH_REMATCH[1]}
else
  echo "Can't get ZM_AUTH_TOKEN!"
  exit 1
fi

PAYLOAD="$(cat <<- END
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
  <soap:Header>
    <context xmlns="urn:zimbra">
      <format type="js"/>
    </context>
  </soap:Header>
  <soap:Body>
    <BatchRequest xmlns="urn:zimbra" onerror="stop">
      <ModifyIdentityRequest xmlns="urn:zimbraAccount" requestId="0">
        <identity id="$IDENTITY_ID">
          <a name="zimbraPrefDefaultSignatureId"></a>
          <a name="zimbraPrefForwardReplySignatureId">11111111-1111-1111-1111-111111111111</a>
        </identity>
      </ModifyIdentityRequest>
    </BatchRequest>
  </soap:Body>
</soap:Envelope>
END
)"

curl -X POST -H "Cookie: ZM_AUTH_TOKEN=$ZM_AUTH_TOKEN" "$SERVER_URL/service/soap/BatchRequest" -d "$PAYLOAD"
echo
