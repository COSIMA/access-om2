#!/usr/bin/env python

import os, sys
import re
import stat
import shutil
import argparse
import subprocess as sp
import glob
import datetime as dt
import calendar
import netCDF4 as nc
from jinja2 import Template

exp_defs = {'1deg_corenyf' : {'ocn_pes' : 240, 'ice_pes' : 24, 'atm_pes' : 1,
                               'res' : '360x300', 'timestep' : 3600,
                               'cpl_timestep' : 21600, 'atm_grid' : 'nt62'},
            '1deg_jra55' : {'ocn_pes' : 240, 'ice_pes' : 24, 'atm_pes' : 16,
                            'res' : '360x300', 'timestep' : 3600,
                            'cpl_timestep' : 10800, 'atm_grid' : 'jra55'},
            '01deg_corenyf' : {'ocn_pes' : 3600, 'ice_pes' : 900, 'atm_pes' : 1,
                               'res' : '3600x2700', 'timestep' : 150,
                               'cpl_timestep' : 21600, 'atm_grid' : 'nt62'},
            '01deg_jra55' : {'ocn_pes' : 6000, 'ice_pes' : 1200, 'atm_pes' : 16,
                             'res' : '3600x2700', 'timestep' : 180,
                             'cpl_timestep' : 10800, 'atm_grid' : 'jra55'},
            '025deg_corenyf' : {'ocn_pes' : 1920, 'ice_pes' : 480, 'atm_pes' : 1,
                                'res' : '1440x1080', 'timestep' : 1200,
                                'cpl_timestep' : 21600, 'atm_grid' : 'nt62'},
            '025deg_jra55' : {'ocn_pes' : 1920, 'ice_pes' : 480, 'atm_pes' : 16,
                              'res' : '1440x1080', 'timestep' : 1200,
                              'cpl_timestep' : 10800, 'atm_grid' : 'jra55'}}

mca_opts = ['--mca', 'orte_base_help_aggregate', '0',
            '--mca', 'btl_openib_eager_limit', '4096',
            '--mca', 'btl_openib_max_send_size', '8192',
            '--mca', 'mtl', 'mxm',
            '--mca', 'coll_fca_enable', '1']

def run(exp, top_dir):
    """
    Run the experiment.
    """

    exp_def = exp_defs[exp]
    ocn_exe = os.path.join(top_dir, 'src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x')

    cice_build = 'auscom_{}_{}p'.format(exp_def['res'], exp_def['ice_pes'])
    ice_exe = os.path.join(top_dir, 'src/cice5/',
                           'build_{}/cice_{}.exe'.format(cice_build, cice_build))
    atm_grid = exp_def['atm_grid']
    atm_exe = os.path.join(top_dir, 'src/matm/build_{}/matm_{}.exe'.format(atm_grid, atm_grid))

    cmd = ['mpirun'] + mca_opts + ['-np',
           str(exp_def['ocn_pes']), ocn_exe, ':', '-np', str(exp_def['ice_pes']),
           ice_exe, ':', '-np', '1', atm_exe]

    os.chdir(os.path.join(top_dir, exp))
    with open('accessom.out', 'w') as fout, open('accessom.err', 'w') as ferr:
        popen = sp.Popen(cmd, stdout=sp.PIPE, stderr=ferr)
        # Write to stdout and to file.
        for line in popen.stdout:
            print(line.decode(), end='')
            fout.write(line.decode())
            fout.flush()
    popen.wait()

    return popen.returncode

def get_curr_cice_restart(exp_dir):

    res_file = os.path.join(exp_dir, 'INPUT', 'ice.restart_file')
    if not os.path.exists(res_file):
        return None
    with open(res_file, 'r') as f:
        s = f.read().strip()

    return os.path.join(exp_dir, s)

def get_archive_dir(exp_dir, run_date):

    timestamp = str(run_date).replace(' ', '_').replace(':', '')
    archive_dir = os.path.join(exp_dir, 'ARCHIVE_{}'.format(timestamp))

    if not os.path.exists(archive_dir):
        os.mkdir(archive_dir)
    return archive_dir

