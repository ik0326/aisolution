import math
import random
import copy
import matplotlib.pyplot as plt
from matplotlib import animation, rc, gridspec
# from IPython.display import HTML

N = 100  # エージェントの個数
SIZE = N   # 仮想空間のサイズ
INTERVAL = 100 #描画スピード
TIMELIMIT = 200  # シミュレーションの打ち切り時刻
SEED = 65535  # 乱数の初期化
R = 15  # 感染範囲
SPEED = N/50  # エージェントの歩幅
TREATMENT_PERIOD = 60  # 感染してから治るまでの期間
MORTALITY_RATE = 0.05  # 死亡率
MORTALITY_PERIOD = 20  # 感染から死亡までの期間
CONTROL_RATE = 0.8  # 自粛する割合（0～1）
CONTROL_RATE_AFTER = 0.0  # 対策後に自粛する割合（0～1）
MASK_RATE = 0.0  # マスクを装着している割合（0～1）
OVER_CAPACITY = N/2  # 感染拡大の目安
REQUEST_NOT_TO_GO_OUTSIDE_F = False  # 途中で自粛命令を出すか否か

#Agent class
class Agent:
    """
    エージェントを表現するクラスの定義
    Attributes
    ----------
    state : string
        エージェントの健康状態。S(健常状態), I(感染), R(免疫獲得), D(死亡)。
    x : int
        エージェントのx座標。
    y : int
        エージェントのy座標。
    x_v : float
        エージェントのx座標方向の速度。
    y_v : float
        エージェントのy座標方向の速度。
    term : int
        感染してからの日数。
    mask : int(0 or 1)
        マスク着用の有無。0はマスクなしで1はマスクあり。
    control_f : int(0 or 1)
        活動自粛の有無。0は自粛（移動スピードが小さい）、1は普段通り行動。
    mortality : int(0 or 1)
        感染した場合生き残れるかどうかのID。
    """
    def __init__(self, state):
        self.state = state  # 状態の設定（S or I or R or D）
        self.x = random.randint(1,SIZE)  # x座標の初期値
        self.y = random.choice([0,SIZE])  # y座標の初期値
        radian = math.radians(random.randint(1,360))
        self.x_v = math.cos(radian)*SPEED  # x方向の速さ
        self.y_v = math.sin(radian)*SPEED  # y方向の速さ
        self.term = 0  # 感染してからの日数
        self.mask_f = 0  # マスク着用の有無
        self.control_f = 1  # 活動自粛の有無
        self.mortality = random.random()  # 感染した場合生き残れるかどうかのID

    def _calcnext(self, agents):  # 次時刻の計算
        if self.state == "S":
            self._state_S(agents)  # 状態S用の計算
        elif self.state == "I":
            self._state_I()  # 状態I用の計算
        elif self.state == "R":
            self._state_R()  # 状態R用の計算
        elif self.state == "D":
            self._state_D()  # 状態D用の計算
        else:  # 合致するカテゴリがない
            print("ERROR カテゴリがありません")

    def _update_xy(self):
        """
        エージェントのxy座標を更新する
        """
        if self.x + self.x_v < 0 or SIZE < self.x + self.x_v:
            self.x_v *= -1
        if self.y + self.y_v < 0 or SIZE < self.y + self.y_v:
            self.y_v *= -1
        self.x = self.x + self.x_v * self.control_f
        self.y = self.y + self.y_v * self.control_f


    def _state_S(self, agents):  # 状態Sの計算メソッド
        # カテゴリ1のすべてのエージェントとの距離を調べる
        sx = self.x  # 状態Sのx座標
        sy = self.y  # 状態Sのy座標
        for i in range(len(agents)):
            ax = agents[i].x  # 抽出したstate1のx座標
            ay = agents[i].y  # 抽出したstate1のx座標
            if agents[i].mask_f == 1:  # マスクの有無による感染範囲の設定
                aR = R/4
            else:
                aR = R
            if agents[i].state == "I":
                if (sx-ax)*(sx-ax) + (sy-ay)*(sy-ay) < aR:  # 指定した範囲内に状態Iがいる場合
                    self.state = "I"  # 状態Iに変換（感染）
                    self.term += 1  # 感染日数に1を追加する
                    break
        # xy座標を更新
        self._update_xy()

    def _state_I(self):  # 状態Iの計算メソッド
        self.term += 1  # 感染日数を追加
        if self.term > TREATMENT_PERIOD:  # 一定の感染日数が経つと免疫を獲得する
            self.state = "R"
        if self.term > MORTALITY_PERIOD and self.mortality < MORTALITY_RATE:
            self.state = "D"
        # xy座標を更新
        self._update_xy()

    def _state_R(self):  # 状態Rの計算メソッド
        # xy座標を更新
        self._update_xy()

    def _state_D(self):
      pass

  # agentクラスの定義終わり


