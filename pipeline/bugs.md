# ツールバグ・ログ（記事執筆中に検出 / 別タスクで修正）

記事完成優先（Q3=B）。ここに記録だけして、修正は別途まとめて行う。EN/ZH版にも同症状の可能性が高い（JSは3言語同期前提）。

| 重大度 | tool_slug | 箇所 | 症状 | 想定修正 |
|---|---|---|---|---|
| 重大 | fourier-epicycles | `drawFrame` 約L447 / `computeDFT` | エピサイクル角速度に DFT 生インデックス `freq:k`(0〜N-1) を使用。負周波数成分(k>N/2)を `k-N` に折り返していないため約N倍速で回り、連続トレースがエイリアシングして破綻（トゲトゲ）。ペン先はサンプル点2π/N刻みでのみ正しい。 | freq を `k<=N/2 ? k : k-N` に折り返す |
| 重大 | fourier-epicycles | 誤解セクション 約L592 / howtoカード | 実在しない「位相の表示をON」案内＋脱字「波形が非常にになってしまう」。howtoが実UIと不一致（サンプル数は固定256で編集不可／使用円数は1〜200で「1〜128」は誤り／近似誤差は振幅比 `1-Σused/Σtotal` でRMSではない／Lissajousプリセットは存在しない）。 | 文面を実UIに合わせて修正、脱字補修 |
| 中 | lorenz-attractor | 約L428 `updateStats` | 最大リャプノフ指数の推定式 `est=lyapLog/(lyapN*DT*simTime)` が次元的に誤り。軌道間距離を再正規化せず生距離の対数を積算→飽和し λ≈0.906 を返さない。 | 一定間隔で2軌道を再正規化し log(d/d0) を平均する標準法に置換 |
| 中 | magnetic-pendulum | `getMagnets` 約L236 | 3磁石の配置が等間隔120°でなく上半分に偏る（角度 30°/90°/150°、実質60°間隔）。`y:-r*Math.cos(Math.PI*2/3)`=+0.5r の符号が誤り（-0.5r が正）。本来は正三角形 90°/210°/330°。フラクタル吸引盆が非対称・非物理になる。 | 配置を `(r*cosθ, r*sinθ)`, θ=90°,210°,330° に統一（または当該yの符号反転） |
| 軽微 | double-pendulum | L244 ヒント文 | 「θ₁+0.01° ずれ」表記が実値 `state[0]+0.0001`=10⁻⁴rad≈0.0057° と不一致。 | 表記を「約0.006°(10⁻⁴rad)」に直す or オフセットを0.01°相当に |
| 中 | newtons-cradle | `step()` 約L435-436 衝突処理 | 等質量・反発係数 e の衝突則が `v1'=e·v2+(1-e)·v1/2, v2'=e·v1+(1-e)·v2/2`。e<1 で**運動量が保存しない**（v1=1,v2=0 で和が e=0.98→0.990、0.9→0.950、0.8→0.900 と毎回減少。正しくは常に1.000）。ツールの売り（運動量保存）に反する。正しい式は `v1'=((1-e)/2)v1+((1+e)/2)v2, v2'=((1+e)/2)v1+((1-e)/2)v2`（和=v1+v2を常に保存、相対速度後=−e·相対速度前）。e=1では両者一致するため既定値98%では誤差小だが系統的に誤り。 | 衝突式を運動量保存形に置換。EN/ZH も同一JSのため同症状。 |
| 軽微 | newtons-cradle | theory-box 約L258 | 弾性衝突式の表記 `v1'=e·v2, v2'=e·v1` が実コードとも不一致、かつ e<1 で運動量非保存（和=e(v1+v2)）。e=1のスワップのみ正しい。 | 表記を運動量保存形に統一（上記と同一の正しい式） |
| 中 | random-walk-2d | `doStep` 約L339-343 | 理論MSD線が `D=stepSize²/4` で `2·D·t` を描画。2次元では `<r²>=2·d·D·t=4Dt` が正しく、`2Dt` は1次元の式。実測（lattice4で `<r²>/t≈a²=25`）に対し理論線は `a²/2=12.5` と**ちょうど半分**になり重ならない（gaussでは実測≈2a²でさらに乖離）。 | 理論線を `4*D*t` に（または `<r²>=2Dt` 表記なら D=stepSize²/2 と定義）。lattice8/gauss/levy の分散に合わせ D を歩行タイプ別に定義するのが本筋。 |
| 軽微 | heat-diffusion | howto-card 約L1144-1152 | howto本文がコードと不一致：ブラシ「1〜50mm」（実装1〜8セル）、速度「0.1〜10倍速」（実装1〜20）、α「mm²/s」表記（コードは相対無次元値 銅11.6等）、例「初期 最高50°C/最低20°C」（実装は一様25°C `T.fill(25)`）。計算自体（FTCS, 全材料で a≤0.232<0.25 安定）は正しい。 | howto文面を実UI・実装値に合わせて修正 |
| 軽微 | wave-interference | 約L443 standingMode / howto | `standingMode` は `setPreset('standing')` でしか更新されず、その後 f1/f2 を変えても逆進フラグが残る。howto例は `v=343m/s` だが既定 `v=5`（無次元）で文と既定値が不一致。重ね合わせ計算自体は正しい。 | preset後にスライダー操作したら standingMode を解除、howto の v 表記を実既定に合わせる |
| 重大 | spring-pendulum | `deriv` 約L421 運動方程式 | 動径方程式の重力項の符号が反転：`ddr = r·θ̇² − g·cosθ + (k/m)(L0−r)`。θを下向き鉛直から測る標準系では重力の動径成分は **+g·cosθ**（外向き）が正しい。現状の −g·cosθ では吊り下げ平衡(θ=0)が**不安定**になり、安定平衡が「おもりが上」側になる（物理的に逆さ）。既定 θ0=10°・r0=0.55 から積分すると暴れて発散的（実測でエネルギー5900%増/RK4破綻）。正しくは `ddr = r·θ̇² + g·cosθ − (k/m)(r−L0)`、PE_grav=−mgr·cosθ。修正版では energy drift 0.000%、2:1共振でバネ⇄振れのエネルギー授受が綺麗に出る。 | 重力項を +g·cosθ に符号修正（θ基準を下向き鉛直に統一）。theory-box の式も同様に。 |
| 中 | spring-pendulum | preset `applyPreset('resonance')` 約L369 / resonanceBox L349 | 「共振」プリセット(k=2,m=0.5,L0=0.5)は ω_spring/ω_pendulum=√(k/m)/√(g/L0)=0.45 で 2:1 条件から大きく外れる。加えて resonanceBox が振り子周波数に L0 を使う(√(g/L0))が、実際の振れ周波数は**伸び切った平衡長** r_eq=L0+mg/k を使う(√(g/r_eq))のが正しい。真の2:1は m=0.5,L0=0.5 で k≈28（r_eq≈0.675、ω_spring/ω_swing≈2.0）。 | プリセットを真の2:1(k≈28)に、resonanceBox の振り子周波数を r_eq ベースに修正。 |
| 軽微 | fourier-series | gibbsBadge 約L348 vs theory/FAQ L202 | Gibbsオーバーシュートのバッジが `((maxVal-A)/A*100)` ＝振幅A基準で**約17.9%**を表示するのに、理論box/FAQは「約9%」(ジャンプ2A基準)と記載。同じ現象を別の分母で表しており不整合。実測 max=1.179A。 | バッジ表記をジャンプ基準9%に統一、または両表記を明記(「ジャンプの約9%＝振幅の約18%」) |
| 軽微 | rlc-resonance | 約L462 statZ0 vs getZ L295 | 並列モードの共振時インピーダンス表示が `Z0=Q²·R` だが、`getZ` の並列式（R・L・C 全並列）は共振で `Z=R` を返す。両者が不一致（理想並列なら R、現実的タンク回路 R直列L なら Q²R≈L/(RC)）。直列モードは Z=R で整合。※ 並列 Q=`R/(ω0L)`=ω0RC は正しい（別agentの誤指摘）。 | getZ の並列トポロジを統一（タンク回路なら getZ も Q²R 相当に）、または statZ0 を getZ(f0) と一致させる |
| 軽微 | convection-cells | theory L196 / stats | 理論boxは Nu=C·Ra^n を提示するが Nusselt数は計算もstat表示もされない。速度場も簡易移流拡散モデル(完全NS非実装)で、buoyScale=Ra·4e-5 は経験定数。教育用途では妥当だがUIに簡易モデル注記が薄い。 | Nu のstat追加、または理論boxから Nu を削除し簡易モデルである旨を明記 |
| 中 | simple-pendulum | theory-box L269 `$$...$$` | 運動方程式の LaTeX が `\ddot{<TAB>heta}` 等、`\theta` の `\t` がタブ文字に化けて3箇所破損（`\sin<TAB>heta`, `\dot{<TAB>heta}` も同様）。MathJax で運動方程式が壊れて表示される。Python実測では RK4 と楕円積分が一致し計算ロジック自体は正しい。 | L269 のタブを `\theta` に置換。EN/ZH 版にも同症状の可能性。 |
| 中 | orbital-mechanics | 既定値 a_km=8000,e=0.30 / preset Molniya | 既定で近地点高度 = a(1-e)-RE = 5600-6371 = **-771km**（地表より下＝軌道が地球に突入）。Molniyaプリセット(12000,0.72)も近地点高度 -3011km で同様に非物理（実Molniyaは近地点約600km）。stat に負の高度が出る。 | 既定を rp>RE になる値に（例 a=12000,e=0.1 等）、Molniyaは a≈26600,e≈0.74 相当に修正。 |
| 軽微 | escape-velocity | COMPARE配列 L495 中性子星 | 中性子星の参照棒が ve=1.8e5 km/s だが、プリセット(M=466200Me,R=0.00157Re)から実計算すると ve=1.93e5 km/s（約7%乖離）。ツール自身の計算値と参照棒が食い違う。 | COMPARE の中性子星値を 1.93e5 に合わせる。 |
| 中 | gyroscope | `getParams` L334-335 / theory L314 | 歳差速度を `omegaP=tau/L`（tau=mgd·sinθ）＝ `mgd·sinθ/(Iω)` と計算。定常歳差は本来θに依存せず `mgd/(Iω)` が正しい（τ=mgd sinθ を L sinθ で割りsinθが約分）。既定θ=90°では一致するが、傾けると歳差速度がsinθ倍に過小評価される。理論box L314 のRHS `mgd/(Iω sinθ)` も誤り（正しくは sinθ無し）。 | omegaP を `tau/(L*Math.sin(theta))` に（またはθ非依存式に）。theory式も修正。 |
| 重大 | rankine-cycle | 冷凍モード `satR134a` L349-355 | R-134aの飽和圧 `P=exp(10.4-2160/Tk)*0.001` が実測の約1/140（T=5℃で~2.6kPa、実際は約360kPa）。hf/hfg多項式も実値の数倍ずれ。冷凍サイクルのCOP・各状態量が非物理。さらに L566 `dT_isen` は計算後未使用、h2s も係数0.8の場当たり式。 | R-134a物性を実テーブル/正しいAntoine式に置換。等エントロピー圧縮を s 一定で解く。 |
| 中 | rankine-cycle | 蒸気物性 `satWater`/`superheatSteam` L301-328 | 蒸気表が粗い多項式近似でIAPWSと数値乖離。ランキンモードの効率は定性傾向（圧力↑で効率↑、ポンプ仕事微小）は正しいが絶対値は教育用近似。過熱度も `Tsat+20℃` 固定でUI制御不可。 | 実用途では iapws 等の実テーブルへ。過熱度スライダー追加が望ましい。 |
| 中 | fin-heat-transfer | フィン形状セレクタ `finType` L271-275/376 | 「矩形/三角形/環状」ボタンは canvas の見た目だけ変え、効率計算は常に矩形フィン式（η=tanh(mL)/mL, m=√(hP/kA)）を使用。三角・環状フィンは P,A や効率式が異なるはずだが未実装。タイトルが複数形状対応を示唆するのに物理は1種類のみ。 | 形状ごとに P,A・効率式を実装、または形状はモデル近似である旨を明記。 |
| 中 | numerical-integration | 誤差チャート L461 / メソッド表 L400-406 | 誤差 vs n グラフで「ガウス5点」が `gauss5(f,a,b)` を n に依存せず単一区間で評価→誤差が n によらず一定の水平線になり非物理。メソッド表でもガウス2/3点は `*Math.ceil(n/k)` で複合化するのにガウス5点は未スケールで不公平比較。台形/シンプソンの誤差次数比較は正しい。 | ガウス5点を複合化（`*Math.ceil(n/5)`）し誤差を n 依存に。 |
| 軽微 | kalman-filter | 既定パラメータ Q=0.01,R=1,freq=1 | 既定は信号1Hz(10サンプル/周期)に対しモデル過信(Q小)で過度に平滑化し追従遅れ→フィルタ後RMSE(0.66)が生RMSE(0.47)より悪化。フィルタの利点が既定では見えない。GPSプリセット等では正しく改善(1.13→0.71)。 | 既定Qを上げる/信号を遅くする等、改善が見える既定に。チューニング注記を追加。 |
| 重大 | root-locus | `findClosedLoopPoles` L420-433 | 2極系の閉ループ特性式を `s²+(p1+p2)s+p1p2+K` としているが、極が p1,p2 にあるとき開ループ G=K/((s-p1)(s-p2)) の閉ループ特性は `s²-(p1+p2)s+p1p2+K`（sの係数の符号が逆）。既定(p=-1,-3,K=5)で閉ループ極を **+2±2j（右半面=不安定)** と誤算出。一方 estimateCriticalK は -1(∞=常に安定)を返し矛盾。stat の ζ=-0.707(0にクランプ)/OS/Ts も破綻。3極以上は別途 cube-root 近似で非ロバスト。**そのため記事化を見送り wheatstone-bridge に差し替え。** | sの係数を `-(p1+p2)` に符号修正。高次は数値的に多項式の根を解く。 |
| 中 | acoustic-resonance | 定在波描画 L442/461 (閉管) | 閉管の圧力/変位描画に `xNorm/2` の係数があり閉管の定在波形が物理と不一致(開管と同じ式が正しい)。共鳴**周波数**の式 f_n=(2n-1)c/4L は正しい。 | 閉管描画も `cos/sin(harmonic*π*xNorm)` に統一。 |
| 中 | neural-network | `forward` L354 / `backward` L363 | 出力層が活性化セレクタに関係なく常にシグモイド固定（hidden層のみ relu/tanh 反映）。出力δも sigmoidD 固定。relu/tanh 選択時に出力層が一貫しない。また出力ノード3指定でも各出力を独立シグモイド+MSE扱いで多クラス(softmax)非対応。XOR既定では正常動作。 | 出力層も選択活性化＋対応する導関数に。多クラスは softmax+交差エントロピー。 |
| 重大 | nyquist-sampling | `compute` L511-512 | 末尾で `drawSignal(p,fa)` を2回呼び `drawFreqChart` を一度も呼ばない。右の折り返しチャート(freqCanvas)が描画されず常に空白。数値計算(f_alias, SNR)は正しい。 | L512 を `drawFreqChart(p, fa)` に修正。 |
| 中 | quantum-tunneling | tunnel-badge 既定HTML L216 | 既定バッジが `T=1.2×10⁻⁵` とハードコードだが、既定(V0=5,E=3,d=1nm,電子)のWKB計算は T≈5.1×10⁻⁷（約24倍乖離）。初期表示だけ古い値。スライダー操作後は正しい値に更新される。またWKB式のみ実装で薄い障壁/E≈V0では厳密式とずれる(既定でWKB 5e-7 vs 厳密 2e-6)。 | 初期バッジを計算値に同期。薄い障壁では厳密式 T=1/(1+V0²sinh²(κd)/(4E(V0-E))) を使用。 |
| 中 | venturi-meter | howto-example カード L315「具体的な計算例」 | 静的な計算例の数値が JS の `compute()` と一致しない。例1「D₁=100,D₂=60,ΔP=35,ρ=1000 → V₂≒8.4m/s, Q≒19.1m³/h, Re≒5.0×10⁵, 損失≒2.1kPa」だが、実コード再現（Python）では V₂=8.79m/s, Q=89.5m³/h, Re=5.27×10⁵, 永久損失=(0.10+0.05·0.6)·35=4.55kPa。Q が約4.7倍ずれ（19.1 は誤り）、損失も 2.1≠4.55。例2「D₁=50,D₂=30,ΔP=150 → V₂≒19.7m/s, Q≒1.33m³/h, 損失≒18kPa」も実値 V₂=19.6(ρ=860)/18.2(ρ=998)m/s, Q=49.9/46.3 m³/h（1.33 は2桁誤り）、損失=19.5kPa。compute() のロジック自体は正しい（デフォルトD1=100/D2=50/dp=20 で Q=45.3,V2=6.41,Re=3.20e5,loss=2.50 が stat カードと一致）。静的howtoテキストのみの誤り。 | howto-example の数値を compute() 実出力に差し替え（例1: V₂≒8.79, Q≒89.5, Re≒5.27×10⁵, 損失≒4.55kPa）。EN/ZH版にも同じ翻訳済み誤り例がある可能性が高い。 |
| 軽微 | ballistic-pendulum | howto-example カード L297 | 計算例「弾丸10g・vb=800m/s・ブロック0.5kg・腕長0.5m → 高さ12.6mm・振れ角14.3°・衝突後KE61.6J」が誤り。実計算では共通速度 v=mvb/(m+M)=0.01·800/0.51=15.69m/s、h=v²/2g=12.54m（=12541mm！）で腕長0.5mを遥かに超え、ツールの `Math.min(h,L)` で h=0.5m=θ90°にクランプされる（物理的にはオーバーローテーション）。記載の12.6mm/14.3°と全く一致しない。衝突後KEも 0.5·0.51·15.69²=62.8J で61.6Jと微妙にずれ、「衝突前3200J」も½·0.01·800²=3200Jは正しいが損失率は98.04%（M/(m+M)=0.5/0.51）であり本文の整合が崩れている。Python実測で確認。compute() の計算ロジック自体は正しい。 | howto例を物理的に妥当な値に差し替え（例：vb=300,M=5,L=1 → v=0.599m/s, h=18.3mm, θ=10.97°, 損失率99.8%）。EN/ZH版にも同じ誤り例が翻訳されている可能性が高い。 |

