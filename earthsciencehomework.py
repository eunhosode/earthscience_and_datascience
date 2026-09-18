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

print(df.head())   # 제대로 읽혔는지 확인

# 2. 최근 800 ka만 선택
recent = df[df["age_calkaBP"] <= 800].copy()
recent = recent.sort_values("age_calkaBP")

# 3. 1 ka 간격으로 보간
ages = np.arange(0, 801, 1)

d18o = np.interp(
    ages,
    recent["age_calkaBP"],
    recent["d18O_benthic"]
)

# 4. 이동평균으로 작은 요철 완화
smooth = pd.Series(d18o).rolling(
    window=11,
    center=True,
    min_periods=1
).mean()

# 5. 큰 봉우리 찾기
peaks, _ = find_peaks(
    smooth,
    prominence=0.25,
    distance=70
)

peak_ages = ages[peaks]

print("주요 빙하기 봉우리 연대(ka):")
print(peak_ages)

# 6. 그래프로 확인
plt.figure(figsize=(12, 5))

plt.plot(ages, smooth)
plt.scatter(peak_ages, smooth.iloc[peaks])

plt.xlabel("Age (ka BP)")
plt.ylabel(r"$\delta^{18}O$ (‰)")
plt.title("Major Glacial Peaks in LR04")

plt.xlim(800, 0)
plt.grid(alpha=0.3)

# 7. 봉우리 간 간격과 평균
periods = np.diff(peak_ages)

print("봉우리 사이 간격(천 년):")
print(periods)

print("평균 간격:")
print(np.mean(periods), "천 년")

plt.show()