def calcn(agents):
    """次時刻の状態を計算"""
    # 状態Sのデータ
    xlistS, ylistS = [], []
    # 状態Iのデータ
    xlistI, ylistI = [], []
    # 状態Rのデータ
    xlistR, ylistR = [], []
    # 状態Dのデータ
    xlistD, ylistD = [], []

    for i in range(len(agents)):
        agents[i]._calcnext(agents)
        # a[i].putstate()
        # グラフデータに現在位置を追加
        if agents[i].state == "S":
            xlistS.append(agents[i].x)
            ylistS.append(agents[i].y)
        elif agents[i].state == "I":
            xlistI.append(agents[i].x)
            ylistI.append(agents[i].y)
        elif agents[i].state == "R":
            xlistR.append(agents[i].x)
            ylistR.append(agents[i].y)
        elif agents[i].state == "D":
            xlistD.append(agents[i].x)
            ylistD.append(agents[i].y)

    return xlistS, ylistS, xlistI, ylistI, xlistR, ylistR, xlistD, ylistD
    # calcn()関数の終わり


def scatter_plot(image, n, xlistS, ylistS, xlistI, ylistI, xlistR, ylistR, xlistD, ylistD):
    """散布図描画用関数"""
    image += ax[n].plot(xlistS, ylistS, ".", markersize=12, label="Susceptible", color="b", alpha=0.5) #状態Sのプロット
    image += ax[n].plot(xlistI, ylistI, ".", markersize=15, label="Infected", color="r") #状態Iのプロット
    image += ax[n].plot(xlistR, ylistR, ".", markersize=12, label="Recovered", color="g", alpha=0.5) #状態Rのプロット
    image += ax[n].plot(xlistD, ylistD, ".", markersize=12, label="Dead", color="k") #状態Dのプロット
    return image

# 初期化
random.seed(SEED) # 乱数の初期化
# 状態SのエージェントをN個生成
agentsA = [Agent("S") for i in range(N)]
# 対策あり可視化用エージェントを複製
agentsB = copy.deepcopy(agentsA)
# 自粛するエージェントの設定
for agent in random.sample(agentsB,int(CONTROL_RATE*N)):
    agent.control_f = 0
# マスクを着用するエージェントの設定
for agent in random.sample(agentsB,int(MASK_RATE*N)):
    agent.mask_f = 1


# 状態Iのエージェントの設定
agentsA[0].state = "I"
agentsA[0].x = SIZE/2
agentsA[0].y = SIZE/2
agentsA[0].control_f = 1
agentsB[0].state = "I"
agentsB[0].x = SIZE/2
agentsB[0].y = SIZE/2
agentsB[0].control_f = 1

agentsA[1].state = "I"
agentsA[1].x = SIZE/2
agentsA[1].y = SIZE/2
agentsA[1].control_f = 1
agentsB[1].state = "I"
agentsB[1].x = SIZE/2
agentsB[1].y = SIZE/2
agentsB[1].control_f = 0


# グラフデータの初期化
T = []
# Statas数推移
statasS_sum_left= []
statasI_sum_left= []
statasR_sum_left= []
statasD_sum_left= []
statasS_sum_right= []
statasI_sum_right= []
statasR_sum_right= []
statasD_sum_right= []

