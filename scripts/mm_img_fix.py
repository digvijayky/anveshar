"""Robust nuclei segmentation for the melanoma H&E (fixes the min-size/erosion issue).
Rewrites the imaging outputs only. Real CC BY 4.0 image, no simulation.
"""
import os, requests, numpy as np, pandas as pd
from PIL import Image
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from scipy import ndimage as ndi
from skimage import color, filters, morphology, measure, exposure, segmentation, feature

FS = 16
for p in ["/home/yarlagad/.local/share/fonts/Arial.ttf", "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf"]:
    if os.path.exists(p):
        font_manager.fontManager.addfont(p); plt.rcParams["font.family"] = "Arial"; break
plt.rcParams.update({"font.size": FS, "figure.dpi": 150})

OUT = "/data1/lesliec/vijay/spatial_transcriptomicsg/my_work_Gosabopos/github/concord/examples/multimodal/uveal_melanoma"
IMG_URL = "https://upload.wikimedia.org/wikipedia/commons/1/12/Histopathology_of_nodular_melanoma.jpg"
TMP = "/data1/lesliec/vijay/spatial_transcriptomicsg/my_work_Gosabopos/tmp/tmp/melanoma_he.jpg"
import time
raw = b""
if os.path.exists(TMP) and os.path.getsize(TMP) > 10000:
    raw = open(TMP, "rb").read()
for attempt in range(6):
    if raw[:2] == b"\xff\xd8":   # valid JPEG
        break
    try:
        raw = requests.get(IMG_URL, timeout=60,
                           headers={"User-Agent": "concord-research/1.0 (https://digvijayky.com; research use)"}).content
    except Exception:
        raw = b""
    if raw[:2] != b"\xff\xd8":
        time.sleep(8)
assert raw[:2] == b"\xff\xd8" and len(raw) > 10000, f"could not download a valid JPEG (got {len(raw)} bytes)"
open(TMP, "wb").write(raw)
img = np.array(Image.open(TMP).convert("RGB"))
hed = color.rgb2hed(img)
h = exposure.rescale_intensity(hed[:, :, 0], out_range=(0, 1))
e = exposure.rescale_intensity(hed[:, :, 1], out_range=(0, 1))

hs = filters.gaussian(h, 1.0)
th = filters.threshold_otsu(hs)
mask = hs > th
mask = morphology.remove_small_objects(mask, 8)
mask = ndi.binary_fill_holes(mask)
# split touching nuclei with a distance-transform watershed
dist = ndi.distance_transform_edt(mask)
coords = feature.peak_local_max(dist, min_distance=4, labels=mask, exclude_border=False)
markers = np.zeros(dist.shape, dtype=int)
for i, (r, c) in enumerate(coords, 1):
    markers[r, c] = i
lbl = segmentation.watershed(-dist, markers, mask=mask)
props = measure.regionprops(lbl)
areas = np.array([p.area for p in props if p.area >= 8])
n = int(len(areas))

hsv = color.rgb2hsv(img)
pigment_pct = round(100 * float((hsv[:, :, 2] < 0.45).mean()), 2)   # dark pixels (melanin proxy)
mp = img.shape[0] * img.shape[1] / 1e6
stats = {"width": int(img.shape[1]), "height": int(img.shape[0]), "megapixels": round(mp, 3),
         "n_nuclei": n, "median_nucleus_area_px": float(np.median(areas)) if n else 0,
         "nuclear_density_per_megapixel": round(n / mp, 1) if mp else 0,
         "pigment_dark_pixel_pct": pigment_pct,
         "note": "pixels not calibrated to microns; melanin can confound H&E deconvolution"}
pd.DataFrame([stats]).to_csv(f"{OUT}/uvm_imaging_he_stats_source.csv", index=False)

overlay = segmentation.mark_boundaries(exposure.rescale_intensity(img / 255.0), lbl, color=(0.1, 0.95, 0.1))
fig, axs = plt.subplots(2, 2, figsize=(11, 8.4))
for a in axs.ravel(): a.axis("off")
axs[0, 0].imshow(img); axs[0, 0].set_title("H&E (melanoma), original", fontsize=FS)
axs[0, 1].imshow(h, cmap="magma"); axs[0, 1].set_title("Hematoxylin (nuclei channel)", fontsize=FS)
axs[1, 0].imshow(e, cmap="viridis"); axs[1, 0].set_title("Eosin (cytoplasm, stroma)", fontsize=FS)
axs[1, 1].imshow(overlay); axs[1, 1].set_title(f"Segmented nuclei (n={n})", fontsize=FS)
fig.suptitle("Melanoma H&E image analysis (CC BY 4.0, Weiss et al. 2015)", fontsize=FS)
plt.tight_layout(); plt.savefig(f"{OUT}/uvm_imaging_he_analysis.pdf"); plt.close()
print("IMG_DONE nuclei=", n, "pigment%=", pigment_pct, "density/MP=", stats["nuclear_density_per_megapixel"])
