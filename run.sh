#!/usr/bin/env bash
ls -al run.sh
PROJECT_NAME=wordpress
COMPOSE_YML=./docker/wordpress.yml
echo ${PROJECT_NAME}
echo ${COMPOSE_YML}
subcommand=$1; shift
case "$subcommand" in
    start)
        docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} build && docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} up -d
    ;;
    stop)
        docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} stop
    ;;
    ssh)
        docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} exec $1 bash
    ;;
    exec)
        docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} exec $@
    ;;
    down)
        docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} down
    ;;
esac