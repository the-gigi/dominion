set -euo pipefail

USER=$1

openssl genrsa -out "${USER}.key" 2048
openssl req -new -key "${USER}.key" -out ${USER}.csr -subj "/CN=${USER}/O=dominion"

CA_LOCATION=~/.minikube
openssl x509 -req -in "${USER}.csr" -CA ${CA_LOCATION}/ca.crt \
         -CAkey "${CA_LOCATION}/ca.key" -CAcreateserial \
         -out ${USER}.crt -days 5000


kubectl config use-context dominion
kubectl config set-credentials ${USER} --client-certificate=${USER}.crt  --client-key=${USER}.key
kubectl config set-context dominion-${USER} --cluster=dominion --namespace=default --user=${USER}

