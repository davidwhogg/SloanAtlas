import os

ncolor = 5
nsb = 3

# for i in range(ncolor*nsb):
#     print i
#     os.chdir('../general_quantiles')
#     print i
#     if i <= 9:
#         os.system('mkdir quantile0%d' %(i))
#     else:
#         os.system('mkdir quantile%d' %(i))
        
#     os.chdir('../all_images')


qs = [13] #range(15) 
for i in qs: 
    print i
    os.system("echo 'sloan_atlas, quantile=%d' | idl > quantile_%d.log "%(i,i))
    os.chdir("../")
    if i <= 9:
        os.system('rsync -avrz general_quantiles/quantile0%d broiler:quantiles/' %(i))
    else:
        os.system('rsync -avrz general_quantiles/quantile%d broiler:quantiles/' %(i))
    os.system('pwd')
    os.chdir("all_images")