#描画するグラフの設定
fig = plt.figure(figsize=(7.5,5))
gs = gridspec.GridSpec(2, 2, height_ratios=(3, 1))
ax = [plt.subplot(gs[0, 0]), plt.subplot(gs[0, 1]), plt.subplot(gs[1, 0]), plt.subplot(gs[1, 1])]
#空のグラフが出てしまうのを回避
plt.close()

#アニメーション用のグラフ保管場所
ims = []

legend_flag = True  # 凡例描画のフラグ
control_flag = True  # 自粛宣言したか

# エージェントシミュレーション
for t in range(TIMELIMIT):
    T.append(t)
    xlistS, ylistS, xlistI, ylistI, xlistR, ylistR, xlistD, ylistD = calcn(agentsA)  # 次時刻の状態を計算
    im = []

    # 左側グラフ（対策なしの表示
    # subplot0：散布図
    im += scatter_plot(im, 0, xlistS, ylistS, xlistI, ylistI, xlistR, ylistR, xlistD, ylistD)

    # subplot2：推移図
    statasS_sum_left.append(len(xlistS))
    statasI_sum_left.append(len(xlistI))
    statasR_sum_left.append(len(xlistR))
    statasD_sum_left.append(len(xlistD))
    im += ax[2].stackplot(T, statasI_sum_left, statasR_sum_left, statasS_sum_left, statasD_sum_left, colors=["r","g", "b", "k"], alpha=0.7)

    # 右側グラフ（対策あり）の表示
    xlistS, ylistS, xlistI, ylistI, xlistR, ylistR, xlistD, ylistD = calcn(agentsB)  # 次時刻の状態を計算
    if REQUEST_NOT_TO_GO_OUTSIDE_F and control_flag:  # もし感染者の累計が全体のN/4を超えたら自粛要請が出る
        control_flag = False
        listS = [agentS for agentS in agentsB if agentS.state == "S"]
        for agent in random.sample(listS,int(CONTROL_RATE_AFTER*len(listS))):
            agent.control_f = 0  # 自粛状態になる

    # subplot1：散布図
    im += scatter_plot(im, 1, xlistS, ylistS, xlistI, ylistI, xlistR, ylistR, xlistD, ylistD)

    # subplot3：推移図
    statasS_sum_right.append(len(xlistS))
    statasI_sum_right.append(len(xlistI))
    statasR_sum_right.append(len(xlistR))
    statasD_sum_right.append(len(xlistD))
    im += ax[3].stackplot(T, statasI_sum_right, statasR_sum_right, statasS_sum_right, statasD_sum_right, colors=["r","g", "b", "k"], alpha=0.7)

    #描画設定
    if legend_flag:  # 一回のみ凡例を描画
        ax[0].legend(loc='lower center', bbox_to_anchor=(1.1, 1.1), ncol=4)
        ax[0].set_xlim(0, SIZE)
        ax[0].set_ylim(0, SIZE)
        ax[0].tick_params(labelbottom=False,labelleft=False,labelright=False,labeltop=False, length=0)
        ax[0].tick_params(length=0)
        ax[0].set_title("No Measures")
        ax[1].set_xlim(0, SIZE)
        ax[1].set_ylim(0, SIZE)
        ax[1].tick_params(labelbottom=False,labelleft=False,labelright=False,labeltop=False, length=0)
        ax[1].tick_params(length=0)
        ax[1].set_title("80% stay")
        ax[2].tick_params(labelbottom=False,labelleft=True,labelright=False,labeltop=False)
        ax[2].axhline(OVER_CAPACITY, ls = "--", color = "black")
        ax[3].tick_params(labelbottom=False,labelleft=True,labelright=False,labeltop=False)
        ax[3].axhline(OVER_CAPACITY, ls = "--", color = "black")
        legend_flag = False

    ims.append(im)

ani = animation.ArtistAnimation(fig, ims, interval=INTERVAL)

rc('animation', html='jshtml')
ani