def copy_files_around_before_run(exp_dir, run_date, config_files, run_type,
                                 initial_input_dir):
    """
    Possibly setup the INPUT directory. Save the input directory to be used by
    this run..
    """

    input_dir = os.path.join(exp_dir, 'INPUT')

    if run_type == "'initial'":
        shutil.copytree(initial_input_dir, input_dir, copy_function=shutil.copy)

    for f in os.listdir(input_dir):
        os.chmod(os.path.join(input_dir, f), stat.S_IRUSR | stat.S_IWUSR)

    # Keep a copy of the configs in the INPUT for good measure
    for c in config_files:
        shutil.copy(c, input_dir)

    output_dir = os.path.join(exp_dir, 'OUTPUT')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    trash_dir = os.path.join(exp_dir, 'TRASH')
    if not os.path.exists(trash_dir):
        os.mkdir(trash_dir)

    archive_dir = get_archive_dir(exp_dir, run_date)

    # Delete any old ice restart from input, otherwise they build up.
    ice_res = get_curr_cice_restart(exp_dir)
    if ice_res is not None:
        for f in glob.glob(os.path.join(input_dir, './iced.*.nc')):
            if os.path.normpath(f) != os.path.normpath(ice_res):
                shutil.move(f, trash_dir)

    # Keep a copy of INPUT for later reference. We should be able to restart
    # from this.
    # shutil.copytree(input_dir, os.path.join(archive_dir, 'INPUT'))

    try:
        os.mkdir(os.path.join(exp_dir, 'RESTART'))
    except FileExistsError:
        pass

def copy_files_around_after_run(exp_dir, run_date):

    archive_dir = get_archive_dir(exp_dir, run_date)

    # Move everything to archived output dir.
    shutil.move(os.path.join(exp_dir, 'OUTPUT'), archive_dir)
    for f in glob.glob(os.path.join(exp_dir, './*')):
        if os.path.isfile(f):
            shutil.move(f, os.path.join(archive_dir, 'OUTPUT'))

    # Copy contents of RESTART into INPUT ready for the next run.
    for f in glob.glob(os.path.join(exp_dir, 'RESTART/*')):
        shutil.copy(f, os.path.join(exp_dir, 'INPUT'))

def datetime_to_model_format(date):
    """
    Convert a datetime date to dodgy model format string.
    """

    return str(date.year).zfill(4) + str(date.month).zfill(2) + \
           str(date.day).zfill(2)

def days_in_months(date, months, caltype):
    """
    Return how many days there are in a number of months following a date.

    The date should be at a month boundary.

    Does not use leap year days.
    """

    assert date.day == 1

    curr_date = date
    days = 0
    for m in range(months):
        days_in_month = calendar.monthrange(curr_date.year, curr_date.month)[1]
        if days_in_month == 29 and caltype == 'noleap':
            days += 28
        else:
            days += days_in_month

        curr_date += dt.timedelta(days=days_in_month)

    return days

def init_namelists(exp_dir, timestep, atm_ice_coupling_timestep, runtime,
                   curr_date, elapsed_time_in_seconds, run_type):
    """
    Set timestep and runtime of experiment.
    """

    assert run_type == "'initial'" or run_type == "'continue'"

    ice_timestep = timestep
    ocn_timestep = timestep
    atm_timestep = timestep
    ice_ocn_coupling_timestep = timestep

    runtime_in_seconds = runtime
    runtime_in_months = 0
    runtime_in_days = runtime_in_seconds // 86400
    runtime_in_ice_timesteps = runtime_in_seconds // ice_timestep

    configs = []
    for template_file in glob.glob('{}/templates/*'.format(exp_dir)):
        with open(template_file, 'r') as f:
            template = Template(f.read())
            s = template.render(ice_timestep=ice_timestep,
                                ocn_timestep=ocn_timestep,
                                atm_timestep=atm_timestep,
                                runtime_in_seconds=runtime_in_seconds,
                                runtime_in_months=runtime_in_months,
                                runtime_in_days=runtime_in_days,
                                runtime_in_ice_timesteps=runtime_in_ice_timesteps,
                                ice_ocn_coupling_timestep=ice_ocn_coupling_timestep,
                                atm_ice_coupling_timestep=atm_ice_coupling_timestep,
                                current_date=datetime_to_model_format(curr_date),
                                elapsed_time_in_seconds=elapsed_time_in_seconds,
                                run_type=run_type)

            config_file = os.path.join(exp_dir, os.path.basename(template_file))
            configs.append(config_file)
            with open(config_file, 'w') as of:
                of.write(s)

    return configs

