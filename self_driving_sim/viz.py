# viz.py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO
import pygame, numpy as np
from self_driving_sim.utils import WIDTH, HEIGHT

def draw_nn(screen, net):
    # define positions
    layer_sizes = [7,14,8,3]
    positions = []
    for i, size in enumerate(layer_sizes):
        x = WIDTH - 300 + i*90
        ys = np.linspace(100, HEIGHT-100, size)
        positions.append([(x,y) for y in ys])

    fig, ax = plt.subplots(figsize=(3,3))
    for (w, ip) in [(net.w1,0),(net.w2,1),(net.w3,2)]:
        for i in range(w.shape[0]):
            for j in range(w.shape[1]):
                color = 'g' if w[i,j]>0 else 'r'
                ax.plot([positions[ip][i][0],positions[ip+1][j][0]],
                        [positions[ip][i][1],positions[ip+1][j][1]], color=color, alpha=min(1,abs(w[i,j])*5))

    for layer, posn in zip([net.z1, net.z2, net.out], positions[1:]):
        for act, (x,y) in zip(layer, posn):
            circ = plt.Circle((x,y), 10, color=plt.cm.viridis(act))
            ax.add_patch(circ)

    ax.axis('off')
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=80)
    buf.seek(0); img = pygame.image.load(buf, 'nn'); buf.close(); plt.close(fig)
    screen.blit(img, (WIDTH-300, 0))
