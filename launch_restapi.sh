#!/usr/bin/env bash

module --force purge
source /cvmfs/software.eessi.io/versions/2023.06/init/bash

module load aiida-core/2.7.2-foss-2023a

verdi restapi --hostname 0.0.0.0
