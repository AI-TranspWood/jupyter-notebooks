#!/usr/bin/env bash


FLASK_PORT_FILE="${HOME}/flask_port.env"
PID_FILE=$HOME/.aiida_restapi.pid
VERSION_FILE=$HOME/.aiida_restapi_version.env
DEFAULT_FLASK_PORT=5000

REQ_VERSION=${1:-2023.06}
if [[ "$REQ_VERSION" == "2023.06" ]]; then
    module --force purge
    ml load EESSI/2023.06
    module load aiida-core/2.7.2-foss-2023a
elif [[ "$REQ_VERSION" == "2025.06" ]]; then
    module --force purge
    ml load EESSI/2025.06
    module load aiida-core/2.9.2-foss-2025b
else
    echo "Unsupported version: $REQ_VERSION"
    exit 1
fi

export AIIDA_PATH=$(realpath $HOME/.aiida_$EBVERSIONAIIDAMINCORE)


if [ -f "${FLASK_PORT_FILE}" ]; then
    FLASK_PORT="$(cat "${FLASK_PORT_FILE}" | tr -d '[:space:]')"
    if [[ -z "${FLASK_PORT}" ]]; then
        echo "Warning: ${FLASK_PORT_FILE} is empty. Using default port 5000."
        FLASK_PORT="${DEFAULT_FLASK_PORT}"
    fi
else
    FLASK_PORT="${DEFAULT_FLASK_PORT}"
fi

function print_url() {
    echo "AiiDA REST API started."
    echo "API URL http://localhost:${FLASK_PORT}/api/v4"
    echo "Explorer URL https://aiidateam.github.io/aiida-explorer/?api_url=http%3A%2F%2F127.0.0.1%3A${FLASK_PORT}%2Fapi%2Fv4"
}

if [ -f "${PID_FILE}" ]; then
    PID=$(cat "${PID_FILE}")
    if ps -p "${PID}" | grep -q ${PID}; then
        if [[ -f "${VERSION_FILE}" ]] && [[ "${EESSI_VERSION}" != "`cat ${VERSION_FILE}`" ]]; then
            echo "Another verion of AiiDA REST API is running. STOPPING IT"
            kill "${PID}"
            echo "Starting the new version of AiiDA REST API..."
        else
            print_url
            exit 1
        fi
    else
        rm "${PID_FILE}"
    fi
fi

# Porrt inside container always 5000, the FLASK_PORT is used to track the mapped port on the host machine.
verdi restapi --hostname 0.0.0.0 --port 5000 > /dev/null 2>&1 &
PID=$!
echo "${PID}" > "${PID_FILE}"
echo "${FLASK_PORT}" > "${FLASK_PORT_FILE}"
echo "${EESSI_VERSION}" > "${VERSION_FILE}"

print_url
