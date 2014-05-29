vis = '../13A-064.sb21341436.eb23334759.56447.48227415509.ms'
outvis = 'W51_Cband_Carray_H2CO.ms'

# width=4 added on May 29, 2014 (existing versions probably do not have this)
split(vis=vis, outputvis=outvis, spw='17:250~600',
      datacolumn='corrected', field='W51 Ku', width=4)

uvcontsub(outvis)

imagename = 'H2CO_11_speccube_contsub_1024_1as_uniform'
clean(vis=outvis,
      imagename=imagename,field='W51 Ku', 
      mode='velocity', 
      weighting='uniform', niter=50000, spw='0', cell=['1.0 arcsec'],
      imsize=[1024,1024],
      outframe='LSRK',
      multiscale=[0,3,6,12,24],
      usescratch=T,
      threshold='0.1 mJy',
      restfreq='4.82966GHz')
exportfits(imagename=imagename+".image", fitsimage=imagename+".fits", overwrite=True)
