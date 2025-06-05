#!/bin/bash

#### SETTINGS

set -u

readonly BASE_DIR_PATH="$(pwd)"
SCRIPT_DIR_PATH="$(dirname $0)"; cd "${SCRIPT_DIR_PATH}"
readonly SCRIPT_DIR_PATH="$(pwd)"; cd "${BASE_DIR_PATH}"
readonly DOCKER_PROD_SERVICE_NAME='prod'
readonly DOCKER_UPDATE_SERVICE_NAME='update'
readonly EMAIL_ADDRESSES='sgardoll@ipsl.fr,laurent.troussellier@ipsl.fr'
readonly EMAIL_SUBJECT_TAG='[ESGVOC BACKEND][UPDATE]'
readonly UPDATE_MARK_FILE_PATH="${SCRIPT_DIR_PATH}/update/mark"

#### FUNCTIONS

function shutdown_test_service
{
  local service_list="$(docker compose ps --services)"
  if [[ "${service_list}" == *"${DOCKER_UPDATE_SERVICE_NAME}"* ]] ; then
     local output="$(docker compose down ${DOCKER_UPDATE_SERVICE_NAME} 2>&1)"
     if [ ${?} -ne 0 ] ; then
       echo -e "error while purging ${DOCKER_UPDATE_SERVICE_NAME} service:\n${output}" >&2
     fi
  fi
}

# $1: email subject
# $2: email body
# $3: recipients (space separated list of emails)
# $4: CCs (comma separated list of emails) or none
function send_clear_email
{
  local email_subject="${1}"
  local email_body="${2}"
  local recipients="${3}"
  local ccs="${4-}"

  if [[ -n "${ccs}" ]]; then
    echo -e "${email_body}" | mail -s "$(echo -e "${email_subject}\n${MIME_TYPE}")" -c "${ccs}" "${recipients}"
  else
    echo -e "${email_body}" | mail -s "$(echo -e "${email_subject}\n${MIME_TYPE}")" "${recipients}"
  fi
  return_code=${?}
  return ${return_code}
}

# $1: email subject
# $2: email body
function send_email
{
  send_clear_email "${EMAIL_SUBJECT_TAG} ${1}" "${2}" "${EMAIL_ADDRESSES}"
}

# $1: message
# $2: email body
function die
{
  local msg="error while ${1}"
  local std_err_msg="$(date): ${msg}"
  echo "${std_err_msg}" >&2
  send_email "${msg}" "${2}"
  shutdown_test_service
  exit 1
}

#### MAIN

if [[ -f "${UPDATE_MARK_FILE_PATH}" ]] ; then
  cd "${SCRIPT_DIR_PATH}"

  echo "starts ${DOCKER_UPDATE_SERVICE_NAME} service"
  output="$(docker compose up -d ${DOCKER_UPDATE_SERVICE_NAME} 2>&1)"
  if [ ${?} -ne 0 ] ; then die "starting ${DOCKER_UPDATE_SERVICE_NAME} service" "${output}" ; fi

  echo "get status of ${DOCKER_UPDATE_SERVICE_NAME} service"
  output="$(docker exec -it ${DOCKER_UPDATE_SERVICE_NAME} sh -c 'esgvoc status' 2>&1)"
  if [ ${?} -ne 0 ] ; then die "requesting status" "${output}" ; fi

  echo "update data of ${DOCKER_UPDATE_SERVICE_NAME} service"
  output="$(docker exec -it ${DOCKER_UPDATE_SERVICE_NAME} sh -c 'esgvoc install' 2>&1)"
  if [ ${?} -ne 0 ] ; then die "updating data of ${DOCKER_UPDATE_SERVICE_NAME} service" "${output}" ; fi

  echo "install test packages in ${DOCKER_UPDATE_SERVICE_NAME} service"
  output="$(docker exec -it ${DOCKER_UPDATE_SERVICE_NAME} sh -c 'pip install pytest httpx' 2>&1)"
  if [ ${?} -ne 0 ] ; then die "installing test packages" "${output}" ; fi

  echo "tests ${DOCKER_UPDATE_SERVICE_NAME} service"
  output="$(docker exec -it ${DOCKER_UPDATE_SERVICE_NAME} sh -c 'pytest tests' 2>&1)"
  if [ ${?} -ne 0 ] ; then die "testing ${DOCKER_UPDATE_SERVICE_NAME} service" "${output}" ; fi

  echo "shutdown ${DOCKER_UPDATE_SERVICE_NAME} service"
  output="$(docker compose down ${DOCKER_UPDATE_SERVICE_NAME} 2>&1)"
  if [ ${?} -ne 0 ] ; then die "deleting ${DOCKER_UPDATE_SERVICE_NAME} service" "${output}" ; fi

  echo "update data of ${DOCKER_PROD_SERVICE_NAME} service"
  output="$(docker exec -it ${DOCKER_PROD_SERVICE_NAME} sh -c 'esgvoc install' 2>&1)"
  if [ ${?} -ne 0 ] ; then die "updating data of ${DOCKER_PROD_SERVICE_NAME} service" "${output}" ; fi

  echo "restarts ${DOCKER_PROD_SERVICE_NAME} service"
  output="$(docker exec -it ${DOCKER_PROD_SERVICE_NAME} sh -c 'kill -HUP 1' 2>&1)" # It is always PID 1 .
  if [ ${?} -ne 0 ] ; then die "restarting ${DOCKER_PROD_SERVICE_NAME} service" "${output}" ; fi

  echo "deletes update mark file"
  output="$(rm ${UPDATE_MARK_FILE_PATH} 2>&1)"
  if [ ${?} -ne 0 ] ; then die "deleting update mark" "${output}" ; fi

else
  echo "nothing to update"

fi

exit 0