## 修正ログ（2026-06-07 セッション・実コード再検証しながら1件ずつ）

**⚠ 重要：Exploreエージェントのバグ報告は不正確なことがある。修正前に必ず実コードで再検証する（下記 nyquist は誤検出だった）。**

- ✅ **simple-pendulum**（中・theta破損）：269/271行の `\theta` がタブ文字化（`\t`→TAB）で運動方程式・エネルギー式のMathJaxが破損。JA+ZH各5箇所を `\theta` に修正。ローカル＋本番デプロイ＋ライブ確認済（ZHのgooglebot meta保持）。修正スクリプト `E:\NovaSolver\fix_theta.py`。EN版は元から正常。
- ✅ **torque-lever**（中・theta破損）：site-wide走査で同じタブ破損を発見（JAのみ1箇所）。修正・本番デプロイ・ライブ確認済。※ `_tmp/`・`scripts/deploy-*` 配下の同破損は非公開アーカイブのため放置。
- ❌ **nyquist-sampling**（誤検出・取り下げ）：実コードは L512 が既に `drawFreqChart(p, fa)` を呼んでおり、エージェント報告の「drawSignal二重呼び」は事実無根。バグなし。
- ✅ **root-locus**（重大・閉ループ極の符号誤り）：`findClosedLoopPoles` で `a=p1+p2` に対し根を `[-a±√disc]/2` としていた（正しくは `[a±√disc]/2`）。既定 p=-1,-3,K=5 が +2±2j（不安定）と誤算出→ -2±2j, ζ0.707（安定）に修正。`re:-a/2`→`re:a/2`、コメントの特性式符号も訂正。3言語デプロイ・ライブ確認済。`E:\NovaSolver\fix_rootlocus.py`。
- ✅ **gyroscope**（中・歳差がθ依存）：`omegaP=tau/L`＝mgd·sinθ/(Iω) でθ依存だった。正しくは Ωp=τ/(L sinθ)=mgd/(Iω)＝θ非依存（θ=0では0）。`omegaP=(sinθ>1e-9)?tau/(L·sinθ):0` に修正、理論式の分母の余分な sinθ も除去、JA FAQの整合も修正。θ=30/45/60/90°で同値（0.6245）・θ=0で0を再現確認。3言語デプロイ・ライブ確認済。`E:\NovaSolver\fix_gyroscope.py`。EN/ZHのFAQ訳文の同種記述は未修正（軽微）。
- ✅ **軽微バグ群（2026-06-07 一括対応・各々実コード検証）**：
  - **double-pendulum**：比較軌道ヒントが「θ₁+0.01°」(EN 0.001°) だが実値 `+0.0001 rad≈0.006°`。3言語のヒントを「θ₁+10⁻⁴ rad（約0.006°）」に修正。
  - **escape-velocity**：COMPARE 中性子星 ve=1.8e5 がツール計算値と食違い。プリセット(466200Me,0.00157Re)実計算 1.928e5 km/s に合わせ修正（3言語）。
  - **fourier-series**：Gibbsバッジが `(maxVal-A)/A`＝振幅基準17.9%表示だが理論/FAQは「ジャンプ基準9%」。除数を `2*A` に変更し ~9% に統一（3言語）。
  - **rlc-resonance**：statZ0 と理論が並列共振=Q²R（タンク回路式）だが getZ は理想並列RLC（共振|Z|=R）でグラフと矛盾。statZ0 を `getZ(getF0())` に（グラフと常に一致）、理論を「並列共振 Z=R」に統一（3言語）。
  - **wave-interference**：`standingMode` が standing プリセット後スライダー操作しても解除されず逆進波が残存。JA/ZH は `render()` 無引数（=ユーザー操作）で解除。**EN は別実装**（`addEventListener('input',()=>render(simTime))`）のためリスナー側で解除。
  - **kalman-filter**：既定 Q=0.01,R=1.0 で 1Hz信号にフィルタ後RMSE(0.67)＞生(0.50)＝フィルタが悪化。node探索で Q=10⁻⁰·⁵(≈0.316),R=10⁻⁰·⁶(≈0.251) に再調整→フィルタ後0.40<生0.50（20%改善）（3言語）。
  - **heat-diffusion**：howtoカード3枚が実UIと乖離（ブラシ「1〜50mm」→1〜8セル／速度「0.1〜10倍」→1〜20倍／材料α「117/12/0.1 mm²/s」→相対値11.6/1.2/0.13／例「初期50/20°C」→一様25°C・熱源100°C）。JA/EN/ZH各々の翻訳済みhowtoを実UIに修正。
  - **convection-cells**：理論/FAQ が Nu=C·Ra^n を提示するのに Nu の stat 表示なし。Nu stat を追加し `Nu=Ra<1708?1:max(1,0.069·Ra^(1/3))`（物理的にNu≥1）で計算表示（3言語）。
  全てローカル修正→3言語デプロイ→ライブ/ md5 確認済（ZH googlebot meta 全保持）。スクリプト：`fix_minor_batch.py`/`fix_minor_code.py`/`fix_rlc_theory.py`/`fix_wave_interference.py`/`fix_kalman.py`＋手編集。
- ✅ **quantum-tunneling**（中・初期バッジ）：ハードコード初期値 T=1.2×10⁻⁵ が既定(V0=5,E=3,d=1nm,電子)のWKB計算値 5.09e-7 と約24倍乖離（update()は load 時に走り上書きするがソースが誤りで一瞬古値が出る）。初期 badge/T-val を 5.09e-7、kappa-val を 7.245 に同期。**注**：本ツールは title/meta/JSON-LD/FAQ 全てが「WKB計算機」前提（EN解説は厳密矩形障壁式とWKBが厚障壁極限である旨を既に明記）。厳密解への切替は全テキストと矛盾し範囲外のため WKB を維持＝初期値同期のみ実施。node検証で既定WKB=5.09e-7確認。3言語デプロイ・ライブ確認。`E:\NovaSolver\fix_quantum_tunneling.py`。
- ✅ **numerical-integration**（中・ガウス求積）：(1)誤差チャートの `errG5` が全n で `gauss5(f,a,b)` を全区間評価＝水平線。(2)さらに**メソッド表で `gauss2(f,a,b)*Math.ceil(n/2)` と単区間積分値に乗算**＝複合化でなく値が壊れる（n=16でgauss2=15.49、正は2.0）。複合ガウス `gaussComposite(rule,f,a,b,panels)`（区間をpanels分割し各で求積を合計）を追加し、表(ceil(n/k))・チャート(ceil(nn/5))の両方で使用。node検証：複合gauss2=1.9999、errG5 が n増で 1.1e-7→4.4e-16 と減少。3言語デプロイ・ライブ確認。`E:\NovaSolver\fix_numint.py`。
- ⚠️ **neural-network**（中・出力層活性化）→**コードは正しい（誤検出寄り）**：出力層sigmoid固定＋隠れ層のみ選択活性化は、2値分類(XOR)＋MSEの**正しいML設計**。node検証：出力層を選択活性化にすると hidden=ReLU で XOR が完全学習失敗（MSE=0.5、sigmoid出力なら0.033）。よって bugs.md の提案（出力も選択活性化に）は ReLU を壊す退行のため**不採用**。代わりに誤解防止の注記「隠れ層に適用。出力層は2値分類のため常にSigmoid」を3言語のセレクタ下に追加・デプロイ。
- ✅ **acoustic-resonance**（中・定在波描画）：**bugs.md の当初診断（「/2を除去・開管式に統一」）は誤り**。実バグは圧力(色塗り)と変位(白線)が cos↔sin で入れ替わり（開管・閉管の両方）。画面ラベル「開端=圧力節」かつ色塗りは赤=圧縮/青=希薄＝圧力ゆえ、開端(大気圧)は圧力0=節であるべき→`pressure=sin`が正、`cos`は誤り。変位は直交させ`cos`に。閉管の `/2`（1/4波長）は物理的に正しいので**保持**。node検証で全境界条件(開端節・閉端腹・内部節)一致。`pressure cos→sin`/`disp sin→cos` を開管・閉管の4箇所修正。3言語デプロイ・ライブ確認。`E:\NovaSolver\fix_acoustic.py`。
- ✅ **orbital-mechanics**（中・近地点が地中）：**JA版のみ**。既定 a=8000,e=0.30 で近地点高度 a(1-e)-RE=5600-6371=-771km（軌道が地球内部）、Molniyaプリセット(12000,0.72)も -3011km。既定を a=12000,e=0.30（近地点+2029km）、Molniyaを実値 a=26600,e=0.74（近地点+545km・遠地点約39900km）に修正。**注**：EN/ZH は JA と別の新実装（既定 a=6771,e=0=円・近地点400km、play/save付き、e最大1.5）で本バグ無し＝JAのみ修正。JA版はいずれEN/ZH実装へ寄せるのが本筋（別タスク）。JAデプロイ・ライブ確認。`E:\NovaSolver\fix_orbital.py`。
- ✅ **random-walk-2d**（中・理論MSD線が半分）：理論線が `D=stepSize²/4` で `2Dt` を描画＝2次元の `<r²>=4Dt`（2Dtは1次元式）の半分。かつ全タイプで lattice4 の分散を流用。歩行タイプ別の期待MSD/step（lattice4=a²、lattice8=1.5a²、gauss=2a²、levyは超拡散で線なし）を描画するよう置換し、全ラベル/式の「2Dt」→「4Dt」に統一（JA/ZH各4・EN5箇所、chartラベルは言語別）。node検証：実測スロープ÷予測=1.01/1.00/0.95。3言語デプロイ・ライブ確認。`E:\NovaSolver\fix_random_walk.py`。
- ✅ **newtons-cradle**（中・衝突則の運動量非保存）：等質量・反発係数eの衝突が `v1'=e·v2+(1-e)v1/2, v2'=e·v1+(1-e)v2/2`＝和(v1+v2)(1+e)/2 で e<1 で運動量が減少（ツールの売り＝運動量保存に反する）。運動量保存形 `v1'=((1-e)/2)v1+((1+e)/2)v2, v2'=((1+e)/2)v1+((1-e)/2)v2`（和=v1+v2、相対速度=−e倍、e=1でスワップ）に修正。theory-box の LaTeX も同形に統一（3言語共通）。node検証：e=0.8〜1.0 で和=1.000・相対速度=e。3言語デプロイ・ライブ確認。`E:\NovaSolver\fix_newtons_cradle.py`。
- ✅ **magnetic-pendulum**（中・3磁石配置）：getMagnets の下2磁石の y が `-r*cos(120°)=+0.5r` で符号誤り→3磁石が 30°/90°/150°（全て上半分・60°間隔）に偏り、正三角形でなく吸引盆が非対称。`y: -r*Math.cos(...)`→`y: r*Math.cos(...)`（=-0.5r）に修正し 90°/210°/330° の正三角形に（node検証）。3言語デプロイ・ライブ確認（ZH googlebot保持）。`E:\NovaSolver\fix_magnetic_pendulum.py`。
- ✅ **lorenz-attractor**（中・最大リャプノフ指数）：旧 `est=lyapLog/(lyapN*DT*simTime)` は生の軌道間距離の log を再正規化せず積算→アトラクタ径で飽和し λ≈0.906 を返さない。独立した再正規化シャドウ対（lyA/lyB を間隔 LY_D0=1e-8 に保つ Benettin 法）を追加、`est=lyapSum/lyapTime` に置換（可視2軌道は発散表示のまま維持）。node検証：カオス 0.896（教科書0.906）、rho=10 安定 −0.586。3言語デプロイ・ライブ確認（ZH googlebot保持）。`E:\NovaSolver\fix_lorenz.py`。
- ✅ **fourier-epicycles**（重大・負周波数折返し＋howto文面）：computeDFT で `freq:k`（0..N-1）をそのまま角速度に使用→k>N/2成分が連続トレースで約N倍速回転＝エイリアシング（ペン先はサンプル点でのみ正）。`freq: (k<=N/2 ? k : k-N)` に折返し（node検証：連続トレース最大ステップ 0.61→0.095、6.4倍平滑）。3言語JS共通修正。**howtoカード3枚＋誤解セクション#3**を実UIに全面書換（実在しない「サンプル数256〜2048入力欄」→固定256表示のみ／「使用円数1〜128」→1〜200／「再生速度0.5〜2.0倍」→1〜50×／「近似誤差=平均二乗誤差」→振幅比1−Σ使用÷Σ全／実在しない「リサージュ曲線プリセット」「位相表示ON」案内を削除、脱字「波形が非常にに」補修）。JA/EN/ZH各々の翻訳済みhowto・誤解文を個別修正。3言語デプロイ（md5一致で確認、ZH googlebot meta保持）。`E:\NovaSolver\fix_fourier_epicycles_freq.py`＋手編集。
- ✅ **spring-pendulum**（重大・重力項符号＋共振）：deriv の動径方程式 `ddr` の重力項が `-g·cosθ`（θ=0が不安定平衡＝発散）。`+g·cosθ` に符号修正（node検証：旧3989%発散→新エネルギー drift 0.000%、θ=0で安定吊り下げ）。theory-box LaTeX・EN解説文のインライン項も `+g\cosθ` に。resonanceBox の振り子周波数を伸び切り平衡長 `r_eq=L0+mg/k` ベースに（旧 `g/L0`）。共振プリセットを真の2:1に再調整（k=2→29.5、ratio=2.00、r0=0.6→0.67）。**追加**：デフォルト k=2 は柔らかすぎて r_eq≈2.95m で固定スケール描画から外れるため k=25（r_eq≈0.70m、画面内・連成運動が見える）に。3言語デプロイ・ライブ確認（ZH googlebot+robots meta 保持）。`E:\NovaSolver\fix_spring_pendulum.py`。
- ✅ **rankine-cycle**（重大の一部・R-134a飽和圧力）：`satR134a` の P 相関 `exp(10.4-2160/T)*0.001` が約22〜24倍過小（0°Cで0.012 MPa、実際0.293）。P-h線図の圧力軸が物理的に誤り。Clausius-Clapeyronを実データ2点(-20/0/40°C)で再較正し `exp(8.504-2658/T)` MPa に修正（-20/0/40°Cで0.136/0.293/1.016≈実0.133/0.293/1.017）。**エンタルピー(hf/hg)＝COPは元から妥当**なので未変更。3言語デプロイ・ライブ確認済。`E:\NovaSolver\fix_rankine.py`。※steam-tables(水)の粗さは別途。


