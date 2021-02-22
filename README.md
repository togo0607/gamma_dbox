<script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
<script type="text/x-mathjax-config">
 MathJax.Hub.Config({
 tex2jax: {
 inlineMath: [['$', '$'] ],
 displayMath: [ ['$$','$$'], ["\\[","\\]"] ]
 }
 });
</script>
注：このREADMEのTeX表記はローカルにクローンしてVSCode等を通せば見ることが出来ます。他の対処法分かる方いたら教えてもらえると嬉しいです。

# 分布関数から比熱比$\gamma$を計算するスクリプト
## 分布関数と$\gamma$の関係
$v_{\parallel} > 0$領域のみ0でない値を持つ(一方向)イオンの分布関数$f(v_{\parallel})$に対し、以下の関係が成り立つ。
$$ \int_0^{\infty}\textrm{d}v_{\parallel}\frac{f(v_{\parallel})}{v_{\parallel}^2} = \frac{n}{u_{\parallel}^2 - \gamma T_{\textrm{i}\parallel}/m_{\textrm{i}}} $$
詳細については別紙「プラズマ音速の導出.pdf」を参照のこと。$f(v_{\parallel})$として単一の矩形分布関数では$\gamma = 3$以外の結果を出せない(伝導熱流束が0のため)ので、このスクリプトでは矩形分布関数の重ね合わせにより二温度分布を持たせることで、その成分比に応じた$\gamma$の振る舞いを調べる。

## 重ね合わせ矩形分布関数と電場による運動
下図のような矩形を重ね合わせた分布関数を作り、二温度成分を持たせる。

![分布関数](img/Fig1.svg)

## 計算手順
**Specify the characteristics of $f(v_{\parallel}$)**

インプットパラメータとして下記を与える。
- 伝導熱流束の向き($q_{\textrm{switch}}$): 0は$q_{\parallel}^{\textrm{cond}} > 0$、1は$q_{\parallel}^{\textrm{cond}} < 0$
- 二つの矩形分布の共通速度($v_{\\textrm{c}}$ [m/s])
- 低温成分の温度($T_1$ [eV])
- 高温成分の温度($T_2$ [eV])

**Constants**

定数として下記を与える。
- イオン質量($m = 1.672\times 10^{-27}$ [kg]) (軽水素イオンなので状況に応じて変えても良い)
- 素電荷($e = 1.602\times 10^{-19}$ [C])

**Compute some characteristic parameters of $f(v_{\parallel})$**

分布関数を特徴付ける量として以下を計算する。
- 低温成分の幅($\Delta _1 = \sqrt{\frac{12T_1e}{m}}$ [m/s])
- 高温成分の幅($\Delta _2 = \sqrt{\frac{12T_2e}{m}}$ [m/s])

$q_{\textrm{switch}} =1$のときは$\Delta$を負の値で与える。またそのとき分布関数の下端$v_{\textrm{c}} + \Delta_2$が0以下であればプログラムを止める。

**Compute the moment quantities of $f(v_{\parallel})$**

分布関数のモーメント(解析的に計算済み)を高温成分の密度の比$C_{\textrm{h}} = n_{02}/(n_{01}+n_{02})$の関数として計算する。
- 実効流速
$$u_{\textrm{eff}} = \frac{1}{n}\int_{-\infty}^{\infty}v_{\parallel}f(v_{\parallel})\textrm{d}v_{\parallel} = v_{\textrm{c}} + (1 - C_{\textrm{h}})\frac{\Delta_1}{2} + C_{\textrm{h}}\frac{\Delta_2}{2}$$
- 実効温度
$$T_{\textrm{eff}} = \frac{1}{en}\int_{-\infty}^{\infty}m(v_{\parallel} - u_{\textrm{eff}})^2f(v_{\parallel})\textrm{d}v_{\parallel} = \frac{m}{e}\left[ \frac{1}{3}\left( \left( 1 - C_{\textrm{h}} \right)\Delta_1^2 + C_{\textrm{h}}\Delta_2^2 \right) - \left( u_{\textrm{eff}} - v_{\textrm{c}} \right)^2 \right]$$
- 対流熱流束(密度で規格化)
$$\frac{q_{\parallel}^{\textrm{conv}}}{n} = \left( \frac{1}{2}mu_{\textrm{eff}}^2 + \frac{3}{2}eT_{\textrm{eff}} \right)u_{\textrm{eff}}$$
- 伝導熱流束(密度で規格化)
$$\frac{q_{\parallel}^{\textrm{cond}}}{n} = \frac{1}{n}\int_{-\infty}^{\infty}\frac{1}{2}m\left( v_{\parallel} - u_{\parallel} \right)^3f(v_{\parallel})\textrm{d}v_{\parallel}$$
- 比熱比
$$\gamma = \frac{m}{eT_{\textrm{eff}}}\left(u_{\textrm{eff}}^2 - \frac{n}{\int_0^{\infty}\textrm{d}v_{\parallel}\frac{f(v_{\parallel})}{v_{\parallel}^2}} \right) 
= \frac{m}{eT_{\textrm{eff}}}\left( u_{\textrm{eff}}^2 - \frac{v_{\textrm{c}}\left( v_{\textrm{c}} + \Delta_1 \right) \left(v_{\textrm{c}}+\Delta_2 \right) }{v_{\textrm{c}} + \left( 1 - C_{\textrm{h}} \right) \Delta_2 + C_{\textrm{h}}\Delta_1} \right)$$

$q_{\textrm{switch}} =0$のときは$\gamma$の極小値とそれを与える$C_{\textrm{h}}$を、$q_{\textrm{switch}} =1$のときは$\gamma$の極大値とそれを与える$C_{\textrm{h}}$を返す。

**Get $f(v_{\parallel})$ for some of $C_{\textrm{h}}$**

$C_{\textrm{h}} = 0, 0.2, 0.4, 0.6, 0.8, 1$の場合の分布関数$f(v_{\parallel})$ (1で規格化)を取得

**Plots**

以下をプロットする。
- $f(v_{\parallel})$ ($C_{\textrm{h}} = 0, 0.2, 0.4, 0.6, 0.8, 1$) ("f_v_para.svg", "f_v_para.pdf")
- $\gamma (C_{\textrm{h}})$ ("gamma.svg", "gamma.pdf")
- $u_{\textrm{eff}} (C_{\textrm{h}})$ ("flow.svg", "flow.pdf")
- $T_{\textrm{eff}} (C_{\textrm{h}})$ ("temp.svg", "temp.pdf")
- $q_{\parallel}^{\textrm{cond}}/q_{\parallel}^{\textrm{conv}} (C_{\textrm{h}})$ ("heatflux.svg", "heatflux.pdf")