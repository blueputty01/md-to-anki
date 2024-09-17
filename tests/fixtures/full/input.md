A **vector-valued** function consists of two parts: a **domain**, which is a collection of numbers, and a **2::rule**, which assigns to each number in the domain one and only one vector.
$\mathbf{F}(t)=f_{1}(t)\mathbf{i}+f_{2}(t)\mathbf{j}+f_{3}(t)\mathbf{k}$
The functions $f_1$, $f_2$, and $f_3$ are the **component** functions of F.
![|300](z_attachments/Pasted%20image%2020240911120937.png)
plotting out all the points $F(t)$ as $t$ ranges over all real values (in the domain) we trace out a curve in space

A **circular helix** is defined by $F(t) = \cos t i + \sin t j + t k$
![|300](z_attachments/Pasted%20image%2020240911122202.png)

$\mathbf{F}$ and $\mathbf{G}$ are vector-valued functions; $f$ and $g$ are real-valued functions
$\begin{array}{c c}{{(\mathbf{F}+\mathbf{G})(t)=**\mathbf{F}(t)+\mathbf{G}(t)}}**&{{\qquad\qquad(\mathbf{F}\cdot\mathbf{G})(t)=**\mathbf{F}(t)\cdot\mathbf{G}(t)}}**\\ {{(\mathbf{F}-\mathbf{G})(t)=**\mathbf{F}(t)-\mathbf{G}(t)}}**&{{\qquad(\mathbf{F}\times\mathbf{G})(t)=**\mathbf{F}(t)\times\mathbf{G}(t)}}\\{{(f\mathbf{F}(t)=**f(t)\mathbf{F}(t)}}**&{{\qquad\qquad\mathbf{F}\circ g (t)=**\mathbf{F}(g(t))}}**\\**\end{array}$
+ is vector valued, dot product is real valued, cross product is vector valued, real value function thing is vector valued, composition is vector valued

Let $\mathbf{F}(t)=f_{1}(t){\hat{\mathbf{i}}}+f_{2}(t){\hat{\mathbf{j}}}+f_{3}(t)\mathbf{k}$
Then $\mathbf{F}$ has a limit at $t_0$ if and only if $f_1$, $f_2$, and $f_3$ have limits at $t_0$. In that case: **$\operatorname*{lim}_{t\rightarrow t_{0}}{\bf F}(t)=\left[\operatorname*{lim}_{t\rightarrow t_{0}}f_{1}(t)\right]\mathbf{i}+\left[\operatorname*{lim}_{t\rightarrow t_{0}}f_{2}(t)\right]\mathbf{j}+\left[\operatorname*{lim}_{t\rightarrow t_{0}}f_{3}(t)\right]\mathbf{k}$**

$\operatorname*{lim}_{t\to t_{0}}(\mathbf{F}+\mathbf{G})(t)=**\operatorname*{lim}_{t\to t_{0}}\mathbf{F}(t)+\operatorname*{lim}_{t\to t_{0}}\mathbf{G}(t)**$
$\operatorname*{lim}_{t\rightarrow t_{0}}f F(t)=**\operatorname*{lim}_{t\rightarrow t_{0}}f(t)\operatorname*{lim}_{t\rightarrow t_{0}}\operatorname{F}(t)**$
$\operatorname*{lim}_{t\rightarrow t_{0}}\left(\mathbf{F}\cdot\mathbf{G}\right)(t)=**\operatorname*{lim}_{t\rightarrow t_{0}}\mathbf{F}(t)\cdot\operatorname*{lim}_{t\rightarrow t_{0}}\mathbf{G}(t)**$
$\operatorname*{lim}_{t\rightarrow t_{0}}\left({\bf F}\times{\bf G}\right)(t)=**\operatorname*{lim}_{t\rightarrow t_{0}}{\bf F}(t)\times\operatorname*{lim}_{t\rightarrow t_{\alpha}}{\bf G}(t)**$
$\operatorname*{lim}_{s\to s_{0}}(\mathbf{F}\circ g)(s)=**\operatorname*{lim}_{t\to t_{0}}\mathbf{F}(t)**$ if $g(s) \neq t_0$ for all $s$ in an open interval about $s_0$

A vector-valued function $\mathbf{F}$ is continuous at a point $t_0$ in its domain if **$\operatorname*{lim}_{t\to t_{0}}\mathbf{F}(t)=\mathbf{F}(t_{0})$**

A vector-valued function $\mathbf{F}$ is continuous at $t_0$ if and only if **each of its component functions is continuous at $t_0$**.