## 2026-06-10 ストック記事バッチ（30件ドライブ）で検出したツールバグ
| 重大度 | tool_slug | 箇所 | 症状 | 想定修正 |
|---|---|---|---|---|
| 重大 | bridge-truss | buildTruss() ~L271-324 | Pratt/Warren/Howe の3プリセットが同一トポロジ＝同一結果（dedupeで同一19要素に collapse）。フォームボタン実質無効でFAQ説明と矛盾 | 各プリセットに別の斜材接続を与える。EN/ZH同症状 |
| 中 | bernoulli-applications | calcVenturi ~L326-343 | 既定(v1=10,D2=50)で P2=-550kPa(絶対負圧)＝物理不可だがキャビ警告なし | 蒸気圧閾値で警告、または穏当な既定に |
| 中 | reynolds-transport | howto-example L489 | 静的例 ΔP≈61/P2≈89kPa が実JS(ΔP=53.7/P2=96.3)と~12%不一致 | 例文を実値に。EN/ZH同症状 |
| 中 | beam-column | update() L242-264 | Mb,Rd=Wy·fy で χ_LT未適用なのにFAQ/JSON-LD(L81,381)は「χLTを乗じる」と明記＝実装と矛盾 | χ_LT実装 or FAQ修正。EN/ZH同症状 |
| 軽微 | projectile-3d | updateStats L553,557 | 飛行時間が点数×dt(1ステップ過大)、Magnus偏向statがφ非0で純Magnusでない | (len-1)*dt に、偏向は射出方位基準に |
| 軽微 | bevel-gear-force | howto-example L304 | 静的例 Fa=Ft·tan35°(sinγ分解なし) が実モデル Fa=Ft·tanα·sinγ と不整合 | 例文を実式に統一 |

### 2026-06-10 バッチA 追加検出
| 重大度 | tool_slug | 箇所 | 症状 | 想定修正 |
|---|---|---|---|---|
| 重大 | arc-flash | L205 Vfactor=sqrt(V/480), L192/208 E係数 | 電圧入力VはkV(既定0.48)なのに480Vで除算→Vfactor≈0.032。距離係数0.0093はinch前提だがcm使用。結果 Iₐ/E/AFB/PPE が全条件で≈0=絶対値が無意味(相対スケーリングは正) | 除算を0.48(kV)に、距離をinch換算。EN/ZH同症状 |
| 中 | ac-impedance-rlc | howto-example ~L785 | 静的例 R=100/L=10mH/C=1uF/f=1000Hz で |Z|≈109Ω/φ≈-30° と表記だが実値 |Z|=138.8Ω/φ=-43.9° | 例文を実値に。EN/ZH同症状 |
| 軽微 | ball-bearing-hertz-stress | FAQ#4 ~L462 | Db 12→18mm で外輪応力「約6.5GPa」と表記だが実計算6.83GPa | 「約6.8GPa」に。EN/ZH同症状 |

### 2026-06-10 バッチB 追加検出
| 重大度 | tool_slug | 箇所 | 症状 | 想定修正 |
|---|---|---|---|---|
| 中 | contact-lens-oxygen-permeability | HEMA Dk式 L230/JS L415 | Dk=5.5·exp(0.072·WC) の係数0.072が過大→WC70%でDk≈850(非物理、自FAQ「Dk≈80」と矛盾) | 係数を~0.04へ。EN/ZH同症状 |
| 中 | transistor-amp | calcAC 利得式 | Av=gm·(RC‖RL) で非バイパスRE項を無視→既定RE=1kで実利得を大幅過大表示。静的計算例も実JS出力と不一致 | RE非バイパス時は分母にRE。例文を実値に |
| 中 | capacitor-charge | preset clamp | カメラフラッシュ/除細動器プリセット(V0=300/5000)がslider上限100Vにclampされ高電圧例が機能せず | slider上限拡大 or プリセット値見直し |
| 中 | ultrasound-doppler-flow | howto-example L324-327 | 7.5MHz例で Fd≈968Hz/深度154cm 等が実値(8.44kHz/15.4cm)と10倍ずれ | 例文を実値に。EN/ZH同症状 |
| 軽微 | ohms-law | L324 pUnit | power statカードに ' (??)' プレースホルダが残存表示 | '(??)' を除去。EN/ZH同症状 |
| 軽微 | shockley-diode | L689,802 静的文 | n依存の√近似が物理的に誤り、1N4148例/温度依存が実モデルと不一致 | 例文修正 |
| 軽微 | kirchhoff-laws | howto-example L716 | V_par=6.67V表記だが実式120/220×12=6.55V | 6.55Vに。EN/ZH同症状 |
| 軽微 | dipole-antenna-resonance | howto-example L297 | 800MHz/VF0.96例で全長185.6mm表記だが実値180.0mm | 例文修正。EN/ZH同症状 |
| 軽微 | ac-circuit-impedance | AMラジオpreset | ラベル540kHzだが実f0≈531kHz(L/C不整合) | ラベル or 定数調整 |

### 2026-06-10 修正完了（本番デプロイ済み・md5検証・ライブ確認）
以下4件の機能バグを JA/EN/ZH の3言語で修正し本番反映（サーバー保全：サーバーコピーDL→該当JSのみ置換→アップ→md5一致→ライブ確認→IndexNow）：
- ✅ **arc-flash**：`Math.sqrt(V/480)`→`Math.sqrt(V/0.48)`（V=kV）、エネルギー係数 `0.0093`→`567`（Doughtyの距離・単位整合に校正、表示式・MathJaxも同期）。既定で E≈0→**4.54 cal/cm²・Cat2** に回復。
- ✅ **bridge-truss**：buildTruss() を再設計（上弦ノードを下弦直上に整列＋`top(i)`、プリセット別の斜材接続）。Pratt全引張/Howe全圧縮/Warren交互、3プリセットが別解・statically determinate・node検証PASS。
- ✅ **contact-lens-oxygen-permeability**：HEMA Dk係数 `0.072`→`0.0397`（Holden 1984、コード＋表示＋FAQ全7箇所）。WC38%→Dk24.9、WC70%→88.6 と物理化。
- ✅ **ohms-law**：power statカードの ` (??)` プレースホルダ除去（JA版のみ該当）。
※ 残りの howto-example 等の静的テキスト数値ずれ（reynolds-transport/ac-impedance-rlc/kirchhoff/dipole/ball-bearing/ultrasound/shockley/bevel/bernoulli/transistor-amp/capacitor 他）は未修正＝低優先で別パス。

### 2026-06-10 静的テキスト数値ずれ 修正完了（本番デプロイ済み・md5検証・IndexNow）
9ツール×3言語の howto/FAQ/会話の誤った数値を、各ツールの実JS式からPython再計算して訂正（JSは不変・サーバー保全）。24ファイル更新（3件は元々正で不要）：
- reynolds-transport(ΔP61→53.7/P2 89→96.3kPa) / ac-impedance-rlc(|Z|109→138.8Ω,φ-30→-43.9°; EN例も訂正) / kirchhoff-laws(V_par6.67→6.55V) / dipole-antenna(全長185.6→180.0mm; EN 0.978→0.993m) / ball-bearing(外輪6.5→6.8GPa) / ultrasound-doppler(Fd968Hz→8.44kHz,深度154→15.4cm,エイリアシング有) / shockley-diode(n=2は√誤り→2.4µA; 1N4148 4.3→1.35mA; EN例41.3→0.120mA) / bevel-gear(Fa=Ft·tanα·sinγへ訂正,比70→20.9%) / transistor-amp(IC1.65→3.11mA,Av-120→-128)。
- 補足: EN版が JA/ZH と別実装の例を持つツール(transistor-amp 等)が散見。今回は各ページ自身のJSに整合させた。EN/JA/ZHのモデル統一は別タスク。


### 2026-06-10 バッチC（Zenn第4セッション 30本執筆中に検出）
記事化は完成優先・ツールは未修正（RECIPE STEP6）。記事本文は実JSをPython再現した検証値のみ使用し、バグ値は不採用。

| 重大度 | tool_slug | 箇所 | 症状 | 想定修正 |
|---|---|---|---|---|
| 重大 | catenary-cable | solveCatenaryA() ~L365 `if (f(hi) < 0) return hi;` | 二分法のガードがほぼ全入力で発火（真の根 a は hi=L*1000 より下にあり f(hi)<0 が常態）→ 上限値 a≈100000 をそのまま返す。CATENARYモードの H/Tmax/S/σ/ΔL が全て誤り（既定で H≈5000kN と表示、正しくは6.33kN／S≈100m→正102.6m）。放物線モードは正常 | ガードを除去し [1e-2, L*1e4] で f(a)=a(cosh(L/2a)-1)-d の単調二分法に。小a側のoverflowは+∞扱い。EN/ZH同症状の可能性高 |
| 中 | bragg-diffraction | FAQ JSON-LD + 可視FAQ「なぜ整数次数…」 L70/642 | Cu Kα/d=2.5Åで n=1,2,3 の 2θ を 35.88→71.96→152.99° と記載。実 bragg() は 35.88→76.05→135.04° | FAQ数値を実bragg()値に再生成。EN/ZH同症状 |
| 中 | column-buckling-adv | L197 | 「P-δ曲線」chart-card が同一 `chart-title` を5重ネスト（canvasは最内のみ）。div均衡/折りたたみ崩れリスク | 単一の chart-card+chart-title+canvas に整理。EN/ZH同症状 |
| 中 | baseball-pitch-magnus | computeTrajectory L502-503 / applyPreset L468-476 | 回転軸の規約が反転。FmagY=Fmag·cos(axis)/FmagX=Fmag·sin(axis) かつ axis=90°が「縦」表記→ストレート(90°)で縦リフト=0・横変化56.8cm と物理的に逆。applyPresetがslPdist/ラベル未更新 | FmagY=sin/FmagX=cos に入替 or 軸ラベルを0°=縦に。applyPresetにslPdist代入とラベル同期追加。EN/ZH同症状 |
| 軽微 | bohr-hydrogen-model | 静的statカード初期値 L208-209 | 初期プレースホルダの始/終状態エネルギーが既定(n1=4→2)と逆。load時のcompute()で即訂正される表示上のみ | プレースホルダを e1=-0.850/e2=-3.400 に |
| 軽微 | belt-friction | howto-card「具体的な計算例」~L615 | μ=0.35・2回転で倍力比14.9×/Thold≈33.6N と記載だが実値 e^(0.35·4π)=81.3×。「3回転→57倍」も実値733×。slider範囲/単位(1-1000N・rad)も実UI(50-5000N・deg)と不一致。live計算は正 | 例文を実値に、範囲/単位をUIに整合。EN/ZH同症状 |
| 軽微 | column-buckling-adv | drawColumn(K,e,Pcr) ~L294 | 変形図が端条件Kに依らず常に正弦半波＋ピン2点を描画。K≠1でモード形状が非忠実（statカードのPcr/λ/I/Aは正） | Kでモード形状を選択（固定端=cos等）し支持端も描き分け |
| 軽微 | drag-terminal-velocity | L178 inline syncFromNum / L203 Re / FAQ | tools-common.js の syncFromNum をinline再定義し陰蔽(CLAUDE.md §20.1違反、動作は可)。Reは代表径D=2√(A/π)の概算。FAQが空気密度ρを「固定」と誤記(実は0.5-1.3可変) | inline定義を削除しcommon利用、FAQ訂正 |
| 軽微 | choked-flow | statChoked L560 | チョーク時ラベルが "chocked"(誤字)で非チョーク時の日本語「通常流れ」と表記不統一 | "choked"/「チョーク」に統一。EN/ZH同症状 |
| 軽微 | atkinson-cycle | howto-example L303-306 | 例が η≈42.2%/T3≈2680K/P3≈3850kPa（実機モデル風）で、ツールの理想空気標準 compute()(η≈66.6%等)と不整合 | 例をcompute()実値に再計算 or 実機値と明示区別。EN/ZH同症状 |
| 軽微 | betz-limit | howto-guide L802-805 | ロータ径スライダー説明が「2〜10m」だが実 slD は 10〜250m | 説明を10〜250mに。EN/ZH同症状 |
| 軽微 | biot-savart-law | howto-cards ~L703-720 | slider範囲表記(I1-50A,R0.01-0.5m等)が実UI(slI0.1-10A,slR0.5-20cm,slZ0-50cm,slN1-200)と不一致。計算例 B(0)≈9.4mT も実値23.56mTと乖離。live計算(fieldOnAxis)は正 | howto文を実UI/実式に再計算。EN/ZH同症状 |
| 軽微 | bit-error-rate | howto ~L296 | 「シミュレーション実行」ボタン案内があるが実装は oninput 自動計算でボタン無し | 「値変更で自動再計算」に修正。EN/ZH同症状 |
| 軽微 | bloom-filter-false-positive | 例 ~L200 / howto ~L195 | 計算例の偽陽性率が実値と約40倍ずれ(0.81%/3.2% 表記 vs 実0.020%/0.82%)。存在しない「シミュレート」ボタン案内 | 例数値を訂正しボタン記述削除。EN/ZH同症状 |
| 軽微 | bezier-curve | 例 ~L313 | 二次の例が P2=(80,20) を使うが、ツールは端点 P0=(0,0)/P3=(100,0) 固定・二次は P0,P1,P3。例の tan26.6°/κ等が再現不能 | ツールの固定端点・P0/P1/P3規約で例を書き直し。EN/ZH同症状 |


