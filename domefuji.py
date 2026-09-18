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


print("Dome Fuji 자료 범위")
print(
    round(ice["age_ka"].min(), 1),
    "~",
    round(ice["age_ka"].max(), 1),
    "ka BP"
)


# ==========================================================
# 5. 1 ka 간격으로 보간
# ==========================================================

ages = np.arange(
    0,
    int(ice["age_ka"].max()) + 1,
    1
)

d18o = np.interp(
    ages,
    ice["age_ka"],
    ice["d18O"]
)


# ==========================================================
# 6. 작은 변동을 줄이기 위해 11 ka 이동평균
# ==========================================================

smooth = pd.Series(d18o).rolling(
    window=11,
    center=True,
    min_periods=1
).mean()


# ==========================================================
# 7. 주요 빙하기 찾기
#
# 빙하 코어에서는 δ18O가 더 낮을수록 추운 시기.
# 따라서 -smooth의 봉우리를 찾으면
# 원래 그래프의 큰 골짜기를 찾을 수 있음.
# ==========================================================

peaks, properties = find_peaks(
    -smooth,
    prominence=1.0,
    distance=70
)

glacial_ages = ages[peaks]


# ==========================================================
# 8. 빙하기 사이 간격 계산
# ==========================================================

periods = np.diff(glacial_ages)

print("\n주요 빙하기 연대 (ka BP)")
print(glacial_ages)

print("\n빙하기 사이의 간격 (천 년)")
print(periods)

if len(periods) > 0:
    print(
        "\n평균 반복 간격:",
        round(np.mean(periods), 1),
        "천 년"
    )


# ==========================================================
# 9. 그래프
# ==========================================================

plt.figure(figsize=(13, 6))

# 원자료
plt.plot(
    ages,
    d18o,
    alpha=0.35,
    label="Dome Fuji d18O"
)

# 이동평균
plt.plot(
    ages,
    smooth,
    linewidth=2,
    label="11 kyr moving average"
)

# 자동으로 찾은 주요 빙하기
plt.scatter(
    glacial_ages,
    smooth.iloc[peaks],
    s=55,
    zorder=5,
    label="Major glacial periods"
)

plt.xlabel("Age (ka BP)")
plt.ylabel(r"Ice $\delta^{18}O$ (‰)")

plt.title(
    "Dome Fuji Ice Core Oxygen Isotope Record"
)

# 왼쪽 = 과거, 오른쪽 = 현재
plt.xlim(
    ice["age_ka"].max(),
    0
)

plt.grid(alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()
