#!/usr/bin/env python

import sys, os
import glob
from jinja2 import Template

def main():

    timestep = 160
    ice_timestep = timestep
    ocn_timestep = timestep
    atm_timestep = timestep
    ice_ocn_coupling_timestep = timestep
    atm_ice_coupling_timestep = 21600

    runtime_in_seconds = 864000
    runtime_in_months = 0
    runtime_in_days = runtime_in_seconds // 86400
    runtime_in_ice_timesteps = runtime_in_seconds // ice_timestep

    for config in glob.glob('01deg/templates/*'):
        print(config)
        with open(config, 'r') as f:
            template = Template(f.read())
            s = template.render(ice_timestep=ice_timestep,
                                ocn_timestep=ocn_timestep,
                                atm_timestep=atm_timestep,
                                runtime_in_seconds=runtime_in_seconds,
                                runtime_in_months=runtime_in_months,
                                runtime_in_days=runtime_in_days,
                                runtime_in_ice_timesteps=runtime_in_ice_timesteps,
                                ice_ocn_coupling_timestep=ice_ocn_coupling_timestep,
                                atm_ice_coupling_timestep=atm_ice_coupling_timestep)

            fname = os.path.basename(config)
            with open(os.path.join('01deg', fname), 'w') as of:
                of.write(s)

if __name__ == '__main__':
    sys.exit(main())