### 2026-06-10 バッチC 修正完了（本番デプロイ済み・md5一致・ライブ確認・IndexNow送信）
- ✅ **catenary-cable（重大）**：`solveCatenaryA()` の誤ガード `if(f(hi)<0) return hi`（ほぼ全入力で発火）を除去し、単調減少 f に対する二分法の更新方向を是正（`f(mid)>0 → lo=mid`、反復200回・収束1e-12）。既定 L=100/d=10/w=50 で H が **5000kN→6.33kN**、S=102.62m、a=126.63 に回復（node実測・記事値一致）。JA/EN/ZH の3言語に同一JS適用、md5一致・ライブで修正コード配信確認。
- ✅ **bragg-diffraction（中）**：FAQ可視テキスト＋FAQPage JSON-LD の「2θ=35.88→**71.96→152.99**°」を実 bragg() 値「35.88→**76.05→135.04**°」に訂正（各ファイル2箇所×3言語）。digits置換のみでJSON-LD妥当性保持、ライブ確認。
- ⏸ **baseball-pitch-magnus（保留）**：sin/cos入替の単純修正は不可。`FmagY=cos(axis)` は curve/sinker/slider（軸>90で下向き）には物理的に正しく、fastballプリセット(axis=90)＋ラベル「90°縦」のみ矛盾。入替するとfastballは直るが下方変化系3種を壊すためネット改善せず。正修正は軸→力モデルの再設計＋全プリセット再調整（コンテンツ作業）。当て推量デプロイは回避し別タスク化。
- （column-buckling-adv の chart-title 5重ネスト、各種 howto/FAQ の静的数値ずれ・存在しないボタン案内・slider範囲表記不整合は低優先で未対応）


### 2026-06-10〜11 トラフィック加重監査 Wave1（アクセス上位35ツール・全件修正・本番デプロイ済）
発端: アクセス・利益最大化の定量診断（GSC/GA4/nginx/閲覧API）。Google=品質抑制（imp9,921/28d・順位20.8・技術ブロック無し）、AdSense未承認、Bing 13,320クリック/14日。品質総点検が全レバー（Bing信頼・Google回復・AI引用・AdSense再申請）に効くと判断し、閲覧数上位35ツール（Zenn監査済148除外後）をサブエージェント5体で精査→**35/35にバグ、重大16件**。

**重大（計算が誤り）→ 修正・3言語デプロイ済（md5一致・ライブ確認・IndexNow 200）**:
earthquake-magnitude(PGA式3桁ずれ→全入力で震度0→Fukushima-Tanaka 1990に差替＋死んだ数値入力修正) / steam-tables(Antoine定数誤り+117%・蒸気比体積1000倍ずれ8.314→8314・エントロピーsf+164%→ln式) / valve-sizing(気体Cv 5.9倍→Masoneilan式) / cooling-tower(Merkel操作線勾配が逆数→NTU-32%・L/G傾向逆転) / airfoil(零揚力角の符号逆→キャンバーで揚力減→Glauert積分) / combustion-stoichiometry(質量%をvol%表示→モル計算) / gear-tooth(内歯車かみあい率のrb2i誤り→z2無効) / phase-diagram(二分法方向固定→Cu-Niでてこの法則が全停止＋過共晶液相線反転＋Fe-C NaN) / steam-properties(相判定破綻:150°C/10barが湿り蒸気＋数値入力ブランク化) / sheet-metal(スプリングバック2桁過大・R依存逆→K=4X³-3X+1) / nuclear-shielding(透過率>1=遮蔽で線量増＋NIST μ/ρ誤値で非保守) / magnetic-field(双極子に重複項→2〜3.5倍過大＋HiDPI座標ずれ) / sn-curve(数値入力が毎キーストロークでブランク化) / crystal-xrd(最強ピーク誤判定(024)145°→形状因子+正しい多重度で(111)43.4°) / coil-inductance(長岡係数式誤り+27%→楕円積分式＋E(k)級数も破損していたためAGM化) / nyquist-criterion(交差なし=PM0→無条件安定系を不安定と誤判定→PM∞化)。

**中位19ツール→ 第2ラウンドで修正・デプロイ済（57ファイル md5一致）**:
weld-joint-strength(Ip にd²混入→SF 2.33倍非保守) / bolt-preload(kj=5kbでLg死にパラメータ→Shigley二重円錐剛性実装・例のT 19.2→205N·m) / hertz-contact+contact-mechanics(地下応力チャート式誤り→τpeak 0.310p0@0.481a・0.300@0.786b、MathJax <em>破損修復) / pid-controller(微分項無フィルタ→Td大で発振→一次フィルタ) / waveform-generator(振幅表示10倍ずれ・THD高調波2-8のみ→47%) / wind-load(見付面積D·H→B·H) / lissajous+fluid-viscosity+bicycle(プリセットの数値入力非同期) / yplus(入力ブランク化) ほか、全ツールの howto/FAQ/JSON-LD の誤数値をPython実測値で是正（ZH 4ファイルのJSON-LD破損も修復）。

**手法**: サーバー原本DL→監査5体(Python実測必須)→修正4-5体(exact-string patch+count==1+EOL保持+node検証+QAゲート(divΔ0/JS parse/JSON-LD parse))→親が抜き取り検証→tar一括デプロイ→md5全件→ライブgrep→IndexNow。残り: 上位36-100位(65ツール、リスト=_analysis/audit100.json、サーバーコピー=_audit/server_ja/)。


### 2026-06-11 トラフィック加重監査 Wave2（36〜70位の35ツール・全件修正・本番デプロイ済）
監査=Claudeサブエージェント5体（Python実測）→**35/35にバグ、重大8件**。修正適用=codex exec（仕様書SPEC_PILOT+A〜E駆動、Claude検収）→105ファイル中103変更（EN/ZH heat-loss-buildingは該当テキスト無しで正当未変更）、md5全一致・ライブ確認・IndexNow 200。

**重大8件（修正済・node/python検証値つき）**:
- **wbgt-heat-index（安全性）**: 危険区分が公式基準から1段甘い(危険≥35) → 環境省/JSA基準(≥31危険・28-31厳重警戒…)に3言語で是正。WBGT32.5→「危険」表示確認
- **lens-optics**: 倍率符号反転（m=−v/u）→ 正立/倒立判定が全ケース逆・光線図3本が不交差 → m=v/u に修正（凸f120/u200→m=−1.5実像倒立）
- **gear-stress（非保守）**: ヘルツ応力σHに(u+1)/u欠落 → SH 4.74→正2.74。FAQのFt式1000倍ずれも是正
- **thermal-stress（非保守）**: Timoshenko曲率分母に1/(nm)項欠落(7%〜986倍ずれ)＋界面応力が次元誤りで1000倍小 → κ=0.767/m, σ_int=81.5MPa に回復。拘束モードはFAQと整合する単軸240MPaに統一
- **hydraulic-cylinder**: 油圧動力 W=P·Q/600(bar用係数)をMPa入力に適用=10倍小 → /60。既定14MPa/30L/min→7.0kW
- **spring-design**: 座屈判定式が端末条件と逆方向＋許容応力二重低減 → critR=2.62/ec、τa=0.45σB。既定の偽「座屈危険！/許容超過！」解消（L0/D=2.67<5.24安定・応力比0.83安全）
- **linkage-mechanism**: 伝達角が全角度で定数(dBD≡L3) → 固定ピボットD基準に修正。既定μ_min 70.5°→真値26.4°(<40°警告が初めて機能)
- **magnetic-materials**: 鉄損1000倍(2330W/kg)・Br 10倍小・μrが宣言値と乖離 → kh/ke再スケール(50Hz珪素鋼2.9W/kg)・Br/μrは材料宣言値表示に

中位27ツールのhowto/FAQ/JSON-LD誤数値・死にパラメータ（CT線量のpitch/mA/kVp無効果→実装、三角形Iyy=hb³/36→/48、流量計の電磁=ピトー重複、ベルト巻付角の大プーリ誤用ほか）も全数Python検証値で是正。

### 2026-06-11 Wave3（71〜100位の30ツール）監査完了・修正進行中
**重大7件検出**: solar-radiation(傾斜面日射の二重補正→太陽定数1367W/m²超えの2759W/m²出力) / arch-structure(ゴシックアーチ上下逆=crown高0) / frame-analysis(たわみ角法の式誤り→柱モーメント−50%・スウェイ2-3倍過大・ピン/ローラーも誤り) / airfoil-lift(キャンバー揚力がほぼ相殺=2412のα0でCL0.025) / air-quality-dispersion(σzがA/B級で5km超NaN・E/F指数誤り) / control-bode(むだ時間Lが`+DOMelement`=NaN→完全無効果) / cam-profile(修正正弦が不連続・ストローク未達)。仕様書=\_audit/fix4/SPEC_F〜J、codex 5ジョブ実行中。


### 2026-06-11 トラフィック加重監査 Wave3（71〜100位の30ツール・全件修正・本番デプロイ済）＝**top-100完遂**
監査=Claudeサブエージェント5体→**30/30にバグ、重大7件**。修正=codex 5ジョブ（SPEC_F〜J）→90ファイル中87変更（未変更3=EN/ZHに該当テキスト無しの正当スキップ）、QA 90/90、md5全一致・ライブ確認・IndexNow 200。

**重大7件（修正済・検証値）**: solar-radiation(傾斜面日射の/cosZ二重補正→太陽定数超え2759W/m²→全域1209以下に) / frame-analysis(たわみ角法を3元連立に書き直し。梁端±45・柱頭45・柱脚22.5kN·m、水平50kNでδ=21.33mm・40/60kN·m、ピン±41.54、ローラー=機構判定。Claude独立実装と全数値一致) / arch-structure(ゴシックアーチ上下逆→y(0)=0,y(L/2)=f) / airfoil-lift(CL=2π(α−α0)に修正。2412@0°=0.226) / air-quality-dispersion(σzをBriggs級別式に→A/B級のNaN解消・E/F指数修正) / control-bode(むだ時間L=+DOMelement=NaN→lSlider読取。K10/τ1/L0.5でGM=−8dB不安定が正しく出る) / cam-profile(修正正弦を正準3区分式に→連続・ストローク到達)。

中位23ツールのhowto/FAQ/JSON-LD誤数値・死にパラメータも全数是正（WBGT級の安全表記、ベルト巻付角、騒音バリアの受音点ガード、アンテナループ放射抵抗1e4倍、注水プリセットclamp等）。

**運用ノート**: codexジョブgear... jobIが最終QAスクリプト実行で無応答ハング（CPU増加ゼロ）→kill。パッチ適用は完了済みでClaude側QAゲートで検収継続=影響なし。codexハング時は「ファイル変更の実体確認→自前QA」で回収可能。


### 2026-06-12 トラフィック加重監査 Wave4（101〜135位の35ツール・全件修正・本番デプロイ済）
監査=Claudeサブエージェント5体（Python実測、所見=_audit/wave4_findings_A〜E.md）→**35/35にバグ、重大13件**。magnetic-forceはJA全域mojibake破損（既知のJA完全破損8件の一つ）のため修正対象から除外し再構築タスクへ。修正=codex 5ジョブ（fix5/SPEC_K〜O、計約2.3Mトークン）→Claude検収で**codexの単位系誤り1件を検出・是正**（下記運用ノート）→102ファイル中100変更（未変更2=EN/ZH 2d-conductionの正当スキップ）、QAゲート102/102、サーバーmd5全102一致・ライブ確認・IndexNow 200。

**重大13件（修正済・検証値）**:
- **continuous-beam×2（非保守）**: 反力の端モーメント補正符号が逆（2等スパンで[75,90,75]→正[45,150,45]kN、Rmax40%過小）＋BMDが端モーメント補間を二重計上（Mmax+78%過大）。たわみも標準形に書換え（市松載荷11.364mm=厳密解一致）
- **pressure-relief-valve×2（安全弁選定が全域誤り）**: 気体オリフィス面積31.62倍過大（スプリアス係数）→API520 SI形（C=0.03948系）でA=122.5mm²→記号E。液体はUS定数38にSI入力で134倍過大→11.78·Q[L/min]√(G/ΔP)形でA=9.55mm²→記号D。背圧>設定圧のNaNもガード
- **slope-stability（非保守）**: 間隙水圧の水頭にスライス底面標高の差引き漏れ→FS34%過大。修正後2.176（R掃引min）。併せて死にコードだった臨界円自動探索findBestCircle()をcompute()に接続（表示FS 5.61→3.09）
- **blast-wave（非保守）**: 爆風圧の区分式がKinney-Graham比1/6.6〜1/100で「安全」誤表示→K-G連続式へ置換（Z=1で1009kPa、既定W100kg/R50mが「安全」→「軽微損傷」へ）
- **aircraft-performance×2**: Vmd式が√CD0倍誤り（46→327km/h）で実用上昇限度が全プリセット0固定→解消。Breguet航続距離のg除算欠落で9.81倍過大（既定18,955→1,931km）
- **antenna-radiation**: λ/4モノポールのE面式cos(π/4·cosθ)→cos(π/2·cosθ)（主ビームが軸方向を向く非物理→水平0dB最大に）。yagi3反射器位相も修正（F/B 0→7.1dB）
- **creep-analysis**: Norton係数Aが約1.6e14倍過小で破断寿命・1000hひずみが全入力死に値→材料毎に物理較正（316SS A=0.282等、700℃/120MPaでtr=83.7h）
- **heat-treatment**: 冷却速度がplain/Mn鋼で全域死にパラメータ（臨界冷却速度333℃/s>slider最大100）→sliderを1000℃/sへ拡張（howto表記と整合）、CR500でマルテンサイト95%/HRC61.5到達。HRC換算もASTM E140補間へ
- **sheet-pile-embedment（非保守）**: サーチャージqが根入れ計算に無効→qを含む先端モーメント釣り合いの二分法へ（H=6/φ=32/q=15でd0 5.02→5.67m、q単調性確認）

**中位・軽微**: 残り全ツールのhowto/FAQ/JSON-LD誤数値・死にパラメータ・存在しないUI言及を全数Python/node検証値で是正（ISAに20〜32km昇温層実装、応力集中をPetersonテーブル化、fresnel円形開口のFresnel積分実装（J0数値積分・軸上厳密解と0.0008%一致）、adhesive非対称Volkersen化、PKのAUC=D/CL整合、solenoid軸上磁界符号＋チャート単位混在、cam角度クランプ、CPW 50Ω例k0.6→0.81、配管熱応力例の安全判定逆転是正等）。EN/ZHの既存div不均衡6件（continuous-beam/slope-stability/cfd-mesh-quality）も特定・修復。

