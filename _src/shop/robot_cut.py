from PIL import Image
import numpy as np
from scipy import ndimage as ndi
im = np.array(Image.open("src.png").convert("RGB")).astype(np.float32)
d = 255 - im.min(axis=2)
def bgmask(T):
    cand = d <= T
    lab, n = ndi.label(cand)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    return np.isin(lab, list(border))
ds = ndi.gaussian_filter(d, 1.8)
def bgmask2(T):
    cand = ds <= T
    lab, n = ndi.label(cand)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    return np.isin(lab, list(border))
m = bgmask2(4.5)
print("bg", m.mean())
fg = (~m).astype(np.float32)
# 작은 티끌 제거 + 윤곽 매끄럽게
fgs = ndi.gaussian_filter(fg, 1.6)
hard = fgs > 0.5
lab, n = ndi.label(hard)
sizes = ndi.sum(hard, lab, range(1, n + 1))
keep = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 400])
hard = keep
# 부호 거리로 1px 안티앨리어싱
din = ndi.distance_transform_edt(hard)
dout = ndi.distance_transform_edt(~hard)
sd = np.where(hard, din, -dout)
a = np.clip(0.5 + (sd - 1.6) / 1.3, 0, 1)
# 가장자리 3px 안쪽은 원래 흰 배경과 섞인 정도만큼 살짝 투명하게(어두운 배경에서 흰 테 방지)
band = hard & (din <= 3)
s = np.clip(d / 22.0, 0.45, 1.0)
pass
A = a[..., None]
C = np.where(A > 0.02, (im - (1 - A) * 255.0) / np.maximum(A, 0.02), im)
C = np.clip(C, 0, 255)
out = np.dstack([C, a * 255]).astype(np.uint8)
img = Image.fromarray(out, "RGBA")
bbox = img.getchannel("A").point(lambda v: 255 if v > 6 else 0).getbbox()
img = img.crop(bbox)
img.save("robot_full.png")
print("bbox", bbox, img.size)
def comp(bg, name, pad=40):
    c = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), bg)
    c.alpha_composite(img, (pad, pad))
    c.convert("RGB").save(name)
comp((11, 23, 48, 255), "chk_navy.png")
comp((240, 244, 250, 255), "chk_soft.png")
im2 = Image.open("chk_navy.png")
im2.crop((30,680,330,900)).resize((600,440), Image.LANCZOS).save('z_lhand.png')
im2.crop((130,180,560,420)).resize((860,480), Image.LANCZOS).save('z_head.png')
im2.crop((0,820,700,980)).resize((1050,240), Image.LANCZOS).save('z_swoosh.png')
