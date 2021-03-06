import os
import matplotlib.pyplot as plt
import numpy as np
from models.earm_lopez_embedded_flat import model as earm

"""
Creates figure 1A and 1B.

"""
figs = os.path.join('.', 'Figures')
if not os.path.exists(figs):
    os.makedirs(figs)


def create_figure_1():
    datafile = os.path.join('TimingData', 'gpu_timings.csv')
    cupsoda_data = np.genfromtxt(datafile, delimiter=',', dtype=None, names=True)

    datafile = os.path.join('TimingData', 'scipy_timings.csv')
    scipy_data = np.genfromtxt(datafile, delimiter=',', dtype=None, names=True)

    fig = plt.figure(figsize=(12, 7))

    for count, model in enumerate(['tyson', 'ras', 'earm']):
        # SciPy
        scipy_n_sim = [d['nsims'] for d in scipy_data if d['model'] == model and d['num_cpu'] == 1]
        scipy_time = [d['scipytime'] for d in scipy_data if d['model'] == model and d['num_cpu'] == 1]
        # cupSODA
        cupsoda_n_sim = []
        for x in [d['nsims'] for d in cupsoda_data if d['model'] == model and d['card'] == 'gtx980-diablo']:
            if x not in cupsoda_n_sim:
                cupsoda_n_sim.append(x)
        cupsoda_time = []
        for x in cupsoda_n_sim:
            cupsoda_time.append([d['pythontime'] for d in cupsoda_data
                          if d['model'] == model and d['mem'] == 2 and d['card'] == 'gtx980-diablo' and d[
                              'nsims'] == x])

        if model == 'tyson':
            ax1 = plt.subplot2grid((3, 2), (0, 0))
            ax1.plot(scipy_n_sim, scipy_time, 'b-o', label='SciPy (lsoda)', ms=12, lw=3, mew=0, )
            ax1.plot(cupsoda_n_sim, cupsoda_time, '-v', ms=12, lw=3, mew=2, mec='red', color='red',
                     label='PySB/cupSODA')
        if model == 'ras':
            ax2 = plt.subplot2grid((3, 2), (1, 0), sharex=ax1)
            ax2.plot(scipy_n_sim, scipy_time, 'b-o', label='SciPy (lsoda)', ms=12, lw=3, mew=0, )
            ax2.plot(cupsoda_n_sim, cupsoda_time, '-v', ms=12, lw=3, mew=2, mec='red', color='red',
                     label='PySB/cupSODA')
        if model == 'earm':
            ax3 = plt.subplot2grid((3, 2), (2, 0), sharex=ax1)
            ax3.plot(scipy_n_sim, scipy_time, 'b-o', label='SciPy (lsoda)', ms=12, lw=3, mew=0, )
            ax3.plot(cupsoda_n_sim, cupsoda_time, '-v', ms=12, lw=3, mew=2, mec='red', color='red',
                     label='PySB/cupSODA')
        plt.xscale('log')
        plt.yscale('log')
    x_limit = [0, 11000]
    ax1.set_xlim(x_limit)
    ax1.set_ylim(0, 100)
    ax2.set_xlim(x_limit)
    ax2.set_ylim(0, 1000)
    ax3.set_xlim(x_limit)
    ax3.set_ylim(0, 1000)

    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.setp(ax2.get_xticklabels(), visible=False)

    ax1.set_yticks(ax1.get_yticks()[3:])
    ax2.set_yticks(ax2.get_yticks()[3:])

    f_size1 = 18
    f_size2 = 24

    ax1.yaxis.set_tick_params(labelsize=f_size1)
    ax2.yaxis.set_tick_params(labelsize=f_size1)
    ax3.yaxis.set_tick_params(labelsize=f_size1)
    ax3.xaxis.set_tick_params(labelsize=f_size1)
    ax1.legend(fontsize=14, bbox_to_anchor=(.9, 1.19), fancybox=True)

    ax2.set_ylabel('Time (s)', fontsize=f_size1)
    ax3.set_xlabel("Number of simulations", fontsize=f_size1)

    ax1.annotate('A', xy=(0, 1), xycoords='axes fraction', fontsize=f_size2, xytext=(-70, 25),
                 textcoords='offset points', ha='left', va='top')
    ax2.annotate('B', xy=(0, 1), xycoords='axes fraction', fontsize=f_size2, xytext=(-70, 10),
                 textcoords='offset points', ha='left', va='top')
    ax3.annotate('C', xy=(0, 1), xycoords='axes fraction', fontsize=f_size2, xytext=(-70, 10),
                 textcoords='offset points', ha='left', va='top')

    ax1.annotate('Cell cycle', xy=(0, 1), xycoords='axes fraction', fontsize=f_size2, xytext=(5, -5),
                 textcoords='offset points', ha='left', va='top')
    ax2.annotate('Ras/cAMP/PKA', xy=(0, 1), xycoords='axes fraction', fontsize=f_size2, xytext=(5, -5),
                 textcoords='offset points', ha='left', va='top')
    ax3.annotate('EARM', xy=(0, 1), xycoords='axes fraction', fontsize=f_size2, xytext=(5, -5),
                 textcoords='offset points', ha='left', va='top')

    proteins_of_interest = []
    for i in earm.initial_conditions:
        proteins_of_interest.append(i[1].name)
    vals = np.linspace(.8, 1.2, 11)
    median = int(np.median(range(0, len(vals))))
    image = np.loadtxt(os.path.join('SensitivityData', 'sens_earm_parameter_set_one.csv'))

    ax4 = plt.subplot2grid((3, 2), (0, 1), rowspan=3)
    all_runs_1 = []

    length_values = len(vals)
    length_image = len(image)
    for j in range(0, length_image, length_values):
        per_protein1 = []
        for i in range(0, length_image, length_values):
            if i == j:
                continue
            tmp = image[j:j + length_values, i:i + length_values].copy()
            tmp -= tmp[median, :]
            per_protein1.append(tmp)
        all_runs_1.append(per_protein1)

    ax4.boxplot(all_runs_1, vert=False, labels=None, showfliers=False)
    ax4.set_xlabel('Percent change in time-to-death', fontsize=f_size1)
    xtickNames = plt.setp(ax4, yticklabels=np.sort(proteins_of_interest))
    ax4.yaxis.tick_right()
    plt.setp(xtickNames, fontsize=30)
    plt.tick_params(axis='y', which='major', labelsize=16)
    plt.tick_params(axis='x', which='major', labelsize=18)

    ticks = [-6, -4, -2, 0, 2, 4, 6, 8]
    ax4.xaxis.set_ticks(ticks)
    ax4.set_xticklabels(ticks)
    ax4.annotate('D', xy=(0, 1), xycoords='axes fraction', fontsize=f_size2,
                 xytext=(0, 25), textcoords='offset points',
                 ha='left', va='top')
    plt.tight_layout()
    fig.subplots_adjust(hspace=.1, wspace=.01, left=.084, top=.93, bottom=0.1)
    plt.savefig(os.path.join(figs, 'figure_1.png'), bbox_tight='True')
    plt.savefig(os.path.join(figs, 'figure_1.eps'), bbox_tight='True')


if __name__ == '__main__':
    create_figure_1()