**運用ノート**: codexがpressure-relief-valveでAPI520の単位系を誤実装（気体C=0.21498で5.4倍過小、液体L/min↔m³/h取り違えで16.7倍過小=非保守方向）。codexの自己検証は「式の内部整合」しか見ないため、**検収側で第一原理値（監査所見の絶対値ターゲット）と突合することが必須**と再確認。Claude側で定数修正→3言語node再検証→例文数値も追従修正。


### 2026-06-12 トラフィック加重監査 Wave5（136〜170位の35ツール・全件修正・本番デプロイ済）
対象リスト生成: pageview順からカテゴリハブ・記事ページを「スライダー有無のサーバー実体確認」で除外（wave5.json）。監査=Claudeサブエージェント5体（所見=_audit/wave5_findings_A〜E.md）→**35/35にバグ、重大12件**（異常なし2: pressure-drop-valve / earth-pressure）。修正=codex 5ジョブ（fix6/SPEC_P〜T、計約2.4Mトークン）→105ファイル中99変更、QAゲート105/105、サーバーmd5全105一致・ライブ確認・IndexNow 200。

**重大12件（修正済・検証値）**:
- **antenna-pattern×3**: 指向性が全タイプπ倍(+4.97dB)過大→半波長ダイポール2.15dBi回復 / HPBWが2ローブ跨ぎ(258°)→主ローブ探索で78.1° / エンドファイアの位相進行β欠落→ψ=πd(cosθ−1)で主ローブθ=0、ブロードサイドも再設計、SLL機能死亡も解消(-11.3dB=一様アレー理論値)
- **crane-load（危険側）**: SWLが弾性係数80GPaを破断強度として使用し実勢の40〜50倍過大(d20mmで2,073kN)→1770MPa級×充填率×撚り効率でSWL=35.5kN
- **microwave-filter**: 楕円(Cauer)モードが偽実装(リプル2倍・阻止域捏造)→選択肢から除去。GD曲線も捏造式→極位相の数値微分で実装(Butterworth N4 fc=1GHz: τ(0)=0.416ns=理論値)。LC素子数2N+1→N/2N
- **wire-rope-strength（非保守）**: 弾性伸び表示×1000誤り(105%/m)→0.105%。FAQ充填率の傾向逆転、例の破断荷重2.4倍過大も是正
- **inclined-plane**: 上向き初速で摩擦符号反転を無視(表示2.01s vs 真値3.05s、静止保持ケースも有限値)→上昇/静止判定/下降の区分積分。a≈0の0除算、シミュの静止再判定欠落も修正
- **ball-physics**: 表示単位系の破綻(自由落下が10倍速・KEが1万分の1消失)→px/ms→m/s換算統一(落下0.926s・KE=PE=4.116J)
- **drag-calculation**: カスタム流体の密度入力がlog10解釈(1.2入力→15.85kg/m³で計算)→線形入力化。浮力項(ρp−ρ)も追加
- **battery-sizing（非保守）**: 温度補正の符号が逆で寒冷時に必要容量が減る→鉛0℃でkTemp=0.75、全化学種で低温時必要Ah増加に
- **frequency-response**: ボード線図が分母|D|除算脱落で逆数形状(共振がディップ表示・同画面スタットと278倍矛盾)→正規化導入、共振ピーク16.89µm/N=スタット一致、2DOF合成・反共振も復元
- **fluid-sloshing**: 等価振り子長 tanh/k1→coth/k1(浅水で6倍ずれ)→Teq=1/f1の整合回復(h=0.1で4.055s)

**中位・軽微**: 全数是正（ISA…ではなくWave5分: 沈下式の排水長→層厚(両面排水で2倍過小解消)、SLSクリープのJ(0)=1/E整合、wave-2d周波数表示10倍ずれ、ripple-pool数値入力の発散バイパス、binary-phaseソルバス未実装でTE以下が全域α+β、entrance-region例のRe1000倍、fan-curve動作点マーカー位置、loan/busbar/bearing/PK例の結論逆転・桁誤り等）。**ship-stabilityはGZ曲線を壁側公式に統一した上で、単調増加となる「最大GZ角/安定範囲」スタットをClaude側で「—」表示に是正**（壁側近似の適用外を誤読させないため）。
**既存破損の発見・修復**: 本番由来のdiv不均衡7件（en/wave-2d, en+zh/binary-phase, en+zh/bearing-life, en+zh/inclined-plane, zh/microwave-filter, zh/worm-gear=ヘッダー構造復元含む）、zh/adsorption JSON-LD不正もこの機会に修復。

**運用ノート**: codexジョブQが2回ストール。1回目(12分)はAPI長考で自然復帰、2回目は既知の「最終QAスクリプトハング」→kill→パッチ実体は全21ファイル適用済→Claude側QA+絶対値ターゲット突合で回収（Wave3 jobIと同パターン）。ログmtime監視のウォッチドッグ(60s周期/10分閾値)が両方を検知。


### 2026-06-12 トラフィック加重監査 Wave6（171〜205位の35ツール・全件修正・本番デプロイ済）＋JA破損8件再構築
体制改良: 監査エージェントがSPEC草案まで起草しClaudeがレビュー・確定する方式に移行（スループット向上、検収基準は不変）。Wave6監査=5体→**35/35にバグ、重大15件**（所見=_audit/wave6_findings_A〜E.md）。修正=codex 5ジョブ（fix7/SPEC_A〜E）→105/105ファイル変更、QAゲート105/105、サーバーmd5全一致・ライブ確認・IndexNow 200。

**重大15件（修正済・検証値）**: beam-modes(片持ち/固定梁のモード形状σ式誤り=境界条件違反→2.000/0復元) / electromagnetic-shielding(反射損が絶対導電率使用で全材料+77.6dB過大=非保守→Cu@1MHz 108.0dB) / drag-calculation(カスタム密度がlog10解釈=13倍ずれ→線形化) / ball-physics(単位系破綻=10倍速・KE消失→0.926s/KE=PE) / battery級ではないが…ocean-wave(JONSWAP α式誤りでスペクトル247〜427倍＋U10死にパラメータ＋エネルギー/2余剰→α閉形式＋γ2パス正規化で4√m0≡Hs厳密化・U10誠実削除) / natural-convection(カスタム流体5入力が全死=TypeError→復旧) / frequency級…bridge-builder(プリセットのノード写像バグで全4種が初期表示から崩壊SF0.36→1.21) / composite-failure(応力復元が根本破綻FI=56.5→正1.24) / elastic-billiards(衝突ガード符号逆=一切跳ね返らない→1文字修正) / centrifugal-force-sim(合力矢印のy成分欠落→修正) / biomass-energy(メタン係数二重適用=40%過小→7.518GJ) / boundary-layer-turbulent(例のRe 10倍＋層流に乱流式) / laser-optics(M²伝播式が物理誤り=最大+422%→zR=πw₀²/(M²λ)) / heat-pipe(アンモニアσ+146〜209%・水μのexp/10^取り違え+55〜111%で4流体比較が物理と逆順→文献整合の物性に全面再較正＋臨界温度カット) / hvac-load(例の機器選定31%過小=非保守＋地域プリセット無効=東京とシンガポール同値→地域別絶対湿度実装＋暖房負値ガード)。
中位・軽微も全数是正（FFT振幅校正2|X|/Σw、FIR DC正規化、電気めっきCr価数n=6、PRV…ではなくinfluence-line例の支点直上修正、cam-followerβクランプ、fan-curve/drag-coefficientチャートマーカー位置、queuing P-K式余剰項、捏造企業導入実績の一般化等）。
**既存破損の発見・修復**: 本番由来div不均衡5件（zh/michelson=FAQボタンが</div>で閉鎖→</button>復元、zh/pump-selection、en+zh/fft-spectrum、＋codexがen/zh bearing-capacity等を修復）。

**JA破損8件の再構築完了**: 実態は全域mojibake破損=magnetic-forceのみ（ENテンプレートから完全再構築、cp932逆変換で原文95%復元）。他7件は健全JAを基盤に実バグ修正＝未定義JS関数3件（lissajous clearSaved / flow-around-cylinder saveSnapshot / magnetic-force saveResult）・誤例文・範囲詐称を是正。QA8/8（div/JS/JSON-LD/mojibake/canonical）・md5一致・IndexNow 200。**EN/ZH側の負債**（EN構造破損・EN mojibake・同名未定義関数）はMASTERPLANに記録済み=後続小バッチで対応。


### 2026-06-12 トラフィック加重監査 Wave7（206〜240位の35ツール・全件修正・本番デプロイ済）
監査5体→**35/35にバグ、重大13件**（所見=_audit/wave7_findings_A〜E.md）。修正=codex 5ジョブ（fix8/SPEC_A〜E）→105/105ファイル変更、QAゲート105/105、サーバーmd5全一致・IndexNow 200。

**重大13件（修正済・検証値）**: microwave-stripline(Hammerstad-Jensen Z0を√εrで除算=−13%→√εeff、50Ω合成幅2.43→3.14mm) / modal-analysis-1d×2(非対称行列へのHotellingデフレーションでf2/f3が50%過小・自由-自由は全モード機能死→Jacobiソルバへ全置換、f2 1883→3896Hz=numpy一致) / pid-tuning×4(Cohen-Coon変数取り違えでθ/τ>1.25のTi負値→標準形θ(32+6r)/(13+8r)、偽2次Padeで ZNオーバーシュート11%表示(真値88%)→リングバッファ厳密むだ時間、閾値式の安定余裕GM 14.25dB表示(真値1.49=10倍非保守)→補間式、SIMC偽実装→Skogestad則) / steel-connection(設計ボルト張力N0がJIS/AIJから乖離、M16 F8T+27%非保守→0.75σyAe表に差替) / lightning-protection(保護角法がα(hr)を全高に適用=保護半径27%過大の非保守→評価高さ統一＋クラス別適用上限でN/A表示) / modal-analysis(モード形比の符号が両モード反転=自FAQと矛盾→修正) / resonance-lcr(並列モードのQ/BW/共振インピーダンス3スタットが直列値=グラフと自己矛盾→Q=1.581/BW=31.8Hz/Z=50Ω) / contact-ellipse-hertz(接触半径式の係数4欠落＋等価曲率誤りでp_max×0.30〜0.40の非保守→楕円積分厳密係数8点に差替、既定7079MPa) / control-chart(np図の管理限界が(1−p̄)欠落=c図式→UCL 33.4→30.4) / hydraulic-jack(圧力上限スライダーが完全死にパラメータ=254MPa無警告→リリーフ弁飽和P=min(F/A,plim)実装)。
中位・軽微も全数是正（heat-exchanger例、fem-truss色逆転、laser級…charpy/hydrostaticプリセット同期、fabry-perot例次元誤り、thermal-fatigue隠れ温度補正の明記、wilkinson例、LMP説明逆転、boussinesq例の物理不可能記述等）。

**運用ノート**: Wave8監査用Claudeサブエージェントが月次支出上限に到達し起動不能化。Wave7検収はメインループ単独で実施（QAゲート＋置換実体のnode検証: stripline√εeff・Jacobi存在・CC/SIMC式形・厳密むだ時間実装を確認）。以降のWave8+は体制再設計が必要（codexへの監査委譲 or 上限引き上げ待ち）。


### 2026-06-12 トラフィック加重監査 Wave8（241〜275位の35ツール・全件修正・本番デプロイ済）
体制移行: Claudeサブエージェントが月次支出上限到達のため、監査をcodexに委譲（AUDIT_BRIEF.md=確立済み監査手順書をcodex execに渡し、findings＋SPEC草案を起草→Claudeメインループがレビュー確定・検収）。監査5ジョブ→**35/35にバグ、重大17件**（所見=fix9/wave8_findings_A〜E.md）。修正=codex 5ジョブ（fix9/SPEC_A〜E）→105/105ファイル変更、QAゲート105/105、サーバーmd5全一致・IndexNow 200。

**重大17件（修正済・検証値）**: screw-thread(トルクをN·mmで計算しN·m表示=1000倍→/1000) / semiconductor-pn(逆方向電流が-1Vで-2.94e-4A=8桁過大→ショックレー式) / thermoelectric-peltier(既定材料/単位でZT≈2.5e-5なのに本文ZT≈1主張→誠実化) / thin-walled-beam(L断面のせん断中心/反り定数がハードコード0→計算 or 未実装明示) / acoustics-room(表示fcが55.4/RT60でSchroeder周波数=体積依存を無視) / boiling-heat-transfer(流動モードと流速入力が完全死) / bolt-fatigue(Goodman安全率が平均応力無視=非保守→修正Goodman) / corrosion-electrochemical(腐食速度100倍過大→Faraday単位是正) / crank-slider(角速度をrad/s UIで/10) / digital-filter(BPF/BSF変換が数学的に無効→fail-loud) / eigenvalue-vibration×2(Jacobi θ=0で既定固有値破綻＋FRFが表示正規化モード形使用→質量正規化) / bond-wire(疲労式がスパン/径無視→L_s/D_w式) / campbell-diagram(後向き旋回危険速度がマージン統計から欠落) / explosion-blast(K-G式と同種のスケーリングバグ=Kを等価薬量でなく圧力後に適用→scaled distance) / filtration(ケーキ成長速度3600倍→flux/(1-eps)/60) / fluid-bearing(偏心率がSommerfeldとOcvirk関係に反し逆方向)。
中位・軽微も全数是正（buoyancy状態が密度ベース、cooling-coil乾入口加湿、base-excitation非絶縁域の負効率、sun-sync観測緯度未使用、fluid-pump存在しないQ0/ボタン言及等）。

**運用ノート**: codex監査時、PowerShell here-stringで`python -`へスクリプトをパイプするとハング（QAスクリプト実行型ハングの別系統）。AUDIT_BRIEFに「スクリプトはファイルに書いて実行」ルールを恒久追記し、グループC/Eの再実行で解消。codex監査体制はパイロット(グループA)で品質確認済み＝サブエージェント同等。検収側でQAゲート＋重大置換のnode独立検証（screw /1000・blast scaled-distance・filtration /60・Jacobi θ=0ガード確認）を実施。本番由来div不均衡8件も修復。


### 2026-06-12 トラフィック加重監査 Wave9（276〜310位の35ツール・全件修正・本番デプロイ済）
codex監査5ジョブ→**35/35にバグ、重大19件**（所見=fix10/wave9_findings_A〜E.md）。修正=codex 5ジョブ（fix10/SPEC_A〜E）→105/105中99変更（未変更6=metacentric-height-stability=clean判定、duct-sizing=軽微のみ正当スキップ）、QAゲート105/105、サーバーmd5全一致・IndexNow 200。

**重大19件（修正済・検証値）**: pressure-vessel-design×2(厚肉ケースで薄肉応力統計を流用＋ASME分母欠落→t/R≥0.1でLamé式分岐・適用外表示) / pressure-vessel(圧力UIがkPa表記だが計算はMPaスケール→ラベル是正) / pump-cavitation(NPSHAが速度ヘッドを二重計上) / plate-buckling(SSSS二軸座屈係数が耐力過大評価) / mixing-tank(混合時間がNienow乱流式から約467倍ずれ→Re^-0.5除去) / optical-resonator(内部損失) / engine-kinematics×2(ピストン微分/平均速度式の誤り＋ロッド長≤クランク半径でNaN→クランプ) / fatigue-spectrum(σm=Suで無限疲労損傷がゼロ表示) / food-pasteurization-d-value(微生物プリセットのz/T_ref値が選択時に未適用) / car-braking-distance(効率110%で非物理的に短い制動距離=非保守) / radiation-shielding(吸収式) / underwater-acoustic-sonar-range(吸収式が10-100kHz損失を過小評価し探知距離過大) / その他重大数件。
中位・軽微も全数是正（jintegral既定UIが入力非表示、yield-criteriaのDrucker-Pragerが楕円スケッチのみ、acid-base-pH低濃度で水自己イオン化無視、circular-motion力チャート0.1倍軸ラベル不一致、column-base-plate極端偏心で∞表示等）。

