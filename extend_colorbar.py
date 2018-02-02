## problem to be solved: extend the colorbar used in plt.contourf. 
## Issue identified: extend='both', norm = MidpointNormalize(midpoint=0.) and self-defined colormap seem to contradict with each other. 

#%% How to define your own colormap
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as colors

var = sio.loadmat(path+'figures/split_bar12_2.mat')
color_lists = var['split_bar12_2']
n_bins = 12  # Discretizes the interpolation into bins
cmap_name = 'my_list'
cm = LinearSegmentedColormap.from_list(
        cmap_name, color_lists, N=n_bins)

#%% linearly normalize the colorbar using two linear ranges
class MidpointNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))
        
#%% Extend the colorbar beyond the range of values specified
fig,ax= plt.subplots(2,1,figsize=(7, 6),tight_layout = True)
lat_rad = np.radians(lats)
Tlevs = [-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5]
norm = colors.BoundaryNorm(boundaries=Tlevs,ncolors = n_bins)
cf = ax[0].contourf(np.sin(lat_rad),levs/100,treg,levels = Tlevs,
                  norm=MidpointNormalize(midpoint=0.),
                  cmap = cm,extend='both')
#cf.cmap.set_under('yellow')
#cf.cmap.set_over('cyan')
fig.colorbar(cf,ax=ax[0],extend='both')

## Note: 
## - sometimes, I have to specify norm=norm for the code to work
## - the number of values cannot exceed the number of colors of this colormap
## - even using MidpointNormalize, the contour levels have to be equally spaced across the full color range. 
