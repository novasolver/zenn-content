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
