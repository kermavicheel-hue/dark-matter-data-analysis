import numpy as np
import matplotlib.pyplot as plt

# On définit la fonction de densité de NFW
def profil_nfw(r, rho_0, r_s):
    x = r / r_s
    return rho_0 / (x * (1 + x) ** 2)

# Paramètres du halo
rho_0 = 1e7
r_s = 20

# Distances à étudier(en kpc, et non définies sur 0)
r = np.linspace(0.1, 100, 500)

# Calcul de la densité pour chaque distance
densite = profil_nfw(r, rho_0, r_s)

# Graphique
plt.figure(figsize=(8, 5))
plt.plot(r, densite, color="darkblue", lw=2)
plt.axvline(r_s, color="gray", ls="--", lw=1, label=f"r_s = {r_s} kpc")
plt.xlabel("Rayon r (kpc)")
plt.ylabel("Densité ρ(r)")
plt.title("Profil de densité NFW")
plt.yscale("log")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("profil_nfw.png", dpi=150, bbox_inches="tight")
plt.show()

# Effets de la variation de rho_0 sur le profil de densité
r_s = 20
valeurs_rho_0 = [5e6, 1e7, 2e7]

plt.figure(figsize=(8, 5))
#on itère sur les différentes valeurs de rho_0 pour tracer les profils correspondants
for rho_0 in valeurs_rho_0:
    densite = profil_nfw(r, rho_0, r_s)
    plt.plot(r, densite, label=f"rho_0 = {rho_0: .0e}")

plt.xlabel("Rayon r (kpc)")
plt.ylabel("Densité ρ(r)")
plt.title("Effet de rho_0 (r_s fixé à 20 kpc)")
plt.yscale("log")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("effet_rho_0.png", dpi=150, bbox_inches="tight")
plt.show()

# Effets de la variation de r_s sur le profil de densité
rho_0 = 1e7
valeurs_r_s = [10, 20, 40]

plt.figure(figsize=(8, 5))
#on itère sur les différentes valeurs de r_s pour tracer les profils correspondants
for r_s in valeurs_r_s:
    densite = profil_nfw(r, rho_0, r_s)
    plt.plot(r, densite, label=f"r_s = {r_s} kpc")

plt.xlabel("Rayon r (kpc)")
plt.ylabel("Densité ρ(r)")
plt.title("Effet de r_s (rho_0 fixé à 1e7)")
plt.yscale("log")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("effet_r_s.png", dpi=150, bbox_inches="tight")
plt.show()
