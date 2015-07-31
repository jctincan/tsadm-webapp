#!/bin/bash
time ansible-playbook -e @config.json -i hosts -c local -v $@ main.yml