**運用ノート**: codex日次使用上限が2回発生（修正ジョブが一度全停止→使用上限リセット後の18:37に自動再実行をスケジュールし回収）。再実行でグループDが既知の最終QAハング（CPU=0、全7ツール×3言語のmd5報告は完了済み）→kill→Claude側QAゲート＋重大置換のnode検証(pv-design Lamé分岐・car-braking効率ガード・engine-kinematics幾何クランプ確認)で回収。本番由来div不均衡4件(yield-criteria EN/ZH各3余剰、engine-kinematics EN/ZH各1)も修復。


### 2026-06-12 トラフィック加重監査 Wave10（311〜345位の35ツール・全件修正・本番デプロイ済）＝**修正をClaude本体が適用した初回**
体制: ユーザー指示「codexが止まったらClaude Codeが修正」を受け、**監査=codex 5ジョブ／修正適用=Claudeメインループ**に移行。codex監査→**35/35にバグ、重大11件**（所見=fix11/wave10_findings_A〜E.md、SPEC=fix11/SPEC_A〜E.md）。Claudeが汎用アプライヤ（_apply_spec2.py: SPECのOLD/NEW fenced pairをslug別に分割しexact-string置換、count==1 assert）で**196パッチ適用・conflict 0**→QAゲート105/105、サーバーmd5全一致・IndexNow 200。

**重大11件（修正済）**: galvanic-series(溶液抵抗換算誤り) / jet-engine(Brayton熱効率モデルが定量的に誤り) / maglev-simulation(既定PID/力則スケールで即非物理クランプ) / pressure-vessel-nozzle系2件 / 他6件（noise/nuclear-decay/offshore等のグループB-Eの重大）。

**Claude適用で捕捉したcodex SPECのバグ**: jet-engineパッチが`const T4s`を二重宣言（旧コード残骸＋未定義`Wt_needed`参照）→全3言語でJS構文エラー。QAゲートのnode --checkで検出し、残骸ブロックを除去して回収。**=codex起草SPECをClaudeが機械適用する際もnode/QA検証が必須**の実証。

**本番由来の既存破損を一掃**: zh JSON-LD破損7件（miner-rule/noise-vibration/pressure-vessel-nozzle/taylor-tool-life/turn-radius/weber-number/ball-scref=中国語強調引用に半角"が使われJSON途中終端→構造引用符を文脈判定し内容引用符を全角“”化する汎用修復_fix_zh_jsonld.py）／div不均衡6件（en/heat-sink-designerは12余剰＝EN版に日本語テキスト混入の深い破損、div均衡のみ修復しEN内容修復は別途）。

**EN負債メモ**: en/heat-sink-designer は理論セクションに日本語残存＝過去のEN生成不全。div均衡は応急修復済みだが、EN本文の再翻訳は別バッチ要。同種のEN/ZH生成不全が他ツールにも潜在の可能性。


### 2026-06-12 トラフィック加重監査 Wave11（346〜380位の35ツール・修正デプロイ済）
codex監査5ジョブ→**35/35にバグ、重大10件**（所見=fix12/wave11_findings_A〜E.md）。修正適用=Claude本体（_apply_spec2.py→不具合発覚後 _apply_strict.py）。35ツール中**29ツール+gravity-well+magnetic-field-solenoid=31ツールにパッチ適用**、QAゲート全通過、サーバーmd5 105/105一致・IndexNow 200。

**重大例（修正済）**: composite-plate(編集可能な非対称積層で[B]連成を無視) / creep-relaxation(材料A定数が存在するが未使用=プリセットが材料別でなく参照正規化) / magnetic-field-solenoid(無限長式で中心/端磁界を表示=扁平形状で40倍過大→有限長axialField式に、Bideal比較用に残置) / 他グループの重大計。

**★重要な運用知見（Claude機械適用のリスクと対策）**: 初版の汎用アプライヤ_apply_spec2.py（OLD label→次のfenceをOLD content、次のNEW→content）が**SPEC内のfence位置ずれでOLD/NEWを取り違え**、magnetic-field-solenoidの実JS行`const Lind=...`をテキスト用mojibake`邏・7.1mH`で置換→JS構文エラー。**node --check QAで検出**し全fix12をbaselineへ巻き戻し→**ブロックのラベル順で厳格にOLD→NEW隣接ペアのみ採用する_apply_strict.pyで再適用**。教訓: ①codex起草SPECは構造が不揃い（OLD連続・NEW先行・trailing OLD・VERIFY内fence混在）②機械適用は必ずブロックラベル順ペアリング＋node/QA検証③巻き戻し可能なようbaseline保持必須。

**残課題（6ツールのSPEC構造崩れで部分適用/未適用）**: lateral-torsional-buckling / linear-algebra-vis / maze-solver / moment-curvature-section はSPECのOLD/NEW構造崩れ（OLD連続・trailing OLD）で一部パッチがorphan dropされ部分適用。これらの未適用パッチ（重大含む可能性）は**fix12/SPEC_C/D.mdのWARN該当箇所を手作業で再確認して別途適用要**。gravity-well/magnetic-field-solenoidは主要パッチ適用済。
**本番由来既存破損も修復**: zh JSON-LD 5件（中国語強調引用の半角→全角）、div不均衡3件（composite-plate en/zh, enzyme-kinetics zh）。


### 2026-06-12 トラフィック加重監査 Wave12（381〜415位の35ツール・全件修正・本番デプロイ済）
codex監査5ジョブ（**SPEC形式を「## slug＋OLD/NEW厳密交互、VERIFYはfence外」と明示指示**）→**35/35にバグ、重大14件**（所見=fix13/wave12_findings_A〜E.md）。修正適用=Claude本体（_apply_strict.py、ブロックラベル順ペアリング）→**WARN/orphanゼロ・全155パッチ適用・JS破損0**（厳密指示が奏功しWave11のような取り違え皆無）。QAゲート105/105、サーバーmd5全一致・IndexNow 200。

**重大14件（修正済）**: グループA-E計（process-capability/projectile-advanced/pump-design/radar-range/seismic-wave/signal-modulation/subsurface-stress-hertz/suspension-kinematics/topology-maps/torsion-shaft/two-phase-flow/vibration-absorber/waveguide-modes/weir-flow 他の計算式・単位・モデル誤り）。

**本番由来既存破損の修復**: zh JSON-LD 6件（うちsubsurface-stress-hertzは特殊＝FAQ値の引用符が`\"`エスケープと素の`"`混在で文字列終端不正→終端は素の`"`・内部強調は全角“”に分離する手当てで修復）、div不均衡5件（process-capability/sound-level/thermal-expansion-sim zh, topology-maps en/zh）。

**運用知見の確定**: Wave11の取り違え事故を受け、①codexへのSPEC形式指示を厳密化（## slug＋OLD/NEW交互＋VERIFY fence外）②修正はstrict applierのみ③適用後 _js_check.py＋zh JSON-LD＋div の3点QA、で安定運用が確立。Wave12はこの体制で完全クリーン適用を達成。


### 2026-06-12 トラフィック加重監査 Wave13（416〜450位の35ツール・全件修正・本番デプロイ済）＝**Claudeサブエージェント監査体制に復帰**
codex日次上限再到達のため監査をClaudeサブエージェント6体（A-F、月次上限が解消し復活）に切替→**35/35監査、重大12件**（所見=fix14/wave13_findings_A〜F.md）。修正適用=Claude本体（_apply_strict.py）→100パッチ・WARN/conflict 0・JS破損0、QAゲート105/105、サーバーmd5全一致・IndexNow 200。

**重大12件（修正済・検証値）**: concrete-beam(φ係数をひずみε_tでなく幾何比で判定=圧縮支配断面でφMn最大+38%過大の非保守) / conjugate-beam-method(howto例δ_maxが桁違い8.53→実200mm) / fracture-mechanics(塑性域半径r_pの単位係数×1e6=1000倍過大で既定410mm非物理→×1e3) / ideal-gas-3d(密度に余分な×1000で1168g/L表示=1000倍過大) / fanno-flow×2(亜音速M1=0.5→超音速M2=1.89の物理不可能例＋主要式の<em>タグ混入でMathJax破綻) / braced-excavation-strut(howtoが別ツール記述・全水平力誤値) / casting-riser-design(howto例が物理破綻=M_r不可能値・Caine合否逆) / centripetal-force(手順スライダ範囲全不一致) / coanda-effect(howto例θ_s/F_y誤り) / curved-beam-stress(howto例が中空パイプ前提で矩形実装と全面不一致・内外縁大小逆)。
中位・軽微多数も是正。計算コア自体が誤るのはconcrete-beam/fracture-mechanics/ideal-gas-3dの3件、他は静的テキスト集中。

