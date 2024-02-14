curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

nvm -v
nvm install 20.9.0

ln -s "$NVM_DIR/versions/node/v20.9.0/bin/node" "/usr/local/bin/node"
ln -s "$NVM_DIR/versions/node/v20.9.0/bin/npm" "/usr/local/bin/npm"
ln -s "$NVM_DIR/versions/node/v20.9.0/bin/npx" "/usr/local/bin/npx"