from autofit import conf

import os

path = '{}/../../../../autolens_workspace/'.format(os.path.dirname(os.path.realpath(__file__)))

conf.instance = conf.Config(config_path=path+'config', output_path=path+'output')

from autolens.model.profiles import mass_profiles as mp
import autolens as al
import pandas as pd

from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from math import pi, cos, sin


path = '{}/../../data/slacs/'.format(os.path.dirname(os.path.realpath(__file__)))
data_path = '{}/../../../../../output/slacs_shu_shu/F814W/'.format(os.path.dirname(os.path.realpath(__file__)))
pipeline = '/pipeline_power_law_hyper__lens_bulge_disk_power_law__source_inversion__const'
model = '/pipeline_tag__fix_lens_light__pix_voro_image__reg_adapt_bright__bd_align_centre__disk_sersic/' \
        'phase_1__lens_bulge_disk_power_law__source_inversion/phase_tag__sub_2__pos_0.50/' \
        'model.results'

slacs_path = '{}/../../data/slacs_data_table.xlsx'.format(os.path.dirname(os.path.realpath(__file__)))

lens_name = np.array(['slacs0216-0813',
                      'slacs0252+0039',
                      'slacs0737+3216',
                      'slacs0912+0029',
                      'slacs0959+0410',
                      'slacs1205+4910',
                      'slacs1250+0523',
                      'slacs1402+6321',
                      'slacs1420+6019',
                      'slacs1430+4105',
                      'slacs1627-0053',
                      'slacs1630+4520',
                      'slacs2238-0754',
                      'slacs2300+0022',
                      'slacs2303+1422'])
list_ = []
lens = []
SLACS_image = []
lens_plane_source_model_image = []

slacs = pd.read_excel(slacs_path, index_col=0)
del slacs.index.name
slacs = slacs.drop(['slacs0959+5100', 'slacs0959+4416'], axis=0)



for i in range(len(lens_name)):
    full_data_path = Path(data_path + lens_name[i] + pipeline + model)
    if full_data_path.is_file():
        data = pd.read_csv(full_data_path, sep='\s+', header=None, skiprows=19, nrows=7,).set_index(0)
        del data.index.name
        data[2] = data[2].str.strip('(,').astype(float)
        data[3] = data[3].str.strip(')').astype(float)
        data.columns=['param', '-error', '+error']
        list_.append(data)
        lens.append(lens_name[i])
        results = pd.concat(list_, keys=lens)
   #     image_path = path + lens_name[i] +'/F814W_image.fits'
        model_image_path= data_path + lens_name[i] + '/pipeline_power_law_hyper__lens_bulge_disk_power_law__source_inversion__const' \
                                    '/pipeline_tag__fix_lens_light__pix_voro_image__reg_adapt_bright__bd_align_centre__disk_sersic/' \
                                    'phase_1__lens_bulge_disk_power_law__source_inversion/phase_tag__sub_2__pos_0.50/'\
                                    'image/lens_fit/fits/fit_model_image_of_plane_1.fits'
      #  image = aa.array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)
        model_image = al.Array.from_fits(file_path=model_image_path, hdu=0, pixel_scales=0.03)
     #   SLACS_image.append(image)
        lens_plane_source_model_image.append(model_image)
    else:
        slacs = slacs.drop([lens_name[i]], axis=0)



for i in range(len(lens)):

    pl = mp.EllipticalPowerLaw(
            centre=(results.loc[lens[i]]['param']['centre_0'], results.loc[lens[i]]['param']['centre_1']),
            axis_ratio=results.loc[lens[i]]['param']['axis_ratio'], phi=results.loc[lens[i]]['param']['phi'],
            einstein_radius=results.loc[lens[i]]['param']['einstein_radius'], slope=results.loc[lens[i]]['param']['slope'])

    plt.figure()
    al.plot.array(array=lens_plane_source_model_image, critical_curves=pl.critical_curves)


 #   plt.plot(xcritical_rad,ycritical_rad, c='r', lw=1.5, zorder=200)
 #   plt.plot(xcaustic_rad, ycaustic_rad,c='g', lw=1.5, zorder=200)


plt.show()