def get_cice_date(exp_dir):
    """
    See what CICE thinks the current date and time is.
    """

    res_file = get_curr_cice_restart(exp_dir)
    if res_file is None:
        return None, 0

    with nc.Dataset(res_file) as f:
        curr_date = dt.datetime(f.nyr, f.month, f.mday, second=f.sec)
        elapsed_seconds = int(f.time)

    return curr_date, elapsed_seconds

def get_mom_date(exp_dir):
    """
    See what MOM thinks the current date and time is.
    """

    res_file = os.path.join(exp_dir, 'INPUT', 'ocean_solo.res')
    if not os.path.exists(res_file):
        return None, None, None

    with open(res_file, 'r') as f:
        s = f.read()
    m = re.search('\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+Current model time: year, month, day, hour, minute, second', s)
    t = tuple([int(m.group(i)) for i in range(1, 7)])
    curr_date = dt.datetime(*t)

    m = re.search('\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+Model start time:   year, month, day, hour, minute, second', s)
    t = tuple([int(m.group(i)) for i in range(1, 7)])
    init_date = dt.datetime(*t)

    m = re.search('\s+(\d+)\s+\(Calendar: no_calendar=0, thirty_day_months=1, julian=2, gregorian=3, noleap=4\)', s)
    if m.group(1) == '4':
        caltype = 'noleap'
    elif m.group(1) == '3':
        caltype = 'gregorian'
    else:
        caltype = None

    return curr_date, init_date, caltype

def is_continuation_run(exp_dir):
    return os.path.exists(os.path.join(exp_dir, 'INPUT', 'ocean_solo.res'))

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--experiment', default='1deg',
                        help='The experiment to run.')
    parser.add_argument('--model_timestep', type=int, default=-1,
                        help='The ice and ocean timestep in seconds.')
    parser.add_argument('--runtime_seconds', type=int, default=None,
                        help='The per-submit runtime in seconds.')
    parser.add_argument('--runtime_months', type=int, default=None,
                        help='The per-submit runtime in seconds.')
    parser.add_argument('--start_date', default='0001-01-01', help='The start date.')

    args = parser.parse_args()

    if args.model_timestep == -1:
        args.model_timestep = exp_defs[args.experiment]['timestep']
    atm_ice_cpl_timestep = exp_defs[args.experiment]['cpl_timestep']
    assert not (args.runtime_seconds is None and args.runtime_months is None)

    top_dir = os.path.dirname(os.path.realpath(__file__))
    exp_dir = os.path.join(top_dir, args.experiment)
    initial_input_dir = os.path.join(top_dir, 'input', args.experiment, 'INPUT')
    input_dir = os.path.join(exp_dir, 'INPUT')

    mom_curr_date, mom_init_date, caltype = get_mom_date(exp_dir)
    cice_curr_date, cice_elapsed_time_seconds = get_cice_date(exp_dir)
    assert mom_curr_date == cice_curr_date

    if mom_curr_date is None:
        mom_curr_date = dt.datetime.strptime(args.start_date, '%Y-%m-%d')

    if 'jra55' in args.experiment:
        if caltype is None:
            caltype = 'gregorian'
        assert caltype == 'gregorian'
    else:
        if caltype is None:
            caltype = 'noleap'
        assert caltype == 'noleap'

    # May need to figure out the runtime based on current date.
    runtime = args.runtime_seconds
    if runtime is None:
        days = days_in_months(mom_curr_date, args.runtime_months, caltype)
        runtime = days*86400

    if is_continuation_run(exp_dir):
        run_type = "'continue'"
    else:
        run_type = "'initial'"
        assert not os.path.exists(input_dir)

    configs = init_namelists(exp_dir, args.model_timestep, atm_ice_cpl_timestep,
                             runtime, mom_curr_date, cice_elapsed_time_seconds, run_type)

    copy_files_around_before_run(exp_dir, mom_curr_date, configs, run_type,
                                 initial_input_dir)

    ret = run(args.experiment, top_dir)

    if ret == 0:
        copy_files_around_after_run(exp_dir, mom_curr_date)

    return ret

if __name__ == '__main__':
    sys.exit(main())
