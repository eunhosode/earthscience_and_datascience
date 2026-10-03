import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


# ==========================================================
# 1. Dome Fuji DF1, DF2 자료 불러오기
# ==========================================================

df1 = pd.read_csv(
    "kawamura2017-df1_d18o_interp.txt",
    sep="\t",
    comment="#"
)

df2 = pd.read_csv(
    "kawamura2017-df2_d18o_sawdust_raw-interp.txt",
    sep="\t",
    comment="#"
)


# ==========================================================
# 2. 필요한 열만 선택
#
# age_dfo2006_aicc2012 : 연대 (calendar years BP)
# d18O_interp          : 보간된 얼음의 δ18O 값
# ==========================================================

df1 = df1[
    ["age_dfo2006_aicc2012", "d18O_interp"]
].copy()

df2 = df2[
    ["age_dfo2006_aicc2012", "d18O_interp"]
].copy()

df1.columns = ["age_year", "d18O"]
df2.columns = ["age_year", "d18O"]


# 숫자가 아닌 값 제거
df1["age_year"] = pd.to_numeric(df1["age_year"], errors="coerce")
df1["d18O"] = pd.to_numeric(df1["d18O"], errors="coerce")

df2["age_year"] = pd.to_numeric(df2["age_year"], errors="coerce")
df2["d18O"] = pd.to_numeric(df2["d18O"], errors="coerce")

df1 = df1.dropna()
df2 = df2.dropna()


# ==========================================================
# 3. year BP → ka BP 변환
# ==========================================================

df1["age_ka"] = df1["age_year"] / 1000
df2["age_ka"] = df2["age_year"] / 1000


# 1950년 이후의 음수 연대 제거
df1 = df1[df1["age_ka"] >= 0]
df2 = df2[df2["age_ka"] >= 0]


# ==========================================================
# 4. DF1과 DF2 연결
#
# DF1 : 최근 ~340 ka
# DF2 : 그보다 오래된 부분
# 겹치는 구간의 중복을 피하기 위해 340 ka에서 전환
# ==========================================================

df1_use = df1[df1["age_ka"] <= 340]

df2_use = df2[df2["age_ka"] > 340]

ice = pd.concat(
    [df1_use, df2_use],
    ignore_index=True
)

ice = ice.sort_values("age_ka")


from scipy.signal import detrend

# 0~700 ka
dome = ice[
    (ice["age_ka"] >= 0) &
    (ice["age_ka"] <= 700)
].copy()

dome = dome.sort_values("age_ka")


ages = np.arange(0, 701, 1)

d18o = np.interp(
    ages,
    dome["age_ka"],
    dome["d18O"]
)


signal = detrend(d18o)
signal = signal - np.mean(signal)


fft_values = np.fft.rfft(signal)

frequencies = np.fft.rfftfreq(
    len(signal),
    d=1
)

power = np.abs(fft_values) ** 2


frequencies = frequencies[1:]
power = power[1:]

periods = 1 / frequencies


mask = (
    (periods >= 10) &
    (periods <= 200)
)

from scipy.signal import find_peaks

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

plt.title("Fourier Spectrum of Dome Fuji")

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
