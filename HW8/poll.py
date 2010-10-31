import 






results  = parser.parse_args()
title    = results.title
npts     = results.npts
outline  = results.outline

f = plt.figure()
f.set_label(title)
x = datagen.generateData.randData(npts)

if outline:
    plotting.histOutline.OutlinedHistogram(x)
else:
    plotting.histOutline.RegularHistogram(x)






    
