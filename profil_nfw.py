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
# On itère sur les différentes valeurs de rho_0 pour tracer les profils correspondants
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
# On itère sur les différentes valeurs de r_s pour tracer les profils correspondants
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

# Masse enclose calculée en séparant la densité en sphères concentriques
def masse_nfw(r, rho_0, r_s):
    x = r / r_s
    return 4 * np.pi * rho_0 * r_s**3 * (np.log(1 + x) - x / (1 + x))

# Constante gravitationnelle en unités astro : kpc, km/s, masses solaires
G = 4.30091e-6  # kpc . (km/s)^2 / Msun

def vitesse_circulaire(r, rho_0, r_s):
    M = masse_nfw(r, rho_0, r_s)
    return np.sqrt(G * M / r)

# Paramètres du halo (mêmes valeurs de base que précédemment)
rho_0 = 1e7
r_s = 20
r = np.linspace(0.1, 100, 500)

# Masse enclose
masse = masse_nfw(r, rho_0, r_s)

plt.figure(figsize=(8, 5))
plt.plot(r, masse, color="darkgreen", lw=2)
plt.axvline(r_s, color="gray", ls="--", lw=1, label=f"r_s = {r_s} kpc")
plt.xlabel("Rayon r (kpc)")
plt.ylabel("Masse enclose M(r) (M_sun)")
plt.title("Masse enclose du halo NFW")
plt.yscale("log")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("masse_enclose_nfw.png", dpi=150, bbox_inches="tight")
plt.show()

# Courbe de rotation
vitesse = vitesse_circulaire(r, rho_0, r_s)

plt.figure(figsize=(8, 5))
plt.plot(r, vitesse, color="crimson", lw=2)
plt.axvline(r_s, color="gray", ls="--", lw=1, label=f"r_s = {r_s} kpc")
plt.xlabel("Rayon r (kpc)")
plt.ylabel("Vitesse circulaire v_c(r) (km/s)")
plt.title("Courbe de rotation du halo NFW")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("courbe_rotation_nfw.png", dpi=150, bbox_inches="tight")
plt.show()

import pandas as pd
from scipy.optimize import curve_fit

data = pd.read_csv("NGC3198_rotmod.dat", sep="\t", comment="#",
                    names=["Rad", "Vobs", "errV", "Vgas", "Vdisk", "Vbul", "SBdisk", "SBbul"])

# On extrait les colonnes nécessaires pour l'ajustement
rad = data["Rad"].values
vobs = data["Vobs"].values
errv = data["errV"].values

# Courbe de rotation observée
plt.figure(figsize=(8, 5))
plt.errorbar(rad, vobs, yerr=errv, fmt="o", color="black", label="Vobs (SPARC)")
plt.xlabel("Rayon r (kpc)")
plt.ylabel("Vitesse observée (km/s)")
plt.title("Courbe de rotation mesurée - NGC 3198")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("vobs_ngc3198.png", dpi=150, bbox_inches="tight")
plt.show()

# Ajustement
popt, pcov = curve_fit(vitesse_circulaire, rad, vobs, p0=[1e7, 20],
                        sigma=errv, absolute_sigma=True)
rho_0_fit, r_s_fit = popt
erreurs = np.sqrt(np.diag(pcov))
print(f"rho_0 = {rho_0_fit:.2e} +/- {erreurs[0]:.2e}")
print(f"r_s   = {r_s_fit:.1f} +/- {erreurs[1]:.1f} kpc")

# Comparaison visuelle
r_lisse = np.linspace(rad.min(), rad.max(), 300)
v_modele = vitesse_circulaire(r_lisse, rho_0_fit, r_s_fit)

plt.figure(figsize=(8, 5))
plt.errorbar(rad, vobs, yerr=errv, fmt="o", color="black", label="Vobs (SPARC)")
plt.plot(r_lisse, v_modele, color="crimson", lw=2, label="Modèle NFW ajusté")
plt.xlabel("Rayon r (kpc)")
plt.ylabel("Vitesse (km/s)")
plt.title("Ajustement du halo NFW - NGC 3198")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("fit_ngc3198.png", dpi=150, bbox_inches="tight")
plt.show()
