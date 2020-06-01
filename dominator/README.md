# Overview

Dominator is a [Kubernetes operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) implemented in Python using [Kopf](https://kopf.readthedocs.io/en/latest/).

It integrates with Dominion and manages a persistent Dominion game by storing game state and players' state in  Kubernetes custom resources.

This approach allows running cloud games without implementing any persistence and/or networking. The game server and the players just read and update YAML files (Kubernetes custom resources) and Kubernetes takes care of the rest. 

Dominator currently runs outside the cluster, but it will be simple to deploy it in-cluster.

# Pre-requisites

Obviously we need a Kubernetes cluster. For development and testing purposes we will use Minikube.

To install Minikube follow the instructions [here](https://kubernetes.io/docs/tasks/tools/install-minikube/).

This will install kubectl too if not installed already.


Let's start a cluster with a named profile `dominion`:

```
$ minikube start -p dominion
😄  [dominion] minikube v1.10.1 on Darwin 10.15.3
✨  Using the hyperkit driver based on existing profile
👍  Starting control plane node dominion in cluster dominion
🔄  Restarting existing hyperkit VM for "dominion" ...
🐳  Preparing Kubernetes v1.18.2 on Docker 19.03.8 ...
🌟  Enabled addons: default-storageclass, storage-provisioner
🏄  Done! kubectl is now configured to use "dominion"
```

# Provisioning users

Players require a user to join a game. You can provision users using the following procedure:

For a player named `gigi` let's start by creating a private key:

```
$ openssl genrsa -out gigi.key 2048
```

Next, we'll create a CSR (certificate sign request) gigi.csr using the private key. In the subject, CN (common name) is the username and O (organization) is going to be `dominion` in this case.for the group):

```
$ openssl req -new -key gigi.key -out gigi.csr -subj "/CN=gigi/O=dominion"
```

Now, we need to locate the certificate authority (CA) for our Kubernetes cluster in order to generate the final certificate. For minikube it is located in ~/.minikube

```
$ CA_LOCATION=~/.minikube
$ openssl x509 -req -in gigi.csr -CA ${CA_LOCATION}/ca.crt \
         -CAkey ${CA_LOCATION}/ca.key -CAcreateserial \
         -out gigi.crt -days 5000 
```

The next step is to add the new user to the cluster configuration and create a context

```
$ kubectl config set-credentials gigi --client-certificate=gigi.crt  --client-key=gigi.key
User "gigi" set.

$ kubectl config set-context dominion-gigi --cluster=minikube --namespace=default --user=gigi
Context "dominion-gigi" created.
```

The new `gigi` user can't do anything yet. We'll give `gigi` permissions to read and update the dominion custom resources later. 

There is now a script in the users sub-directory called create_user.sh that takes a user name and performs all these steps:

```
$ cd users
$ ./create_user.sh gigi
Generating RSA private key, 2048 bit long modulus (2 primes)
...+++++
...........+++++
e is 65537 (0x010001)
Signature ok
subject=CN = gigi, O = dominion
Getting CA Private Key
Switched to context "dominion".
User "gigi" set.
Context "dominion-gigi" created.
```

# CRDs

Dominator has two CRDs (custom resource definitions): Game and Player

The Game's spec just defines the name and how many players should join before the game starts:

```
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: games.dominion.org
spec:
  scope: Namespaced
  group: dominion.org
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                name:
                  type: string
                numPlayers:
                  type: integer
  names:
    kind: Game
    plural: games
    singular: game
```

The Player's spec has a name, playerType (human or one of the supported computer players) and the nthe various actions a player can perform during their turn: `playActionCard`, `buy` and `done`.

```
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: players.dominion.org
spec:
  scope: Namespaced
  group: dominion.org
  versions:
    - name: v1
      served: true
      storage: true
      schema:
          openAPIV3Schema:
            type: object
            properties:
              spec:
                type: object
                properties:
                  name:
                    type: string
                  playerType:
                    type: string
                  playActionCard:
                    type: string
                    default: ""
                  buy:
                    type: string
                    default: ""
                  done:
                    type: boolean
                    default: false
  names:
    kind: Player
    plural: players
    singular: player
```

To apply the CRDs to the cluster make sure you are in the dominator directory and run:

```
$ kubectl config current-ontext dominion
$ kubectl apply -f crds
customresourcedefinition.apiextensions.k8s.io/games.dominion.org created
customresourcedefinition.apiextensions.k8s.io/players.dominion.org created
```

# Custom Resources

At this point we're ready to create custom resources to represent the game and the players. 
Thr custom resource are in the sample-crs sub-directory of dominator. Let's start with the game, which is simply called game-1, and requires just 2 players:

```
apiVersion: dominion.org/v1
kind: Game
metadata:
  name: game-1
spec:
  name: game-1
  numPlayers: 2
```

Let's create the game:

```
$ kubectl apply -f sample-crs/game-1.yaml
game.dominion.org/game-1 created
```

# Usage

# References

https://docs.bitnami.com/tutorials/configure-rbac-in-your-kubernetes-cluster/