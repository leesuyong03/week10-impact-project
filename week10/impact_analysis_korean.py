import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# 한글 폰트 설정
# =========================================================
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# =========================================================
# 물리 상수 설정
# =========================================================
g = 9.81          # 중력가속도 (m/s²)
h = 1.0           # 초기 낙하 높이 (m)

t_total = 1.2     # 전체 시뮬레이션 시간
points = 3000

# =========================================================
# 반발 계수 및 충돌 시간
# =========================================================

# 맨바닥
e_hard = 0.34
dt_hard = 0.005

# 완충재
e_soft = 0.18
dt_soft = 0.020

# =========================================================
# 시간 배열 생성
# =========================================================
time = np.linspace(0, t_total, points)

# =========================================================
# 위치 및 가속도 계산 함수
# =========================================================
def simulate_motion(e, dt):

    # 자유낙하 시간
    t_fall = np.sqrt(2 * h / g)

    # 충돌 직전 속도
    v1 = -np.sqrt(2 * g * h)

    # 충돌 직후 속도
    v2 = abs(v1) * e

    y = []
    a = []

    for t in time:

        # =================================================
        # 1. 자유낙하 구간
        # =================================================
        if t < t_fall:

            yt = h - 0.5 * g * t**2

            y.append(yt)

            # 중력가속도
            a.append(-g)

        # =================================================
        # 2. 충돌 구간
        # =================================================
        elif t < t_fall + dt:

            y.append(0)

            # 충돌 가속도 계산
            impact_acc = (v2 - v1) / dt

            a.append(impact_acc)

        # =================================================
        # 3. 반등 구간
        # =================================================
        else:

            t_bounce = t - (t_fall + dt)

            yt = v2 * t_bounce - 0.5 * g * t_bounce**2

            # 바닥보다 아래로 내려가지 않게
            if yt > 0:

                y.append(yt)

                a.append(-g)

            else:

                y.append(0)

                a.append(0)

    return np.array(y), np.array(a)

# =========================================================
# 데이터 계산
# =========================================================
y_hard, a_hard = simulate_motion(e_hard, dt_hard)

y_soft, a_soft = simulate_motion(e_soft, dt_soft)

# =========================================================
# 그래프 생성
# =========================================================
fig, (ax1, ax2) = plt.subplots(
    2,
    1,
    figsize=(12, 10)
)

# 배경색 설정
fig.patch.set_facecolor('#f2f2f2')

# =========================================================
# 위치-시간 그래프
# =========================================================
ax1.plot(
    time,
    y_hard,
    color='red',
    linewidth=2.5,
    label='맨바닥 (Hard Surface)'
)

ax1.plot(
    time,
    y_soft,
    color='green',
    linewidth=2.5,
    label='완충재 (Soft Surface)'
)

# 면 채우기
ax1.fill_between(
    time,
    y_hard,
    color='red',
    alpha=0.08
)

ax1.fill_between(
    time,
    y_soft,
    color='green',
    alpha=0.08
)

ax1.set_title(
    '위치-시간 그래프',
    fontsize=22,
    fontweight='bold'
)

ax1.set_xlabel(
    '시간 (s)',
    fontsize=16
)

ax1.set_ylabel(
    '높이 (m)',
    fontsize=16
)

ax1.grid(
    True,
    linestyle='--',
    alpha=0.4
)

ax1.legend(
    fontsize=13
)

# =========================================================
# 가속도-시간 그래프
# =========================================================
ax2.plot(
    time,
    a_hard,
    color='red',
    linewidth=2.5,
    label='맨바닥 가속도'
)

ax2.plot(
    time,
    a_soft,
    color='green',
    linewidth=2.5,
    label='완충재 가속도'
)

# 손상 임계치
threshold = 600

ax2.axhline(
    threshold,
    color='orange',
    linestyle='--',
    linewidth=2.5,
    label='손상 임계치'
)

# 임계 영역 색칠
ax2.fill_between(
    time,
    threshold,
    1500,
    color='orange',
    alpha=0.08
)

ax2.set_title(
    '가속도-시간 그래프',
    fontsize=22,
    fontweight='bold'
)

ax2.set_xlabel(
    '시간 (s)',
    fontsize=16
)

ax2.set_ylabel(
    '가속도 (m/s²)',
    fontsize=16
)

ax2.grid(
    True,
    linestyle='--',
    alpha=0.4
)

ax2.legend(
    fontsize=13
)

# =========================================================
# 그래프 간격 자동 조절
# =========================================================
plt.tight_layout()

# =========================================================
# 그래프 이미지 저장
# =========================================================
plt.savefig(
    'impact_analysis_korean.png',
    dpi=300,
    bbox_inches='tight'
)

# =========================================================
# 그래프 출력
# =========================================================
plt.show()
