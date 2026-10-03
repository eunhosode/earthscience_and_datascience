import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# 1. LR04 데이터 불러오기
file_path = r"lisiecki2005-d18o-stack-noaa.txt"

df = pd.read_csv(
    file_path,
    sep="\t",
    comment="#"
)

from scipy.signal import detrend

# 최근 700 ka 자료
lr04 = df[
    (df["age_calkaBP"] >= 0) &
    (df["age_calkaBP"] <= 700)
].copy()

lr04 = lr04.sort_values("age_calkaBP")


# 1 kyr 간격으로 보간
ages = np.arange(0, 701, 1)

d18o = np.interp(
    ages,
    lr04["age_calkaBP"],
    lr04["d18O_benthic"]
)


# 장기적인 선형 추세 제거
signal = detrend(d18o)

# 평균 제거
signal = signal - np.mean(signal)


# -------------------------------
# Fourier Transform
# -------------------------------

fft_values = np.fft.rfft(signal)

frequencies = np.fft.rfftfreq(
    len(signal),
    d=1       # 1 kyr 간격
)

power = np.abs(fft_values) ** 2


# 주파수 0 제거
frequencies = frequencies[1:]
power = power[1:]

# frequency → period
periods = 1 / frequencies


# 10~200 kyr만 표시
mask = (
    (periods >= 10) &
    (periods <= 200)
)


# 10~200 kyr 범위
p = periods[mask]
pw = power[mask]

# 주기가 작은 것 → 큰 것 순서로 정렬
order = np.argsort(p)
p = p[order]
pw = pw[order]

# 최대값을 1로 맞춰 두 자료를 비교하기 쉽게 함
pw_norm = pw / np.max(pw)

target_periods = [100, 41, 23, 19]

print("궤도 주기와 가까운 Fourier 성분")
print("기준 주기(kyr) | 실제 FFT 주기(kyr) | 상대 세기")

for target in target_periods:
    idx = np.argmin(np.abs(p - target))

    print(
        f"{target:>6}       "
        f"{p[idx]:>8.2f}          "
        f"{pw_norm[idx]:.3f}"
    )

# 그래프
plt.figure(figsize=(12, 6))

# 선 대신 discrete spectrum처럼 표시
plt.stem(
    p,
    pw_norm,
    basefmt=" "
)

plt.xlabel("Period (kyr)")
plt.ylabel("Normalized Spectral Power")

plt.title("Fourier Spectrum of LR04")

# 알려진 궤도주기는 '찾는 기준'이 아니라
# 분석 후 비교하기 위한 참고선으로만 표시
plt.axvline(100, linestyle="--", label="Eccentricity (~100 kyr)")
plt.axvline(41, linestyle="--", label="Obliquity (~41 kyr)")
plt.axvline(23, linestyle="--", label="Precession (~23 kyr)")
plt.axvline(19, linestyle="--", label="Precession (~19 kyr)")

plt.xlim(10, 200)
plt.ylim(0, 1.05)

plt.grid(alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()
