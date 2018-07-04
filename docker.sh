#!/usr/bin/env bash

. docker.config

subcommand=$1; shift
case "$subcommand" in
    start)
        # arguments:
        # -d: detached
        docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} stop && \
        docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} build && \
        docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} up $@
    ;;
    stop)
        docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} stop
    ;;
    exec)
        docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} exec $@
    ;;
    ssh)
        docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} exec $1 bash
    ;;
    remove)
        # arguments:
        # -v: remove volume
        docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} down $@
    ;;
esac
