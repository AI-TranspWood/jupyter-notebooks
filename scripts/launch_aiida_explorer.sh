#!/usr/bin/env bash

# module --force purge
# source /cvmfs/software.eessi.io/versions/2023.06/init/bash

# module load aiida-core/2.7.2-foss-2023a

# verdi restapi $@ &

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export REST_API_PORT=5000
$SCRIPT_DIR/launch_restapi.sh --port ${REST_API_PORT} &
REST_API_PID=$!

# Install NVM if not present
export NVM_DIR="$HOME/.nvm"
if [ -d "$NVM_DIR" ]; then
    echo "NVM is already installed."
else
    echo "Installing NVM..."
    wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
fi
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm

# Ensure node v24 is being used and also reload npm from nvm to avoid using older one from EESSI
nvm deactivate
nvm install 24
nvm use 24

EXPLORER_DIR="$SCRIPT_DIR/../aiida-explorer"
if [ ! -d "$EXPLORER_DIR" ]; then
    git clone https://github.com/aiidateam/aiida-explorer.git ${EXPLORER_DIR}
    cd ${EXPLORER_DIR}
    # Use known working commit
    git checkout 2c3d664
    # Use "./" as a base in production to avoid issues with the base path when served 
    # through jupyter-server-proxy.
    # Without (eg in dev mode) the root url iss http://localhost:JLAB_PORT/proxy/VITE_PORT/
    # which then looks for assets at http://localhost:JLAB_PORT/
    sed -i 's:process.env.VITE_BASE_PATH || "/":"./":g' vite.config.js
    npm install
    npm run build
else
    cd ${EXPLORER_DIR}
fi

# npm run dev -- --host--port 1111
npm run preview -- $@ &
EXPLORER_PID=$!

function cleanup {
    echo "Cleaning up..."
    # Ensure we kill the REST API process when the script exits
    kill $REST_API_PID
    # Ensure we kill the Explorer process when the script exits
    kill $EXPLORER_PID
}

trap cleanup EXIT

# Keep the script running to maintain the processes
wait $REST_API_PID
