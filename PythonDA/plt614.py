import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.basemap import Basemap
import pandas_datareader


# sample 1
# x = np.arange(0.0, 5.0, 0.02)
# y = np.exp(-x)*np.cos(2*np.pi*x)
#
# fig = plt.figure()
# ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
# ax.grid(color='gray')
# ax.plot(x, y)
# ax.set_xlabel('x axis')
# ax.set_xlim((0, 5))
# plt.xticks(np.linspace(0, 5, 11))
#
# # plt.plot(x, y)
# # plt.grid(color='gray')
# plt.show()

# sample 2
# x = np.linspace(-6, 6, 30)
# y = np.linspace(-6, 6, 30)
# X, Y = np.meshgrid(x, y)
# Z = np.sin(np.sqrt(X**2+Y**2))
#
# fig = plt.figure()
# ax = plt.axes(projection='3d')
# ax.contour3D(X, Y, Z, 50, cmap='binary')
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')
# ax.view_init(60, 35)
# plt.show()

# sample 3
# u = np.linspace(0, 2*np.pi, 30)
# v = np.linspace(-0.5, 0.5, 8)/2.0
# v,u = np.meshgrid(v,u)
#
# phi = 0.5*u
#
# r = 1+v*np.cos(phi)
# x = np.ravel(r*np.cos(u))
# y = np.ravel(r*np.sin(u))
# z = np.ravel(v*np.sin(phi))
#
# from matplotlib.tri import Triangulation
# tri = Triangulation(np.ravel(v), np.ravel(u))
#
# ax = plt.axes(projection='3d')
# ax.plot_trisurf(x,y,z,triangles=tri.triangles,cmap='viridis', linewidth=0.2)
# ax.set_xlim(-1,1)
# ax.set_ylim(-1,1)
# ax.set_zlim(-1,1)
# plt.show()

# failed sample
# aapl = pandas_datareader.DataReader('AAPL', 'google')
# goog = pandas_datareader.DataReader('GOOG', 'google')
# baba = pandas_datareader.DataReader('BABA', 'google')
# amzn = pandas_datareader.DataReader('AMZN', 'google')
#
# aapl_close = aapl['Close']
# goog_close = goog['Close']
# baba_close = baba['Close']
# amzn_close = amzn['Close']
#
# stocks = pd.DataFrame({'AAPL':aapl_close,
#                        'GOOG':goog_close,
#                        'BABA':baba_close,
#                        'AMZN':amzn_close})
# stocks.plot()