**運用ノート**: ①codex日次上限→Claudeサブエージェント（月次上限が解消し復活）に監査を切替えて即継続＝両ワーカーを上限状況に応じて使い分ける体制が確立。②グループ割当時のslug指定ミス（dam-stability/dc-motor等の不在slug混入、curved-beam-stress/crystal-growth取りこぼし）をカバレッジ検証(SPEC内## slug header走査)で検出→補完エージェントで全35カバー。③本番由来zh JSON-LD 9件・div 9件も修復。


### 2026-06-12 トラフィック加重監査 Wave14（451〜485位の35ツール・全件修正・本番デプロイ済）
監査=Claudeサブエージェント5体（正確なグループ割当）→**35/35にバグ、重大3件**（所見=fix15/wave14_findings_A〜E.md）。修正適用=Claude本体（_apply_strict.py）→96パッチ・WARN/conflict 0、QAゲート105/105、サーバーmd5全一致・IndexNow 200。

**重大3件（修正済）**: laser-design(縦モード間隔Δνがc[m/s]とL[cm]混在で100倍過小=既定1.43GHz→正142.86GHz、自FAQ「≈150GHz」と整合) / punching-shear-slab(howto許容応力式0.2√fcがJS実装0.33√fcと不一致＝利用率誤り＝安全系) / membrane-stress(t_min係数が全形状で誤り＝球√3倍・円筒/円錐2倍過大)。
中位多数（option-pricing通貨混在、ship-resistance形状係数二重計上で出力2倍＋DOM崩れ、rotational-dynamics setSpeedのID取り違え、wkb例の捏造κ/T、vle-raoult例のmmHg/kPa混同、symmetrical-components例のVUF誤り等）も是正。計算コア自体の定量誤りはlaser-design/punching-shear/membrane-stressの3件に限定、他は静的テキスト集中。

**本番由来既存破損の修復**: ①en/rolling-contact-stressのcanvas描画JSでテンプレートリテラル（バッククォート）が`<code>...</code>`・`\(...\)`にHTMLエンティティ化＝本番で描画関数が構文エラー（既存破損）→バッククォートに復元。②zh JSON-LD 8件（中国語強調引用の半角→全角）。③div不均衡8件（ja/vector-fieldのMathJax制御文字破損由来の孤立div含む）。

**運用ノート**: SPEC NEWにJSテンプレートリテラル（バッククォート）が含まれる場合、markdown経由で`<code>`化する事故が起きうる→適用後の_js_check.py（node --check）が最後の砦。今回もこれで捕捉。本番EN版にテンプレートリテラル破損が既存する例を確認＝EN/ZH生成不全の一種、mojibake一掃パスに含める。


### 2026-06-12 トラフィック加重監査 Wave15（486〜520位の35ツール・全件修正・本番デプロイ済）
監査=Claudeサブエージェント5体→**35/35にバグ、重大3件**（所見=fix16/wave15_findings_A〜E.md）。修正適用=Claude本体（_apply_strict.py）→83パッチ、QAゲート105/105、サーバーmd5全一致・IndexNow 200。

**重大3件（修正済）**: distillation-column(McCabe-Thieleステップオフが上方発散し理論段数Nが常に上限100固定＝計算機能死→正しい逆VLE下降ステップ実装、N≒12) / heat-of-combustion(CO₂/kWhが×3.6で1000倍小表示→×3600、天然ガスη30%で正673g/kWh) / hydrogen-storage-mof(howto-exampleカード二重化＋$100/kg分断で表示崩壊→単一化)。
中位多数（capillary-rise例h294→127mm、castigliano例10mm→33750mm単位破綻、geothermal広告が音響工学書の誤、flow-net-seepageのNf/Nd定義逆転、hydrogen-fcv貯蔵圧力死にパラメータ、jkr単位系GPa/N→MPa/μN統一等）も是正。計算コアの定量誤りはdistillation/heat-of-combustionの2件、他は静的テキスト集中。

**アプライヤ強化**: SPEC_Eが`` ```内容``` ``をfence記号と内容を同一行に書く形式（他グループは複数行fence）で取りこぼし→**_apply_strict.pyを`` ``` ``分割方式に改良**（fence記号が内容と同行/別行どちらでも対応、言語トークン除去、ラベルは直前テキストのOLD/NEW判定）。fix16をbaselineに戻して全5SPEC再適用＝WARN/conflict 0達成。改良版は次wave以降の標準。

**本番由来既存破損**: zh JSON-LD 7件、div不均衡3件（en/hydraulic-jump含む）も修復。


### 2026-06-13 トラフィック加重監査 Wave16（521〜555位の35ツール・全件修正・本番デプロイ済）
監査=Claudeサブエージェント5体→**35/35にバグ、重大6件**（所見=fix17/wave16_findings_A〜E.md）。修正適用=Claude本体（_apply_strict.py、3形式fence対応版）→111パッチ・WARN/conflict 0、QAゲート105/105、サーバーmd5全一致・IndexNow 200。

**重大6件（修正済）**: projectile-with-drag(直径の単位不整合=input mm/tooltip cm/d_cm/200でcm扱い＝物理量約100倍ずれ) / rc-development-length(howto計算例のl_dが式で再現不可) / schmid-factor(howto例数値誤りm=0.75→0.612、λ/φ定義逆転) / rolling-bearing(howto例L10/L10hが2桁オーダー誤り) / rolling-contact(公式<em>破損＋例数値全誤り) / sound-power-iso-3744(howto例S=18.85→6.28・K₁加算誤り・L_W94.3→88.8dB全面誤り)。
中位多数（noise-mapping理論式A_grの符号、paris-law da/dN100倍誤り、photon-energyフラックス誤り、pressure-drop-pipe主損失18.2→99.7kPa等）も是正。計算コアの定量誤りはprojectile直径単位の1件、他は静的テキスト・公式タグ破損集中。

**★アプライヤを3形式fence対応に統合（重要）**: codexやサブエージェントが生成するSPECのfence形式は実際には3種混在＝①OLD:/NEW:がfence前の散文、②OLD:がfence内先頭行、③`` ```OLD``` ``の独立マーカーfence＋別fenceに内容。_apply_strict.pyを`` ``` ``分割＋マーカー正規化で全3形式を統一処理する版に改修。SPEC_D(形式②)・SPEC_E(形式③)で取りこぼし/空OLD発生→改修後はWARN/conflict 0で全適用。fix17をbaselineに戻して再適用し確認。改修版が以降の標準。

**本番由来既存破損**: zh JSON-LD 6件、div不均衡7件（ja/probability-birthdayのFAQ閉じdiv2個欠落含む）も修復。


### 2026-06-13 トラフィック加重監査 Wave17（556〜590位の35ツール・全件修正・本番デプロイ済）
監査=Claudeサブエージェント5体→**35/35にバグ、重大5件**（所見=fix18/wave17_findings_A〜E.md）。修正適用=Claude本体（_apply_strict.py 3形式fence対応版）→85パッチ・WARN/conflict 0、QAゲート105/105、サーバーmd5全一致・IndexNow 200。

**重大5件（修正済）**: thermal-shock(computeRがsf[MPa]/E[Pa]の単位混在でRが10⁶倍小＝全材料R=0.0表示、皮肉にもFAQ本文は正値) / absorption-column(HTU計算でGs=G/3600[kmol/s]をper-hourのKYAと混用＝塔高Zが約3600倍過小、既定Z≈1.9mmと物理破綻) / atmospheric-reentry(howtoアポロ計算例がモデルと桁違い乖離) / bimetal-thermostat(howto例が別式採用で約50倍誤りδ15.2→0.30mm) / centrifuge-stress(環状ディスクのLamé定数B符号誤り＝内孔フープ応力を約1/3過小評価の非保守)。
中位多数（statics-2d初期stat、torque-lever/turbomachineryのMathJax\\times破損、tidal-forces潮汐加速度、carbon-footprint係数全面不整合、boiling-curve熱流束等）も是正。計算コアの定量誤りはthermal-shock/absorption-column/centrifuge-stressの3件、他は静的テキスト集中。

**本番由来既存破損**: zh JSON-LD 6件、div不均衡4件（zh/torque-leverの-3含む）も修復。3形式fence対応アプライヤは安定動作（Wave17もWARN/conflict 0）。


### 2026-06-13 トラフィック加重監査 Wave18（591〜625位の35ツール・修正デプロイ済）
監査=Claudeサブエージェント5体→**35/35にバグ、重大0（計算コアは全件正常）/中21/軽微多数**（所見=fix19/wave18_findings_A〜E.md）。修正適用=Claude本体（_apply_strict.py）→91パッチ、QAゲート(zh complex除き)105/105、サーバー104ファイル反映・IndexNow 200。

**主な中位修正**: compressible-flow(衝撃波テーブル行が`\lt /td\gt`リテラルで表示破綻=機能死級→正常タグに復元) / grinding-specific-energy(計算例がツール式で10〜100倍誤りP280→2800W) / electromagnetic-wave(銅表皮深さ10.6→1.33μm) / lc-oscillation(f0/Q値10倍誤り) / heat-pump-cop(年間電気代係数0.025が1000倍過小) / heisler-charts(理論式<em>破損) / gauss-seidel/greenhouse/ground-anchor等の例文を実在プリセット値へ全面差替。計算コア自体の定量誤りはゼロ（過去wave比で品質向上＝上位ツールほどバグ多の傾向を実証）。

**重要な発見（要追跡）**: heat-pump-copのslug実体ズレ＝server_ja版は地中熱GSHPだがfix19配下(=en/tools, zh/tools経由)は汎用カルノーCOP計算機。**JA本番(/tools/heat-pump-cop.html)とEN/ZH本番(/{en,zh}/tools/heat-pump-cop.html)で別ツールが配信されている疑い**。地中熱GSHP側で地中温度の数値入力が死にパラメータ(syncFromNum先id不一致)・EER定数化のバグも検出（fix19対象外で未修正）。→ slug実体ズレの全数調査が別途必要。

**JSON-LD一掃パス追加対象**: zh/complex-number-vis のJSON-LDがLaTeX単一バックスラッシュ(\omega等=無効JSONエスケープ)＋中国語強調素引用符の多重破損で汎用修復不可（本番で既存破損=退行なし）。当該zhのみデプロイ除外し現状維持。同種のLaTeX-in-JSON-LD破損が他zh/enにも潜在の可能性。


### 2026-06-13 トラフィック加重監査 Wave19（626〜660位の35ツール・全件修正・本番デプロイ済）
監査=Claudeサブエージェント5体→**35/35にバグ、重大3件**（所見=fix20/wave19_findings_A〜E.md）。修正適用=Claude本体（_apply_strict.py）→88パッチ、QAゲート105/105、サーバーmd5全一致・IndexNow 200。

**重大3件（修正済）**: magnetic-hysteresis(MsスライダーがTesla表記だがコアはA/m磁化扱い＝soft/transformer/ferriteプリセットでB-Hループが原点付近に潰れBr/BHmax/損失/μrが全て≈0) / pipe-bend-thrust(合力公式が√(PA²+ṁV²)誤り＝正は2(PA+ṁV)sin(β/2)、9.8→13.9kN) / 他1件。
中位多数（mach-number淀み点温度、low-thrust例ΔV、mechanical-advantage MA定義逆、plate-girder耐力、reactor-design体積5.6倍過小、rollover除算公式等）も是正。計算コアの定量誤りはmagnetic-hysteresis/pipe-bend-thrustの2件、他は静的テキスト集中。

**本番由来既存破損**: zh JSON-LD 5件、div不均衡7件（ja/osmotic-pressureのFAQ閉じdiv2個欠落含む）も修復。_fix_zh_jsonld.pyにLaTeXバックスラッシュ\エスケープ系統を追加（Wave18のcomplex-number-vis型破損に対応）。


### 2026-06-13 トラフィック加重監査 Wave20（661〜695位の35ツール・全件修正・本番デプロイ済）
監査=Claudeサブエージェント5体→**35/35にバグ、重大11件**（所見=fix21/wave20_findings_A〜E.md）。修正適用=Claude本体（_apply_strict.py）→84パッチ＋wind-load重大はreplace_allで個別適用、QAゲート105/105、サーバーmd5全一致・IndexNow 200。

**重大11件（修正済）**: solar-panel-calculator×2(計算結果がDOM要素欠落で完全非表示=機能死＋電力単価二重入力で約180倍スケールずれ) / steam-rankine(BWR=6.8%表示が実0.74%でFAQ「1%未満」と自己矛盾) / surface-treatment×2(howto例のD/ケース深さ/HVが大乖離) / timoshenko-beam(撓み3.7倍・せん断寄与13倍過大) / torsion-pendulum(計算チェーン全破綻fn65→366Hz) / torsional-vibration(固有振動数18倍過大) / vibration-measurement(加速度1000倍誤り＋ISOゾーン誤判定) / wind-load-building(速度圧式で重要度係数Iを二乗=ASCE7-16はI¹、I=1.15でqz+15%過大=非保守。JS 2箇所をreplace_allで修正) / biomedical-signal(number入力が未定義update()呼出＋スライダーsyncToNum引数誤りで機能死)。
中位・軽微多数も是正。計算コアの定量誤りは7件、機能死/配線が3件、安全系非保守がwind-load 1件。

**本番由来既存破損**: zh JSON-LD 4件、div不均衡5件も修復。torsional-vibrationの単位ラベル(count==3)はstrict applierがCONFLICT検出→軽微のため別途replace_all対応可（未適用・低優先）。


### 2026-06-13 トラフィック加重監査 Wave21（696〜730位の35ツール・全件修正・本番デプロイ済）
監査=Claudeサブエージェント5体→**35/35にバグ、重大6件**（所見=fix22/wave21_findings_A〜E.md）。修正適用=Claude本体（_apply_strict.py）→84パッチ、QAゲート105/105、サーバーmd5全一致・IndexNow 200。

**重大6件（修正済）**: buoyancy-stability(BM 20倍誤・GM符号逆=実は不安定なのに安定表示) / carbon-fiber-laminate-tsai-wu(例のSF安全結論が逆＝実0.61で破壊＋初期プリセットTWI=1.32>1で初期表示「破壊」) / cubesat-deployment-spring-tip-off×2(cubesatSize/deployerTypeセレクトが機能死＝compute未読取→applySizePresetで質量同期実装し回復) / electric-power-calc(力率角φスライダーが全回路で死にパラメータ→phiCalcで無条件上書き) / fluid-vortex(強制渦の圧力式が符号反転＝外側に負圧発散の非物理→正符号)。
中位多数も是正。計算コアの定量誤りはbuoyancy/carbon-fiber/fluid-vortexの3件、機能死がcubesat×2/electric-power、安全結論逆転が2件。

**本番由来既存破損**: zh/combustion-calcのcanvas/labelテンプレートリテラルが`<code>`化＋`\(...\)`化で5箇所JS構文エラー（本番で既存破損→バッククォート復元）、zh JSON-LD 4件、div不均衡2件も修復。テンプレートリテラル破損のzh本番混入が複数確認＝EN/ZH生成不全の一種、JSON-LD/mojibake一掃パスに含める。


### 2026-06-13 トラフィック加重監査 Wave22（731〜765位の35ツール・全件修正・本番デプロイ済）
監査=codex 5ジョブ（所見=fix23/wave22_findings_A〜E.md）。SPEC草案E群がpem-electrolyzer-efficiencyを欠落→Claude本体が独立検証(verify_pem.py)で手当て。修正適用=Claude本体（_apply_strict.py）→106パッチ・conflict/orphanゼロ、QAゲート(JS 0失敗/gate 0失敗)、変更57ファイル(ja32/en8/zh17)のサーバーmd5全一致・IndexNow 200。

**重大（修正済）**: hertz-line-contact(howto例の接触半幅a=0.62→0.297mm・最大接触応力pmax=1850→6430MPa・ex2 pmax=1420→3570MPa。式中の E^* が em タグ化していたmojibakeも副次修復) / inductor-rl(howto例のI(τ)=2.16→0.190A・磁気エネルギー0.47→0.0036J、X_L/Zは正) / optical-coherence-tomography(howto公式が本体JSと不一致→Δz=(2ln2/π)λ₀²/(nΔλ)・Δx=0.61λ/NAに修正、数値Δz7→3.1µm/Δx64→3.9µm/DOF2mm→160µm、スライダ範囲も実値に) / optical-fiber-comm(分散27.2ps→実27.2nsの1000倍単位誤り・NA0.14→0.178・受光全角16.1→20.5°) / optical-fiber-design(title/FAQ/chatでOSNRを主機能と謳うが本体JS未実装＝機能死、分散ペナルティ式の表記揺れ) / pem-electrolyzer-efficiency(howto例が全項目誤り。JA/ZH:水素生成量4.7→0.94kg/hr[5倍過大]・効率61.3→82.3%、EN:9.2→0.56kg/hr[16倍過大]・70→82.3%。ファラデーの法則 n_H2=N·I/(2F)·η_F で独立検証) / heat-conduction-cylinder(中心温度の非物理値) / nozzle-flow(超音速解M・全温度・衝撃波圧力比・臨界面積比の4誤り)。
中位・軽微多数も是正（optical-sensor応答度R、parametric-oscillatorの次元/スライダ範囲、merchant-cutting等）。

**本番由来既存破損**: zh JSON-LD 10件（fuel-injection-spray-cone/game-theory/gaussian-beam/jominy-hardenability/lung-compliance-breathing/machining-power-turning/method-of-manufactured-solutions/mooring-line-tension-catenary/muffler-transmission-loss/pem＝素引用符破損→_fix_zh_jsonld.py）、div不均衡3件（inductor-rl en/zh・linear-programming zh＝理論ボックスの余剰close div、_preと同一の既存破損を確認し除去）も一掃。

### 2026-06-13 インフラ: 旧/area/ページを410 Gone化
廃止済みの旧地域ページ（mojibake二重エンコードURL）が Googlebot 481+Bingbot 406/日で404を量産しクロールバジェットを浪費。nginxで /area/ 配下に return 410 を本番適用（/etc/nginx/sites-available/cae-archive、nginx -t通過・reload済、bak=.bak_pre410）。/area/miyagi等→410、ツールページ200維持を検証。サイトマップ非掲載のためクローラー記憶由来の死にURL、410で速やかに破棄させる。


### 2026-06-13 トラフィック加重監査 Wave23（766〜800位の35ツール・全件修正・本番デプロイ済）
監査=Claudeサブエージェント5体（所見=fix24/wave23_findings_A〜E.md・重大26件）。SPEC草案C/D群がOLD/NEWをコードフェンスで囲まない形式→_fence_convert.pyでfenced化してから適用。修正適用=Claude本体（_apply_strict.py）→126パッチ・conflict/orphanゼロ、QAゲート(JS 0失敗/gate 0失敗)、変更78ファイルのサーバーmd5全一致・IndexNow 200。

**計算コアJSバグ（修正済・多くが3言語共通）**:
- potential-flow: 揚力係数 CL=Γ/(πU·R) は誤り。クッタ・ジュコーフスキーより CL=Γ/(U·R)（π倍過小）。magnus既定でCL 1.91→6.0。3言語のJS修正。
- solar-resource: Wh→kWh変換係数が *0.0036（本来 *0.001）で全結果3.6倍膨張（日射PSH 19.4h/day=非物理）。monthlyGHI/monthlyGTの2箇所×3言語修正。Tokyo既定 PSH=5.39・年GHI≈1967へ。
- thermal-comfort-pmv: 水蒸気分圧 pa=(rh/100)*10*exp(...) が ISO 7730 では *1000（×100過小）。既定PMV -0.54→-0.21。pythermalcomfort/ISO7730-2005で検証。3言語修正。
- sound-transmission-class-stc: 「500Hz 透過損失」表示が trans[9]（=1000Hz帯）。正しくは trans[6]（500Hz帯）。statTL500・verdict文・STCST.tl500 の3箇所×3言語（監査の取りこぼしはClaude本体が_stc_fix.pyで補完）。1000Hz用 tlAt1000=trans[9] は維持。ヘッドラインSTC(stc500=fieldIncidence(…,500))は元々正。
- seismic-response: updateChartが数値入力欄に "5 %"/"1.00 s" 等の単位付き文字列を注入→再編集で制御破壊。数値のみ書き込みに修正＋減衰入力の "階" 誤ラベル是正。
- ring-structure: 表示モーメント式 PR/2(1/π−cosθ/2) が実装（正しいRoark式 PR/π(1−(π/2)|sinθ|)）と矛盾→表示式をコードに一致させた。

**worked-example / 静的テキスト誤り（修正済・抜粋）**: sandwich-plate（全項目約9倍誤・3言語）、tower-crane-counter-jib-balance（SF式 (Mr+Mjib)/Mload が誤・SF 0.85→0.17）、satellite-magnetic-torquer-attitude（rad/deg混同でα17倍）、power-cable-ampacity（243A/ΔT=45K非到達）、principal-stress-3d（主応力ソート違反）、radioactive-decay-chain（Tc-99m 24h残量 97.5→6.3MBq）、residence-time-distribution（転化率28%→78.5%）、shrink-fit-stress / stirling-engine-cycle / star-tracker / thyristor / tidal-stream-turbine / stub-matching / refrigeration / phased-array / picard-iteration 他多数。

**dead parameter方針**: numBlades(tidal)・craneModelTc(tower-crane)・PGV(seismic-response-spectrum)等の未配線パラメータは、最小修正の範囲で honest labeling（参考・本計算では未使用）に統一（モデル再設計は別途）。

**本番由来既存破損**: zh JSON-LD 5件（power-cable-ampacity/residence-time-distribution/satellite-magnetic-torquer-attitude/spt-n-value-correction/star-tracker-pointing-accuracy＝素引用符破損→_fix_zh_jsonld.py）も一掃。


### 2026-06-13 トラフィック加重監査 Wave24（801〜835位の35ツール・全件修正・本番デプロイ済）
監査=Claudeサブエージェント5体（所見=fix25/wave24_findings_A〜E.md・重大17件）。SPEC形式指示を明示したのでC/D群もコードフェンス付きで出力（_fence_convert.py不要）。修正適用=Claude本体（_apply_strict.py）→125パッチ・conflict/orphanゼロ、QAゲート(JS 0失敗/gate 0失敗)、変更70ファイルのサーバーmd5全一致・IndexNow 200。**全1,661中835完了＝折返し点（50%）**。

**構造/計算コアJSバグ（修正済）**:
- adiabatic-flame-temperature: chat内に不正な `<int>` タグが混入しDOMを破壊（ja+zh）。除去。
- battery-cell-balancing-active: howto-example の div 内に guide+example+notes が重複ネストしてDOM破壊（ja+zh）。重複除去（div均衡=0確認）。
- cable-stayed-bridge: たわみ推定が L⁴ 絶対式で defMm≈4,375,000mm（=4.4km、非物理・上限クランプ無し）。有界span-ratioヒューリスティック kDef=400·√(N/6)·(70/load)^0.4、defMm=L/kDef·1000（既定 L/400=500mm、cable増で剛性↑・荷重増でたわみ↑）に置換。3言語共通JS。
- co2-emissions: worked-example が約1000倍の単位誤り（kgをtCO2と表示、"10,146 tCO2"→10.02t）＋EF誤＋14kg/tree（実22kg）。死にスタット「1人当たり」（=総量と同値）を「世界平均比(×)」に転用。
- complex-analysis: メビウス変換の留数表示 Res[-1]=2 が誤り（正=-2）。worked-example も実装と別モデルを記述しており全面是正。
- black-body-radiation: preset/slider が数値入力欄を更新しない desync。
- vector-field-2d: 強制渦presetでカーソル渦度が 0 にハードコード（ω=Q≠0 のはず）。

**worked-example / 静的テキスト誤り（修正済・抜粋）**: wahl-correction（τ_max が D項脱落で12.1→482MPaの約40倍誤）、young-laplace（1000倍単位誤）、wind-tunnel-blockage-correction（CD補正が符号逆＋ε混同）、air-quality（AQI overall誤・3言語）、anaerobic-digester-biogas / -yield（CHP・VS・OLR が桁違い）、antibiotic-mic-pk-pd-auc（医療系・曝露3.5倍過大）、atmospheric-boundary（U_log誤）、cable-voltage-drop（往復係数k=2脱落）、chladni-figures（周波数比2.37→4.0）、biosensor/blasius/black-body/blackbody-color/battery-runtime/biofilter 他多数。

**dead parameter方針**: 動作温度T(anaerobic-biogas)・反応器種別select(anaerobic-yield)・targetAUCMIC(antibiotic)等の未配線パラメータは honest labeling（参考・本計算では未使用）に統一。

**本番由来既存破損**: zh JSON-LD 7件（vaccine-cold-chain-thermal-mass/wave-particle-duality/wind-tunnel-blockage-correction/window-function-spectral/adiabatic-flame-temperature/ampere-law/battery-runtime-peukert＝素引用符破損→_fix_zh_jsonld.py）も一掃。


### 2026-06-13 トラフィック加重監査 Wave25（836〜870位の35ツール・全件修正・本番デプロイ済）
監査=Claudeサブエージェント5体（所見=fix26/wave25_findings_A〜E.md・重大20件）。修正適用=Claude本体（_apply_strict.py）→110パッチ・conflict/orphanゼロ、QAゲート(JS 0失敗/gate 0失敗)、変更62ファイルのサーバーmd5全一致・IndexNow 200。**全1,661中870完了（約52%）**。

**計算コアJSバグ（修正済・3言語共通）**:
- corrosion-rate: ファラデー腐食速度の秒/年係数が 3.156e8（本来 3.156e7）で10倍過大。`const factor=55.85/(2·96485·7.87)·3.156e7; CR=icorr·factor·10`（`*10`はcm→mm換算で正当）に修正。CR(10µA)=0.116・CR(85µA)=0.987 mm/yr、JSON-LD FAQの0.01166/µAと一致。computeStats・buildTempDataの2箇所。
- euler-buckling-plate: 板座屈係数の近似が CCCC で k_min=6.51（教科書/ヘッダ/FAQは10.07）、SSCC 5.11（5.42）。SSSS基底 (m/ab+ab/m)² に CCCC=`×2.5175`（→4×2.5175=10.07）・SSCC=`×1.355`（→5.42）を適用。JS3箇所（kBest探索・チャート・モード図）×3言語。
- datacenter-pue-cooling-efficiency: 外気温 T_out が読まれるがPUE式で未使用（dead parameter）→honest labeling。

**worked-example / 静的テキスト誤り（修正済・抜粋）**: francis-turbine（出力3,345MW=1000倍誤、実3.3MW）、electromagnetic-induction（相互インダクタンスM 150mH→1.13mH・存在しない二次EMF出力）、crank-nicolson（r=0.15→0.015の10倍）、flutter-analysis/foundation-settlement/flash-distillation（ツールに存在しない入力EI/GJ/E0等を記述→既定入力ベースに書換え）、drum-brake/electric-potential-field/electrical-motor-ac（howto数値が再現不可）、fractal-tree（フラクタル次元1.26→2.71）、gas-compressibility（Z値・bar/MPa単位）、dna-replication（存在しないUI・bp範囲）他多数。

**dead parameter方針**: T_out(datacenter-pue)・吸収剤再生温度(direct-air-capture-dac)等の未配線パラメータは honest labeling（参考・本計算では未使用）。

**本番由来既存破損**: zh JSON-LD 7件（concrete-creep-shrinkage/drone-quadcopter-noise-1m/element-stiffness-matrix/feedforward-compensation/fractal-tree/gait-cycle-spatial-temporal/gas-compressibility-factor）、div不均衡5件（en/zh diffraction・en/zh electromagnetic-induction＝理論ボックスの余剰close除去、zh/convection-diffusion＝close不足補填、_divbalance.pyで汎用処理）も一掃。


### 2026-06-13 トラフィック加重監査 Wave26（871〜905位の35ツール・全件修正・本番デプロイ済）
監査=Claudeサブエージェント5体（所見=fix27/wave26_findings_A〜E.md・重大14件）。修正適用=Claude本体（_apply_strict.py）→113パッチ・conflict/orphanゼロ、QAゲート(JS 0失敗/gate 0失敗)、変更64ファイルのサーバーmd5全一致・IndexNow 200。**全1,661中905完了（約54%）**。

**この回は計算コアJSバグ0**＝全35ツールのコア計算は物理的に正。誤りはworked-example / FAQ / howto の静的テキスト（数値・存在しないUI参照・dead param）に集中。

**安全/医療系の重大（修正済）**:
- iv-drip-rate-clinical-pharma【医療】: howto例のドパミン投与量が 1429mcg/kg/min（ツール式の正値は 2.38、約600倍過大＝非保守）、ヘパリン125gtt/min（実17）。FAQ過量閾値も「120%」表示だがコードは150%判定→150%に統一。ja+zh（enは元々正）。
- leaf-spring-deflection【安全】: howto例 δ≈85mm/σ≈420MPa が片持ち式 δ=PL³/(3nEI) と矛盾、実値 δ=3049mm/σ=4667MPa（50-100倍）。ja+en。
- mass-spectrometer: Na⁺例 v=914m/s（実91,593）、KE=15.4eV（実1000）。ja+en。
- magnetic-levitation: 力係数が /(2x²)（ツールは /(4x²)）＋範囲外入力。
- harbor-resonance: 第1共振周期 T₁ が30倍誤り（claim 330分 vs 4L/c=11.0分）。
- modulation-transfer-function: 回折カットオフ周波数が約840倍誤り（claim 0.774 vs 実649）。
- ion-thruster-isp-thrust: 排気速度29.8→54.3km/s・Isp 3040→5533s、化学ロケット例の誤用。

**中位・dead parameter**: HRSG（HP/IP/LP圧力slider 3本が死にパラメータ）、milk-pasteurization（processType selectがcompute()未読込の死にパラメータ）、hydrodynamic-bearing/hemodialyzer/interference-fit/maxwell-betti/knudsen/langmuir/kriging等の例数値・単位ラベル是正。dead paramは honest labeling（参考・本計算では未使用）。

**本番由来既存破損**: zh JSON-LD 9件（geofoam/henderson-hasselbalch/huber-regression/inelastic-collision/langmuir-hinshelwood/leaf-spring/lifecycle-assessment-lca/mach-cone/mass-spectrometer）、div不均衡4件（zh/harbor-resonance・en/lava-lamp・zh/magnetic-levitation＝余剰close除去、zh/inelastic-collision＝footer閉じdiv2個欠落を`</body>`前補填）も一掃。


### 2026-06-13 トラフィック加重監査 Wave27（906〜940位の35ツール・全件修正・本番デプロイ済）
監査=Claudeサブエージェント5体（所見=fix28/wave27_findings_A〜E.md・重大16件）。修正適用=Claude本体（_apply_strict.py）→101パッチ・conflict/orphanゼロ、QAゲート(JS 0失敗/gate 0失敗)、変更62ファイルのサーバーmd5全一致・IndexNow 200。**全1,661中940完了（約57%）**。

**この回も計算コアJSバグ0**＝全35ツールのコア計算は物理的に正。誤りは静的テキスト（公式・符号・数値・存在しないUI・dead param）。

**安全系の重大（修正済）**:
- npsh: 使い方ガイドの計算式が符号誤り。「NPSHa = Patm/ρg + Hs − Pv/ρg − Hloss」（吸込揚程Hsを加算）→ 正しくは「NPSHa = Patm/ρg − Pv/ρg − Hs − Hloss」（h_sは液面より上で正）。worked例も 10.33+1.5−0.235−0.4=11.195m → 10.33−0.235−1.5−0.4=8.195m に修正、余裕5.195m。
- powerline-galloping-iced-stability: Den Hartog不安定判定が反転。「H値が3.5を超えると不安定」→ ツール実装の正しい規約「H=dCl/dα+Cd が H<0（負減衰）で不安定」。D型氷 H=-2.5+1.2=-1.30。worker例・notes・guide・EN例を全面是正。
- pelton-turbine: howto公式 F=ρQV(1+cosβ)・η=2φ(1−φ)(1+cosβ)² が物理破綻（cos170°使用で非現実値）。ツール実装（正）に整合。

**その他の重大（修正済）**: momentum-conservation（弾性 v₁'・非弾性損失とも誤、ja+en）、monte-carlo-radiative-transfer（ℓ=1/μs等の誤公式・ja/en/zh）、mosfet-switching-loss（Esw 0.6→30µJ等の桁違い）、pump-specific-speed（Ns 8倍誤）、open-channel-flow（径深R誤）、nuclear-binding-energy（係数・He-4/Ni-62例）。

**中位・dead parameter**: multiple-effect-evaporator（潜熱λ slider未使用）、mutual-information-estimation（jointEntropyBaseline void）、ode-solver（RK45/許容誤差など存在しないUI記述を削除）、molecular-dynamics/quantum-harmonic/refrigerant-selection等の例・範囲是正。dead paramは honest labeling（参考・本計算では未使用）。

**本番由来既存破損**: zh JSON-LD 6件（molecular-dynamics/noise-figure-cascade/ode-solver/pole-placement-detail/powerline-galloping/poynting-vector）、div不均衡4件（en/zh momentum-conservation・en/octave-band・zh/refrigerant-selection＝全て理論ボックスの余剰close除去）も一掃。


### 2026-06-13 トラフィック加重監査 Wave28（941〜975位の35ツール・全件修正・本番デプロイ済）
監査=Claudeサブエージェント5体（所見=fix29/wave28_findings_A〜E.md・重大15件）。修正適用=Claude本体（_apply_strict.py）→103パッチ・conflict 0（orphan 1=tornadoのLOWテキスト1件、QA green・critical 0につき許容）、QAゲート(JS 0失敗/gate 0失敗)、変更61ファイルのサーバーmd5全一致・IndexNow 200。**全1,661中975完了（約59%）**。

**計算コアJSバグ（修正済・3言語共通）**:
- stage-lighting-led-lumens-efficacy: 省エネ率 `energy_saving=(1-eff/(eff+15))*100` は誤り（eff=100で13%、chat/FAQ/howtoの85%等と矛盾）。正しくは `(1-15/eff)*100`=85%。
- subwoofer-port-tuning-bass-reflex: ポート空気速度の式が次元誤り（`2πFb·x_max/A_port`、コーン面積S_d欠落で単位1/(s·m)）→既定で128m/s表示・verdict「chuffing NG」固着。ドライバ径別 S_d マップを追加し v=2πFb·x_max·S_d/A_port に修正、12in既定で6.7m/s（OK）。
- titration-simulator: 強塩基→強酸滴定で `calcStrongAcid_StrongBase(Cb,Va,Ca,Vb)` と引数順が逆→滴定曲線が反転。`(Ca,Va,Cb,Vb)` に修正。
- tire-dynamics: preset適用が数値入力に `.textContent` で書込み→再編集で desync（ja+en）。

**安全系 worked-example の非保守（修正済）**:
- snow-load-greenhouse-collapse: 例が SF=2.04「安全」表示だがツール式では SF=0.34（崩壊）。in-range の正例に書換え。
- snow-loaded-tree-branch-bending: 例が σ8.8MPa/SF=2.3「低リスク」だが実 σ151MPa/SF=0.23（確実破断）。
- structural-reliability: ja/en/zh の例が FORM エンジン（β計算は正）と不一致（ja β2.18→3.78等）。
- unit-load-method（δが10⁴誤・3言語）、unsymmetric-bending（α/β/σが両軸和で誤・3言語）。

**その他**: retaining-wall/seismic-hazard（コアは保守的・誤り無し、例の数値のみ是正）、snowfall-roof-load-codes（kN/t混同）、soil-liquefaction（CSR/FS例）、supercapacitor/surge-tank/stepper/transformer-design/transistor-bias/vehicle-dynamics 等の例是正。dead param: rocket ambientTempPlumeC・tornado 旋回半径R/中心圧Δp→honest labeling。

**本番由来既存破損**: zh JSON-LD 4件（stage-lighting/surge-tank-oscillation/transformer-attention-basics/unit-load-method）、div不均衡4件（en/zh structural-reliability・zh/tire-dynamics・en/transistor-bias＝全て余剰close除去）も一掃。
