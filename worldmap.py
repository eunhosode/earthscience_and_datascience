import matplotlib.pyplot as plt
import geopandas as gpd
from collections import Counter

# --------------------------------------------------
# LR04 57개 코어 지점
# (이름, 위도, 경도, 해양)
# --------------------------------------------------

sites = [
    ("DSDP 502", 11.49, -79.37, "Atlantic"),
    ("DSDP 552", 56.04, -23.23, "Atlantic"),
    ("DSDP 607", 41.00, -32.96, "Atlantic"),
    ("DSDP 610", 53.22, -18.89, "Atlantic"),
    ("ODP 658", 20.75, -18.58, "Atlantic"),
    ("ODP 659", 18.08, -21.03, "Atlantic"),
    ("ODP 662", -1.39, -11.74, "Atlantic"),
    ("ODP 664", 0.11, -23.16, "Atlantic"),
    ("ODP 665", 2.95, -19.67, "Atlantic"),

    ("ODP 677", 1.20, -83.74, "Pacific"),

    ("ODP 704", -46.88, 7.42, "Atlantic"),

    ("ODP 722", 16.62, 59.80, "Indian"),
    ("ODP 758", 5.38, 90.37, "Indian"),

    ("ODP 806", 0.32, 159.36, "Pacific"),
    ("ODP 846", -3.09, -90.82, "Pacific"),
    ("ODP 849", 0.18, -110.52, "Pacific"),

    ("ODP 925", 4.20, -43.49, "Atlantic"),
    ("ODP 927", 5.47, -44.48, "Atlantic"),
    ("ODP 928", 5.46, -43.75, "Atlantic"),
    ("ODP 929", 5.98, -43.74, "Atlantic"),

    ("ODP 980", 55.48, -14.70, "Atlantic"),
    ("ODP 981", 55.48, -14.65, "Atlantic"),
    ("ODP 982", 57.52, -15.87, "Atlantic"),
    ("ODP 983", 60.40, -23.64, "Atlantic"),
    ("ODP 984", 61.43, -24.08, "Atlantic"),

    ("ODP 999", 12.74, -78.74, "Atlantic"),

    ("ODP 1012", 32.28, -118.38, "Pacific"),
    ("ODP 1020", 41.00, -126.40, "Pacific"),

    ("ODP 1085", -29.37, 13.99, "Atlantic"),
    ("ODP 1087", -31.47, 15.31, "Atlantic"),

    ("ODP 1088", -41.13, 13.60, "Atlantic"),
    ("ODP 1089", -40.94, 9.89, "Atlantic"),
    ("ODP 1090", -42.91, 8.90, "Atlantic"),
    ("ODP 1092", -46.41, 7.08, "Atlantic"),

    ("ODP 1123", -41.79, -171.50, "Pacific"),

    ("ODP 1143", 9.36, 113.29, "Pacific"),
    ("ODP 1146", 19.46, 116.27, "Pacific"),
    ("ODP 1148", 18.84, 116.57, "Pacific"),

    ("GeoB1032", -22.92, 6.03, "Atlantic"),
    ("GeoB1034", -21.74, 5.42, "Atlantic"),
    ("GeoB1035", -21.60, 5.03, "Atlantic"),
    ("GeoB1041", -3.48, -7.59, "Atlantic"),
    ("GeoB1101", 1.66, -10.98, "Atlantic"),
    ("GeoB1105", -1.67, -12.43, "Atlantic"),
    ("GeoB1113", -5.75, -11.04, "Atlantic"),
    ("GeoB1117", -3.82, -14.90, "Atlantic"),
    ("GeoB1211", -24.47, 7.54, "Atlantic"),
    ("GeoB1214", -24.69, 7.24, "Atlantic"),
    ("GeoB1312", -31.66, -29.66, "Atlantic"),
    ("GeoB1505", 2.27, -33.02, "Atlantic"),

    ("MD95-2042", 37.80, -10.17, "Atlantic"),

    ("TT013-PC72", 0.11, -139.40, "Pacific"),
    ("RC13-110", -0.10, -95.65, "Pacific"),

    ("RC13-229", -25.49, 11.31, "Atlantic"),

    ("V19-28", -2.37, -84.65, "Pacific"),
    ("V19-30", -3.38, -83.52, "Pacific"),
    ("V21-146", 37.68, 163.03, "Pacific"),
]

# --------------------------------------------------
# 해양별 색
# --------------------------------------------------

ocean_counts = Counter(site[3] for site in sites)

colors = {
    "Atlantic": "crimson",
    "Pacific": "limegreen",
    "Indian": "darkorange"
}

labels = {
    "Atlantic": "Atlantic Ocean",
    "Pacific": "Pacific Ocean",
    "Indian": "Indian Ocean"
}


# --------------------------------------------------
# 세계지도 불러오기
# --------------------------------------------------

world = gpd.read_file(
    "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
)

fig, ax = plt.subplots(figsize=(15, 8))

# 바다 배경
ax.set_facecolor("#dff4ff")

# 육지
world.plot(
    ax=ax,
    color="lightgray",
    edgecolor="black",
    linewidth=0.4
)


# --------------------------------------------------
# 해양별로 점 그리기
# --------------------------------------------------

for ocean in colors:

    selected = [site for site in sites if site[3] == ocean]

    latitudes = [site[1] for site in selected]
    longitudes = [site[2] for site in selected]

    ax.scatter(
        longitudes,
        latitudes,
        s=45,
        color=colors[ocean],
        edgecolor="black",
        linewidth=0.5,
        label=f"{labels[ocean]} ({ocean_counts[ocean]})",
        zorder=5
    )


# --------------------------------------------------
# 그래프 설정
# --------------------------------------------------

ax.set_title(
    "Locations of the 57 Core Sites Used in the LR04 Stack",
    fontsize=16
)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

ax.set_xlim(-180, 180)
ax.set_ylim(-90, 90)

ax.set_xticks(range(-180, 181, 30))
ax.set_yticks(range(-90, 91, 30))

ax.grid(
    True,
    linestyle="--",
    alpha=0.3
)

ax.legend(
    loc="lower left",
    title="Ocean"
)

plt.tight_layout()

# 이미지로 저장하고 싶으면 사용
#plt.savefig(
#    "LR04_57_sites_worldmap.png",
#    dpi=300,
#    bbox_inches="tight"
#)

plt.show()
